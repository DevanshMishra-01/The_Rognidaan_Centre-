##libraries


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

## reading file


df=pd.read_csv(r"heart_cleaned.csv")
df.drop("Unnamed: 0", axis=1, inplace=True)



from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,classification_report
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

## splitting data 
X=df.drop('HeartDisease',axis=1)
y=df['HeartDisease']
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.20, random_state=42,stratify=y)

## feature scaling 
scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.transform(X_test)
models={
    'Logistic Regression':LogisticRegression(),
    "Knn":KNeighborsClassifier(),
    'Naivebayes':GaussianNB(),
    'Decisiontree':DecisionTreeClassifier(),
    'SVM':SVC()
}

##model training and evaluation


results=[]
for name,model in models.items():
    model.fit(X_train_scaled,y_train)
    y_pred=model.predict(X_test_scaled)
    acc=accuracy_score(y_test,y_pred)
    f1=f1_score(y_test,y_pred) 
    results.append(
    {
        'model':name,
        'Accuracy':acc,
        'f1 score':round(f1,4)
    }
    )



### model selection --results
"""
[{'model': 'Logistic Regression', 'Accuracy': 0.875, 'f1 score': 0.8878},
{'model': 'Knn', 'Accuracy': 0.8858695652173914, 'f1 score': 0.8986},
{'model': 'Naivebayes', 'Accuracy': 0.8695652173913043, 'f1 score': 0.8788},
{'model': 'Decisiontree', 'Accuracy': 0.7554347826086957, 'f1 score': 0.7692},
{'model': 'SVM', 'Accuracy': 0.8641304347826086, 'f1 score': 0.8804}]
"""


## saving the model


import joblib
joblib.dump(models['Knn'],'Knn_model.pkl')
joblib.dump(scaler,'Scaler.pkl')
joblib.dump(X.columns.to_list(),'features.pkl')

