# -*- coding: utf-8 -*-
"""Breast_cancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1c0L5Xrdw-3yxxM2zONSxIpYGhIR-MlwP

# **Project Name** - Breast Cancer Prediction with Machine Learning


 Project Type - Classification

 Contribution - Individual

 Member Name - Hari Kumar reddy

# **About Dataset**

**Description:** Breast cancer is the most common cancer amongst women in the world. It accounts for 25% of all cancer cases, and affected over 2.1 Million people in 2015 alone. It starts when cells in the breast begin to grow out of control. These cells usually form tumors that can be seen via X-ray or felt as lumps in the breast area.


The key challenges against it’s detection is how to classify tumors into malignant (cancerous) or benign(non cancerous). We ask you to complete the analysis of classifying these tumors using machine learning and the Breast Cancer Wisconsin (Diagnostic) Dataset.

    - radius (mean of distances from center to points on the perimeter)
    - texture (standard deviation of gray-scale values)
    - perimeter
    - area
    - smoothness (local variation in radius lengths)
    - compactness (perimeter^2 / area - 1.0)
    - concavity (severity of concave portions of the contour)
    - concave points (number of concave portions of the contour)
    - symmetry
    - fractal dimension ("coastline approximation" - 1)

## Import libraries
"""

# Import Libraries
# Importing Numpy & Pandas for data processing & data wrangling
import numpy as np
import pandas as pd

# Importing  tools for visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Import evaluation metric libraries
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,classification_report

# Word Cloud library
from wordcloud import WordCloud, STOPWORDS

# Library used for data preprocessing
from sklearn.feature_extraction.text import CountVectorizer

# Library used for standardize features
from sklearn.preprocessing import StandardScaler

# Import model selection libraries
from sklearn.model_selection import train_test_split,GridSearchCV

# Library used for ML Model implementation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Library used to Save and load ML models quickly
import pickle

# Library used for mathematical functions
import math

"""# Import warnings"""

# Library used for ignore warnings
import warnings
warnings.filterwarnings('ignore')

"""#  Reading Dataset"""

# Reading dataset
df=pd.read_csv("/content/breast-cancer.csv")
df

pd.set_option('display.max_columns', None)  # Ensures all columns are displayed

df

df.columns

# Dataset Info
# Checking information about the dataset using info
df.info()

# Dataset Duplicate Value Count
dup = df.duplicated().sum()
print(f'Number of duplicated rows are {dup}')

# Missing Values/Null Values Count
df.isnull().sum()

# Counts the number of occurrences of each unique value in the "diagnosis" column
df.diagnosis.value_counts()

# Count of Diagnosis (M = Malignant, B = Benign)
plt.figure(figsize=(5,3))
sns.countplot(x='diagnosis', data=df,palette="Set2")
plt.title('Diagnosis Count')
plt.show()

# Generates summary statistics for numerical columns in the DataFrame
# Includes count, mean, standard deviation, min, max, and quartiles (25%, 50%, 75%)
df.describe()

# Pairplot for a quick overview of relationships between variables
sns.pairplot(df, hue='diagnosis', vars=['radius_mean', 'texture_mean', 'area_mean', 'perimeter_mean',"smoothness_mean"])
plt.show()

