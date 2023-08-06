
def readImg(path):
    import gdal
    dataset = gdal.Open(path)
    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray()  # 获取数据
    return im_data, im_geotrans, im_proj

def writeImg(path, arr, geotrans, proj, nodata, imgFormat="ENVI", datatype=gdal.GDT_Float32):
    # 将数组写入文件
    # 可以是二维和三维矩阵，其中三维数组的第一个维度表示波段
    # print(path)
    dims = np.shape(arr)
    driver = gdal.GetDriverByName(imgFormat)  # GTiff or ENVI
    if len(dims) == 2:
        dataset = driver.Create(path, dims[1], dims[0], 1, datatype)
        dataset.GetRasterBand(1).WriteArray(arr)
        dataset.GetRasterBand(1).SetNoDataValue(nodata)
    elif len(dims) == 3:
        dataset = driver.Create(path, dims[2], dims[1], dims[0], datatype)
        for i in range(dims[0]):
            dataset.GetRasterBand(i + 1).WriteArray(arr[i, :, :])
            dataset.GetRasterBand(i + 1).SetNoDataValue(nodata)
    else:
        print("dims of arr ERROR!", len(dims))
        return
    dataset.SetGeoTransform(geotrans)  # 写入仿射变换参数
    dataset.SetProjection(proj)  # 写入投影
    dataset = None
    
def pixelArea(dLat1, dLat2, dLon1, dLon2):
    # *[Matlab处理气象数据（六）数据的面积加权_设计の诗 - CSDN博客](https: // blog.csdn.net / ymyz1229 / article / details / 106039683)
    import math
    pi = 3.1415926
    R = 6371007.181  # units - m
    return (pi / 180.0) * R * R * abs(math.sin(dLat1 / 180.0 * pi) - math.sin(dLat2 / 180.0 * pi)) * abs(dLon1 - dLon2)

def mapAreaOfPixels(dims, left, lonSize, top, latSize):
    # 需要输出的面积矩阵的维度 （bands, rows, cols）
    # left, map的最左像元的左边界经度值, 西经为负
    # lonSize, 像元经度方向的大小
    # top, map的最上面像元的上边界的纬度值
    # latSize, 像元维度方向的大小, 北纬为正
    import numpy as np
    listLatOfPixels = np.arange(top, top-latSize*(dims[1] + 1), -latSize)   # 像元的上下边界列表
    listLonOfPixels = np.arange(left, left+lonSize*(dims[2] + 1), lonSize)   # 像元的左右边界列表
    mapAreaOfPixels = np.zeros(dims, np.float)
    for r in range(len(listLatOfPixels) - 1):     # 此处可考虑并行运算
        for c in range(len(listLonOfPixels) - 1):
            mapAreaOfPixels[:, r, c] = pixelArea(listLatOfPixels[r], listLatOfPixels[r+1],
                                                 listLonOfPixels[c], listLonOfPixels[c+1])
    return mapAreaOfPixels

def mapAreaSum(mapAreaOfPixels, validPixels):
    # 确定全图的有效像元的总面积
    import numpy as np
    areaSum = np.sum(mapAreaOfPixels[0, validPixels])
    return areaSum

def matrixTrend(X, Y):    # 求趋势（多个序列同时计算）
    # X&Y的形状都是n*m，其中X为自变量，Y为因变量；n为每条序列的长度，m为序列的数量
    import numpy as np
    meanX = np.mean(X, 0)
    meanY = np.mean(Y, 0)
    minusX = X - meanX
    minusY = Y - meanY
    # print(minusX)
    k_fenzi = np.sum(minusX * minusY, 0)
    k_fenmu = np.sum(minusX * minusX, 0)
    # print(k_fenzi)
    k = k_fenzi / k_fenmu
    return k
def matrixTrendAutoX(Y):
    import numpy as np
    Y_trans = np.transpose(Y)
    x1 = np.reshape(np.arange(0, Y_trans.shape[0]), (Y_trans.shape[0], 1))
    x2 = np.ones((1, Y_trans.shape[1]))
    X = np.dot(x1, x2)
    trend = matrixTrend(X, Y_trans)
    return trend

baseGeoTrans = (-180, 0.5, 0, 90, 0, -0.5)
baseProj = '''GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],
AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,
AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST]]'''


def date2doy(year, month, day):
    # * [Python：日期表达的转换（day of year & year month day） - 阿尔伯塔 - 博客园](https://www.cnblogs.com/maoerbao/p/11518831.html)
    month_leapyear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_notleap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    doy = 0

    if month == 1:
        pass
    elif year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        for i in range(month - 1):
            doy += month_leapyear[i]
    else:
        for i in range(month - 1):
            doy += month_notleap[i]
    doy += day
    return doy

def doy2date(year, doy):
    # * [Python：日期表达的转换（day of year & year month day） - 阿尔伯塔 - 博客园](https://www.cnblogs.com/maoerbao/p/11518831.html)
    month_leapyear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_notleap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month, day = nanYGH, nanYGH

    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        for i in range(0, 12):
            if doy > month_leapyear[i]:
                doy -= month_leapyear[i]
                continue
            if doy <= month_leapyear[i]:
                month = i + 1
                day = doy
                break
    else:
        for i in range(0, 12):
            if doy > month_notleap[i]:
                doy -= month_notleap[i]
                continue
            if doy <= month_notleap[i]:
                month = i + 1
                day = doy
                break
    return month, day