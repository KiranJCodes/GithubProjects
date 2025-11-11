# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
try:
    # Download and get the path
    download_path = kagglehub.dataset_download("kabure/german-credit-data-with-risk")
    
    # Find the actual CSV file in the downloaded directory
    for file in os.listdir(download_path):
        if file.endswith('.csv'):
            file_path = os.path.join(download_path, file)
            df = pd.read_csv(file_path)
            break
    print(f"Dataset loaded from: {file_path}")
    
except Exception as e:
    print(f"Download failed: {e}")
    print("Please ensure you have Kaggle API credentials setup")
    
    
## Handle missing and duplicate values by deleting them
df.isna().sum()
df.duplicated().sum()

df = df.dropna().reset_index(drop=True)


## EDA now

df[['Age','Credit amount','Duration']].hist(bins=20,edgecolor='black')
plt.suptitle("Distrubution of Numerical values",fontsize=16)
plt.show

plt.figure(figsize=(15,5))
for i, col in enumerate(['Age','Credit amount','Duration']):
    plt.subplot(1, 3, i+1)
    sns.boxplot(y = df[col],color='gold')
    plt.title(col)
plt.tight_layout()
plt.show()


cols = ['Job','Housing','Saving accounts','Checking account','Purpose']
plt.figure(figsize=(15,10))
for i, col in enumerate(cols):
    plt.subplot(3,3,i+1)
    sns.countplot(data=df,x=col,palette='Set1',
                  order=df[col].value_counts().index)
    plt.title(f"Distrubution of {col}" )
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## heatmap
corr = df[["Age","Job","Credit amount","Duration"]].corr()
sns.heatmap(corr, annot=True,cmap='coolwarm',fmt=".2f")
plt.show()



df.groupby('Job')['Credit amount'].mean()

df.groupby('Sex')['Credit amount'].mean()

pd.pivot_table(df,values='Credit amount', index = "Housing",
               columns = 'Purpose')

sns.scatterplot(data = df,x="Age", y ="Credit amount",
                hue = 'Sex', size="Duration",alpha=0.7)
plt.title("Credit amount against Age colored by Sex and sized by Duration")
plt.show()


sns.violinplot(data = df,x = "Saving accounts", y = "Credit amount",palette="deep")
plt.title("Credit amount Distrubtion against savings")
plt.show()

df["Risk"].value_counts(normalize=True) * 100


plt.figure(figsize=(8,4))
for i,col in enumerate(['Age','Credit amount','Duration']):
    plt.subplot(1,3,i+1)
    sns.boxplot(data = df, x ="Risk", y = col,palette="deep")
    plt.title(f"{col} by Risk")

df.groupby("Risk")[['Age',"Credit amount","Duration"]].mean()


plt.figure(figsize=(10,8))
for i,col in enumerate(cols):
    plt.subplot(3,3,i+1)
    sns.countplot(data = df,x = col, hue="Risk",palette="Set2",
                  order=df[col].value_counts().index)
    plt.title(f"{col} by Risk")
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df.columns

features = ['Age','Sex','Job','Housing','Saving accounts',
            'Checking account','Credit amount','Duration']

target ='Risk'

dfmodel = df[features + [target]].copy()

dfmodel.head()


#### encoding

from sklearn.preprocessing import LabelEncoder
import joblib

catcols = dfmodel.select_dtypes(include='object').columns.drop('Risk')

labeldict = {}

for col in catcols:
    le = LabelEncoder()
    dfmodel[col] = le.fit_transform(dfmodel[col])
    labeldict[col] = le
    joblib.dump(le,f"{col}_encoder.pkl")
    
## print
labeldict
    
letarget = LabelEncoder()
dfmodel[target] =  letarget.fit_transform(dfmodel[target])

dfmodel[target].value_counts()
# 1 is good , 0 is bad

joblib.dump((letarget),'target_encoder.pkl')
dfmodel.head()


from sklearn.model_selection import train_test_split

X = dfmodel.drop(target,axis=1)

y = dfmodel[target]


Xtrain, Xtest, ytrain,ytest = train_test_split(X, y,test_size=0.2,
                                               stratify= y,random_state = 42)


Xtrain.shape
Xtest.shape

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

def trainmodel(model,parmgrid,Xtrain,
               Xtest,ytrain,ytest):
    grid = GridSearchCV(model, parmgrid,cv=5,scoring='accuracy',n_jobs=-1)  
    grid.fit(Xtrain,ytrain)
    bestmodel = grid.best_estimator_
    ypred = bestmodel.predict(Xtest)
    acc = accuracy_score(ytest,ypred)
    return bestmodel, acc, grid.best_params_

