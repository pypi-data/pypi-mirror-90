# Module name: umaat-Ultimate Machine-learning Algorithm Accuracy Test
# Short description: umaat (or) Ultimate Machine-learning Algorithm Accuracy Test  is a package that houses the  functions which can produce accuracy results for each algorithm in the categories of  Clustering,Regression & Classification based on passing the arguments - independent and dependent variables/features
# Advantage:The result from this algorithm gives the user of choice to choose the best  algorithm  for their dataset based on the accuracy produced
# Developers:  Vishal Balaji Sivaraman (@The-SocialLion) 
# Contact email address: vb.sivaraman_official@yahoo.com 
# Modules required: numpy,pandas,matplotlib,Scikit

# Command to install umaat:
# >>> pip install umaat

# IMPORTING REQUIRED MODULES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from time import sleep

# Program/Source Code:
# X denotes all the independent features in a dataset
# Y denotes all the dependent features in a dataset
# Note: Data preprocessing is not involved in the dataset also test dataset cant be attached here but will soon bring it in an update
class model_accuracy: 
  def accuracy_test(self,X,Y):
    from sklearn.model_selection import train_test_split
    while True:
      print("WELCOME TO MACHIENE LEARNING - ALGORITHM  ACCURACY TEST")
      print("\nAccuracy is calculated for 1)Regression,2)Classification 3)Clustering Models,4) all of the above(Applicable to numeric type of data),5)exit")
      i=int(input("Enter your Choice"))
      if i==1: 
        print("\n \t \t SUPERVISED LEARNING ")
        print("\n \t \t REGRESSION ALGORITHM ACCURACY TEST!")
        print("\nOnce the result is displayed the user can choose their desired algorithm for constructing their finished model")
        print("\n Note: No datapreprocessing is involved in this process ")
        print("\n If incase if u need to preprocess your data then for the upcoming filed type 0")
        o=float(input("enter test size for computation of accuracy of all the possible ml algorithms"))
        print("\n Generating train & test datasets for the given data..")
        X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = o, random_state = 0)
        print("\n Completed the genration of train and test datasets for the given data")
        Regressor_accuracy(X_train, X_test, y_train, y_test)
        break
      elif i==2:
        print("\n \t \t SUPERVISED LEARNING ")
        print("\n \t \t CLAFFICATION ALGORITHM ACCURACY TEST!")
        print("\nOnce the result is displayed the user can choose their desired algorithm for constructing their finished model")
        print("\n Note: No datapreprocessing is involved in this process ")
        print("\n If incase if u need to preprocess your data then for the upcoming filed type 0")
        o=float(input("enter test size for computation of accuracy of all the possible ml algorithms"))
        print("\n Generating train & test datasets for the given data..")
        X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = o, random_state = 0)
        print("\n Completed the genration of train and test datasets for the given data")
        Classifier_accuracy(X_train, X_test, y_train, y_test)
        break
      elif i==3:
        print("\n \t \t UNSUPERVISED LEARNING ")
        print("\n \t \t CLUSTERING ALGORITHM ACCURACY TEST !")
        print("\nOnce the result is displayed the user can choose their desired algorithm for constructing their finished model")
        print("\n Note: No datapreprocessing is involved in this process ")
        print("\n If incase if u need to preprocess your data then for the upcoming filed type 0")
        o=float(input("enter test size for computation of accuracy of all the possible ml algorithms"))
        print("\n Generating train & test datasets for the given data..")
        X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = o, random_state = 0)
        print("\n Completed the genration of train and test datasets for the given data")
        Clustering_accuracy(X_train,X_test,y_train,y_test)
        break
      elif i==4:
        print("\n \t \t ALGORITHM ACCURACY TEST !..")
        print("\n \t \t SUPERVISED LEARNING VS UNSUPERVISED LEARNING")
        print("\n Note: Incase if the values of the dependent variable y is continous then the preffered choice is to go ahead with Regression models as classification models might throw an error ")
        print("\nOnce the result is displayed the user can choose their desired algorithm for constructing their finished model")
        print("\n Note: No datapreprocessing is involved in this process ")
        print("\n If incase if u need to preprocess your data then for the upcoming filed type 0")
        o=float(input("enter test size for computation of accuracy of all the possible ml algorithms"))
        print("\n Generating train & test datasets for the given data..")
        X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = o, random_state = 0)
        print("\n Completed the genration of train and test datasets for the given data")
        AAT(X_train,X_test,y_train,y_test)
        break
      elif i==5: 
         print("\n Thank you")
         break
      else:
        print("\n Invalid Choice Please try again")


def Regressor_accuracy(X_train, X_test, y_train, y_test):
  print("\nLoading all the possible Regression models ")
  print("\nLoading completed.. ")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
     sys.stdout.write('\r')
     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
     sys.stdout.flush()
     sleep(0.25)
  print("\n please enter the numbe of k folds required for your algorithm")
  print("\n if in case if the user wishes to choose the best k fold for the algorithm then enter 0 below")
  ch=round(int(input("\n enter number of k folds")))
  a1,b1,c1,d1,e1,f1,g1,h1=linear_reg(X_train,y_train,X_test,y_test,ch)
  a2,b2,c2,d2,e2,f2,g2,h2=poly_reg(X_train,y_train,X_test,y_test,ch)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  a3,b3,c3,d3,e3,f3,g3,h3=svr_linear(X_train,y_train,X_test,y_test,ch)
  a4,b4,c4,d4,e4,f4,g4,h4=svr_poly(X_train,y_train,X_test,y_test,ch)
  print("\n.........LOADING.......")
  a5,b5,c5,d5,e5,f5,g5,h5=svr_rbf(X_train,y_train,X_test,y_test,ch)
  a6,b6,c6,d6,e6,f6,g6,h6=svr_sig(X_train,y_train,X_test,y_test,ch)
  a7,b7,c7,d7,e7,f7,g7,h7=decision_reg(X_train,y_train,X_test,y_test,ch)
  a8,b8,c8,d8,e8,f8,g8,h8=random_reg(X_train,y_train,X_test,y_test,ch)
  a9,b9,c9,d9,e9,f9,g9,h9=XGB_reg(X_train,y_train,X_test,y_test,ch)
  print("\nTesting Accuracy for all the possible Regression models")
  for i in range(21):
     sys.stdout.write('\r')
     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
     sys.stdout.flush()
     sleep(0.25)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nNote: For any 2 columns it should assumed that the Linear Regression would be a Simple Linear Regression which means that for multiple columns the Linear Regression would be a multiple Linear Regression")
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Regression':['Linear Regression', 'Polynomial Regression', 'Support Vector Regression(kernel="linear")','Support Vector Regression(kernel="poly")','Support Vector Regression(kernel="rbf")','Support Vector Regression(kernel="sigmoid")','Decision Tree Regression','Random Forest regression','XG Boost Regression'], 'R2_score':[a1,a2,a3,a4,a5,a6,a7,a8,a9],'K-Folds Accuracy score':[b1,b2,b3,b4,b5,b6,b7,b8,b9],'Variance_score':[c1,c2,c3,c4,c5,c6,c7,c8,c9],'K-Folds Deviation Score':[d1,d2,d3,d4,d5,d6,d7,d8,d9],'Max_Error':[e1,e2,e3,e4,e5,e6,e7,e8,e9],'Mean Absolute Error':[f1,f2,f3,f4,f5,f6,f7,f8,f9],'Mean Squared Error':[g1,g2,g3,g4,g5,g6,g7,g8,g9],'Median Absolute Error':[h1,h2,h3,h4,h5,h6,h7,h8,h9]} 
  df = pd.DataFrame(data) 
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Regression Models Data frame')
  display(df)
  A1=abs(a1+b1+c1)/3
  A2=abs(a2+b2+c2)/3
  A3=abs(a3+b3+c3)/3
  A4=abs(a4+b4+c4)/3
  A5=abs(a5+b5+c5)/3
  A6=abs(a6+b6+c6)/3
  A7=abs(a7+b7+c7)/3
  A8=abs(a8+b8+c8)/3
  A9=abs(a9+b9+c9)/3
  E1=abs(e1+f1+g1+h1)/4
  E2=abs(e2+f2+g2+h2)/4
  E3=abs(e3+f3+g3+h3)/4
  E4=abs(e4+f4+g4+h4)/4
  E5=abs(e5+f5+g5+h5)/4
  E6=abs(e6+f6+g6+h6)/4
  E7=abs(e7+f7+g7+h7)/4
  E8=abs(e8+f8+g8+h8)/4
  E9=abs(e9+f9+g9+h9)/4
  reg_plot(A1,A2,A3,A4,A5,A6,A7,A8,A9,E1,E2,E3,E4,E5,E6,E7,E8,E9)

