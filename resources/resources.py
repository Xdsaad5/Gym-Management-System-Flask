import json

from database.DbHandlerClasses import *
from flask_restful import Resource
from flask import request,render_template,Response,session
from flask_session import Session
import os
from werkzeug.utils import secure_filename
duplicateApp=None
trainerData = None
def copyAppInstance(app):
    global duplicateApp
    duplicateApp = app

Session(duplicateApp)

def dbDictionary(app):
    app.config.from_pyfile("config.py")
    return {'host':app.config['HOST'],'user':app.config['USER'],'password':app.config['PASSWORD'],'database':app.config['DATABASE']}
class AdminLoginApi(Resource):
    def post(self):
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            emailCheck = email.split('@')
            if len(emailCheck) == 1:
                return Response(response=render_template('loginAsAdmin.html',error="Please Enter Valid syntax of Email."))
            if emailCheck[1] !="gmail.com" and emailCheck[1]!="yahoo.com" and emailCheck[1]!='hotmail.com':
                return Response(response=render_template('loginAsAdmin.html',error="INVALID Email."))
            if len(password)<8:
                return Response(response=render_template('loginAsAdmin.html',error="Password Length is too short."))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = adminDbHandler(dbConfig['host'],dbConfig['user'],dbConfig['password'],dbConfig['database'])
            status = obj.verifyAdmin(email,password)
            if status == False:
                return Response(response=render_template('loginAsAdmin.html',error="Invalid Email or Password."))
            session['email'] = email
            session['password'] = password
            return Response(response=render_template('adminHome.html'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
    def get(self):
        try:
            dbConfig = dbDictionary(duplicateApp)
            obj = adminDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            data = obj.displayTrainer()
            if data == False:
                return ({"msg": "No record Found"}), 201
            data = json.dumps(data)
            return Response(data,mimetype="application/json",status=200)
        except Exception as e:
            return ({"Error": str(e)}), 201
class removeTrainer(Resource):
    def post(self):

        email = request.form.get('email')
        print(email)
        emailCheck = email.split('@')
        if len(emailCheck) == 1:
            return Response(response=render_template('removeTrainer.html', error="Please Enter Valid syntax of Email."))
        global duplicateApp
        dbConfig = dbDictionary(duplicateApp)
        obj = adminDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
        status = obj.removeTrainer(email)
        if bool(status) == False:
            return Response(response=render_template('removeTrainer.html', error="Invalid Email."))
        return Response(response=render_template('removeTrainer.html',error="Successfully Deleted"), status=200, mimetype="text/html")
class removeTrainee(Resource):
    def post(self):
        username = request.form.get('username')
        print(username)
        global duplicateApp
        dbConfig = dbDictionary(duplicateApp)
        obj = adminDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
        status = obj.removeTrainee(username)
        if bool(status) == False:
            return Response(response=render_template('removeTrainee.html', error="Invalid Email."))
        return Response(response=render_template('removeTrainee.html',error="Successfully Deleted."), status=200, mimetype="text/html")

class registerTrainee(Resource):
    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        contact = request.form.get('mobile_number')
        gender = request.form.get('gender')
        f = request.files['imageFile']
        insertImgStatus = str(f).split('.')
        print('username '+username)
        emailCheck = email.split('@')
        if len(emailCheck) == 1:
            return Response(response=render_template('registerAsTrainee.html', error="Please Enter Valid syntax of Email."))
        if emailCheck[1] != "gmail.com" and emailCheck[1] != "yahoo.com" and emailCheck[1] != 'hotmail.com':
            return Response(response=render_template('registerAsTrainee.html', error="INVALID Email."))
        if len(password) < 8:
            return Response(response=render_template('registerAsTrainee.html', error="Password Length is too short."))
        if len(contact) < 10 or len(contact) > 11:
            return Response(response=render_template('registerAsTrainee.html', error="Length of phone number is too short."))
        if int(age) < 1:
            return Response(response=render_template('registerAsTrainee.html', error="Enter valid age."))

        if len(insertImgStatus) == 2:
            imgUrl = duplicateApp.config['UPLOADED_IMAGE']+'/images/'+secure_filename(f.filename)
            traineeObj=trainee(username,email,password,int(age),contact,gender,imgUrl)
        else:
            traineeObj=trainee(username,email,password,int(age),contact,gender)
        dbConfig = dbDictionary(duplicateApp)
        obj = traineeDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
        status = obj.signUpTrainee(traineeObj)
        if status != True:
            return Response(response=render_template('registerAsTrainee.html',error="Invalid username or email"), status=200, mimetype="text/html")
        if len(insertImgStatus) == 2:
            f.save(os.path.join(duplicateApp.config['ABSOLUTE_PATH']+'/images', secure_filename(f.filename)))
        session['username'] = username
        session['password'] = password
        return Response(response=render_template('traineeHome.html'), status=200, mimetype="text/html")
class traineeLoginApi(Resource):
    def post(self):
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            if len(password)<8:
                return Response(response=render_template('loginAsTrainee.html',error="Password Length is too short."))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = traineeDbHandler(dbConfig['host'],dbConfig['user'],dbConfig['password'],dbConfig['database'])
            status = obj.login(username,password)
            if status == False:
                return Response(response=render_template('loginAsTrainee.html',error="Invalid Username or Password."))
            session['username'] = username
            session['password'] = password
            return Response(response=render_template('traineeHome.html'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))

class trainerLoginApi(Resource):
    def post(self):
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            emailCheck = email.split('@')
            if len(emailCheck) == 1:
                return Response(response=render_template('loginAsTrainer.html',error="Please Enter Valid syntax of Email."))
            if emailCheck[1] !="gmail.com" and emailCheck[1]!="yahoo.com" and emailCheck[1]!='hotmail.com':
                return Response(response=render_template('loginAsTrainer.html',error="INVALID Email."))
            if len(password)<8:
                return Response(response=render_template('loginAsTrainer.html',error="Password Length is too short."))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = trainerDbHandler(dbConfig['host'],dbConfig['user'],dbConfig['password'],dbConfig['database'])
            status = obj.login(email,password)
            if status == False:
                return Response(response=render_template('loginAsTrainer.html',error="Invalid Email or Password."))
            session['email'] = email
            return Response(response=render_template('trainerHome.html',welcome='Welcome '+emailCheck[0]), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class registerTrainer(Resource):
    def post(self):
        print("in post")
        try:
            name= request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            speciality=request.form.get('speciality')
            exper = request.form.get('experience')
            competition = request.form.get('participated_in_any_competition')
            fee = request.form.get('consult_fee')
            contact = request.form.get('mobile_number')
            emailCheck = email.split('@')
            if len(emailCheck) == 1:
                return Response(response=render_template('registerAsTrainer.html',error="Please Enter Valid syntax of Email."))
            if emailCheck[1] !="gmail.com" and emailCheck[1]!="yahoo.com" and emailCheck[1]!='hotmail.com':
                return Response(response=render_template('registerAsTrainer.html',error="INVALID Email."))
            if len(password)<8:
                return Response(response=render_template('registerAsTrainer.html',error="Password Length is too short."))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = trainerDbHandler(dbConfig['host'],dbConfig['user'],dbConfig['password'],dbConfig['database'])
            trainer = Trainer(name,email,password,speciality,exper,competition,fee,contact)
            status = obj.signUpAsTrainer(trainer)
            if status != True:
                return Response(response=render_template('registerAsTrainer.html',error=status))
            session['email']=email
            session['password'] = password
            return Response(response=render_template('loginAsTrainer.html'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))


class trainerImages(Resource):
    def post(self):
        try:
            email = session.get('email')
            f = request.files['imageFile']
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = trainerDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            status = obj.addPicture(email,duplicateApp.config['UPLOADED_IMAGE']+'/trainerImages/'+secure_filename(f.filename))
            name = email.split('@')
            f.save(os.path.join(duplicateApp.config['ABSOLUTE_PATH']+'/trainerImages', secure_filename(f.filename)))
            return Response(response=render_template('trainerPicture.html',error=name[0]+' Your picture has successfully added.'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))

class trainerVideos(Resource):
    def post(self):
        try:
            email = session.get('email')
            f = request.files['videoFile']
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            obj = trainerDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            status = obj.addVideo(email,duplicateApp.config['UPLOADED_IMAGE']+'/trainerVideos/'+secure_filename(f.filename))
            name = email.split('@')
            f.save(os.path.join(duplicateApp.config['ABSOLUTE_PATH']+'/trainerVideos', secure_filename(f.filename)))
            return Response(response=render_template('trainerPicture.html',error=name[0]+' Your video has successfully added.'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))

class selectTrainer(Resource):
    def get(self,email):
        try:
            if email is None:
                return {'msg': "Email not Found."}
            dbConfig = dbDictionary(duplicateApp)
            obj = traineeDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            status = obj.selectTrainer(session.get('username'),email)
            if bool(status) == False:
                return {'msg': status}
            return {'msg': status}
        except Exception as e:
            print(str(e))

class getTrainer(Resource):
    def get(self,email):
        try:
            print(email)
            username = session.get('username')
            if username is None:
                return Response(response=render_template('loginAsTrainee.html', error="Pleases Login First."))
            dbConfig = dbDictionary(duplicateApp)
            obj = adminDbHandler(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            data = obj.displayOneTrainer(email)
            global trainerData
            trainerData = data
            return trainerData
        except Exception as e:
            print(str(e))


class equipmentsApi(Resource):
    def get(self):
        # try:
        # temp=equipments.objects().to_json()
        # return Response(temp,mimetype='application/json',status=200)
        # except Exception as e:
        # return Response(str(e),mimetype='application/json',status=200)
        body = equipments.objects()
        return Response(body.to_json(), mimetype='application/json', status=200)

    def post(self):
        try:
            name = request.form.get('name')
            quantity = request.form.get('quantity')
            f = request.files['imageUrl']
            price = request.form.get('price')
            weight = request.form.get('weight')
            imgUrl = duplicateApp.config['UPLOADED_IMAGE'] + '/equipmentsPicture/' + secure_filename(f.filename)
            status = equipments(name=name, quantity=quantity, imageUrl=imgUrl, price=price, weight=weight).save()
            print(status.id)
            f.save(
                os.path.join(duplicateApp.config['ABSOLUTE_PATH'] + '/equipmentsPicture', secure_filename(f.filename)))
            return {'mssg': "Successfully Added."}, 200
        except Exception as e:
            return Response(str(e), mimetype='application/json', status=200)


class getEquipments(Resource):
    def get(self):
        try:
            temp = equipments.objects()
            myDic = {}
            myList = []
            for item in temp:
                myDic.update(name=item.name)
                myDic.update(quantity=item.quantity)
                myDic.update(imageUrl=item.imageUrl)
                myDic.update(price=item.price)
                myDic.update(weight=item.weight)
                myList.append(myDic)
                myDic = {}
            return myList
        except:
            return {'msg': "Not Found."}


class getFoodSupplements(Resource):
    def get(self):
        try:
            temp = foodSuplements.objects()
            myDic = {}
            myList = []
            for item in temp:
                myDic.update(name=item.name)
                myDic.update(quantity=item.quantity)
                myDic.update(imageUrl=item.imageUrl)
                myDic.update(price=item.price)
                myList.append(myDic)
                myDic = {}
            return myList
        except:
            return {'msg': "Not Found."}


class placeorderEquipments(Resource):
    def put(self, orderName):
        try:
            oldData = request.get_json()
            print("oldData",oldData)
            for item in oldData:
                print("item",item)
                updated_Data = equipments.objects.get(name=item)
                updated_Data.quantity =str(int(updated_Data.quantity) -1)
                i = equipments.objects.get(name=item)
                i.update(quantity=updated_Data.quantity)

            return "Your Order will recieve in 5 working days."
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)

class placeorderFoodSupplements(Resource):
    def put(self, orderName):
        try:
            oldData = request.get_json()
            print("oldData",oldData)
            for item in oldData:
                print("item",item)
                updated_Data = foodSuplements.objects.get(name=item)
                updated_Data.quantity =str(int(updated_Data.quantity) -1)
                i = foodSuplements.objects.get(name=item)
                i.update(quantity=updated_Data.quantity)
            return "Your Order will recieve in 5 working days."
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)
class equipmentApi(Resource):
    def get(self, name):
        try:
            temp = equipments.objects().get(name=name).to_json()
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)
        return Response(temp, mimetype='application/json', status=200)

    def put(self, name):
        try:
            temp = request.get_json()
            t = equipments.objects().get(name=name).update(**temp)
            return {"msg ": "updated."}, 200
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)

    def delete(self, name):
        # try:
        print(name)
        obj = equipments.objects().get(name=name).delete()
        print(obj)
        return {'msg': "deleted"}
        # except:
        return Response("Not found", mimetype='application/json', status=200)


