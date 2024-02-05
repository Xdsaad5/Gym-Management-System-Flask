import json

import pymysql
from  database.model import *
class adminDbHandler:
    def __init__(self,hst,user,password,db):
        try:
            self.__host=hst
            self.__user=user
            self.__password=password
            self.__db=db
            self.__myDb = None
            self.__connectionWithDb()
        except Exception as e:
            return str(e)
    def __connectionWithDb(self):
        if self.__myDb != None:
            return
        try:
            self.__myDb = pymysql.connect(host=self.__host,user=self.__user,password=self.__password,database=self.__db)
        except Exception as e:
            return str(e)

    def verifyAdmin(self,email,passw):
        if email == None or passw == None:
            return False
        try:
            myCursor = self.__myDb.cursor()
            sql = "select email, password from admin  where email=%s and password=%s"
            values = (email,passw)
            myCursor.execute(sql,values)
            data = myCursor.fetchall()
            myCursor.close()
            if data == ():
                return False
            else:return data
        except Exception as e:
            return str(e)
    def removeTrainee(self,userName):
        if userName == "" or userName is None:
            return
        try:
            myCursor = self.__myDb.cursor()
            sql = "Delete from traineeImages where username=%s"
            values = (userName)
            status = myCursor.execute(sql, values)
            self.__myDb.commit()
            sql = "Delete from trainee where username=%s"
            values=(userName)
            status=myCursor.execute(sql,values)
            self.__myDb.commit()
            myCursor.close()
            return status
        except Exception as e:
            return False
        finally:
            if myCursor is not None:
                myCursor.close()

    def removeTrainer(self, email):
        if email == "" or email is None:
            return
        try:

            myCursor = self.__myDb.cursor()
            sql = "select * from trainee where assigned_trainer=%s"
            status = myCursor.execute(sql, email)
            data = myCursor.fetchall()
            for item in data:
                print(item)
                sql = "SET FOREIGN_KEY_CHECKS=0;"
                myCursor.execute(sql)
                sql = "update trainee set assigned_trainer=%s where username=%s"
                values = ("",item[0])
                print(item[0])
                status = myCursor.execute(sql, values)
                self.__myDb.commit()

            sql = "Delete from trainerImages where email=%s"
            values = (email)
            status = myCursor.execute(sql, values)
            self.__myDb.commit()
            sql = "Delete from trainerVideos where email=%s"
            values = (email)
            status = myCursor.execute(sql, values)
            self.__myDb.commit()
            sql = "Delete from trainer where email=%s"
            values = (email)
            status = myCursor.execute(sql, values)
            self.__myDb.commit()
            myCursor.close()
            return status
        except Exception as e:
            return False

    def displayTrainee(self):
        try:
            myCursor = self.__myDb.cursor()
            sql = "select username,age,gender,mobile_number,assigned_trainer from trainee"
            myCursor.execute(sql)
            traineeData = myCursor.fetchall()
            if traineeData == ():
                return False
            myDic= {}
            myList=[]
            for item in traineeData:
                myDic.update(name=item[0])
                myDic.update(age=item[1])
                myDic.update(gender=item[2])
                myDic.update(contact=item[3])
                if item[4] == None:
                    myDic.update(Assigned_Trainer='No one assign.')
                else:
                    myDic.update(Assigned_Trainer=item[4])
                myList.append(myDic)
                myDic={}
            i=0
            for i in myList:
               sql = "select image_url from traineeImages where username=%s"
               values=(i['name'])
               myCursor.execute(sql,values)
               imgUrl = myCursor.fetchall()
               i.update(imageUrl=imgUrl[0][0])
            myCursor.close()
            return myList
        except Exception as e:
            print(str(e))
    def displayTrainer(self,imgeUrl=False):
        try:
            myCursor = self.__myDb.cursor()
            sql="select * from trainer"
            myCursor.execute(sql)
            trainerData = myCursor.fetchall()
            if trainerData == ():
                myCursor.close()
                return False
            myDic= {}
            myList=[]
            for item in trainerData:
                myDic.update(name=item[0])
                myDic.update(email=item[1])
                myDic.update(speciality=item[3])
                myDic.update(experience=item[4])
                myDic.update(participated_in_any_competition=item[5])
                myDic.update(consult_fee=str(item[6]))
                myDic.update(mobile_number=item[7])
                myList.append(myDic)
                myDic={}
            print("myList",myList)
            if imgeUrl == True:
                i = 0
                for i in myList:
                    sql = "select image_url from trainerImages where email=%s"
                    values = (i['email'])
                    myCursor.execute(sql, values)
                    imgUrl = myCursor.fetchall()
                    print(imgUrl)
                    if bool(imgUrl) == False:
                        print("In If imgUrl")
                        i.update(imageUrl='/static/image/f-img-1.jpg')
                    else:
                        i.update(imageUrl=imgUrl[0][0])
            myCursor.close()
            return myList
        except Exception as e:
            print(str(e))

    def displayOneTrainer(self, email):
        try:
            myCursor = self.__myDb.cursor()
            sql = "select * from trainer where email=%s"
            myCursor.execute(sql,email)
            trainerData = myCursor.fetchall()
            if trainerData == ():
                myCursor.close()
                return False
            myDic = {}
            myList = []
            for item in trainerData:
                myDic.update(name=item[0])
                myDic.update(email=item[1])
                myDic.update(speciality=item[3])
                myDic.update(experience=item[4])
                myDic.update(participated_in_any_competition=item[5])
                myDic.update(consult_fee=str(item[6]))
                myDic.update(mobile_number=item[7])
                myList.append(myDic)
                myDic = {}
            i = 0
            for i in myList:
                sql = "select image_url from trainerImages where email=%s"
                values = (i['email'])
                myCursor.execute(sql, values)
                imgUrl = myCursor.fetchall()
                if imgUrl == ():
                    i.update(imageUrl='/static/image/f-img-1.jpg')
                else:
                    i.update(imageUrl=imgUrl[0][0])
            myCursor.close()
            return myList
        except Exception as e:
            print(str(e))
    def __del__(self):
        if self.__myDb is not None:
            self.__myDb.close()
        else:
            return



