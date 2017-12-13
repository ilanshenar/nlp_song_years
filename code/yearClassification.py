from __future__ import division
import random
import math
from sklearn import svm

year_span = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]

#num_test = 50
max_num_songs_from_year = 20

f = open('../text/emotion_vector_50spy.txt', 'r')
data = f.read().split("\n")
data = [x.split(",") for x in data]
data.pop(len(data) - 1)

random.shuffle(data)

train_year_count = {y: 0 for y in year_span}

train = []
test = []

for d in data:
    if train_year_count[str(d[1])] >= max_num_songs_from_year:
        train.append(d)
    else:
        test.append(d)
        train_year_count[str(d[1])] += 1
        
print (train_year_count)

test_x = []
test_y = []

train_x = []
train_y = []

for x in test:
    features = [float(y) for y in x[3:9]]
    test_x.append(features)
    test_y.append(int(x[1]))
    
for x in train:
    features = [float(y) for y in x[3:9]]
    train_x.append(features)
    train_y.append(int(x[1]))
    
clf = svm.SVR()
clf.fit(train_x, train_y)
pred_y = clf.predict(test_x)

correctly_classified = {y: 0 for y in year_span}

acc = 0
for i in range(len(pred_y)):
    #print(pred_y[i], test_y[i])
    if math.fabs(test_y[i] - pred_y[i]) < 2:
        acc += 1
        correctly_classified[str(test_y[i])] += 1
acc /= len(pred_y)
print(acc)

print (correctly_classified)


