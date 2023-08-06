

import gdal
def writeImg(path, arr, geotrans, proj, imgFormat="ENVI", datatype=gdal.GDT_Float32):
    # 将数组写入文件
    # 可以是二维和三维矩阵，其中三维数组的第一个维度表示波段
    dims = np.shape(arr)
    driver = gdal.GetDriverByName(imgFormat)  # GTiff or ENVI
    if len(dims) == 2:
        dataset = driver.Create(path, dims[1], dims[0], 1, datatype)
        dataset.GetRasterBand(1).WriteArray(arr)
    elif len(dims) == 3:
        dataset = driver.Create(path, dims[2], dims[1], dims[0], datatype)
        for i in range(dims[0]):
            dataset.GetRasterBand(i + 1).WriteArray(arr[i, :, :])
    else:
        print("dims of arr ERROR!", len(dims))
        return
    dataset.SetGeoTransform(geotrans)  # 写入仿射变换参数
    dataset.SetProjection(proj)  # 写入投影
    # if (dataset == None):
    #     print("creating dataset ERROR!")
    #     return
    
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
    areaSum = np.sum(mapAreaOfPixels[0, validPixels])
    return areaSum


baseGeoTrans = (-180, 0.5, 0, 90, 0, -0.5)
baseProj = '''GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],
AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,
AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST]]'''
