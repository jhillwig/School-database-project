import pymysql


#local database: user will need to be changed depending on where the SQL is stored
dbserver = pymysql.connect(host="dbdev.cs.kent.edu",user= "jhillwig",password= "9yaVCvb9",database= "jhillwig") #for connecting to the CS server