class trainerDbHandler:
    def __init__(self,hst,user,password,db):
        try:
            self.__host=hst
            self.__user=user
            self.__password=password
            self.__db=db
            self.__myDb = None
            self.__connectionWithDb()
        except Exception as e:
            return str(e)
    def __connectionWithDb(self):
        if self.__myDb != None:
            return
        try:
            self.__myDb = pymysql.connect(host=self.__host,user=self.__user,password=self.__password,database=self.__db)
        except Exception as e:
            return str(e)
    def signUpAsTrainer(self,Trainer ):
        if Trainer is None:
            return
        try:
            myCursor = self.__myDb.cursor()
            sql = "INSERT INTO trainer(name,email,password,speciality,experience,participated_in_any_competition," \
                  "consult_fee,mobile_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            print(Trainer.name)
            values=(Trainer.name,Trainer.email,Trainer.password,Trainer.speciality,Trainer.experience,
                    Trainer.participated_in_any_competition,Trainer.consult_fee,Trainer.mobile_number)
            myCursor.execute(sql,values)
            self.__myDb.commit()
            myCursor.close()
            return True
        except Exception as e:
            return e

    def login(self,email,password):
        if email == None or password == None:
            return False
        try:
            myCursor = self.__myDb.cursor()
            sql = "select email, password from trainer where email=%s and password=%s"
            values = (email, password)
            myCursor.execute(sql, values)
            data = myCursor.fetchall()
            myCursor.close()
            if data == ():
                return False
            else:
                return data
        except Exception as e:
            return str(e)
    def __del__(self):
        if self.__myDb is not None:
            self.__myDb.close()
        else:
            return
    def addPicture(self,email,url):
        try:
            if email == "":
                return "In valid Email"
            myCursor = self.__myDb.cursor()
            sql = "INSERT INTO trainerImages(email,image_url) VALUES (%s,%s)"
            values = (email,url)
            status = myCursor.execute(sql,values)
            self.__myDb.commit()
            myCursor.close()
            return status
        except Exception as e:
            print(str(e))
            return False
    def addVideo(self,email,url):
        try:
            if email == "":
                return "In valid Email"
            myCursor = self.__myDb.cursor()
            sql = "INSERT INTO trainerVideos(email,video_url) VALUES (%s,%s)"
            values = (email,url)
            status = myCursor.execute(sql,values)
            self.__myDb.commit()
            myCursor.close()
            return status
        except Exception as e:
            print(str(e))
            return False

