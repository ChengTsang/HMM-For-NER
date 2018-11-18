
#!/usr/bin/python3
import numpy as np
def readfile(file):
    return open(file, "r")


def emission(numerator, denominator):
    result = float(numerator / denominator)
    return result
    #return(np.log(result))

def CalculateQ(yi_2, yi_1, yi):
    countRecord = readfile("ner_rare.counts")
    numerator = 0
    denominator = float('-inf')
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

def handle(file,dic):
    index = 0
    target = readfile(file)
    sentences = []
    dp_tag = [] #I create 2 lists respectively containing each whole sentence and each whole tag sequence.
    dp_prob = [] #I also create dp_prob list to store the probability of the tagged sequence up to each word.
    for each in target:
        word = each.strip("\n")
        if(word == ""):
            sentences.append([])
            dp_tag.append([])
            dp_prob.append([])
    #The following steps I input each seperate sentence into separate sentences list I created just now.
    target = readfile(file)
    for re_word in target:
        re_word = re_word.strip("\n")
        if(re_word != ""):
            sentences[index].append(re_word)
        else:
            index += 1

    count = 0
    for sentence in sentences: #Loop through the sentences in the target file
        Viterbi(len(sentence), sentence, dp_tag[count], dic, dp_prob[count])
        count += 1

    return (sentences, dp_tag, dp_prob)

def tagRatio():
    b = readfile('ner_rare.counts')
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
    return wordCal
#wordCal contains the ratio of each tag of each word.
    
def Viterbi(k, word_array, tag_array, dic, prob_array):
    if word_array[k-1] in dic:
        if k==1:
            a = [-1]*10
            tag = [k for k, v in dic[word_array[k-1]].items()]
            for i in range(len(tag)):
                a[i] = CalculateQ("*", "*", tag[i]) * float(dic[word_array[k-1]][tag[i]])
            (value,loc) = max((v,i) for i,v in enumerate(a))
            tag_array.append("*")
            tag_array.append("*")
            tag_array.append(tag[loc])
            prob_array.append(value)
            return value
  
        else:
            v = Viterbi(k-1, word_array, tag_array, dic, prob_array)
            b = [-1]*10
            tag = [k for k, v in dic[word_array[k-1]].items()]
            for i in range(len(tag)):
                b[i] = v * CalculateQ(tag_array[-2], tag_array[-1], tag[i]) * float(dic[word_array[k-1]][tag[i]])
            (value,loc) = max((x,y) for y,x in enumerate(b))
            tag_array.append(tag[loc])
            prob_array.append(value)
            return value
    else:
        if k==1:
            a = [-1]*10
            tag = [k for k, v in dic['_RARE_'].items()]
            for i in range(len(tag)):
                a[i] = CalculateQ("*", "*", tag[i]) * float(dic['_RARE_'][tag[i]])
            (value,loc) = max((v,i) for i,v in enumerate(a))
            tag_array.append("*")
            tag_array.append("*")
            tag_array.append(tag[loc])
            prob_array.append(value)
            return value
  
        else:
            v = Viterbi(k-1, word_array, tag_array, dic, prob_array)
            b = [-1]*10
            tag = [k for k, v in dic['_RARE_'].items()]
            for i in range(len(tag)):
                b[i] = v * CalculateQ(tag_array[-2], tag_array[-1], tag[i]) * float(dic['_RARE_'][tag[i]])
            (value,loc) = max((x,y) for y,x in enumerate(b))
            tag_array.append(tag[loc])
            prob_array.append(value)
            return value

def run():
    dic = tagRatio()
    (sentences, dp_tag, dp_prob) = handle('ner_dev.dat', dic)
    with open('output_2.txt', 'w+') as f:
        for p in range(len(dp_tag)):
            if p > 0:
                f.write("".join(["\n"]))
            for q in range(2, len(dp_tag[p])):
                f.write("".join([str(sentences[p][q-2])+' ', str(dp_tag[p][q])+' ', str(np.log(dp_prob[p][q-2])),'\n']))
        f.write("".join(["\n"]))
    
run()

