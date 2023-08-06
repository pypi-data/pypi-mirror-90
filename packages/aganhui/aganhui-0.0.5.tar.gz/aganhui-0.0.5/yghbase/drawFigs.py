
import matplotlib.pyplot as plt
def baseFig(listY, symbol, listX=-1, savePath="tempFig.jpg", labelX="X", labelY="Series"):
    # 改进：多序列画图
    if listX == -1:
        listX = np.arange(len(listY))
    plt.figure()
    plt.plot(listX, listY, symbol)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.savefig(savePath)
    plt.show()