## DT
dt = DecisionTreeClassifier(random_state=42,class_weight='balanced')
dtparmgrid = {
    'max_depth': [3,5,7,10,None] ,
    'min_samples_split': [2,5,10],
    'min_samples_leaf': [1,2,4]
    }


bestdt,accdt,paramsdt = trainmodel(dt, dtparmgrid, Xtrain, Xtest, ytrain, ytest)

print('Decission Tree accuracy',accdt)

print(f'Best parameters: {paramsdt}')

### RF

rf = RandomForestClassifier(random_state=42,class_weight='balanced',n_jobs=-1)
rfparmgrid = {
    'n_estimators': [100,200] ,
    'max_depth': [5,7,10,None],
    'min_samples_split': [2,5,10],
    'min_samples_leaf': [1,2,4]
    }

bestrf,accrf,paramsrf = trainmodel(rf, rfparmgrid, Xtrain, Xtest, ytrain, ytest)

print('Random Tree accuracy',accrf)

print(f'Best parameters: {paramsrf}')


### et


et = ExtraTreesClassifier(random_state=42,class_weight='balanced',n_jobs=-1)
etparmgrid = {
    'n_estimators': [100,200] ,
    'max_depth': [5,7,10,None],
    'min_samples_split': [2,5,10],
    'min_samples_leaf': [1,2,4]
    }

bestert,accet,paramset = trainmodel(et, etparmgrid, Xtrain, Xtest, ytrain, ytest)

print('Extra Tree accuracy',accet)

print(f'Best parameters: {paramset}')


### XG Boosat


xgb = XGBClassifier(random_state=42,
                    scale_pos_weight=(ytrain==0).sum() / (ytrain==1).sum(),
                    use_label_encooder=False,eval_metric='logloss')
xgbparmgrid = {
    'n_estimators': [100,200] ,
    'max_depth': [3,5,7],
    'learning_rate': [0.01,0.1,0.2],
    'subsample': [0.7,1],
    'colsample_bytree' : [0.7,1]
    }

bestxgb,accxgb,paramsxgb = trainmodel(xgb, xgbparmgrid, Xtrain, Xtest, ytrain, ytest)

print('XGB  accuracy',accxgb)

print(f'Best parameters: {paramsxgb}')


## plot all model details

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc


modelsdata = {
    'XGBoost': {'accuracy': accxgb, 'model': bestxgb, 'params': paramsxgb},
    'Extra Trees': {'accuracy': accet, 'model': bestert, 'params': paramset},
    'Random Forest': {'accuracy': accrf, 'model': bestrf, 'params': paramsrf},
    'Decision Tree': {'accuracy': accdt, 'model': bestdt, 'params': paramsdt}
}

### Total accuracy
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
modelnames = list(modelsdata.keys())
accuracies = [modelsdata[model]['accuracy'] for model in modelnames]
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

bars = plt.bar(modelnames, accuracies, color=colors, alpha=0.8)
plt.title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
plt.ylabel('Accuracy')
plt.xticks(rotation=45)
plt.ylim(0, 1)

for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')

### ROC curve

plt.figure(figsize=(10,8))
plt.subplot(2, 3, 2)
for modelname, data in modelsdata.items():
    if hasattr(data['model'], 'predict_proba'):
        y_proba = data['model'].predict_proba(Xtest)[:, 1]
        fpr, tpr, _ = roc_curve(ytest, y_proba)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{modelname} (AUC = {roc_auc:.3f})', linewidth=2)

plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves Comparison')
plt.legend()


## Feature importance

plt.subplot(2, 3, 3)
featureimportance_data = []
for modelname, data in modelsdata.items():
    if hasattr(data['model'], 'feature_importances_'):
        importance = data['model'].feature_importances_
        featureimportance_data.append((modelname, importance))


if featureimportance_data:
    modelname, importance = featureimportance_data[0]
    features = Xtrain.columns if hasattr(Xtrain, 'columns') else range(len(importance))
    sortedidx = np.argsort(importance)[-10:]  # Top 10 features
    plt.barh(range(len(sortedidx)), importance[sortedidx])
    plt.yticks(range(len(sortedidx)), [features[i] for i in sortedidx])
    plt.title(f'Feature Importance - {modelname}')
    plt.xlabel('Importance Score')
    
    
## Export model

bestxgb.predict(Xtest)
joblib.dump(bestxgb,'XGB_Classifier_model.pkl')