def linear_reg(X_train,y_train,X_test,y_test,ch):
  print("\n LINEAR REGRESSION  MODEL ")
  from sklearn.linear_model import LinearRegression
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = LinearRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n LINEAR REGRESSION  MODEL CONSTRUCTION -COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6


def poly_reg(X_train,y_train,X_test,y_test,ch):
  print("\n POLYNOMIAL REGRESSION  MODEL")
  from sklearn.model_selection import cross_val_score
  from sklearn.preprocessing import PolynomialFeatures
  from sklearn.linear_model import LinearRegression
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  p=int(input("Enter Degree of Polyniomial for Polynomial Regression"))
  poly_reg = PolynomialFeatures(degree = p)
  X_poly = poly_reg.fit_transform(X_train)
  regressor = LinearRegression()
  regressor.fit(X_poly, y_train)
  y_pred = regressor.predict(poly_reg.fit_transform(X_test))
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n POLYNOMIAL REGRESSION  MODEL COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6


def svr_linear(X_train,y_train,X_test,y_test,ch):
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='linear')  MODEL ")
  from sklearn.svm import SVR
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor= SVR(kernel = 'linear')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='linear')  MODEL COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def svr_poly(X_train,y_train,X_test,y_test,ch):
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='polynomial(poly) MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'poly')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='polynomial(poly)')  MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def svr_rbf(X_train,y_train,X_test,y_test,ch):
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='radial basis function(rbf)')   MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'rbf')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='radial basis function(rbf)')   MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def svr_sig(X_train,y_train,X_test,y_test,ch):
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='sigmoid')  MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVR
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = SVR(kernel = 'sigmoid')
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR REGRESSION (KERNEL='sigmoid')   MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def decision_reg(X_train,y_train,X_test,y_test,ch):
  print("\n DECISION TREE REGRESSION  MODEL  ")
  from sklearn.model_selection import cross_val_score
  from sklearn.tree import DecisionTreeRegressor
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = DecisionTreeRegressor(random_state = 0)
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n DECISION TREE REGRESSION  MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def random_reg(X_train,y_train,X_test,y_test,ch):
  print("\n RANDOM FOREST REGRESSION MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  t=int(input("Enter number of trees for random forest regression"))
  regressor = RandomForestRegressor(n_estimators = t, random_state = 0)
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test,y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n RANDOM FOREST REGRESSION  MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def XGB_reg(X_train,y_train,X_test,y_test,ch):
  print("\n XG-BOOST REGRESSION MODEL")
  from sklearn.linear_model import LinearRegression
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import r2_score,explained_variance_score,max_error,mean_absolute_error,mean_squared_log_error,mean_squared_error,median_absolute_error,mean_poisson_deviance,mean_gamma_deviance,mean_tweedie_deviance
  regressor = LinearRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(r2_score(y_test,y_pred))*100)
  f2=(abs(explained_variance_score(y_test, y_pred))*100)
  f3=(abs(max_error(y_test, y_pred)))
  f4=(abs(mean_absolute_error(y_test, y_pred)))
  f5=(abs(mean_squared_error(y_test, y_pred)))
  f6=(abs(median_absolute_error(y_test, y_pred)))
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n XG-BOOST REGRESSION MODEL CONSTRUCTION-COMPLETED ")
  return f1,a,f2,sd,f3,f4,f5,f6

def reg_plot(A1,A2,A3,A4,A5,A6,A7,A8,A9,E1,E2,E3,E4,E5,E6,E7,E8,E9):
  A=calc_p3(A1,A2,A3,A4,A5,A6,A7,A8,A9)
  E=calc_p4(E1,E2,E3,E4,E5,E6,E7,E8,E9)
  N=9
  ind = np.arange(N)  
  width =float(input("enter width for bar-plot(Normal:0.25)"))      
  plt.bar(ind, A, width, label='accuracy',color='b')
  plt.bar(ind + width, E, width,label='error',color='r')

  plt.ylabel('Scores')
  plt.title('Regression-Algorithms (Mean(Accuracy),Mean(Error)-Chart')
  plt.xlabel('Algorithm')
  
  plt.xticks(ind + width / 2, ('Lin-reg','Poly-reg',' SVR1', 'SVR2','SVR3','SVR4','DTR','RFR','XGBR'))
  plt.legend(loc='best')
  plt.show()
  print("\n the following points are hints for the above graph")
  print("\n \t Note: SVR1:SVR(Kernel-linear),\t SVR2:SVR(Kernel-polynomial),\t SVR3:SVR(Kernel-radial basis function (rbf)),\t SVR4:SVR(Kernel-sigmoid)")
  print("\n \t DTR:Decison Tree Regressor,\t RFR: Random Forest Regressor, \t XGBR: XG-Boost Regressor ")

def calc_p3(A1,A2,A3,A4,A5,A6,A7,A8,A9):
  B=[A1,A2,A3,A4,A5,A6,A7,A8,A9]
  C=[]
  for i in range(len(B)):
    if B[i] >100:
       B[i]=1
  for j in range(len(B)):
    if B[j] != 0 :
      C.append(B[j])
  return C

def calc_p4(A1,A2,A3,A4,A5,A6,A7,A8,A9):
  B=[A1,A2,A3,A4,A5,A6,A7,A8,A9]
  C=[]
  for i in range(len(B)):
    if B[i] >10:
       B[i]=1
  for j in range(len(B)):
    if B[j] != 0 :
      C.append(B[j])
  return C




def classs(f):
  d=abs(int(input("\n enter the number of unique classes present in your dataset")))
  if d!=0  and d!=1:
    k=1
    for i in range(d):
      c=input("enter the different classes in any order")
      f.append(c)
    while '' or "" in f:
      for j in range(len(f)):
       if f[j]=="" or f[j]=='':
          print("\n Error! empty element detected!")
          print("\n classes are",f)
          print("\n enter the class again for replacing position",j+1)
          c=input("\n enter the class again for replacing the element at position")
          if c!="" or c!='':
            f[j]=c
          else:
            print("\n classes are",f)
            while c==''or"":
              print("\n Error!! please try again!")
              print("\n classes are",f)
              print("\n enter the class again for replacing position",j+1)
              c=input("\n enter the class again for replacing the element at position")
            f[j]=c
    print("\nclasses are",f)
    print("\n Please verify the above list of classes")
    print("\n If incase if the above list of classes are wrong please enter 1 below else 0 to continue the process ")
    ch=int(input("enter the choice"))
    if ch==1:
      f.clear()
      print("\n List has been cleared succesfully")
      print("\n Transferring to back to stage 1")
      classs(f)
    return f
  else:
      print("\n invalid input")
      sys.exit()

