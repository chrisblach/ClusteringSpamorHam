# ClusteringSpamorHam

For this assignment we decided to do DBScan clusters. 
It actually worked really well as all the spam ending up being outliers (classed as -1)

Top Score:
To be very honest, the top score that our group got was only done using regex, in a very trivial manner. 
If it sees a phone number then it marks as spam, if the text has more than 10 digits than it is also spam and so on.

Clustering:
For the clustering algorithm, we also used regex to extract features labelling them as true and false. 
We then used dbscan to cast a short net on the easy spam, we then eliminated the easy spam, reducing the document
and tried to cluster the remaining texts. This worked very well, and we actually lost the paramters after trying to tweak
it a lot of times. 
As DBScan is very sensitive to parameters, if we had a lot of time to tweak the parameters,
we think this algorithm can go really far. 
We are not good at regex, so fixing the feature extraction regex would give a better score.

newApproach.py:
Clustering algorithm. Give it the Documents.csv, and specify outputs throughout the code.

trivial.py:
Just regex, very simple but got the highest score. Give it the Documents.csv, and specify output.

Both file should run normally if you have all libraries
