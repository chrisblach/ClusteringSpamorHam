import csv
import re
import nltk
from sklearn.cluster import KMeans, MiniBatchKMeans, Birch, DBSCAN
import numpy as np
import operator

website = False
money = False
phone = False
pobox = False
porn = False
morethan10digits = False
allRows = ()
clusterRows = ()
x = ()
y = ()

#Parse text to get some features
with open('Documents.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    rowcount = 0
    count = 0
    for row in data:

        if rowcount is 0:
            text = row[1]
        else:
            text = row[1]
            if (re.search("wap|www|http|co\.uk|\.ac|\.biz|\.net|\.tv", text, re.IGNORECASE) is not None):
                count += 1
                website = True
                if re.search("sent via|fullonsms|indyarocks|\.netw", text, re.IGNORECASE):
                    #print text
                    #website = True
                    count -= 1
                    website = False
                    #print "Skipped!"
                    #print str(rowcount) + " " + text + " length of text: " + str(len(text)) + " number of words: " + str(len(text.split())) + " ratio w/sms: " + str(len(text)/ len(text.split())) + " digits: " + str(sum(c.isdigit() for c in text))
            if (re.search("0800|0808|090|084|087|090|880", text) is not None):
                phone = True
                #print str(rowcount) + " " +text
            if (re.search(ur'[\u00A3]+', text) is not None):
                money = True
                #print text
            elif (re.search("\d+\s?p", text, re.IGNORECASE) is not None):
                #not pm
                if (re.search("\d+\s?pm", text, re.IGNORECASE) is not None):
                    print "Skipped"
                #I cant regex properly so these are some edge cases
                elif (re.search("\d+\s?p[l|a|r|i|u]", text, re.IGNORECASE) is not None):
                    print "Skipped"
                else:
                    money = True
                    #print text
            elif (re.search("pound",text, re.IGNORECASE) is not None):
                money = True
                #print text
            if (re.search("bo?x\d+", text, re.IGNORECASE)):
                pobox = True
                #print text
            elif (re.search("pobox", text, re.IGNORECASE)):
                pobox = True
                #print text
            if (re.search("xxx\S?[a-zA-Z]", text) is not None):
                porn = True
                print str(rowcount) + " " +text
            from functions import text_to_words
            lengthOfText = len(text)
            numberofWords = len(text.split())
            ratio = float(float(lengthOfText)/float(numberofWords))
            #ratio = lengthOfText/numberofWords
            countNumbers = sum(c.isdigit() for c in text)
            if (countNumbers > 3):
                morethan10digits = True
                countNumbers = 1
            else:
                countNumbers = 0
            digitstoWords = float(float(countNumbers)/float(numberofWords))
            text = text_to_words(text, remove_stop=True, stem=True)
            x = (rowcount, text, lengthOfText, numberofWords, ratio, countNumbers, website, money, pobox, phone, digitstoWords, porn, morethan10digits)
            #y = (len(text), len(text.split()), len(text)/ len(text.split()), sum(c.isdigit() for c in text), website, money, pobox, phone)
            y = (website, money, pobox, phone,morethan10digits)
            allRows = allRows + (x,)
            clusterRows = clusterRows + (y,)
            website = False
            phone = False
            money = False
            pobox = False
            porn = False
            morethan10digits = False
        rowcount += 1
    print rowcount - 1
    print count

with open('DocumentsFETest2.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["SMS_id", "SMS", "Length", "Words", "Ratio", "# of Digits", "Website", "Money", "POBOX", "Phone", "Digits to words", "porn","morethan10digits"])
    for row in allRows:
        writer.writerow([row[0] , row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]])

dictX = {}
with open('DocumentsFETest2.csv', 'rb') as csvfile:
    data2 = csv.reader(csvfile, delimiter=',')
    rowcount2 = 0
    for row in data2:
        if rowcount2 is 0:
            text2 = row[1]
        else:
            text2 = row[1]
            text2 = text2.split()
            for frag in text2:
                if dictX.has_key(frag):
                    dictX[frag] += 1
                else:
                    dictX[frag] = 1
        rowcount2 += 1


sorted_dict = sorted(dictX.items(), key=operator.itemgetter(1), reverse=True)
print sorted_dict
dict2 = {}
sorted_index = 0
for index in sorted_dict:
    if sorted_dict[sorted_index][1] > 9:
        dict2[sorted_dict[sorted_index][0]] = sorted_dict[sorted_index][1]
    sorted_index += 1
print dict2

print len(dict2)
x1 = ()
y1 = [0] * (len(dict2))
with open('DocumentsFETest2.csv', 'rb') as csvfile:
    data3 = csv.reader(csvfile, delimiter=',')
    rowcount3 = 0
    for row in data3:
        rowcount3 += 1
        if rowcount3 is 1:
            text3 = row[1]
        else:
            text3 = row[1]
            split = text3.split()
            for frag in split:
                if dict2.has_key(frag):
                    y1[dict2.keys().index(frag)] = 1
            #tpy = tuple(y1)
            from functions import stringToBool, stringToFloat
            tpy = ()
            ratioFinal = stringToFloat(row[4])
            #print ratioFinal
            digitsFinal = int(row[5])
            websiteFinal = stringToBool(row[6])
            moneyFinal = stringToBool(row[7])
            poboxFinal = stringToBool(row[8])
            phoneFinal = stringToBool(row[9])
            digitstoWordsFinal = stringToFloat(row[10])
            pornFinal = stringToBool(row[11])
            morethan10Final = stringToBool(row[12])
            tpy = (ratioFinal, digitsFinal, websiteFinal, moneyFinal, poboxFinal, phoneFinal, digitstoWords, pornFinal)
            x1 = x1 + (tpy,)
            y1 = [0] * (len(dict2))
    print x1[115]

#Cluster
X = np.array(clusterRows)
#km = MiniBatchKMeans(n_clusters=2, init='k-means++', max_iter=100,batch_size=100, verbose=0, compute_labels=True, random_state=None, tol=0.0, max_no_improvement=10, init_size=None, n_init=50, reassignment_ratio=0.01)
#km = Birch(threshold=0.5, branching_factor=50, n_clusters=2, compute_labels=True, copy=True)
km = DBSCAN(eps=0.5, min_samples=130, metric='euclidean', algorithm='auto', leaf_size=30, p=None)
print("Clustering sparse data with %s" % km)
#idx = km.fit(X)
labels = km.fit_predict(X)
RC = rowcount
row_dict = [0]*(RC)
for i in range(0, (RC)):
    row_dict[i] = i+1

results = [1]*(RC-1)
clusters = {}
n = 0
len(row_dict)
for item in labels:
    if item in clusters:
        clusters[item].append(row_dict[n])
    else:
        clusters[item] = [row_dict[n]]
    n += 1
for item in clusters:
    print (len(clusters[item]))
    print "Cluster ", item
    itemInt = int(item)
    # if itemInt is 0:
    #     print str(i) + " text: " + allRows[i - 1][1]
    #     results[i - 1] = 1
    # elif itemInt is 1:
    #     print str(i) + " text: " + allRows[i - 1][1]
    #     results[i - 1] = 0
    if itemInt is -1:
        for i in clusters[item]:
            print str(i) + " text: " + allRows[i - 1][1]
            results[i - 1] = 0
    elif itemInt is 7:
        for i in clusters[item]:
            print i
            #results[i - 1] = 0
    else:
        for i in clusters[item]:
            print i
numberofspam = 0
numberToParse = 0
for i in range(0,len(results)):
    if results[i] is 0:
        numberofspam += 1
    else:
        numberToParse += 1

    print str(i + 1) + " label: " + str(results[i])
print numberofspam

makedocument = "DocumentsTryingOther5.csv"
with open(makedocument, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["SMS_id", "label"])
    for i in range(0,len(results)):
        writer.writerow([i+1, results[i]])

clusterRows2 = ()
##################
# Parse text to get some features
print numberToParse

mapping = [0]*numberToParse
print len(mapping)
L = 0
with open('Documents.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    rowcount = 0
    count = 0
    for row in data:
        if rowcount is 0:
            text = row[1]
        else:
            text = row[1]
            if (re.search("wap|www|http|co\.uk|\.ac|\.biz|\.net|\.tv", text, re.IGNORECASE) is not None):
                count += 1
                website = True
                if re.search("sent via|fullonsms|indyarocks|\.netw", text, re.IGNORECASE):
                    # print text
                    # website = True
                    count -= 1
                    website = False
                    # print "Skipped!"
                    # print str(rowcount) + " " + text + " length of text: " + str(len(text)) + " number of words: " + str(len(text.split())) + " ratio w/sms: " + str(len(text)/ len(text.split())) + " digits: " + str(sum(c.isdigit() for c in text))
            if (re.search("0800|0808|090|084|087|090|880", text) is not None):
                phone = True
                # print str(rowcount) + " " +text
            if (re.search(ur'[\u00A3]+', text) is not None):
                money = True
                # print text
            elif (re.search("\d+\s?p", text, re.IGNORECASE) is not None):
                # not pm
                if (re.search("\d+\s?pm", text, re.IGNORECASE) is not None):
                    print "Skipped"
                # I cant regex properly so these are some edge cases
                elif (re.search("\d+\s?p[l|a|r|i|u]", text, re.IGNORECASE) is not None):
                    print "Skipped"
                else:
                    money = True
                    # print text
            elif (re.search("pound", text, re.IGNORECASE) is not None):
                money = True
                # print text
            if (re.search("bo?x\d+", text, re.IGNORECASE)):
                pobox = True
                #print text
            elif (re.search("pobox", text, re.IGNORECASE)):
                pobox = True
                # print text
            if (re.search("xxx", text) is not None):
                porn = True
                # print str(rowcount) + " " +text
            from functions import text_to_words

            lengthOfText = len(text)
            numberofWords = len(text.split())
            ratio = float(float(lengthOfText) / float(numberofWords))
            # ratio = lengthOfText/numberofWords
            countNumbers = sum(c.isdigit() for c in text)
            if (countNumbers > 10):
                morethan10digits = True
            digitstoWords = float(float(countNumbers) / float(numberofWords))
            text = text_to_words(text, remove_stop=True, stem=True)
            #x = (rowcount, text, lengthOfText, numberofWords, ratio, countNumbers, website, money, pobox, phone,
                 #digitstoWords, porn, morethan10digits)
            # y = (len(text), len(text.split()), len(text)/ len(text.split()), sum(c.isdigit() for c in text), website, money, pobox, phone)
            if (results[rowcount-1] is 1):
                y = (countNumbers, website, money, pobox, phone, morethan10digits)
                #allRows = allRows + (x,)
                clusterRows2 = clusterRows2 + (y,)
                #mapping = mapping + (rowcount,)
                mapping[L] = rowcount
                L += 1
            website = False
            phone = False
            money = False
            pobox = False
            porn = False
            morethan10digits = False
        rowcount += 1
    print rowcount - 1
    print count
print mapping
print len(mapping)
print numberofspam
##################


X = np.array(clusterRows2)
#km = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1)
km = DBSCAN(eps=0.5, min_samples=25, metric='euclidean', algorithm='auto', leaf_size=30, p=None)
print("Clustering sparse data with %s" % km)
#idx = km.fit(clusterRows2)
labels = km.fit_predict(X)
RC = rowcount
row_dict = [0]*(RC)
for i in range(0, (RC)):
     row_dict[i] = i+1

clusters = {}
n = 0
len(row_dict)
for item in labels:
     if item in clusters:
         clusters[item].append(row_dict[n])
     else:
         clusters[item] = [row_dict[n]]
     n += 1
numberofspam2 = 0
for item in clusters:
     print (len(clusters[item]))
     print "Cluster ", item
     itemInt = int(item)
     if itemInt is -1:
         for i in clusters[item]:
             print str(mapping[i-1]) + " text: " + allRows[mapping[i-1]-1][1]
             if (len(allRows[mapping[i-1]-1][1]) > 0):
                results[mapping[i-1] - 1] = 0
                numberofspam2 += 1
     else:
         for i in clusters[item]:
             print str(mapping[i-1]) + " text: " + allRows[mapping[i-1]-1][1]
#print numberofspam2
#totalspam = (numberofspam + numberofspam2)
totalspam = 0


for i in range(0,len(results)):
    if results[i] is 0:
        totalspam += 1
    print str(i + 1) + " label: " + str(results[i])
print "Total: " + str(totalspam)

makeDoc = "leaveOut2.csv"
with open(makeDoc, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["SMS_id", "label"])
    for i in range(0,len(results)):
        writer.writerow([i+1, results[i]])