def Classifier_accuracy(X_train, X_test, y_train, y_test):
  d=[]
  r=classs(d)
  print("\n Continuing with the Process")
  print("\n Transferring to main program")
  for y in range(21):
      sys.stdout.write('\r')
      sys.stdout.write("[%-20s] %d%%" % ('='*y, 5*y))
      sys.stdout.flush()
      sleep(0.25)
  b=np.array(r)
  print("\n Final representation of various classes")
  print("\nClasses are",b)
  print("\n Note: any non negative number is fine for the below field and it need not be the number of classes/categories in the  dataset")
  a=int(input("enter the number of labels for calculation of score"))
  l=int(input("Enter the value of beta for calculation of score"))
  print("\nLoading all the possible Classification  models ")
  print("\nLoading completed.. ")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n please enter the numbe of k folds required for your algorithm")
  print("\n if in case if the user wishes to choose the best k fold for the algorithm then enter 0 below")
  ch=round(int(input("\n enter number of k folds")))
  y_pred1,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1=log_reg(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred2,a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2,m2,n2,o2,p2,q2,r2,s2,t2,u2=KNN(X_train,y_train,X_test,y_test,a,l,ch)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  y_pred3,a3,b3,c3,d3,e3,f3,g3,h3,i3,j3,k3,l3,m3,n3,o3,p3,q3,r3,s3,t3,u3=svc_linear(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred4,a4,b4,c4,d4,e4,f4,g4,h4,i4,j4,k4,l4,m4,n4,o4,p4,q4,r4,s4,t4,u4=svc_poly(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred5,a5,b5,c5,d5,e5,f5,g5,h5,i5,j5,k5,l5,m5,n5,o5,p5,q5,r5,s5,t5,u5=svc_rbf(X_train,y_train,X_test,y_test,a,l,ch)
  print("\n........Loading.........")
  y_pred6,a6,b6,c6,d6,e6,f6,g6,h6,i6,j6,k6,l6,m6,n6,o6,p6,q6,r6,s6,t6,u6=svc_sig(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred7,a7,b7,c7,d7,e7,f7,g7,h7,i7,j7,k7,l7,m7,n7,o7,p7,q7,r7,s7,t7,u7= Naives_cla(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred8,a8,b8,c8,d8,e8,f8,g8,h8,i8,j8,k8,l8,m8,n8,o8,p8,q8,r8,s8,t8,u8=DTC_gini(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred9,a9,b9,c9,d9,e9,f9,g9,h9,i9,j9,k9,l9,m9,n9,o9,p9,q9,r9,s9,t9,u9=DTC_entropy(X_train,y_train,X_test,y_test,a,l,ch)
  t=int(input("enter number of trees for Random Forest Classification"))
  y_pred10,a10,b10,c10,d10,e10,f10,g10,h10,i10,j10,k10,l10,m10,n10,o10,p10,q10,r10,s10,t10,u10=RFC_gini(X_train,y_train,X_test,y_test,a,l,t,ch)
  y_pred11,a11,b11,c11,d11,e11,f11,g11,h11,i11,j11,k11,l11,m11,n11,o11,p11,q11,r11,s11,t11,u11=RFC_entropy(X_train,y_train,X_test,y_test,a,l,t,ch)
  y_pred12,a12,b12,c12,d12,e12,f12,g12,h12,i12,j12,k12,l12,m12,n12,o12,p12,q12,r12,s12,t12,u12=XGB_Class(X_train,y_train,X_test,y_test,a,l,ch)
  print("\nTesting Accuracy for all the possible Classification models")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Classification':['Logistic Regression', 'K-Nearest-Neighbors', 'Support Vector Classifier (kernel="linear") ','Support Vector Classifier(kernel="poly")','Support Vector Classifier(kernel="rbf")','Support Vector Classifier(kernel="sigmoid")','Naive Bayes Classification','Decision Tree Classification(criteria=gini)','Decision Tree Classification(criteria=entropy)','Random Forest Classification(criteria=gini)','Random Forest Classification(criteria=entropy)','XG-Boost Classification'],'Accuracy classification score':[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12],'K-Fold Accuracy score':[b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12],'Balanced Accuracy':[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12],'Cohen’s kappa Score':[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12],'K-Folds Deviation score':[e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12],'F-measure(macro)':[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12],'F-measure(micro)':[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12],'F-measure(weighted)':[h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12],'F-beta score(macro)':[i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12],'F-beta score(micro)':[j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12],'F-beta score(weighted)':[k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12],'Average Hamming Loss':[l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12],'Jaccards Score(macro)':[m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12],'Matthews correlation coefficient (MCC)':[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12],'precision score(macro)':[o1,o2,o3,o4,o5,o6,o7,o8,o9,o10,o11,o12],'precision-score(micro)':[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12],'precision-score(weighted)':[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12],'recall-score(macro)':[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12],'recall score(micro)':[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12],'recall score(weighted)':[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12],'Zero-one classification loss':[u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12]} 
  df = pd.DataFrame(data) 
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Classification Models Data frame')
  display(df)
  print("\n Generating a Bar plot for the same ....")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  A1=abs(a1+b1+c1+d1)/4
  A2=abs(a2+b2+c2+d2)/4
  A3=abs(a3+b3+c3+d3)/4
  A4=abs(a4+b4+c4+d4)/4
  A5=abs(a5+b5+c5+d5)/4
  A6=abs(a6+b6+c6+d6)/4
  A7=abs(a7+b7+c7+d7)/4
  A8=abs(a8+b8+c8+d8)/4
  A9=abs(a9+b9+c9+d9)/4
  A10=abs(a10+b10+c10+d10)/4
  A11=abs(a11+b11+c11+d11)/4
  A12=abs(a12+b12+c12+d12)/4
  L1=abs(l1+u1)/2
  L2=abs(l2+u2)/2
  L3=abs(l3+u3)/2
  L4=abs(l4+u4)/2
  L5=abs(l5+u5)/2
  L6=abs(l6+u6)/2
  L7=abs(l7+u7)/2
  L8=abs(l8+u8)/2
  L9=abs(l9+u9)/2
  L10=abs(l10+l10)/2
  L11=abs(l11+u11)/2
  L12=abs(l12+u12)/2
  Class_plot(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12)
  while True:
    print("\n For further accuracy results like confusion matrix and so on do select a choice below")
    print("\n 1)Logistic Regression Results,2) KNN results,3)SVC Kernel='Linear'reults,4) SVC kernel='poly'results")
    print("\n5) SVC kernel='rbf'results,6)SVC kernel='sigmoid'results,7) Naive Bayes Classification Results results,8) Decision Tree Classification Results,9)Random Forest Classification Results,10) XG-Boost Classification Results")
    print("\n\t11) All the models results,12) exit")
    ch=int(input("Enter your preffered choice"))
    if ch==1:
      log_res(y_pred1,y_test,b,a)
    elif ch==2:
      KNN_res(y_pred2,y_test,b,a)
    elif ch==3:
      SVC_lin_res(y_pred3,y_test,b,a)
    elif ch==4:
      SVC_poly_res(y_pred4,y_test,b,a)
    elif ch==5:
      SVC_rbf_res(y_pred5,y_test,b,a)
    elif ch==6:
      SVC_sig_res(y_pred6,y_test,b,a)
    elif ch==7:
      Naives_res(y_pred7,y_test,b,a)
    elif ch==8:
      DTC_res_gini(y_pred8,y_test,b,a)
      DTC_res_entropy(y_pred9,y_test,b,a)
    elif ch==9:
      RFC_res_gini(y_pred10,y_test,b,a)
      RFC_res_entropy(y_pred11,y_test,b,a)
    elif ch==10:
      XGB_Class_res(y_pred12,y_test,b,a)
    elif ch==11:
      log_res(y_pred1,y_test,b,a)
      KNN_res(y_pred2,y_test,b,a)
      SVC_lin_res(y_pred3,y_test,b,a)
      SVC_poly_res(y_pred4,y_test,b,a)
      SVC_rbf_res(y_pred5,y_test,b,a)
      SVC_sig_res(y_pred6,y_test,b,a)
      Naives_res(y_pred7,y_test,b,a)
      DTC_res_gini(y_pred8,y_test,b,a)
      DTC_res_entropy(y_pred9,y_test,b,a)
      RFC_res_gini(y_pred10,y_test,b,a)
      RFC_res_entropy(y_pred11,y_test,b,a)
      XGB_Class_res(y_pred12,y_test,b,a)
    elif ch==12:
      print("\n Thank you")
      break
    else:
      print("\n Invalid choice! Try again")

def Naives_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n NAIVE BAYES RESULTS:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision score-max,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def XGB_Class_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n XG-BOOST CLASSIFICATION MODEL RESULTS:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision score-max,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def XGB_Class(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n XG-BOOST CLASSIFICATION MODEL")
  from sklearn import metrics
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  from xgboost import XGBClassifier
  classifier = XGBClassifier()
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n XG-BOOST CLASSIFICATION MODEL CONSTRUCTION -COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def Naives_cla(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n NAIVE BAYES MODEL")
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  from sklearn.naive_bayes import GaussianNB
  from sklearn.model_selection import cross_val_score
  classifier = GaussianNB()
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n NAIVE BAYES MODEL CONSTRUCTION -COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def log_reg(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n LOGISTIC-REGRESSION MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.linear_model import LogisticRegression
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,log_loss,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  regressor = LogisticRegression()
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n LOGISTIC-REGRESSION MODEL CONSTRUCTION -COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def log_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\nLOGISTIC REGRESSION DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision score-max,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")


def weights():
  while True:
    print("\n1)uniform,2)distance")
    i=int(input("enter choice from the above list"))
    if i==1:
      c='uniform'
      print("\n You have chosen 'uniform'")
      break
    elif i==2:
      c='distance'
      print("\n you have chosen 'distance'")
      break
    else :
      print("wrong choice please try again")
  return c

def distance():
  while True:
    print("\n 1)Manhattan distance,2)euclidean_distance")
    s=int(input("Enter the preffered choice number from the above options for KNN"))
    if s==1:
      print("\n You have chosen 'Manhattan Distance'")
      break
    elif s==2:
      print("\n You have chosen 'euclidean_distance'")
      break
    else:
      print("wrong choice please try again")
  return s


def KNN_res(y_pred,y_test,P,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n K-NEAREST NEIGHBORS DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")



  
def KNN(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n K-NEAREST NEIGHBOURS(KNN)")
  from sklearn.model_selection import cross_val_score
  from sklearn.neighbors import KNeighborsClassifier
  n=int(input("enter number of neighbors for KNN"))
  w=weights()
  d=distance()
  classifier = KNeighborsClassifier(n_neighbors = n,weights=w, metric = 'minkowski', p = d)
  classifier.fit(X_train, y_train)
  y_pred=classifier.predict(X_test)
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n K-NEAREST NEIGHBOURS(KNN) MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def SVC_lin_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\nSVC KERNEL-'LINEAR' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_linear(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-LINEAR(linear) MODEL")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'linear',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-LINEAR(linear) MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19


def SVC_poly_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\nSVC KERNEL='POLY' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_poly(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-POLYNOMIAL(poly) MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'poly',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-LINEAR(poly) MODEL CONSTRUCTION -COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

  
def SVC_rbf_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\nSVC KERNEL='RADIAL BASIS FUNCTION(rbf)' DETAILED REPORT:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_rbf(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-RADIAL BASIS FUNCTION(rbf) MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.svm import SVC
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'rbf',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-RADIAL BASIS FUNCTION(rbf) MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

  
def SVC_sig_res(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\nSVC KERNEL='SIGMOID' FURTHER RESULTS:")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def svc_sig(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-SIGMOID(sig) MODEL")
  from sklearn.model_selection import cross_val_score
  from sklearn import metrics
  from sklearn.svm import SVC
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= SVC(kernel = 'sigmoid',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n SUPPORT VECTOR CLASSIFICATION(SVC) ,KERNEL-SIGMOID(sig) MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19


def DTC_res_gini(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n DECISION TREE CLASSIFICATION DETAILED REPORT(criteria='gini'):")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def DTC_gini(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n DECISION TREE CLASSIFICATION ,CRITERIAN-'gini'MODEL")
  from sklearn.model_selection import cross_val_score
  from sklearn.tree import DecisionTreeClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= DecisionTreeClassifier(criterion= 'gini',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n DECISION TREE CLASSIFICATION ,CRITERIAN-'gini'MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def DTC_entropy(X_train,y_train,X_test,y_test,a,l,ch):
  print("\n DECISION TREE CLASSIFICATION ,CRITERIAN-'entropy'MODEL")
  from sklearn.model_selection import cross_val_score
  from sklearn.tree import DecisionTreeClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= DecisionTreeClassifier(criterion='entropy',random_state=0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n DECISION TREE CLASSIFICATION ,CRITERIAN-'entropy'MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def DTC_res_entropy(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n DECISION TREE CLASSIFICATION DETAILED REPORT(criteria='entropy'):")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")


def RFC_res_gini(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n RANDOM FOREST CLASSIFICATION - DETAILED REPORT(criteria='gini'):")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def RFC_gini(X_train,y_train,X_test,y_test,a,l,t,ch):
  print("\n RANDOM FOREST CLASSIFICATION ,CRITERIAN-'gini'MODEL-COMPLETED")
  from sklearn.model_selection import cross_val_score
  from sklearn.ensemble import RandomForestClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= RandomForestClassifier(n_estimators = t,criterion='gini', random_state = 0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n RANDOM FOREST CLASSIFICATION ,CRITERIAN-'gini'MODEL CONSTRUCTION-COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19
  
  

def RFC_entropy(X_train,y_train,X_test,y_test,a,l,t,ch):
  print("\n RANDOM FOREST CLASSIFICATION ,CRITERIAN-'entropy'MODEL ")
  from sklearn.model_selection import cross_val_score
  from sklearn.ensemble import RandomForestClassifier
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  classifier= RandomForestClassifier(n_estimators = t,criterion='entropy', random_state = 0)
  classifier.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  f1=(abs(accuracy_score(y_test,y_pred))*100)
  f2=(abs(balanced_accuracy_score(y_test, y_pred))*100)
  f3=(abs(cohen_kappa_score(y_test,y_pred))*100)
  f4= f1_score(y_test, y_pred,average='macro')
  f5= f1_score(y_test, y_pred,average='micro')
  f6= f1_score(y_test, y_pred,average='weighted')
  f7=fbeta_score(y_test, y_pred, average='macro', beta=l)
  f8=fbeta_score(y_test, y_pred, average='micro', beta=l)
  f9=fbeta_score(y_test, y_pred, average='weighted',beta=l)
  f10=hamming_loss(y_test, y_pred)
  f11=jaccard_score(y_test, y_pred, average='macro')
  f12=matthews_corrcoef(y_test, y_pred)
  f13=precision_score(y_test, y_pred, average='macro')
  f14=precision_score(y_test, y_pred, average='micro')
  f15=precision_score(y_test, y_pred, average='weighted')
  f16=recall_score(y_test, y_pred, average='macro')
  f17=recall_score(y_test, y_pred, average='micro')
  f18=recall_score(y_test, y_pred, average='weighted')
  f19=zero_one_loss(y_test,y_pred)
  if ch==0:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  else:
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train,cv=ch)
    a=accuracies.mean()*100
    sd=accuracies.std()*100
  print("\n RANDOM FOREST CLASSIFICATION ,CRITERIAN-'entropy'MODEL CONSTRUCTION -COMPLETED")
  return y_pred,f1,a,f2,f3,sd,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19

def RFC_res_entropy(y_pred,y_test,p,a):
  from sklearn import metrics
  from sklearn.metrics import accuracy_score,auc,average_precision_score,balanced_accuracy_score,brier_score_loss,cohen_kappa_score,confusion_matrix,dcg_score,f1_score,fbeta_score,jaccard_score,hamming_loss,matthews_corrcoef,multilabel_confusion_matrix,ndcg_score,precision_recall_curve,precision_recall_fscore_support,precision_score,recall_score,roc_auc_score,roc_curve,zero_one_loss
  print("\n RANDOM FOREST CLASSIFICATION - DETAILED REPORT(criteria='entropy'):")
  print("\n Confusion Matrix")
  print("\n")
  print(confusion_matrix(y_test,y_pred))
  print("\n Precision Score-macro,micro,weighted")
  print("\n")
  f22=precision_recall_fscore_support(y_test, y_pred, average='macro')
  print(f22)
  print("\n")
  f23=precision_recall_fscore_support(y_test, y_pred, average='micro')
  print(f23)
  print("\n")
  f24=precision_recall_fscore_support(y_test, y_pred, average='weighted')
  print(f24)
  print("\n")

def calc_p1(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12):
  B=[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12]
  C=[]
  for i in range(len(B)):
    if B[i] >100:
       B[i]=1
  for j in range(len(B)):
    if B[j] != 0 :
      C.append(B[j])
  return C

def calc_p2(L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12):
  B=[L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12]
  C=[]
  for i in range(len(B)):
    if B[i] >1:
       B[i]=1
  for j in range(len(B)):
    if B[j] != 0 :
      C.append(B[j])
  return C

def Class_plot(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12):
  A=calc_p1(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12)
  L=calc_p2(L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12)
  N=12
  ind = np.arange(N)  
  width =float(input("enter width for bar-plot(Normal:0.25)"))      
  plt.bar(ind, A, width, label='accuracy',color='g')
  plt.bar(ind + width, L, width,label='loss',color='r')

  plt.ylabel('Scores')
  plt.title('Classification-Algorithms (Mean(Accuracy(prediction)),Mean(LossChart)-Chart')
  plt.xlabel('Algorithm')

  plt.xticks(ind + width / 6, ('Log-reg','KNN','SVC1', 'SVC2','SVC3','SVC4','NB','DTC1','DTC2','RFC1','RFC2','XGBC'))
  plt.legend(loc='best')
  plt.show() 
  print("\n the following points are hints for the above graph")
  print("\n \t Note: SVC1:SVC(Kernel-linear),\t SVC2:SVC(Kernel-polynomial),\t SVC3:SVC(Kernel-radial basis function (rbf)),\t SVC4:SVC(Kernel-sigmoid)")
  print("\n \t DTC1:DTC(criteria='gini'),\t DTC2:DTC(criteria='entropy'),\t RFC1:RFC(criteria='gini'),\t RFC2:RFC(criteria='entropy')") 
  print("\n \t DTC:Decison Tree Classification,\t RFC: Random Forest Classification ")
  print("\n \t XGBC:XG-Boost Classification")

def Clustering_accuracy (X_train,X_test,y_train,y_test):
  n=int(input("enter value for beta"))
  print("\nLoading all the possible Clustering  models ")
  print("\nLoading compelted.. ")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  y_pred1,a1,b1,c1,d1,e1,f1,g1,h1=k_means(X_train,y_train,X_test,y_test,n)
  y_pred2,a2,b2,c2,d2,e2,f2,g2,h2=heirach_agg(X_train,y_train,X_test,y_test,n)
  print("\nTesting Accuracy for all the possible models")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n Accuracy results are in !.")
  print("\n Generating a dataframe for the same ....")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nNote: For clustering accuracy results lie between -1 and 1")
  print("\n Note: Incase if the Accuracy values exceed the above threshold then  please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Clustering':['K-means Clustering', 'Heirachial Clusterng(Agglomerative Clustering)'], 'Adjusted Rand Score':[a1,a2],'Adjusted Mutual Info':[b1,b2],'Completeness score ':[c1,c2],'Fowlkes mallows score ':[d1,d2],'Homogeneity score ':[e1,e2],'Mutual info score ':[f1,f2],'Normalized mutual info score ':[g1,g2],'V-measure score ':[h1,h2]} 
  df = pd.DataFrame(data)
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Clustering Models Data frame')
  display(df) 
  A1=abs(a1+b1+c1+d1+e1+f1+g1+h1)/8
  A2=abs(a2+b2+c2+d2+e2+f2+g2+h2)/8
  cluster_plot(A1,A2)
  while True:
    print("\n For further accuracy results like contigency matrix and so on do select a choice below")
    print("\n 1)K-means Clustering,2)Heirachial Clustering(Agglomerative Clustering),3) all of the above,4) exit")
    ch=int(input("enter choice from the above list"))
    if ch==1:
      k_means_res(y_pred1,y_test,n)
    elif ch==2:
      heirach_agg_res(y_pred2,y_test,n)
    elif ch==3:
      k_means_res(y_pred1,y_test,n)
      heirach_agg_res(y_pred2,y_test,n)
    elif ch==4:
      print("Thank you")
      break
    else:
      print("Invalid Choice Try again")

def k_means_res(y_pred,y_test,n):
  from sklearn import metrics
  print("\n K-MEANS CLUSTERING-DETAILED REPORT")
  print("\n")
  print("\n contingency matrix\n")
  print(metrics.cluster.contingency_matrix(y_test,y_pred))
  print("\nHomeginity completeness\n")
  print(metrics.homogeneity_completeness_v_measure(y_test, y_pred, beta=n))
  print("\n")

def heirach_agg_res(y_pred,y_test,n):
  from sklearn import metrics
  print("\n HEIRACHIAL CLUSTERING CLUSTERING-DETAILED REPORT")
  print("\n")
  print("\n contingency matrix\n")
  print(metrics.cluster.contingency_matrix(y_test,y_pred))
  print("\nHomeginity completeness\n")
  print(metrics.homogeneity_completeness_v_measure(y_test, y_pred, beta=n))
  print("\n")

def k_means(X_train,y_train,X_test,y_test,n):
  print("\n K-MEANS CLUSTERING MODEL")
  from sklearn.cluster import KMeans
  from sklearn import metrics
  wcss = []
  p=int(input("\n enter minimum value of range for number of cluster computations"))
  f=int(input("\n enter maximum value of range for number of cluster computations"))
  print("\n Sketching the elbow method for K-means Clustering")
  print("\n Please wait for some time")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  for a in range(p,f):
      kmeans = KMeans(n_clusters = a, init = 'k-means++', random_state = 42)
      kmeans.fit(X_train)
      wcss.append(kmeans.inertia_)
  plt.plot(range(p,f), wcss)
  plt.title('The Elbow Method')
  plt.xlabel('Number of clusters')
  plt.ylabel('WCSS')
  plt.show()
  print("\n.....Loading......")
  for g in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*g, 5*g))
    sys.stdout.flush()
    sleep(0.25)
  c=int(round(float(input("\n enter the number of cluster based from the above plot"))))
  kmeans=KMeans(n_clusters=c,init='k-means++',random_state=42)
  kmeans.fit(X_train)
  y_pred=kmeans.fit_predict(X_test)
  a1=metrics.adjusted_rand_score(y_test,y_pred)
  b1=metrics.adjusted_mutual_info_score(y_test,y_pred)
  c1=metrics.completeness_score(y_test,y_pred)
  d1=metrics.fowlkes_mallows_score(y_test,y_pred)
  e1=metrics.homogeneity_score(y_test, y_pred)
  f1=metrics.mutual_info_score(y_test, y_pred,contingency=None)
  c=NMIS()
  g1=metrics.normalized_mutual_info_score(y_test, y_pred, average_method=c)
  h1=metrics.v_measure_score(y_test, y_pred, beta=n)
  print("\n K-MEANS CLUSTERING MODEL CONSTRUCTION - COMPLETED")
  return y_pred,a1,b1,c1,d1,e1,f1,g1,h1

def NMIS():
  while True:
    print("\n 1) min, 2)geometric 3) arithmetic 4) max")
    i=int(input("enter choice from the above list"))
    if i==1:
      c='min'
      print("\n You have chosen 'min'")
      break
    elif i==2:
      c='geometric'
      print("\n you have chosen 'geometric'")
      break
    elif i==3:
      c='arithmetic'
      print("\n you have chosen 'arithmetic'")
      break
    elif i==4:
      c='max'
      print("\n you have chosen 'max' ")
      break
    else:
      print("\n invalid choice please try again")
  return c
  
def method():
  while True:
    print("\n As time complexity for dendrogram is high hence")
    print("\n based on your dataset please choose the appropriate method like if u have very less number of columns choose single")
    print("\n 1)ward 2)complete 3)average 4) single")
    i=int(input("enter choice from the above list"))
    if i==1:
      c='ward'
      print("\n You have chosen 'ward'")
      break
    elif i==2:
      c='complete'
      print("\n you have chosen 'complete'")
      break
    elif i==3:
      c='average'
      print("\n you have chosen 'average'")
      break
    elif i==4:
      c='single'
      print("\n you have chosen 'single'")
      break
    else:
      print("\n invalid choice please try again")
  return c

def linkage_1():
  while True:
    print("\n1) euclidean 2)manhattan 3)cosine")
    print("\nif euclidean is chosen then linkage will be ward by default")
    i=int(input("enter choice from the above list"))
    if i==1:
      c='euclidean'
      print("\n You have chosen 'euclidean'")
      break
    elif i==2:
      c='manhattan'
      print("\n you have chosen 'manhattan'")
      break
    elif i==3:
      c='cosine'
      print("\n you have chosen 'cosine'")
      break
    else:
      print("\n invalid choice please try again")
  return c

def linkage_2():
  while True:
    print("\n 1)complete 2)average 3)single")
    i=int(input("enter choice from the above list"))
    if i==1:
        c='complete'
        print("\n You have chosen 'complete'")
        break
    elif i==2:
        c='average'
        print("\n you have chosen 'average'")
        break
    elif i==3:
        c='single'
        print("\n you have chosen 'single'")
        break
    else:
        print("\n invalid choice please try again")
  return c


def heirach_agg(X_train,y_train,X_test,y_test,n):
  print("\n HEIRACHIAL CLUSTERING MODEL")
  import scipy.cluster.hierarchy as sch
  a=method()
  dend=sch.dendrogram(sch.linkage(X_train,method=a))
  print("\n Sketching the Dendrogram For Heirachial Clustering(X_train)")
  for d in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*d, 5*d))
    sys.stdout.flush()
    sleep(0.25)
  print("\n please wait for some time for the dendrogram to appear accurately")
  plt.title('Dendrogram for X_train')
  plt.xlabel('X-Label')
  plt.ylabel('Euclidean distances')
  plt.show()
  end=sch.dendrogram(sch.linkage(X_test,method=a))
  print("\n Sketching the Dendrogram For Heirachial Clustering(X_test)")
  for d in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*d, 5*d))
    sys.stdout.flush()
    sleep(0.25)
  print("\n please wait for some time for the dendrogram to appear accurately")
  plt.title('Dendrogram for X_test')
  plt.xlabel('X-Label')
  plt.ylabel('Euclidean distances')
  plt.show()
  from sklearn.cluster import AgglomerativeClustering
  from sklearn import metrics
  g=linkage_1()
  if g=='euclidean':
    o=int(round(float(input("\nenter number of clusters based on the above two dendrograms"))))
    hc = AgglomerativeClustering(n_clusters =o, affinity = g, linkage = 'ward')
    hc.fit(X_train)
    y_pred = hc.fit_predict(X_test)
    a1=metrics.adjusted_rand_score(y_test,y_pred)
    b1=metrics.adjusted_mutual_info_score(y_test,y_pred)
    c1=metrics.completeness_score(y_test,y_pred)
    d1=metrics.fowlkes_mallows_score(y_test,y_pred)
    e1=metrics.homogeneity_score(y_test, y_pred)
    f1=metrics.mutual_info_score(y_test, y_pred, contingency=None)
    c=NMIS()
    g1=metrics.normalized_mutual_info_score(y_test, y_pred, average_method=c)
    h1=metrics.v_measure_score(y_test, y_pred, beta=n)
  else:
    l=linkage_2()
    o=int(round(float(input("\nenter number of clusters based on the above two dendrograms"))))
    hc = AgglomerativeClustering(n_clusters =o, affinity = g, linkage = l)
    hc.fit(X_train)
    y_pred = hc.fit_predict(X_test)
    a1=metrics.adjusted_rand_score(y_test,y_pred)
    b1=metrics.adjusted_mutual_info_score(y_test,y_pred)
    c1=metrics.completeness_score(y_test,y_pred)
    d1=metrics.fowlkes_mallows_score(y_test,y_pred)
    e1=metrics.homogeneity_score(y_test, y_pred)
    f1=metrics.mutual_info_score(y_test, y_pred, contingency=None)
    c=NMIS()
    g1=metrics.normalized_mutual_info_score(y_test, y_pred, average_method=c)
    h1=metrics.v_measure_score(y_test, y_pred, beta=n)
  print("\n HEIRACHIAL CLUSTERING MODEL CONSTRUCTION -COMPLETED")
  return y_pred,a1,b1,c1,d1,e1,f1,g1,h1

def calc_p5(A1,A2):
  B=[A1,A2]
  C=[]
  for i in range(len(B)):
    if float(B[i]) > 1.0 or float(B[i])== 0.0 or float(B[i]) < -1.0:
       B[i]=0.5
  for j in range(len(B)):
    if float(B[j]) != 0.0 :
      C.append(B[j])
  return C

def cluster_plot(A1,A2):
  A=calc_p5(A1,A2)
  N=2
  ind = np.arange(N)  
  width =float(input("enter width for bar-plot(Normal:0.25)"))      
  plt.bar(ind, A, width, label='accuracy')

  plt.ylabel('Scores')
  plt.title('Clustering -Algorithms (Mean(Accuracy Score)-Chart')
  plt.xlabel('Algorithm')

  plt.xticks(ind + width / 6, ('K-means','Heirachial(AGMC)'))
  plt.legend(loc='best')
  plt.show()

def AAT(X_train,X_test,y_train,y_test):
  print("\n \t SUPERVISED LEARNING ALGORITHM ACCURACY TEST")
  print("\n please enter the number of K-folds required for the algorithm test")
  print("\n if in case if the user wishes to choose the best k fold for the algorithm then enter 0 below")
  ch=round(int(input("\n enter number of K-folds")))
  print("\n REGRESSION ALGORITHM ACCURACY TEST!")
  df1,a1,a2,a3,a4,a5,a6,a7,a8,a9=Regressor_accuracy_test(X_train, X_test, y_train, y_test,ch)
  m1=Regression_results(a1,a2,a3,a4,a5,a6,a7,a8,a9)
  print("\n CLAFFICATION ALGORITHM ACCURACY TEST!")
  df2,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12=Classifier_accuracy_test(X_train, X_test, y_train, y_test,ch)
  m2=Classification_results(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
  print("\n \t UNSUPERVISED LEARNING ALGORITHM ACCURACY TEST")
  print("\n CLUSTERING ALGORITHM ACCURACY TEST !")
  df3,c1,c2=Clustering_accuracy_test(X_train,X_test,y_train,y_test)
  m3=Clustering_results(c1,c2)
  print("\nSketching an accuracy bar plot for the same")
  print("\n......Loading......\n")
  print("\n")
  A=[m1,m2,m3]
  bars=('Regression','Classification','Clustering')
  N=len(A)
  ind = np.arange(N)  
  width =float(input("enter width for bar-plot(Normal:0.25)"))      
  plt.bar(ind, A, color=['green', 'blue', 'cyan'])
  plt.xticks(ind + width / 2, bars)
  plt.ylabel('Scores')
  plt.title('Algorithms-Accuracy-Chart')
  plt.xlabel('Algorithm')
  plt.show()  
  print("\n Note: Based on the above graph the user could come to a conclusion  that out of the three categories o,one category of  algorithms would prove efficient when implementing on the given dataset ")
  print("\n If the user wishes to further proceed with the process where they would like to find out the efficient algorithm in the same category for the given dataset based on the above conclusion")
  print("\n They could do the same by exiting the present process and rerunning  the entire application again and choose their desired category at the beggining ")
  print("\n if the user wants to view the dataframes again please enter 1 below else to exit the algorithm anyother positive number other than one will do ")
  c=int(input("\n enter choice"))
  if c==1:
    disp(df1,df2,df3)
  else:
    print("\n Thank You")

def disp(df1,df2,df3):
  while True:
    print("1) regression dataframe,2) classification dataframe,3) clustering dataframe,4)all of the above dataframes,5)exit")
    ch=int(input("enter choice"))
    if ch==1:
      display(df1)
    elif ch==2:
      display(df2)
    elif ch==3:
      display(df3)
    elif ch==4:
      display(df1)
      display(df2)
      display(df3)  
    else:
      print("\n Thank You")
      break

def Clustering_results(c1,c2):
  m3=0
  c1=round(c1,3)
  c2=round(c2,3)
  B=[c1,c2]
  C=[]
  for i in range(len(B)):
    if float(B[i])==-1.0:
      B[i]=0
    elif float(B[i])<=-0.9 and float(B[i]) >-1.0:
      B[i]=5
    elif float(B[i]) <=-0.8 and float(B[i]) >-0.9:
      B[i]=10
    elif float(B[i]) <=-0.7 and float(B[i]) > -0.8:
      B[i]=15
    elif float(B[i]) <=-0.6 and float(B[i]) > -0.7:
      B[i]=20
    elif float(B[i]) < -0.5 and float(B[i]) > -0.6:
      B[i]=25
    elif float(B[i]) <=-0.5:
      B[i]=25
    elif float(B[i]) <=-0.4 and float(B[i]) > -0.5:
      B[i]=30
    elif float(B[i]) <=-0.3 and float(B[i]) > -0.4:
      B[i]=35
    elif float(B[i]) <=-0.2 and float(B[i]) > -0.3:
      B[i]=40
    elif float(B[i]) <=-0.1 and float(B[i]) > -0.2:
      B[i]=45
    elif float(B[i]) < 0 and float(B[i]) > -0.1:
      B[i]=50
    elif float(B[i])==0:
      B[i]=50
    elif float(B[i]) <=0.1 and float(B[i])>0:
      B[i]=55
    elif float(B[i]) <=0.2 and float(B[i])>0.1:
      B[i]=60
    elif float(B[i])<=0.3 and float(B[i])>0.2:
      B[i]=65
    elif float(B[i])<=0.4 and float(B[i])>0.3:
      B[i]=70
    elif float(B[i])<0.5 and float(B[i]) >0.4:
      B[i]=75
    elif float(B[i]) ==0.5:
      B[i]=75
    elif float(B[i])<=0.6 and float(B[i]) > 0.5:
      B[i]=80
    elif float(B[i]) <=0.7 and float(B[i])>0.6:
      B[i]=85
    elif float(B[i])<=0.8 and float(B[i])>0.7:
      B[i]=90
    elif float(B[i]) <=0.9 and float(B[i]) >0.8:
      B[i]=95
    elif float(B[i]) < 1.0 and float(B[i])>0.9:
      B[i]=100
    elif float(B[i])==1.0:
      B[i]=100
  for j in range(len(B)):
    if float(B[j]) != 0 :
       C.append(B[j])
  m3=sum(C)/2
  return m3

def Regression_results(a1,a2,a3,a4,a5,a6,a7,a8,a9):
   m1=0
   B=[a1,a2,a3,a4,a5,a6,a7,a8,a9]
   C=[]
   for i in range(len(B)):
     if B[i] >100:
       B[i]=0
   for j in range(len(B)):
     if B[j] != 0 :
        C.append(B[j])
   m1=sum(C)/len(C)
   return m1

def Classification_results(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12):
   m2=0
   B=[b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12]
   C=[]
   for i in range(len(B)):
     if B[i] >100:
       B[i]=0
   for j in range(len(B)):
     if B[j] != 0 :
        C.append(B[j])
   m2=sum(C)/len(C)
   return m2
    
  
def Classifier_accuracy_test(X_train, X_test, y_train, y_test,ch):
  d=[]
  r=classs(d)
  print("\n Continuing with the Process")
  print("\n Transferring to main program")
  for y in range(21):
      sys.stdout.write('\r')
      sys.stdout.write("[%-20s] %d%%" % ('='*y, 5*y))
      sys.stdout.flush()
      sleep(0.25)
  b=np.array(r)
  print("\n Final Representation of the list of classes ")
  print("\nClasses are",b)
  print("\n Note: any non negative number is fine for the below field and it need not be the number of classes/categories in the  dataset")
  a=int(input("enter the number of labels for calculation of score"))
  l=int(input("Enter the value of beta for calculation of score"))
  print("\nLoading all the possible Classification  models ")
  print("\nLoading completed.. ")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  y_pred1,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1=log_reg(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred2,a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2,m2,n2,o2,p2,q2,r2,s2,t2,u2=KNN(X_train,y_train,X_test,y_test,a,l,ch)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  y_pred3,a3,b3,c3,d3,e3,f3,g3,h3,i3,j3,k3,l3,m3,n3,o3,p3,q3,r3,s3,t3,u3=svc_linear(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred4,a4,b4,c4,d4,e4,f4,g4,h4,i4,j4,k4,l4,m4,n4,o4,p4,q4,r4,s4,t4,u4=svc_poly(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred5,a5,b5,c5,d5,e5,f5,g5,h5,i5,j5,k5,l5,m5,n5,o5,p5,q5,r5,s5,t5,u5=svc_rbf(X_train,y_train,X_test,y_test,a,l,ch)
  print("\n........Loading.........")
  y_pred6,a6,b6,c6,d6,e6,f6,g6,h6,i6,j6,k6,l6,m6,n6,o6,p6,q6,r6,s6,t6,u6=svc_sig(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred7,a7,b7,c7,d7,e7,f7,g7,h7,i7,j7,k7,l7,m7,n7,o7,p7,q7,r7,s7,t7,u7= Naives_cla(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred8,a8,b8,c8,d8,e8,f8,g8,h8,i8,j8,k8,l8,m8,n8,o8,p8,q8,r8,s8,t8,u8=DTC_gini(X_train,y_train,X_test,y_test,a,l,ch)
  y_pred9,a9,b9,c9,d9,e9,f9,g9,h9,i9,j9,k9,l9,m9,n9,o9,p9,q9,r9,s9,t9,u9=DTC_entropy(X_train,y_train,X_test,y_test,a,l,ch)
  t=int(input("enter number of trees for Random Forest Classification"))
  y_pred10,a10,b10,c10,d10,e10,f10,g10,h10,i10,j10,k10,l10,m10,n10,o10,p10,q10,r10,s10,t10,u10=RFC_gini(X_train,y_train,X_test,y_test,a,l,t,ch)
  y_pred11,a11,b11,c11,d11,e11,f11,g11,h11,i11,j11,k11,l11,m11,n11,o11,p11,q11,r11,s11,t11,u11=RFC_entropy(X_train,y_train,X_test,y_test,a,l,t,ch)
  y_pred12,a12,b12,c12,d12,e12,f12,g12,h12,i12,j12,k12,l12,m12,n12,o12,p12,q12,r12,s12,t12,u12=XGB_Class(X_train,y_train,X_test,y_test,a,l,ch)
  print("\nTesting Accuracy for all the possible Classification models")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Classification':['Logistic Regression', 'K-Nearest-Neighbors', 'Support Vector Classifier (kernel="linear") ','Support Vector Classifier(kernel="poly")','Support Vector Classifier(kernel="rbf")','Support Vector Classifier(kernel="sigmoid")','Naive Bayes Classification','Decision Tree Classification(criteria=gini)','Decision Tree Classification(criteria=entropy)','Random Forest Classification(criteria=gini)','Random Forest Classification(criteria=entropy)','XG-Boost Classification'],'Accuracy classification score':[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12],'K-Fold Accuracy score':[b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12],'Balanced Accuracy':[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12],'Cohen’s kappa Score':[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12],'K-Folds Deviation score':[e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12],'F-measure(macro)':[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12],'F-measure(micro)':[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12],'F-measure(weighted)':[h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12],'F-beta score(macro)':[i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12],'F-beta score(micro)':[j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12],'F-beta score(weighted)':[k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12],'Average Hamming Loss':[l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12],'Jaccards Score(macro)':[m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12],'Matthews correlation coefficient (MCC)':[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12],'precision score(macro)':[o1,o2,o3,o4,o5,o6,o7,o8,o9,o10,o11,o12],'precision-score(micro)':[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12],'precision-score(weighted)':[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12],'recall-score(macro)':[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12],'recall score(micro)':[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12],'recall score(weighted)':[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12],'Zero-one classification loss':[u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12]} 
  df = pd.DataFrame(data) 
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Classification Models Data frame')
  display(df)
  while True:
    print("\n For further accuracy results like confusion matrix and so on do select a choice below")
    print("\n 1)Logistic Regression Results,2) KNN results,3)SVC Kernel='Linear'reults,4) SVC kernel='poly'results")
    print("\n5) SVC kernel='rbf'results,6)SVC kernel='sigmoid'results,7) Naive Bayes Classification Results results,8) Decision Tree Classification Results,9)Random Forest Classification Results,10) XG-Boost Classification Results")
    print("\n\t11) All the models results,12) exit")
    ch=int(input("Enter your preffered choice"))
    if ch==1:
      log_res(y_pred1,y_test,b,a)
    elif ch==2:
      KNN_res(y_pred2,y_test,b,a)
    elif ch==3:
      SVC_lin_res(y_pred3,y_test,b,a)
    elif ch==4:
      SVC_poly_res(y_pred4,y_test,b,a)
    elif ch==5:
      SVC_rbf_res(y_pred5,y_test,b,a)
    elif ch==6:
      SVC_sig_res(y_pred6,y_test,b,a)
    elif ch==7:
      Naives_res(y_pred7,y_test,b,a)
    elif ch==8:
      DTC_res_gini(y_pred8,y_test,b,a)
      DTC_res_entropy(y_pred9,y_test,b,a)
    elif ch==9:
      RFC_res_gini(y_pred10,y_test,b,a)
      RFC_res_entropy(y_pred11,y_test,b,a)
    elif ch==10:
      XGB_Class_res(y_pred12,y_test,b,a)
    elif ch==11:
      log_res(y_pred1,y_test,b,a)
      KNN_res(y_pred2,y_test,b,a)
      SVC_lin_res(y_pred3,y_test,b,a)
      SVC_poly_res(y_pred4,y_test,b,a)
      SVC_rbf_res(y_pred5,y_test,b,a)
      SVC_sig_res(y_pred6,y_test,b,a)
      Naives_res(y_pred7,y_test,b,a)
      DTC_res_gini(y_pred8,y_test,b,a)
      DTC_res_entropy(y_pred9,y_test,b,a)
      RFC_res_gini(y_pred10,y_test,b,a)
      RFC_res_entropy(y_pred11,y_test,b,a)
      XGB_Class_res(y_pred12,y_test,b,a)
    elif ch==12:
      print("\n Classification Algorithm Accuracy Test-Completed")
      break
    else:
      print("\n Invalid choice! Try again")
  return df,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12


def Regressor_accuracy_test(X_train, X_test, y_train, y_test,ch):
  print("\nLoading all the possible Regression models ")
  print("\nLoading completed.. ")
  print("\n please fill the details with care when prompted to avoid errors")
  for i in range(21):
     sys.stdout.write('\r')
     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
     sys.stdout.flush()
     sleep(0.25)
  a1,b1,c1,d1,e1,f1,g1,h1=linear_reg(X_train,y_train,X_test,y_test,ch)
  a2,b2,c2,d2,e2,f2,g2,h2=poly_reg(X_train,y_train,X_test,y_test,ch)
  print("\n........Loading.........")
  print("\n This might take some couple of minutes due to bulk nature of the algorithm")
  print("\n Kindly do bear")
  a3,b3,c3,d3,e3,f3,g3,h3=svr_linear(X_train,y_train,X_test,y_test,ch)
  a4,b4,c4,d4,e4,f4,g4,h4=svr_poly(X_train,y_train,X_test,y_test,ch)
  print("\n.........LOADING.......")
  a5,b5,c5,d5,e5,f5,g5,h5=svr_rbf(X_train,y_train,X_test,y_test,ch)
  a6,b6,c6,d6,e6,f6,g6,h6=svr_sig(X_train,y_train,X_test,y_test,ch)
  a7,b7,c7,d7,e7,f7,g7,h7=decision_reg(X_train,y_train,X_test,y_test,ch)
  a8,b8,c8,d8,e8,f8,g8,h8=random_reg(X_train,y_train,X_test,y_test,ch)
  a9,b9,c9,d9,e9,f9,g9,h9=XGB_reg(X_train,y_train,X_test,y_test,ch)
  print("\nTesting Accuracy for all the possible Regression models")
  print("\nTesting Accuracy for all the possible models")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nAccuracy results are in !.")
  print("\nGenerating Dataframe for the same..")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nNote: For any 2 columns it should assumed that the Linear Regression would be a Simple Linear Regression which means that for multiple columns the Linear Regression would be a multiple Linear Regression")
  print("\n Note: Incase if the Error , deviance values are high please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Regression':['Linear Regression', 'Polynomial Regression', 'Support Vector Regression(kernel="linear")','Support Vector Regression(kernel="poly")','Support Vector Regression(kernel="rbf")','Support Vector Regression(kernel="sigmoid")','Decision Tree Regression','Random Forest regression','XG Boost Regression'], 'R2_score':[a1,a2,a3,a4,a5,a6,a7,a8,a9],'K-Folds Accuracy score':[b1,b2,b3,b4,b5,b6,b7,b8,b9],'Variance_score':[c1,c2,c3,c4,c5,c6,c7,c8,c9],'K-Folds Deviation Score':[d1,d2,d3,d4,d5,d6,d7,d8,d9],'Max_Error':[e1,e2,e3,e4,e5,e6,e7,e8,e9],'Mean Absolute Error':[f1,f2,f3,f4,f5,f6,f7,f8,f9],'Mean Squared Error':[g1,g2,g3,g4,g5,g6,g7,g8,g9],'Median Absolute Error':[h1,h2,h3,h4,h5,h6,h7,h8,h9]} 
  df = pd.DataFrame(data) 
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Regression Models Data frame')
  display(df)
  print("\n Regression Algorithm Accuracy Test-Completed")
  print("\n Note: Incase if the values of the dependent variable y is continous then the preffered choice is to go ahead with Regression models as classification models might throw an error ")
  print("\n If incase the user wants to exit the algorithm due to the above reason please enter the value 0 or 1 below")
  return df,a1,a2,a3,a4,a5,a6,a7,a8,a9

def Clustering_accuracy_test (X_train,X_test,y_train,y_test):
  n=int(input("enter value for beta"))
  print("\nLoading all the possible Clustering  models ")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nLoading compelted.. ")
  y_pred1,a1,b1,c1,d1,e1,f1,g1,h1=k_means(X_train,y_train,X_test,y_test,n)
  y_pred2,a2,b2,c2,d2,e2,f2,g2,h2=heirach_agg(X_train,y_train,X_test,y_test,n)
  print("\nTesting Accuracy for all the possible models")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\n Accuracy results are in !.")
  print("\n Generating a dataframe for the same ....")
  for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
  print("\nNote: For clustering accuracy results lie between -1 and 1")
  print("\n Note: Incase if the Accuracy values exceed the above threshold then  please use data preprocessing tools to scale down the value of the feature and try to run the algorithm again")
  data = {'Type of Clustering':['K-means Clustering', 'Heirachial Clusterng(Agglomerative Clustering)'], 'Adjusted Rand Score':[a1,a2],'Adjusted Mutual Info':[b1,b2],'Completeness score ':[c1,c2],'Fowlkes mallows score ':[d1,d2],'Homogeneity score ':[e1,e2],'Mutual info score ':[f1,f2],'Normalized mutual info score ':[g1,g2],'V-measure score ':[h1,h2]} 
  df = pd.DataFrame(data)
  df=df.style.set_table_attributes("style='display:inline'").set_caption('Clustering Models Data frame')
  display(df) 
  while True:
    print("\n For further accuracy results like contigency matrix and so on do select a choice below")
    print("\n 1)K-means Clustering,2)Heirachial Clustering(Agglomerative Clustering),3) all of the above,4) exit")
    ch=int(input("enter choice from the above list"))
    if ch==1:
      k_means_res(y_pred1,y_test,n)
    elif ch==2:
      heirach_agg_res(y_pred2,y_test,n)
    elif ch==3:
      k_means_res(y_pred1,y_test,n)
      heirach_agg_res(y_pred2,y_test,n)
    elif ch==4:
      print("\n Clustering Algorithm Accuracy Test-Completed")
      break
    else:
      print("\n Invalid choice! try again")
  return df,a1,a2

























