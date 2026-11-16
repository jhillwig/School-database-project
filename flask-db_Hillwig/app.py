#! /usr/bin/python3
from flask import Flask, render_template, request, jsonify
import json
import config
import pymysql

#for the pymysql look at the faculty url, on that the two ways to access the CS database will be shown


#Configuration for pymysql
db = config.dbserver

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello message'

@app.route('/hellothere')
def hellothere():
    name =  "General Kenobi"
    return render_template("hellothere.html", values=name)

@app.route('/search',  methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        values = {
            'name': myName,
            'id': myId }
        return render_template('results.html', **values)
    if request.method == 'GET':
        return render_template('form.html')

@app.route('/values')
def values():
    myInteger = 3
    return render_template('values.html', value = myInteger)

@app.route('/pokedex')
def loop():
    pokedex = ["Pikachu", "Charizard", "Squirtle", "Jigglypuff",  
           "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]     
    return render_template('pokedex.html', pokedex = pokedex)
       
@app.route('/faculty', methods = ['GET','POST'])
def displayFaculty():
        if request.method == 'GET':
            #Function with pymysql
            cursor = db.cursor()
            sql = "call lookAllInstructors();"
            data = ''
            try:
                cursor.execute(sql)            
                data = cursor.fetchall()
            except pymysql.Error as e:
                print(e)
            cursor.close()
            print(data)
            #return f"Done!! Query Result is {data}"
            return render_template('faculty.html', data=data)
        if request.method == 'POST':
            data = request.form['ID']
            print(data)
            cursor = db.cursor()
            #Terrible way to execute it, could lead to sql injection            
            """sql = "delete from instructor where id = " + data
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                db.commit()
            except pymysql.Error as e:
                print(e)"""

            #Better way to do it, more secure againts sql injection

            """sql = "delete from instructor where id = %s"
            try:
                cursor.execute(sql, [data])
                data  = cursor.fetchall()
                db.commit()
            except pymysql.Error as e:
                print(e)"""
            
            #The best way to remove instructor
            #using stored procedures

            sql = "call removeInstructor(%s);"
            try:
                cursor = db.cursor()
                cursor.execute(sql, [data])
                db.commit()
            except pymysql.Error as e:
                print(e)
            cursor.close() 
            #get new faculty data   
            
            try:
                cursor = db.cursor()  
                sql = "call lookAllInstructors();"
                cursor.execute(sql)
                data = cursor.fetchall()
            except pymysql.Error as e:
                print(e)
            cursor.close()    
            return render_template('faculty.html',data= data)

@app.route('/facultysearch', methods = ['GET','POST'])
def facultySearch():        
        if request.method == 'GET':
            return render_template('facultysearch.html')
        if request.method == 'POST':
            myName = request.form['name']
            myId = request.form['id']
            print(myName, myId)    
            if myId != "":
                print("Goin for ID")
                cursor = db.cursor()
                sql = "call lookInstructor(%s);"
                try:
                    cursor.execute(sql,[myId])
                    data = cursor.fetchall()
                except pymysql.Error as e:
                    print(e)
                cursor.close()
            elif myName != "":
                print("Goin for Name")
                cursor = db.cursor()
                sql = "call lookInstructorName(%s);"
                try: 
                    cursor.execute(sql, [myName])
                    data = cursor.fetchall()
                except pymysql.Error as e:
                    print(e)
                cursor.close()            
            else:
                 return render_template('facultysearch.html')
            return render_template('faculty.html', data=data)
        
#================================================================================================================
@app.route('/newfaculty',  methods = ['GET','POST'])
def newFaculty():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call lookAllDepartments();"
        try:
            cursor.execute(sql)
            data = cursor.fetchall()        
        except pymysql.Error as e:
                print(e)
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('newfaculty.html', data = edited)
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        myDept = request.form['dept']        
        mySalary = request.form['salary']
        cursor = db.cursor()
        sql = "call insertInstructor(%s, %s, %s, %s)"    
        try:
            cursor.execute(sql,[myId, myName, myDept, mySalary])
            db.commit()
        except pymysql.Error as e:
                print(e)
        #reload page with all favulty members        
        cursor = db.cursor()
        try:
            sql = "call lookAllInstructors()"
            cursor.execute(sql)
            data = cursor.fetchall()
        except pymysql.Error as e:
                print(e)
        cursor.close()
        return render_template('faculty.html', data=data)
    
#=========================================================================================
#========================= STUDENT IMPLEMENTATION ========================================
@app.route('/student', methods = ['GET','POST'])
def displayStudent():
        if request.method == 'GET':
            #Function with pymysql
            cursor = db.cursor()
            sql = "call lookAllStudents();"
            data = ''
            try:
                cursor.execute(sql)            
                data = cursor.fetchall()
            except pymysql.Error as e:
                print(e)
            cursor.close()
            print(data)
            #return f"Done!! Query Result is {data}"
            return render_template('students.html', data=data)
        if request.method == 'POST':
            data = request.form['ID']
            print(data)
            cursor = db.cursor()
            #Terrible way to execute it, could lead to sql injection            
            """sql = "delete from instructor where id = " + data
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                db.commit()
            except pymysql.Error as e:
                print(e)"""

            #Better way to do it, more secure againts sql injection

            """sql = "delete from instructor where id = %s"
            try:
                cursor.execute(sql, [data])
                data  = cursor.fetchall()
                db.commit()
            except pymysql.Error as e:
                print(e)"""
            
            #The best way to remove instructor
            #using stored procedures

            sql = "call removeStudent(%s);"
            try:
                cursor = db.cursor()
                cursor.execute(sql, [data])
                db.commit()
            except pymysql.Error as e:
                print(e)
            cursor.close() 
            #get new faculty data   
            
            try:
                cursor = db.cursor()  
                sql = "call lookAllStudents();"
                cursor.execute(sql)
                data = cursor.fetchall()
            except pymysql.Error as e:
                print(e)
            cursor.close()    
            return render_template('students.html',data= data)
        
@app.route('/studentsearch', methods = ['GET','POST'])
def studentsearch():        
        if request.method == 'GET':
            return render_template('studentSearch.html')
        if request.method == 'POST':
            myName = request.form['name']
            myId = request.form['id']
            print(myName, myId)    
            data = ''
            if myId != "":
                print("Goin for ID")
                cursor = db.cursor()
                sql = "call lookStudent(%s);"
                    #^assumingly need to create a storeproceedure for here that will return students.
                try:
                    cursor.execute(sql,[myId])
                    data = cursor.fetchall()
                except pymysql.Error as e:
                    print(e)
                cursor.close()
            elif myName != "":
                print("Goin for Name")
                cursor = db.cursor()
                sql = "call lookStudentName(%s);"
                try: 
                    cursor.execute(sql, [myName])
                    data = cursor.fetchall()
                except pymysql.Error as e:
                    print(e)
                cursor.close()            
            else:
                 return render_template('studentSearch.html')
            print(data)
            return render_template('students.html', data=data)
#================================================================================================================
@app.route('/schedule',  methods = ['GET','POST'])
def scheduleStudent():
    #if request.method == 'POST': 
     #   myYears = request.form['years']
      #  myID = request.form['StudentID']
       # print(myYears, myID)
        
            #^New store proceedure invocation
    stu_id = request.args.get('id')
    cursor = db.cursor()
    sql = "call scheduleStudent(%s);"
    cursor.execute(sql,[stu_id])
    data = cursor.fetchall()        
    print(data)
    years = set()
    for row in data:
        years.add(row[4])
    print(years)
    return render_template('studentschedule.html', data=data, years=years, studentID = data[0][0])    
#=========================================================================================
@app.route('/scheduleYears',  methods = ['GET','POST'])
def scheduleStudentYears():
    if request.method == 'POST': 
        myYears = request.form['years']
        myID = request.form['StudentID']
        print(myYears, myID)
        cursor = db.cursor()
        sql = "call studentFilterYear(%s, %s);"
        cursor.execute(sql,[myID, myYears])
        data = cursor.fetchall() 
        print(data)
        cursor.close()                
    return render_template('studentScheduleYears.html', data=data)    
#=========================================================================================
@app.route('/newstudent',  methods = ['GET','POST'])
def newStudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call lookAllDepartments();"
        try:
            cursor.execute(sql)
            data = cursor.fetchall()        
        except pymysql.Error as e:
                print(e)
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('newstudent.html', data = edited)
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        myDept = request.form['dept']        
        myCredits = request.form['credits']
        if myCredits == '':
            myCredits = 0
        cursor = db.cursor()
        sql = "call insertStudent(%s, %s, %s, %s)"    
        try:
            cursor.execute(sql,[myId, myName, myDept, myCredits])
            db.commit()
        except pymysql.Error as e:
                print(e)
        #reload page with all favulty members        
        cursor = db.cursor()
        try:
            sql = "call lookAllStudents()"
            cursor.execute(sql)
            data = cursor.fetchall()
        except pymysql.Error as e:
                print(e)
        cursor.close()
        return render_template('students.html', data=data)
#==============================================================================
    
@app.route('/countfaculty',  methods = ['GET','POST'])
def countFaculty():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call lookAllDepartments();"
        cursor.execute(sql)        
        data = cursor.fetchall()        
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('count.html', data = edited)
    
    if request.method == 'POST':
        dept = request.form['depts']  
        print('deppt = ', dept)
        args = (dept, 0)
        cursor = db.cursor()      
        #sql = "call countDeptFaculty2(%s);"
        #Calling Stored Procedures with output parameters is finicky
        #You have execute the SP and then select the output variables separately in a select query
        cursor.callproc('countDeptFaculty2', args)    
        cursor.execute('SELECT @_countDeptFaculty2_0, @_countDeptFaculty2_1')
        result = cursor.fetchall()
        cursor.close()
        print('result=  ', result)
        return render_template('total.html', data=result[0])
    

if __name__ == '__main__':    
    
    #print(pretty_json)
    app.run(port = 4500)
