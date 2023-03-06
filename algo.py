import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
data = {"Current_sem":4,"sem_1":[50,70,0],"sem_2":[80,90,1],"sem_3":[90,70,1],"Tech_skills":1,"Backlogs":0}
temp = data["Current_sem"]
df=pd.DataFrame(data)
train = df.drop(["Current_sem"],axis=1)
test = df[["sem_"+str(temp-1)]]
X_train,X_test,Y_train,Y_test = train_test_split(train,test,test_size=0.3,random_state=2)
regr = LinearRegression()
regr.fit(X_train,Y_train)
pred = regr.predict(X_test)
print(pred) 