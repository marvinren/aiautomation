# -*-coding:utf-8-*-
import os
from BasicFunction import CONFIG

SplitLen = 0
runTag = "sub"


def getChr(wPath):
    global SplitLen
    # convert to jpg format to bmp  tesseract.exe result.bmp 1 -psm 10 digits
    if os.path.isfile(wPath + "\\result.bmp"):
        os.system("del " + wPath + "\\*.bmp")
    if os.path.isfile(wPath + "\\1.txt"):
        os.system("del " + wPath + "\\*.txt")
    # nconvert -quiet -out bmp -merge_alpha result.png
    # force converting to 24bit bitmap!
    os.system(wPath + "\\nconvert.exe -quiet -out bmp -merge_alpha " + wPath + "\\result.png")
    os.system("copy " + wPath + "\\result.bmp " + wPath + "\\result_r.bmp")
    with open(wPath + "\\result.bmp", "rb") as f1:
        tmp1 = f1.read()

    # confirm split length
    startTag = ord(tmp1[10])  # bitmap start location
    pWidth = ord(tmp1[18])  # width of bitmap in pixel
    pHeigh = ord(tmp1[22])  # heigh of bitmap in pixel
    tBits = len(tmp1[startTag:])  # total bit of bitmap
    SplitLen = (tBits - pHeigh * pWidth * 3) / pHeigh
    # print "startTag="+str(startTag),"pWidth="+str(pWidth),"pHeigh="+str(pHeigh),"tBits="+str(tBits),"spliteLen="+str(SplitLen)

    # copy a new list(for modification)
    pHead = tmp1[0:startTag]
    # copy and convert data of bitmap
    pBody = []
    tmpPix = []

    # get a list that contains the useless(split data) number
    i = 0
    excludeList = []
    while i < tBits:
        #         i=i+pWidth*3
        #         for j in range(1,SplitLen+1):
        #             excludeList.append(startTag+i+j)
        #         i=i+SplitLen
        i = i + pWidth * 3
        for j in range(0, SplitLen):
            # tmp1�����ʵ��λ�ô�0��ʼ������append����-1
            excludeList.append(startTag + i + j + 1)
        i = i + SplitLen
    # print excludeList
    iii = 1
    jjj = 1
    for i in range(startTag, tBits + startTag + 1):
        if i in excludeList:
            iii += 1
            pBody.append(chr(255))
            tmpPix = []
            # print i,len(pBody)
        else:
            jjj += 1
            try:
                tmpPix.append(tmp1[i])
            except Exception, e:
                if i == len(tmp1):
                    print 'error and continue'
                    print i, len(tmp1)
            if len(tmpPix) >= 3:
                # adjust the RGB value,the sequence is b-g-r in tmpPix[0]-tmpPix[2]
                pBody.extend(_adjustRGBValue(tmpPix))
                tmpPix = []
    print len(pBody)
    print iii, jjj

    # auth code pictrue writen into a new bmp file
    with open(wPath + "\\result.bmp", "wb") as f2:
        f2.write(''.join(pHead) + ''.join(pBody))

    # get the split location from the data of result.bmp in yLoc
    cmpStr = chr(255) * pHeigh * 3
    yLine = []
    for i in range(0, pWidth):
        tmpStr = []
        for j in range(0, pHeigh):
            tmpStr.append(pBody[i * 3 + pWidth * j * 3 + SplitLen * j])
            tmpStr.append(pBody[i * 3 + pWidth * j * 3 + SplitLen * j + 1])
            tmpStr.append(pBody[i * 3 + pWidth * j * 3 + SplitLen * j + 2])
        if ''.join(tmpStr) != cmpStr:
            yLine.append(i)
    # print yLine
    yLoc = []
    j = len(yLine)
    yLoc.append(yLine[0])
    for i in range(1, j):
        if yLine[i] - 1 != yLine[i - 1]:
            yLoc.append(yLine[i - 1])
            yLoc.append(yLine[i])
    yLoc.append(yLine[j - 1])
    # print yLoc

    # generate split bmp files according to yLoc
    i = 0
    j = 1
    while i < len(yLoc):
        tmpCmd = wPath + "\\nconvert -quiet -o " + wPath + "\\" + str(j) + ".bmp -crop " + str(
            yLoc[i] - 1) + " 0 " + str(yLoc[i + 1] - yLoc[i] + 2) + " " + str(pHeigh) + " " + wPath + "\\result.bmp"
        # os.system(wPath+"\\nconvert -quiet -o "+wPath+"\\%d.bmp -crop %d 0 %d %d "+wPath+"\\result.bmp" % (j,yLoc[i]-1,yLoc[i+1]-yLoc[i]+2,pHeigh))
        os.system(tmpCmd)
        i = i + 2
        j = j + 1

    # call tesseract to convert bmp files
    for i in range(1, len(yLoc) / 2 + 1):
        tmpCmd = wPath + "\\tesseract.exe " + wPath + "\\" + str(i) + ".bmp " + wPath + "\\" + str(
            i) + " -psm 10 digits"
        os.system(tmpCmd)

    # get the result from txt files
    cmpStr = ""
    for i in range(1, len(yLoc) / 2 + 1):
        with open(wPath + "\\" + str(i) + ".txt") as f1:
            cmpStr = cmpStr + f1.readline()[0:1]
    return cmpStr


def _adjustRGBValue(inPix):
    global runTag
    # len(inPix) must be 3
    tmpPix = []
    # modify value in B
    if runTag == "main":
        tmpB = 0
        tmpG = 89
        tmpR = 70
    else:
        tmpB = int(CONFIG['rgb_B'])
        tmpG = int(CONFIG['rgb_G'])
        tmpR = int(CONFIG['rgb_R'])
    if tmpB < ord(inPix[0]) and tmpG < ord(inPix[1]) and tmpR < ord(inPix[2]):
        # tmpPix=[chr(255),chr(255),chr(255)] if len(inPix)==3 else [chr(255),chr(255),chr(255),chr(255)]
        while len(tmpPix) < 3:
            tmpPix.append(chr(255))
            # tmpPix=inPix
    else:
        # tmpPix=[chr(17),chr(17),chr(17)] if len(inPix)==3 else [chr(17),chr(17),chr(17),chr(17)]
        while len(tmpPix) < 3:
            tmpPix.append(chr(17))
    return tmpPix


def getSplitLenth():
    global SplitLen
    return SplitLen


if __name__ == '__main__':
    runTag = "main"
    print getChr("E:\\workspace\\j2ee\\AutoTestPlatform\\AiTest\\dist\\ocr")
