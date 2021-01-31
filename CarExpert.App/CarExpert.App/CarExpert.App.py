

from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

l1=[
'rozrusznik nie kręci','światła się nie palą','opona łysa z jednej strony','samochód stał na mrozie','brak powietrza w kole','niski poziom oleju','biegi nie chcą się zmieniać','sprzęgło lekko się wciska','samochód zjeżdza z górki','głośny silnik','stuknięcia na górkach I dołkach','słaba siła hamowania','słaba siła silnika','wieksze zuzycie paliwa','miękki pedał hamulca','spryskiwacze nie działaja','wysoka temperatura silnika','samochód gaśnie'
]

disease=[
'rozładowany akumulator','zepsuty rozrząd','zapowietrzone hamulce','przepalona żarówka','zła rozbieżność kół','słaby hamulec ręczny','brak płynu do spryskiwaczy','zamarznięty płyn do spryskiwaczy','przepalony bezpiecznik','dziurawe koło','peknięta miska olejowa','zepsuta skrzynia biegów','zepsute sprzęgło','zużyty filtr powietrza','awaria chłodnicy','brak benzyny'
]




df=pd.read_csv("train.csv")

i = 0;

replacor = {}

for d in disease:
    replacor[d] = i
    i+=1



df.replace({'diagnoza':
            replacor
            },inplace=True)


X= df[l1]

y = df[["diagnoza"]]
np.ravel(y)



tr=pd.read_csv("test.csv")
tr.replace({'diagnoza': replacor},inplace=True)

X_test= tr[l1]
y_test = tr[["diagnoza"]]
np.ravel(y_test)



from sklearn import tree
from sklearn.metrics import accuracy_score
clf = tree.DecisionTreeClassifier(criterion="entropy")   
clf = clf.fit(X,y)
y_pred=clf.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

text_representation = tree.export_text(clf)
print(text_representation)
fig = plt.figure(figsize=(35,30))
_ = tree.plot_tree(clf, feature_names=l1, filled=True)

plt.savefig('tree.png', bbox_inches='tight')

def PredykcjaDrzewem():


    l2=[]
    for x in range(0,len(l1)):
        l2.append(0)

    t1.delete("1.0", END)


    psymptoms = [Symptom1.get(),Symptom2.get(),Symptom3.get()]

    for k in range(0,len(l1)):
        # print (k,)
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf.predict(inputtest)
    predicted=predict[0]

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break


    if (h=='yes'):
        t1.insert(END, disease[a])
    else:
        t1.insert(END, "Not Found")




root = Tk()
root.configure(background='gray')

# entry variables
Symptom1 = StringVar()
Symptom1.set(None)
Symptom2 = StringVar()
Symptom2.set(None)
Symptom3 = StringVar()
Symptom3.set(None)


# Heading
w2 = Label(root, justify=CENTER, text="System ekspercki - Mechanik", fg="white", bg="gray")
#w2.config(font=("Elephant", 30))
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


dst = Button(root, text="Zdiagnozuj", command=PredykcjaDrzewem,bg="green",fg="yellow")
dst.grid(row=8, column=3)


#textfileds
t1 = Text(root, height=1, width=40,bg="orange",fg="black")
t1.grid(row=15, column=1, padx=10)

root.mainloop()
