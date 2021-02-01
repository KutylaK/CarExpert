from tkinter.ttk import Combobox
import tkinter as tk
import tkinter
from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier


l1=[
'rozrusznik nie kręci','światła się nie palą','samochód stał na mrozie','brak powietrza w kole','niski poziom oleju','biegi nie chcą się zmieniać','sprzęgło lekko się wciska','samochód zjeżdza z górki','głośny silnik','stuknięcia na górkach I dołkach','słaba siła hamowania','słaba siła silnika','wieksze zuzycie paliwa','miękki pedał hamulca','spryskiwacze nie działaja','wysoka temperatura silnika','samochód gaśnie'
]

dataset = pd.read_csv("train.csv")
X = dataset.drop('diagnoza', axis=1)
y = dataset['diagnoza']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

print("Drzewo decyzyjne")
print()
classifier = tree.DecisionTreeClassifier(criterion="entropy", max_depth=10)
classifier = classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print()

fig = plt.figure(figsize=(35, 30))
_ = tree.plot_tree(classifier, feature_names=l1, filled=True, rounded=True)
plt.savefig('tree.png', bbox_inches='tight')

print("Las losowy")
print()
classifier_rf = RandomForestClassifier()
classifier_rf = classifier_rf.fit(X_train, y_train)
y_pred = classifier_rf.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print()

sampleTree = classifier_rf.estimators_[5]
fig = plt.figure(figsize=(35, 30))
_ = tree.plot_tree(sampleTree, feature_names=l1, filled=True, rounded=True)
plt.savefig('branch.png', bbox_inches='tight')

print("K-sąsiadów")
print()

classifier_k = KNeighborsClassifier(n_neighbors=3)
classifier_k = classifier_k.fit(X_train, y_train)
y_pred = classifier_k.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print()

def drzewo():
    predict = classifier.predict(x_values())
    t1.insert(END, predict[0])


def las_losowy():
    predict = classifier_rf.predict(x_values())
    t1.insert(END, predict[0])


def k_sasiadow():
    predict = classifier_k.predict(x_values())
    t1.insert(END, predict[0])


def x_values():
    l2 = [0] * len(l1)
    t1.delete("1.0", END)

    x_values = [cb1.current(), cb2.current(), cb3.current()]

    for k in range(0, len(l2)):
        if k in x_values:
            l2[k] = 1
    return [l2]

window = Tk()
window.title("System ekspercki - mechanik")
window.geometry("550x225")

label1 = Label(window, text="Objaw 1.")
label1.grid(row=6, column=2, padx=10, pady=(20, 0))

label2 = Label(window, text="Objaw 2.")
label2.grid(row=8, column=2, pady=(20, 0))

label3 = Label(window, text="Objaw 3.")
label3.grid(row=10, column=2, pady=(20, 0))

btn1 = Button(window, text="Zdiagnozuj drzewem decyzyjnym", command=drzewo, bg="gold", fg="black")
btn1.grid(row=6, column=6, padx=40, pady=(20, 0))

btn2 = Button(window, text="Zdiagnozuj lasem losowym", command=las_losowy, bg="gold", fg="black")
btn2.grid(row=8, column=6, pady=(20, 0))

btn3 = Button(window, text="Zdiagnozuj k-sąsiadów", command=k_sasiadow, bg="gold", fg="black")
btn3.grid(row=10, column=6, pady=(20, 0))

cb1 = Combobox(window, width=30)
cb1['values'] = l1
cb1.grid(row=6, column=3, pady=(20, 0))

cb2 = Combobox(window, width=30)
cb2['values'] = l1
cb2.grid(row=8, column=3, pady=(20, 0))

cb3 = Combobox(window, width=30)
cb3['values'] = l1
cb3.grid(row=10, column=3, pady=(20, 0))

t1 = Text(window, height=1, width=35, bg="green yellow", fg="black", font="none 12 bold")
t1.grid(row=17, column=3, columnspan=6)

label4 = Label(window, text="Decyzja:")
label4.grid(row=16, column=3, columnspan=6)

label5 = Label(window)
label5.grid(row=15, column=3, columnspan=6)

window.mainloop()
