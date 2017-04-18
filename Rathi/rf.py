import csv
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt

with open("nodetable.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    symp = []
    dise = []
    for row in reader:
        if row[2] == 'symptom':
            symp.append(row[1])
        if row[2] == 'disease':
            dise.append(row[1])
    print dise, len(dise)
    print symp, len(symp)



def predictDisease(symptoms):
    #create the training & test sets, skipping the header row with [1:]
    dataset = genfromtxt(open('dataset1.csv','r'), delimiter=',', dtype='f8')[1:]   
    target = [x[407] for x in dataset]
    train = [x[0:405] for x in dataset]
    test = genfromtxt(open('test.csv','r'), delimiter=',', dtype='f8')[1:]
    
    #create and train the random forest
    #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    rf = RandomForestClassifier(n_estimators=1000)
    rf.fit(train, target)


    nsymp = len(symp)            
    check = [0 for col in range(nsymp)]

    #symptoms = ['fever','snuffle','throat sore','malaise' ]

    for i in symptoms:
        check[symp.index(i)] = 1
        
    savetxt('submission2.csv', rf.predict_proba([check]), delimiter=',', fmt='%f')
    
    # savetxt('submission2.csv', rf.predict_proba(test), delimiter=',', fmt='%f')
