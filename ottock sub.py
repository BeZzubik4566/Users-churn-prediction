import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import skorch
from kagglesdk.competitions.types import submission_status
from narwhals import DataFrame
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
import sys
from sklearn.metrics import accuracy_score, precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from catboost import CatBoostClassifier


df_train=pd.read_csv('train.csv')
df_test=pd.read_csv('test.csv')
X_test=df_test

X_train=df_train.drop('Churn',axis=1)
y_train=df_train['Churn']

X_train=pd.get_dummies(X_train)
X_test=pd.get_dummies(X_test)

X_train, X_test = X_train.align(
    X_test,
    join='left',
    axis=1,
    fill_value=0
)

model=CatBoostClassifier(
    iterations=250,
    loss_function='Logloss',
    learning_rate=0.05,
    max_depth=4
)

model.fit(X_train,y_train)
yXpred=model.predict(X_train)

print(accuracy_score(y_train,yXpred))
print(precision_score(y_train,yXpred))

ypred=model.predict_proba(X_test)[:, 1]

submission=pd.DataFrame({
   'Id': range(len(df_test)),
    'Churn': ypred
})
submission.to_csv('submission.csv',index=False)
