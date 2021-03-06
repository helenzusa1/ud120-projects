
# coding: utf-8

# In[5]:

#!/usr/bin/python

"""
Skeleton code for k-means clustering mini-project
"""

import pickle
import numpy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import sys
sys.path.append("../tools/")
from feature_format import featureFormat,targetFeatureSplit

def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):

    """ some plotting code designed to help you visualize your clusters """
    ### plot each cluster with a different color--add more colors for
    ### drawing more than five clusters
    colors = ["b", "c", "k", "m", "g"]

    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])
    ### if you like, place red stars over points that are POIs (just for funsies)

    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()                                         
                                         
### load in the dict of dicts containing all the data on each person in the dataset
data_dict=pickle.load(open("C:/ATT Training courses/ND Machine Learning/Projects/ud120-projects/final_project/final_project_dataset.pkl","r"))
### there's an outlier---remove it!
data_dict.pop("TOTAL",0)
                                
### the input features we want to use
### can be any key in the person-level dictionary (salary, director_fees,etc.)
feature_1="salary"
feature_2="exercised_stock_options"    
feature_3="total_payments"
poi="poi"
features_list=[poi,feature_1,feature_2, feature_3]
data=featureFormat(data_dict,features_list)
poi,finance_features=targetFeatureSplit(data)
                                         
### in the "clustering with 3 features" part of the mini-project,
### you'll want to change this line to
### for f1,f2,_in finance_features:
### *as it's currently written, the line below assume 2 features)
for f1,f2, _ in finance_features:
    plt.scatter(f1,f2)
plt.show()

### cluster here: create predictions of the clutter labels
### for the data and store them to a list called pred
clf_before=KMeans(n_clusters=2)
clf_before.fit(finance_features)
pred_before = clf_before.predict(finance_features)

### rename the "name" parameter when you change the number of features
### so that the figure gets saved to a different file
try:
    Draw(pred_before,finance_features,poi,mark_poi=False,name="cluster_before_scaling.pdf",f1_name=feature_1,f2_name=feature_2)                                         
except NameError:
    print "no predictions object named pred_before found, no clusters to plot"         
    
    
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler()
scaled_finance_features= scaler.fit_transform(finance_features)
print scaled_finance_features
clf_after=KMeans(n_clusters=2)
pred_after=clf_after.fit_predict(scaled_finance_features)

for f1, f2, _ in scaled_finance_features:
    plt.scatter(f1,f2)
plt.show()

try:
    Draw(pred_after,scaled_finance_features,poi,mark_poi=False,name="cluster_after_scaling.pdf",f1_name=feature_1,f2_name=feature_2)
except NameError:
    print "no predictions object named pred_after found, no cluster to plot"

stock=[]
salary=[]
for i in data_dict:
    if data_dict[i]["exercised_stock_options"] != 'NaN':
        stock.append(float(data_dict[i]["exercised_stock_options"]))
    if data_dict[i][feature_1] != 'NaN':
        salary.append(float(data_dict[i][feature_1]))
        
stock_max=max(stock)
stock_min=min(stock)
salary_max=max(salary)
salary_min=min(salary)

##another way to get max, min
##stock_max=data[:,2].max
##stock_min=(data[:,2][np.nonzero(data[:,2])]).min()

print "Max exercised stock options is ", stock_max, "; Min is ", stock_min
print "Max salary is ", salary_max, "; Min is ", salary_min



# In[ ]:



