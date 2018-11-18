
#!/usr/bin/python
def readfile(file):
    return open(file, "r")


def emission(word, tag, file):
    a = readfile(file)
    numerator = 1
    denominator = 0
    for line in a:
        if tag in line.split():
            denominator += float(line.split(" ")[0])
        if word in line.split() and (" "+"WORDTAG"+" ") in line:
            numerator = float(line.split(" ")[0])
    return(numerator / denominator)

def replacewords(f_count, f_raw, f_write):
    b = readfile(f_count)
    record = {}
    for line in b:
        if "WORDTAG" in line:
            item = line.split(" ")
            # We need to see the whole dataset and determine how many times each word is occurring, 
            # irrespective of the tags. For example, 'Taipei' is occurring 5 times with tag 'I-LOC' and once with tag 'I-ORG'. 
            # This means it is occurring 6 times in the entire dataset, which means it is not an infrequent word. 
            if item[-1].strip("\n") in record:
                record[item[-1].strip("\n")] += int(item[0])    
            else:
                record[item[-1].strip("\n")] = int(item[0])  
    for key in record.copy():
        if record[key]>=5:
            del record[key]

    raw = readfile(f_raw)
    newfile = open(f_write, "w")
    for row in raw:
        segments = row.split(" ")
        if segments[0] in record:
            segments[0] = "_RARE_"
        newfile.write(" ".join(segments))

r1 = replacewords('ner.counts','ner_train.dat','ner_train_rare.dat')
#a= emission('mind', 'O', 'ner.counts')
#print(a)

