from __future__ import division
import random
import math
from sklearn import svm

year_span = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]

num_test = 15000

f = open('emotion_vector.txt', 'r')
data = f.read().split("\n")
data = [x.split() for x in data]
data.pop(len(data) - 1)

random.shuffle(data)

train = data[num_test + 1:]
test = data[:num_test]

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

acc = 0
for i in range(len(pred_y)):
    #print(pred_y[i], test_y[i])
    if math.fabs(test_y[i] - pred_y[i]) < 3:
        acc += 1
acc /= len(pred_y)
print(acc)