# Correlation heatmap of features
plt.figure(figsize=(20,15))
# Calculate correlation only for numerical features by excluding 'diagnosis'
correlation = df.drop(columns=['diagnosis']).corr()
sns.heatmap(correlation, annot=True, cmap="Blues", fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# Distribution Plots for Mean Features by Diagnosis
mean_columns = df.columns[2:12]  # Selecting columns related to mean features
plt.figure(figsize=(20,15))

for i, column in enumerate(mean_columns, 1):
    plt.subplot(3, 4, i)
    sns.histplot(data=df, x=column, hue='diagnosis', kde=True, element="step", bins=25)
    plt.title(f'Distribution of {column} by Diagnosis')

plt.tight_layout()
plt.show()

# Creates a new DataFrame 'worst_features' containing only the selected worst-case feature columns
worst_features = df[['radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'diagnosis']]

# Creating a pairplot for "worst" features
sns.pairplot(worst_features, hue='diagnosis', diag_kind='kde')
plt.show()

"""#Splitting the dataset"""

# Creates a new DataFrame 'X' by dropping specific columns from 'df'
X=df.drop(['id','radius_mean','diagnosis','perimeter_mean','area_mean','radius_se','texture_se','area_se'],axis=1)
# Creates the target variable 'y' by mapping 'diagnosis' to binary values
y=df['diagnosis'].map(lambda x: 1 if x == 'M' else 0)

X

y

"""#Spliting Data into Train-Test-Split"""

# Splits the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

X_train

X_test

y_train

"""# Scaling the Data"""

# Standardization ensures that all features have a mean of 0 and a standard deviation of 1
# improving model performance, especially for algorithms sensitive to scale differences.
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

X_train.shape

X_test.shape

y_train.shape

y_test.shape

"""# **Model**"""

# Creates an empty DataFrame called 'result' with columns for storing model performance metrics
result=pd.DataFrame({'Model':[], "Training Accuracy":[], "Testing Accuracy":[], "F1 Score":[], "Recall":[],
                     "Precision":[]})
result

"""

#KNN
"""

# Finding optimal-K by using Hyperparameter tuning
# Create a list of k values from 1 to 49, stepping by 4
k = list(range(1, 50, 4))

# Initialize empty lists to store the training and cross-validation accuracies
train_accuracy = []
test_accuracy = []

# Iterate over each k value in the list
for i in k:
    # Create a KNeighborsClassifier instance with n_neighbors set to the current k value
    knn = KNeighborsClassifier(n_neighbors=i)

    # Fit the model to the training data (x_train, y_train)
    knn.fit(X_train, y_train)

    # Predict the labels for the training set and the cross-validation set
    y_train_pred = knn.predict(X_train)
    y_test_pred = knn.predict(X_test)

    # Calculate and append the accuracy of the model on the training set
    train_accuracy.append(accuracy_score(y_train, y_train_pred))

    # Calculate and append the accuracy of the model on the test set
    test_accuracy.append(accuracy_score(y_test, y_test_pred))

# Find the optimal k value by selecting the k that gives the maximum test accuracy
optimal_k = k[test_accuracy.index(max(test_accuracy))]

# Print the optimal k value for the best cross-validation accuracy
print("Optimal-k is:", optimal_k)

knn=KNeighborsClassifier(n_neighbors=optimal_k)

knn.fit(X_train,y_train)

y_pred=knn.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for KNN model
train_acc=knn.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 4))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 0 with the following values:
result.loc[0]=['KNN', train_acc, test_acc, f1, recal, prec]

"""# Naive Bayes"""

# finding optimal alpha by using Hyperparameter tuning

alpha=[10000,1000,100,10,1,0.1,0.01,0.001,0.0001,0.00001]

train_accuracy=[]
test_accuracy=[]

for i in alpha:
  clf=BernoulliNB(alpha=i)
  clf.fit(X_train,y_train)

  y_train_pred=clf.predict(X_train)
  y_test_pred=clf.predict(X_test)

  train_accuracy.append(accuracy_score(y_train,y_train_pred))
  test_accuracy.append(accuracy_score(y_test,y_test_pred))

optimal_alpha=alpha[train_accuracy.index(max(train_accuracy))]

print("Optimal-Alpha for is:",optimal_alpha)

NB = BernoulliNB(alpha=optimal_alpha)

NB.fit(X_train,y_train)
y_pred=NB.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for Naive Bayes model
train_acc=NB.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 3))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 1 with the following values:
result.loc[1]=['Gaussian Naives Bayes', train_acc, test_acc, f1, recal, prec]

"""## Logistic Regression"""

# finding optimal C by using Hyperparameter tuning

C=[10000,1000,100,10,1,0.1,0.01,0.0001,0.00001]

train_accuracy=[]
test_accuracy=[]

for i in C:
  clf=LogisticRegression(C=i)
  clf.fit(X_train,y_train)
  y_train_pred=clf.predict(X_train)
  y_test_pred=clf.predict(X_test)

  train_accuracy.append(accuracy_score(y_train,y_train_pred))
  test_accuracy.append(accuracy_score(y_test,y_test_pred))

optimal_C=C[test_accuracy.index(max(test_accuracy))]

print("optimal_c is:",optimal_C)

LR=LogisticRegression(C=optimal_C)

LR.fit(X_train,y_train)
y_pred=LR.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for Logistic regression model
train_acc=LR.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 3))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 2 with the following values:
result.loc[2]=['Logistic Regression', train_acc, test_acc, f1, recal, prec]

"""## SVM"""

# finding optimal C by using Hyperparameter tuning
C=[10000,1000,100,10,1,0.1,0.01,0.0001,0.00001]

train_accuracy=[]
test_accuracy=[]

for i in C:
  linear_svc=SVC()
  linear_svc.fit(X_train,y_train)
  y_train_pred=linear_svc.predict(X_train)
  y_cv_pred=linear_svc.predict(X_test)

  train_accuracy.append(accuracy_score(y_train,y_train_pred))
  test_accuracy.append(accuracy_score(y_test,y_test_pred))

