from flask import Flask,url_for,redirect,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import sleep
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import random

app = Flask(__name__)
app.secret_key = "Priyansh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.jinja_env.globals.update(isinstance=isinstance)

@app.route('/')
def index():
    return redirect(url_for('Home'))

@app.route('/Home')
def Home():
    return render_template("index.html")

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/tool' , methods=["GET","POST"])
def tool():

    if request.method == "POST":
        '''data_dict = request.form.to_dict()
        data_dict.pop("name")
        for i in data_dict:
            data_dict[i]=eval(data_dict[i])
            data_dict[i]=[data_dict[i]]
        data_list = []
        data_list.append(data)'''

        #Or

        user_dict = {}
        current_sem = request.form['current_sem']
        #user_dict["Name"] = request.form["name"]
        user_dict["Current sem"] = current_sem
        for i in range(1,int(current_sem)):
            temp_list = []
            temp_list.append(int(request.form["Attendance_"+str(i)]))
            temp_list.append(int(request.form["Events_"+str(i)]))
            temp_list.append(int(request.form["Sem_Percent_"+str(i)]))
            user_dict["Sem "+str(i)] = temp_list
        user_dict["Tech skills"] = int(request.form["tech_skills"])
        user_dict["Backlogs"] = request.form["backlogs"]

        backlogs = int(user_dict["Backlogs"])
        backlogs_percentage = (backlogs * 100)/32
        final_backlog_percent = 100 - backlogs_percentage
        user_dict["Backlogs"] = final_backlog_percent

     
        data = user_dict
        current_sem = int(data["Current sem"])
        df=pd.DataFrame(data)
        train = df.drop(["Current sem"],axis=1)
        temp_list = []
        for i in range(1,current_sem):
            temp_list.append("Sem "+str(i))
        
        test = df[temp_list]
        X_train,X_test,Y_train,Y_test = train_test_split(train,test,test_size=0.3,random_state=2)
        regr = LinearRegression()
        regr.fit(X_train,Y_train)
        pred = regr.predict(X_test)
        pred=np.average(pred)
        pred = int(pred)
        CGPA = pred/10+0.5

        #Data Visualization
        counter=int(data["Current sem"])
        list1=[]
        for i in range(1,counter):
            list1.append(data["Sem "+str(i)])
        a=list1
        new_dict = {key:val for key, val in data.items() if key not in ('Current sem','Tech skills','Backlogs') } 
        xaxis = list(new_dict.keys())  # semester values and keys
        new_dict_1 = {key:val for key, val in data.items() if key == 'Current sem'} 
        new_dict_1 = list(new_dict_1.keys())
        xaxis.append(new_dict_1[0])
        xaxis_att = list(new_dict.keys())
        list2=[] #converted attendance into a list
        for i in range(0,counter-1):
            list2.append(list1[i][0])

        list3=[]
        for i in range(0,counter-1):
            list3.append(list1[i][2])
        
        predicted_score = pred
        list3.append(predicted_score)
        print(list3)

        random_number = str(random.randint(0,1000))

        #Creating a bar graph from the filtered data

        fig = plt.figure(figsize = (6, 4)) 
        colors = []
        bar_chart = dict(zip(xaxis, list3)) 
        for key, val in bar_chart.items(): 
            if key == 'Current sem':
                colors.append('red')
            else:
                colors.append('blue')

        # creating the bar plot for grades
        plt.bar(bar_chart.keys(), bar_chart.values(), color = colors,width = 0.3) 
        
        plt.xlabel("Semester") 
        plt.ylabel("semester percentage(%)") 
        plt.title("Students percentages(%) by Semester") 
        plt.savefig("static/images/Graphs/Grade_Bar_graph_"+random_number+".png")

        #Grade rise according to semesters
        '''b = sns.kdeplot(list3, shade=True)
        b.axes.set_title('Grade rise according to semesters', fontsize = 15)
        b.set_xlabel('Grade', fontsize = 20)
        b.set_ylabel('Count', fontsize = 20)
        grade_rise_fig = b.get_figure()
        grade_rise_fig.savefig("static/images/Graphs/Grade_rise_"+random_number+".png")'''

        # creating the bar plot for attendance

        fig = plt.figure(figsize = (6, 4)) 
        plt.bar(xaxis_att, list2, color ='blue', width = 0.3) 
        plt.xlabel("Semester") 
        plt.ylabel("Attendance(%)") 
        plt.title("Students Attendance(%) by Semester") 
        plt.savefig("static/images/Graphs/Attendance_Bar_graph_"+random_number+".png")

        #Filtering the data to be passed. Doesn't affect the prediction
        if(user_dict["Tech skills"]==1):
            user_dict["Tech skills"]="Yes"
        elif(user_dict["Tech skills"]==-1):
            user_dict["Tech skills"]="No"
        user_dict["Backlogs"]=request.form["backlogs"]

        return render_template("result.html" , data = user_dict , final_grade = pred , CGPA=CGPA, Grade_bar_graph = "static/images/Graphs/Grade_Bar_graph_"+random_number+".png" , Attendance_bar_graph="static/images/Graphs/Attendance_Bar_graph_"+random_number+".png")
    else:
        return render_template("form.html")



if __name__ == '__main__':
    app.run(debug = True)