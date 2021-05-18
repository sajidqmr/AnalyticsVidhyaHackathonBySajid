# -*- coding: utf-8 -*-
"""loan_analytic_vidhya.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SBvoW2yS7zTdEhxBWhUWD4b80yPYwWut
"""

import pandas as pd # to read csv file of training and testing dataset

train = pd.read_csv('/content/train_ctrUa4K.csv')
test = pd.read_csv('/content/test_lAUu6dG.csv')
train.head(5)

test.head(5)

train.info()

test.info()

"""**missing value treatment (imputation)**
there are lots of missing value or nan,
we will use mode to fill categorical data and mean to fill numerical data
"""

train['Gender'].fillna(train['Gender'].mode()[0], inplace = True)
train['Married'].fillna(train['Married'].mode()[0], inplace = True)
train['Dependents'].fillna(train['Dependents'].mode()[0], inplace = True)
train['Self_Employed'].fillna(train['Self_Employed'].mode()[0], inplace = True) #categorical imputation

train['LoanAmount'].fillna(train['LoanAmount'].mean(), inplace = True)
train['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mean(), inplace = True)
train['Credit_History'].fillna(train['Credit_History'].mean(), inplace = True) #numeric imputation

train.info()

train_df['Loan_Status'].value_counts()

"""**dataset is imbalanced**
yes is 422 and no is 192
yes--> is 68%
no is--> 32%
we have to balance it using oversampling by synthetic Synthetic Minority Oversampling Technique

test data imputation
"""

test.info()

test.isnull().sum()

test['Gender'].fillna(test['Gender'].mode()[0], inplace = True)
test['Dependents'].fillna(test['Dependents'].mode()[0], inplace = True)
test['Self_Employed'].fillna(test['Self_Employed'].mode()[0], inplace = True)
test['LoanAmount'].fillna(test['LoanAmount'].mean(), inplace = True)
test['Loan_Amount_Term'].fillna(test['Loan_Amount_Term'].mean(), inplace = True)
test['Credit_History'].fillna(test['Credit_History'].mean(), inplace = True)

test.isnull().sum()

train_df=train.drop(['Loan_ID'],axis=1)
test_df=test.drop(['Loan_ID'],axis=1)
train_df

"""**one hot encoding**
to convert categorical variables into numeric for ml models to run
"""

train_one_hot= pd.get_dummies(train_df)

train_one_hot

test_one_hot= pd.get_dummies(test_df)

test_one_hot

X= train_one_hot.drop(['Loan_Status_N','Loan_Status_Y'],axis=1)
y = train_one_hot['Loan_Status_Y']
X

y

"""**train test split**"""

from sklearn.model_selection import train_test_split
X_train,X_valid,y_train,y_valid = train_test_split(X,y,test_size=0.1,random_state=1)

"""baseline model using decision tree without balancing dataset"""

from sklearn.tree import DecisionTreeClassifier
base_model = DecisionTreeClassifier()
base_model.fit(X_train,y_train)
y_pred_1 = base_model.predict(X_valid)
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_valid,y_pred_1)
acc

"""**balancing dataset using SMOTE**"""

from imblearn.over_sampling import SMOTE
oversample=SMOTE(k_neighbors=2)
#transform the dataset
X,y=oversample.fit_resample(X,y)

X_bal=pd.DataFrame(X)
X_bal

y_bal=pd.DataFrame(y)
y_bal.value_counts()

X_train_bal,X_valid_bal,y_train_bal,y_valid_bal = train_test_split(X_bal,y_bal,test_size=0.1,random_state=1)

"""**model after balancing** """

model_1 = DecisionTreeClassifier()
model_1.fit(X_train_bal,y_train_bal)
y_pred_1 = model_1.predict(X_valid_bal)
acc_1 = accuracy_score(y_valid_bal,y_pred_1)
acc_1

"""**normalization of data for better performance**"""

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
X_train_bal_norm = scaler.fit_transform(X_train_bal)
X_valid_bal_norm =scaler.fit_transform(X_valid_bal)

X_train_bal_norm

model_2 = DecisionTreeClassifier()
model_2.fit(X_train_bal_norm,y_train_bal)
y_pred_2 =model_2.predict(X_valid_bal_norm)
acc_2 = accuracy_score(y_valid_bal,y_pred_2)
acc_2

"""**random forest classifier for model_3**"""