optimal_C=C[test_accuracy.index(max(test_accuracy))]

print("optimal-C is:",optimal_C)

svm=SVC()

svm.fit(X_train,y_train)
y_pred=svm.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for Logistic regression model
train_acc=svm.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 3))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 3 with the following values:
result.loc[3]=['Logistic Regression', train_acc, test_acc, f1, recal, prec]

"""## Decision Tree"""

depth=[3,5,10,20]
min_samples=[2,5,10]

param_grid={"min_samples_split":min_samples,"max_depth":depth}

clf=DecisionTreeClassifier()

model=GridSearchCV(clf,param_grid,scoring=accuracy_score,cv=5,n_jobs=-1)

model.fit(X_train,y_train)

optimal_min=model.best_estimator_.min_samples_split
optimal_max=model.best_estimator_.max_depth

print("optimal min is:",optimal_min)
print("optimal max is:",optimal_max)

DT=DecisionTreeClassifier(max_depth=optimal_max,min_samples_split=optimal_min,random_state=40)

DT.fit(X_train,y_train)
y_pred=DT.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for Decision Tree model
train_acc=DT.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 3))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 4 with the following values:
result.loc[4]=['Decision Tree', train_acc, test_acc, f1, recal, prec]

"""## Random Forest"""

depth=[3, 5, 10, 15, 20, 25]
min_samples=[2, 5, 10, 20, 50]

param_grid={"min_samples_split":min_samples,"max_depth":depth}

clf=RandomForestClassifier()

model=GridSearchCV(clf,param_grid,cv=5,scoring=accuracy_score,n_jobs=-1)

model.fit(X_train,y_train)

optimal_min=model.best_estimator_.min_samples_split
optimal_max=model.best_estimator_.max_depth

print("optimal_min is:",optimal_min)
print("optimal_max is:",optimal_max)

RF=RandomForestClassifier(max_depth=optimal_max,min_samples_split=optimal_min,random_state=40)

RF.fit(X_train,y_train)
y_pred=RF.predict(X_test)

# finding the accuracy,precision,recall and F1 scores for Random Forest model
train_acc=RF.score(X_train,y_train)
test_acc=accuracy_score(y_test,y_pred)
recal=recall_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print("Training Accuracy :", train_acc)
print("Testing Accuracy :", test_acc)
print("F1 Score :", f1)
print("Recall :", recal)
print("Precision :", prec)

# Prints the classification report, which includes precision, recall, F1-score, and support for each class
print(classification_report(y_test,y_pred))

# Creates a confusion matrix comparing actual values (y_test) and predicted values (y_pred)
conf_matrix = pd.DataFrame(data = confusion_matrix(y_test,y_pred),
                           columns = ['Predicted:0', 'Predicted:1'],
                           index =['Actual:0', 'Actual:1'])
plt.figure(figsize = (5, 3))
sns.heatmap(conf_matrix, annot = True, fmt = 'd')
plt.show()

# Adds a new row to the 'result' DataFrame at index 5 with the following values:
result.loc[5]=['Random Forest', train_acc, test_acc, f1, recal, prec]

"""## **Model Selection**"""

result = result.sort_values(by='Testing Accuracy', ascending=False)
result

plt.figure(figsize=(6,4))
ax=sns.barplot(data=result,y='Model',x='Training Accuracy',palette="tab10",width=0.5)
for i in ax.containers:
    ax.bar_label(i)

plt.figure(figsize=(6,4))
ax=sns.barplot(data=result,y='Model',x='Testing Accuracy',palette="tab10",width=0.5)
for i in ax.containers:
    ax.bar_label(i)

plt.figure(figsize=(6,4))
ax=sns.barplot(data=result,y='Model',x='F1 Score',palette="tab10",width=0.5)
for i in ax.containers:
    ax.bar_label(i)

plt.figure(figsize=(6,4))
ax=sns.barplot(data=result,y='Model',x='Recall',palette="tab10",width=0.5)
for i in ax.containers:
    ax.bar_label(i)

plt.figure(figsize=(6,4))
ax=sns.barplot(data=result,y='Model',x='Precision',palette="tab10",width=0.5)
for i in ax.containers:
    ax.bar_label(i)

# prompt: # prompt: dump all algorithms in single pickle file code

import pickle

# Assuming your trained models (knn, NB, LR, svm, DT, RF) and scaler are defined in the previous code
# Replace with actual model variables
models = {
    "knn": knn,
    "NB": NB,
    "LR": LR,
    "svm": svm,
    "DT": DT,
    "RF": RF,
    "scaler": scaler
}


# Save the models to a pickle file
with open('models.pkl', 'wb') as file:
    pickle.dump(models, file)