class foodSuplementsApi(Resource):
    def get(self):
        try:
            temp = foodSuplements.objects().to_json()
            return Response(temp, mimetype='application/json', status=200)
        except Exception as e:
            return print(str(e))

    def post(self):
        try:
            name = request.form.get('name')
            quantity = request.form.get('quantity')
            f = request.files['imageUrl']
            price = request.form.get('price')

            imgUrl = duplicateApp.config['UPLOADED_IMAGE'] + '/foodsupplementsPicture/' + secure_filename(f.filename)
            status = foodSuplements(name=name, quantity=quantity, imageUrl=imgUrl, price=price).save()
            print(status.id)
            f.save(os.path.join(duplicateApp.config['ABSOLUTE_PATH'] + '/foodsupplementsPicture',
                                secure_filename(f.filename)))
            return {'mssg': "Successfully Added."}, 200
        except Exception as e:
            return Response(str(e), mimetype='application/json', status=200)

    '''def put(self):
        temp=request.get_json()
        t=student.objects().update(**temp)
        return { "id ": "updated" },200
    def delete(self):
        student.objects().delete()
        return "deleted Successfully"
        '''


class foodSuplementApi(Resource):
    def get(self, name):
        try:
            temp = foodSuplements.objects().get(name=name).to_json()
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)

    def put(self, name):
        try:
            temp = request.get_json()
            t = foodSuplements.objects().get(name=name).update(**temp)
            return {"msg ": "updated."}, 200
        except:
            return Response(str("Not found"), mimetype='application/json', status=200)

    def delete(self, name):
        try:
            foodSuplements.objects(name=name).delete()
            return {'msg': "deleted"}
        except:
            return Response("Not found", mimetype='application/json', status=200)