class traineeDbHandler:
    def __init__(self, hst, user, password, db):
        try:
            self.__host = hst
            self.__user = user
            self.__password = password
            self.__db = db
            self.__myDb = None
            self.__connectionWithDb()
        except Exception as e:
            return str(e)

    def __connectionWithDb(self):
        if self.__myDb != None:
            return
        try:
            self.__myDb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                          database=self.__db)
        except Exception as e:
            return str(e)
    def signUpTrainee(self,trainee):
        if trainee is None:
            return
        try:
            myCursor = self.__myDb.cursor()
            sql = "INSERT INTO trainee(username,email,password,age,mobile_number,gender) VALUES (%s,%s,%s,%s,%s,%s)"
            print(trainee.username)
            values = (trainee.username, trainee.email, trainee.password,trainee.age,trainee.mobile_number,trainee.gender)
            status = myCursor.execute(sql, values)
            self.__myDb.commit()
            if bool(status) == False:
                return False
            sql = "INSERT INTO traineeImages(username,image_url) VALUES (%s,%s);"
            values = (trainee.username,trainee.imgPath)
            myCursor.execute(sql,values)
            self.__myDb.commit()
            myCursor.close()
            return True
        except Exception as e:
            return e

    def login(self, username, password):
        if username == None or password == None:
            return False
        try:
            myCursor = self.__myDb.cursor()
            sql = "select username, password from trainee where username=%s and password=%s"
            values = (username, password)
            myCursor.execute(sql, values)
            data = myCursor.fetchall()
            myCursor.close()
            if data == ():
                return False
            else:
                return data
        except Exception as e:
            return str(e)
    def selectTrainer(self,traineeName,selectedTrainerEmail):
        try:
            print("In SelectTrainer.")
            if selectedTrainerEmail is None:
                return "Empty e-mail."
            myCursor = self.__myDb.cursor()
            sql = "select assigned_trainer from trainee where username=%s"
            myCursor.execute(sql, traineeName)
            data = myCursor.fetchall()
            if data[0][0] == selectedTrainerEmail:
                myCursor.close()
                return "Already Assigned."
            sql = "update trainee set assigned_trainer=%s where username=%s"
            values=(selectedTrainerEmail,traineeName)
            status = myCursor.execute(sql,values)
            self.__myDb.commit()
            print("Data",data[0][0])
            if bool(data[0][0]) == False:
                return "Successfully Assigned."
            if data is not None:
                return "You have changed Your Trainer."
        except Exception as e:
            return str(e)
    def __del__(self):
        if self.__myDb is not None:
            self.__myDb.close()
        else:
            return

#trainer = Trainer("saad","saad@yahoo.com",'bsef20a032','Training experience in abroad','5years','All pakistan.','2000','3008101304'''
'''
obj2=traineeDbHandler("localhost","root","saad","gym_database")

print(obj2.selectTrainer('rimsha','saad@yahoo.com'))'''
'''
obj = adminDbHandler('localhost','root','saad','gym_database')
print(obj.displayOneTrainer('saad@yahoo.com'))'''
