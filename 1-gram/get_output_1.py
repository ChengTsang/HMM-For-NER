
#!/usr/bin/python3
import numpy as np
def readfile(file):
    return open(file, "r")


def emission(numerator, denominator):
    result = float(numerator / denominator)
    return(np.log(result))

def simpletagger(rare_count, filedev, fileout):
# In the following steps, there are totally 8 types of named entities and I put all of them in a dictionary.
# Then I count each word's different tags and also put them in another dictionary.
    b = readfile(rare_count)
    tagRecord = {}
    wordRecord = {}
    for line in b:
        if "1-GRAM" in line:
            item = line.split(" ")
            if item[-1].strip("\n") in tagRecord:
                tagRecord[item[-1].strip("\n")] += int(item[0])
            else:
                tagRecord[item[-1].strip("\n")] = int(item[0])
        if "WORDTAG" in line:
            segment = line.split(" ")
            quantity = segment[0]
            tag = segment[2]
            word = segment[3].strip("\n")
            if word not in wordRecord:
                wordRecord[word] = {}
            if tag not in wordRecord[word]:
                wordRecord[word][tag] = quantity
    wordCal = {}
    for tag in tagRecord: 
        for word in wordRecord:
            if word not in wordCal:
                wordCal[word] = {}
            if tag in wordRecord[word]:     # if some tag exists in some word's dictionary
                wordCal[word][tag] = emission(int(wordRecord[word][tag]), int(tagRecord[tag]))
#wordCal contains the ratio of each tag of each word.

    wordStd = {}   #wordStd will contain the max tag ratio one of each word in wordCal.
    for word in wordCal:
        if word not in wordStd:
            wordStd[word] = {}
        max_value = max(wordCal[word].values())
        tag = [k for k, v in wordCal[word].items() if v == max_value]
        wordStd[word][''.join(tag)] = max_value
    
    newfile = open(fileout, "w")
    devFile = readfile(filedev)
    for line in devFile:
        if line.strip("\n") == "":
            newfile.write("".join(["\n"]))
        elif line.strip("\n") not in wordStd:
            assignTag = [k for k, v in wordStd['_RARE_'].items()]
            prediction = [v for k, v in wordStd['_RARE_'].items()]
            newfile.write("".join([line.strip("\n") + " ", ''.join(assignTag)+" ", str(prediction).strip("[]"), "\n"]))
        else:
            assignTag = [k for k, v in wordStd[line.strip("\n")].items()]
            prediction = [v for k, v in wordStd[line.strip("\n")].items()]
            newfile.write("".join([line.strip("\n") + " ", ''.join(assignTag)+" ", str(prediction).strip("[]"), "\n"]))
    newfile.close()
    #print(wordStd['Taipei'])

def run():
    simpletagger('ner_rare.counts', 'ner_dev.dat', 'output_1.txt')
run()
#a= emission('mind', 'O', 'ner.counts')
#print(a)

