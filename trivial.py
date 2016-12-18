import csv
import re
import nltk
from sklearn.cluster import KMeans
import numpy as np

x = ()
trows = ()
spam = False

with open('Documents.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    rowcount = 0
    count = 0
    for row in data:
        if rowcount is 0:
            text = row[1]
        else:
            text = row[1]
            if sum(c.isdigit() for c in text) > 9:
                count += 1
                spam = True
                print "greater!"
                print str(rowcount) + " " + text
            if (re.search("wap|www|http|co\.uk|\.ac|\.biz|\.net|\.tv", text, re.IGNORECASE) is not None):
                if spam is not True:
                    count += 1
                spam = True
                if re.search("sent via|fullonsms|indyarocks|\.come|\.netw", text, re.IGNORECASE):
                    #print text
                    spam = False
                    print "Skipped!"
            if (re.search("0800|0808|090|084|087|090|880", text) is not None):
                if spam is not True:
                    count += 1
                phone = True
                spam = True
                #print text
            if (re.search(ur'[\u00A3]+', text) is not None):
                if spam is not True:
                    count += 1
                spam = True
                money = True
                #print text
            elif (re.search("\d+\s?p", text, re.IGNORECASE) is not None):
                if (re.search("\d+\s?pm", text, re.IGNORECASE) is not None):
                    print "Skipped"
                elif (re.search("\d+\s?p[l|a|r|i|u]", text, re.IGNORECASE) is not None):
                    print "Skipped"
                else:
                    if spam is not True:
                        count += 1
                    spam = True
                    money = True
                #print text
            elif (re.search("pound",text, re.IGNORECASE) is not None):
                money = True
                #print text
            if (re.search("bo?x\d+", text)):
                if spam is not True:
                    count += 1
                spam = True
                pobox = True
                #print text
            elif (re.search("pobox", text, re.IGNORECASE)):
                if spam is not True:
                    count += 1
                spam = True
                pobox = True
                # print text
            # allRows = allRows + (x,)
            # clusterRows = clusterRows + (y,)
            website = False
            phone = False
            money = False
            pobox = False
        if (spam is False and rowcount is not 0):
            x = (rowcount, 1)
            trows = trows + (x,)
        elif spam is True:
            x = (rowcount, 0)
            trows = trows + (x,)
        spam = False
        rowcount += 1
    print rowcount - 1
    print count
    print trows

with open('DocumentsFE4.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["SMS_id", "label"])
    for row in trows:
        writer.writerow([row[0], row[1]])