from sklearn.ensemble import RandomForestClassifier
model_3 = RandomForestClassifier()
model_3.fit(X_train_bal,y_train_bal)
y_pred_3 = model_3.predict(X_valid_bal)
acc_3 = accuracy_score(y_valid_bal,y_pred_3)
acc_3

from sklearn.ensemble import RandomForestClassifier
model_4 = RandomForestClassifier()
model_4.fit(X_train_bal_norm,y_train_bal)
y_pred_4 = model_3.predict(X_valid_bal_norm)
acc_4 = accuracy_score(y_valid_bal,y_pred_4)
acc_4

"""**EXTRATREE CLASSIFIER**"""

from sklearn.ensemble import ExtraTreesClassifier
model_5 = ExtraTreesClassifier()
model_5.fit(X_train_bal,y_train_bal)
y_pred_5 = model_5.predict(X_valid_bal)
acc_5 = accuracy_score(y_valid_bal,y_pred_5)
acc_5

"""**LOGISTIC REGRESSION** *italicized text*"""

from sklearn.linear_model import LogisticRegression
model_6 = LogisticRegression()
model_6.fit(X_train_bal,y_train_bal)
y_pred_6 = model_6.predict(X_valid_bal)
acc_6 = accuracy_score(y_valid_bal,y_pred_6)
acc_6

"""**SUPPORT VECTOR MACHINE**"""

from sklearn.svm import SVC
model_7 = SVC()
model_7.fit(X_train_bal,y_train_bal)
y_pred_7 = model_7.predict(X_valid_bal)
acc_7 = accuracy_score(y_valid_bal,y_pred_7)
acc_7

"""**BEST ML MODEL WAS RANDOM FOREST**
WITH ACCURACY OF 87%

**HYPERPARAMETER TUNING OF RANDOM FOREST**
"""

from sklearn.ensemble import RandomForestClassifier
model_3 = RandomForestClassifier(n_estimators=200,random_state=1)
model_3.fit(X_train_bal,y_train_bal)
y_pred_3 = model_3.predict(X_valid_bal)
acc_3 = accuracy_score(y_valid_bal,y_pred_3)
acc_3

"""**DEEP LEARNING MODEL USING TENSORFLOW**"""

import tensorflow as tf
from tensorflow import keras
from keras import layers

tf.random.set_seed(1)
model_8 = keras.models.Sequential([
                                   keras.layers.Dense(50,activation='relu'),
                                   keras.layers.Dense(40,activation='relu'),
                                   keras.layers.Dense(1,activation='sigmoid')
])

model_8.compile(optimizer='Adam',loss=keras.losses.CategoricalHinge(),
                metrics=['accuracy'])

model_8.fit(X_train_bal_norm,y_train_bal,epochs=100)

y_pred_8 = model_8.predict(X_valid_bal_norm)
model_8.evaluate(X_valid_bal_norm,y_valid_bal)

"""**TIME TO GET THE PREDICTION USING RANDOM FOREST AND DEEP LEARNING MODEL FOR TEST DATASET**"""

test_one_hot

prediction_by_RandomForest = model_3.predict(test_one_hot)
prediction_by_RandomForest

prediction_by_deeplearning = model_8.predict(test_one_hot)
prediction_by_deeplearning

sub= pd.read_csv('/content/sample_submission_49d68Cx.csv')
sub

test['Loan_Status']=prediction_by_RandomForest

test

pr=pd.DataFrame(prediction_by_RandomForest)
pr

test.Loan_Status.replace((1, 0), ('Y', 'N'), inplace=True)

test

test.info()

sub_df=pd.DataFrame({'Loan_ID' : test["Loan_ID"],'Loan_Status' : test['Loan_Status']})

sub_df

submission_ran_for = sub_df.to_csv('submission_random_forest.csv',index=False)

pr1=pd.DataFrame(prediction_by_deeplearning)
pr1

test['Loan_Status']=pr1

test

test.Loan_Status.replace((1, 0), ('Y', 'N'), inplace=True)

test.head(3)

sub_df1=pd.DataFrame({'Loan_ID' : test["Loan_ID"],'Loan_Status' : test['Loan_Status']})
sub_df1

sub_df1=pd.DataFrame({'Loan_ID' : test["Loan_ID"],'Loan_Status' : test['Loan_Status']})
submission_deeplearning = sub_df1.to_csv('submission_deep_learning.csv',index=False)