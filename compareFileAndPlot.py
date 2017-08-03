import numpy as np
import matplotlib.pyplot as plt
import datetime
import json


#将几个提交的结果进行比较，并画出折线图
path = "C:\\Users\\NLSDE\\Desktop\\GZ_kdd\\"
def initTime():
    timeId=[]
    timeDay=[]
    timeMin=[]
    startDay = datetime.datetime.strptime("2016-06-01","%Y-%m-%d")
    startTime = datetime.datetime.strptime("08:00:00","%H:%M:%S")
    for i in range(0,30,1):
        endDay = startDay + datetime.timedelta(days=i)
        timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
    for i in range(0,62,2):
        endTime = startTime + datetime.timedelta(minutes=i)
        timeMin.append(datetime.datetime.strftime(endTime,"%H:%M:%S"))
    for i in range(len(timeDay)):
        for j in range(len(timeMin)-1):
            timeId.append("["+timeDay[i]+" "+timeMin[j]+","+timeDay[i]+" "+timeMin[j+1]+")")
    return timeId

def initLinkId():
    linkid=[]
    with open(path+"gy_contest_link_info.txt") as f:
        f.readline()
        all = f.readlines()
        for i in range(len(all)):
            linkid.append(all[i].split(";")[0])
    return linkid
#获取linkid对应的数字
def initLinkId_num():
    linkDict = {}
    with open(path + "reDict.json") as f:
        linkDict = json.loads(f.read())
    return linkDict
#计算一个link的MAPE
def my_score(Y_real, Y_pred):
    loss = 0
    cnt = 0
    for i in range(len(Y_real)):
        if float(Y_real[i]) == 0:
            continue
        else:
            loss += abs(float(Y_pred[i])/float(Y_real[i])-1)
            cnt += 1
    return loss/cnt
def compareFile(file1,file2,file3):
    linkid = initLinkId()
    linkdict = initLinkId_num()
    result_dict_1={}
    result_dict_2={}
    result_dict_3={}
    fin_result_1={}
    fin_result_2 = {}
    fin_result_3={}
    for i in linkid:
        result_dict_1[i]=[]
        result_dict_2[i]=[]
        result_dict_3[i]=[]
        fin_result_1[i]=[]
        fin_result_2[i]=[]
        fin_result_3[i]=[]
    with open(path+"selfValid\\"+file1) as f1:
        all = f1.readlines()
        for i in range(len(all)):
            values = all[i].replace("\n","").split("#")
            result_dict_1[values[0]].append((values[1],values[3]))
        for i in result_dict_1:
            result_dict_1[i] = sorted(result_dict_1[i])
            for j in result_dict_1[i]:
                fin_result_1[i].append(j[1])
    with open(path+"selfValid\\"+file2) as f2:
        all = f2.readlines()
        for i in range(len(all)):
            values = all[i].replace("\n","").split("#")
            result_dict_2[values[0]].append((values[1],values[3]))
        for i in result_dict_2:
            result_dict_2[i] = sorted(result_dict_2[i])
            for j in result_dict_2[i]:
                fin_result_2[i].append(j[1])
    with open(path+"selfValid\\"+file3) as f3:
        all = f3.readlines()
        for i in range(len(all)):
            values = all[i].replace("\n","").split("#")
            result_dict_3[values[0]].append((values[1],values[3]))
        for i in result_dict_3:
            result_dict_3[i] = sorted(result_dict_3[i])
            for j in result_dict_3[i]:
                fin_result_3[i].append(j[1])

    MAPE = {}
    for idx in range(1,133):
        MAPE[idx] = 0
    for i in linkid:
        # x = np.array(range(900))
        y1 = np.array(fin_result_1[i])
        y2 = np.array(fin_result_2[i])
        y3 = np.array(fin_result_3[i])
        # plotInOneFigure(linkdict[i],x,y1,y2,y3,file1,file2,file3)
        # plotInOneSubFigure(linkdict[i], x, y1, y2, y3, file1, file2, file3)
        MAPE[linkdict[i]] = my_score(y1,y2)
        # y1_y3 = my_score(y1,y3)
    xlabel = sorted(MAPE.keys())
    ylabel = []
    for key,value in MAPE.items():
        ylabel.append(value)
    print(min(MAPE.items(), key=lambda x: x[1]))
    print(max(MAPE.items(), key=lambda x: x[1]))
    plotMapeFigure("MAPE",xlabel,ylabel,file2)
    # plotMapeFigure(i,x,y1_y3, file3)
def plotMapeFigure(i,x,y,name):
    plt.figure()
    plt.plot(x, y, color="blue", linewidth=2.5, linestyle="-", label=name+"_MAPE")
    plt.xlabel("Linkid")  # X轴标签
    plt.ylabel("MAPE")  # Y轴标签
    plt.title(i)  # 标题
    plt.legend(loc='upper right')
    plt.show()
#将所有图像画在一张图表中
def plotInOneFigure(i,x,y1,y2,y3,file1,file2,file3):
    plt.figure()
    plt.plot(x,y1,color="blue", linewidth=2.5, linestyle="-",label=file1.split(".")[0])
    plt.plot(x,y2,color="red",  linewidth=2.5, linestyle="-",label=file2.split(".")[0])
    plt.plot(x,y3,color="green", linewidth=2.5, linestyle="-", label=file3.split(".")[0])
    plt.xlabel("time")  # X轴标签
    plt.ylabel("TrafficVolume")  # Y轴标签
    plt.title(i)  # 标题
    plt.legend(loc='upper right')
    plt.show()
#将所有图像画在不同的sub图中
def plotInOneSubFigure(i,x,y1,y2,y3,file1,file2,file3):
    plt.figure()
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
    plt.sca(ax1)
    plt.plot(x,y1,color="blue", linewidth=2.5, linestyle="-",label=file1.split(".")[0])
    plt.ylabel("TrafficVolume")  # Y轴标签
    plt.title(i)  # 标题
    plt.legend(loc='upper right')
    plt.sca(ax2)
    plt.plot(x,y2,color="red",  linewidth=2.5, linestyle="-",label=file2.split(".")[0])
    plt.ylabel("TrafficVolume")  # Y轴标签
    plt.legend(loc='upper right')
    plt.sca(ax3)
    plt.plot(x,y3,color="green", linewidth=2.5, linestyle="-", label=file3.split(".")[0])
    plt.xlabel("time")  # X轴标签
    plt.ylabel("TrafficVolume")  # Y轴标签
    plt.legend(loc='upper right')
    plt.show()
if __name__ == '__main__':
    compareFile("selfValid_TrueY.txt","selfValid_lastValue_1.1.txt","selfvalid_SVRAndfcnmean5KNNLastValue1.0.txt")
