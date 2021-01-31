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

disease=[
'rozładowany akumulator','zepsuty rozrząd','zapowietrzone hamulce','zła rozbieżność kół','słaby hamulec ręczny','brak płynu do spryskiwaczy','zamarznięty płyn do spryskiwaczy','przepalony bezpiecznik','dziurawe koło','peknięta miska olejowa','zepsuta skrzynia biegów','zepsute sprzęgło','zużyty filtr powietrza','awaria chłodnicy','brak benzyny'
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
_ = tree.plot_tree(classifier, feature_names=l1, filled=True)
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



print("K-sąsiadów")
print()

classifier_k =  KNeighborsClassifier(n_neighbors=3)
classifier_k = classifier_k.fit(X_train,y_train)
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

    x_values = [Symptom1.get(), Symptom2.get(), Symptom3.get()]

    for k in range(0, len(l2)):
        if l1[k] in x_values:
            l2[k] = 1

    return [l2]


root = Tk()
root.configure(background='gray')

Symptom1 = StringVar()
Symptom1.set(None)
Symptom2 = StringVar()
Symptom2.set(None)
Symptom3 = StringVar()
Symptom3.set(None)



w2 = Label(root, justify=CENTER, text="System ekspercki - Mechanik", fg="white", bg="gray")

w2.grid(row=1, column=0, columnspan=2, padx=100)

S1Lb = Label(root, text="Objaw 1", fg="yellow", bg="black")
S1Lb.grid(row=7, column=0, pady=10, sticky=W)

S2Lb = Label(root, text="Objaw 2", fg="yellow", bg="black")
S2Lb.grid(row=8, column=0, pady=10, sticky=W)

S3Lb = Label(root, text="Objaw 3", fg="yellow", bg="black")
S3Lb.grid(row=9, column=0, pady=10, sticky=W)


lrLb = Label(root, text="Diagnoza", fg="white", bg="red")
lrLb.grid(row=15, column=0, pady=10,sticky=W)


# entries
OPTIONS = sorted(l1)

S1En = OptionMenu(root, Symptom1,*OPTIONS)
S1En.grid(row=7, column=1)

S2En = OptionMenu(root, Symptom2,*OPTIONS)
S2En.grid(row=8, column=1)

S3En = OptionMenu(root, Symptom3,*OPTIONS)
S3En.grid(row=9, column=1)


dst = Button(root, text="Zdiagnozuj drzewem decyzyjnym", command=drzewo, bg="green", fg="yellow")
dst.grid(row=8, column=3)

dst = Button(root, text="Zdiagnozuj lasem losowym", command=las_losowy, bg="green", fg="yellow")
dst.grid(row=9, column=3)

dst = Button(root, text="Zdiagnozuj k-sąsiadów", command=k_sasiadow, bg="green", fg="yellow")
dst.grid(row=10, column=3)


t1 = Text(root, height=1, width=40,bg="orange",fg="black")
t1.grid(row=15, column=1, padx=10)

root.mainloop()