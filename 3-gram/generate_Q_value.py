
#!/usr/bin/python3
import numpy as np
def readfile(file):
    return open(file, "r")


def emission(numerator, denominator):
    result = float(numerator / denominator)
    return(np.log(result))

def CalculateQ(yi_2, yi_1, yi):
    countRecord = readfile("ner_rare.counts")
    numerator = 0
    denominator = 0
    for line in countRecord:
        if "2-GRAM" in line:
            item = line.split(" ")
            if (yi_2 in item[2].split() and yi_1 in item[3].split()):
                denominator = float(item[0])
        if "3-GRAM" in line:
            eachLine = line.split(" ")
            if (yi_2 in eachLine[2].split() and yi_1 in eachLine[3].split() and yi in eachLine[4].split()):
                numerator = float(eachLine[0])       
    return emission(numerator, denominator)

def trigramCal(fileout='Q_value.txt'):
    target = readfile('trigrams.txt')
    newfile = open(fileout, "w")
    for trigram in target:
        trigramList = trigram.split(" ")
        prob = CalculateQ(trigramList[0],trigramList[1],trigramList[2].strip("\n"))
        newfile.write("".join([trigramList[0] + " ", trigramList[1]+" ", trigramList[2].strip("\n")+" ", str(prob), "\n"]))
    newfile.close()

def run():
    trigramCal()
run()

