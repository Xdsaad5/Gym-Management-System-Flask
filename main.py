from flask import Flask,request,render_template,Response,session
from flask_restful import Api,Resource
from flask_session import Session
from resources import routes,resources
from database import db
from database.DbHandlerClasses import adminDbHandler,traineeDbHandler,trainee
import random
import smtplib as s
import os
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.secret_key=app.config['SECRET_KEY']
app.config["MONGODB_SETTINGS"]
db.initialize_db(app)
api = Api(app) #instansiate api's
routes.initialize_routes(api) #initialize routes
resources.copyAppInstance(app) #coppying app instance in resource.py for db configurations
actualOtp=0
file =None
@app.route('/')
def homePage():
    return render_template("home.html")
@app.route('/loginAsAdmin')
def loginAsAdmin():
    return render_template("loginAsAdmin.html")
@app.route('/loginAsTrainer')
def loginAsTrainer():
    return render_template("loginAsTrainer.html")
@app.route('/registerAsTrainer')
def registerAsTrainer():
    return render_template("registerAsTrainer.html")
@app.route('/loginAsTrainee')
def loginAsTrainee():
    return render_template("loginAsTrainee.html")
def sendEmail(email,userOtp):
    print("userotp",userOtp)
    ob = s.SMTP('smtp.gmail.com', 587)
    ob.ehlo()
    ob.starttls()
    ob.login(app.config['SENDER_EMAIL'], app.config['SENDER_PASSWORD'])
    subject = "OTP"
    body = "Your otp is "+str(userOtp)
    message = "subject:{}\n\n{}".format(subject, body)
    ob.sendmail(app.config['SENDER_EMAIL'], email, message)
    ob.quit()
    global actualOtp
    actualOtp=userOtp
    return True
@app.route('/registerTrainee')
def register():
    return render_template("registerAsTrainee.html")
@app.route('/registerAsTrainee',methods=['POST'])
def registerAsTrainee():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    contact = request.form.get('mobile_number')
    gender = request.form.get('gender')
    f = request.files['imageFile']
    global file
    file = f
    insertImgStatus = str(f).split('.')
    print('username ' + username)
    emailCheck = email.split('@')
    if len(emailCheck) == 1:
        return Response(response=render_template('registerAsTrainee.html', error="Please Enter Valid syntax of Email."))
    if emailCheck[1] != "gmail.com" and emailCheck[1] != "yahoo.com" and emailCheck[1] != 'hotmail.com':
        return Response(response=render_template('registerAsTrainee.html', error="INVALID Email."))
    if len(password) < 8:
        return Response(response=render_template('registerAsTrainee.html', error="Password Length is too short."))
    if len(contact) < 10 or len(contact) > 11:
        return Response(
            response=render_template('registerAsTrainee.html', error="Length of phone number is too short."))
    if int(age) < 1:
        return Response(response=render_template('registerAsTrainee.html', error="Enter valid age."))
    sendEmail(email,random.randint(1000,9999))
    session['username']=username
    session['email']=email
    session['password']=password
    session['age']=age
    session['contact']=contact
    session['gender']=gender
    session['imageUrl'] =  app.config['UPLOADED_IMAGE']+'/images'+f.filename
    f.save(os.path.join(app.config['ABSOLUTE_PATH'] + '/images', f.filename))
    return render_template("getOtp.html")
@app.route('/getOtp',methods=['POST'])
def getOtp():
    username = session.get('username')
    if username is None:
        return render_template("loginAsTrainee.html",error="Please Login or register first.")
    enteredOtp = request.form['otp']
    global actualOtp
    print(actualOtp)
    print(enteredOtp)
    if int(enteredOtp) != actualOtp:
        print("In otp if")
        return render_template("registerAsTrainee.html",error="Please Enter valid OTP.")
    username=session.get('username')
    email=session.get('email')
    password = session.get('password')
    age = session.get('age')
    contact = session.get('contact')
    gender = session.get('gender')
    imageUrl = session.get('imageUrl')
    session.clear()
    traineeObj = trainee(username, email, password, int(age), contact, gender, imageUrl)
    obj = traineeDbHandler(app.config['HOST'],app.config['USER'],app.config['PASSWORD'],app.config['DATABASE'])
    status = obj.signUpTrainee(traineeObj)
    if status != True:
        return render_template('registerAsTrainee.html', error="User Already Exist.")
    session['username'] = username
    return render_template("traineeHome.html")

@app.route('/adminHome')
def adminHome():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template("adminHome.html")
@app.route('/removeTrainer')
def removeTrainer():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template("removeTrainer.html")
@app.route('/removeTrainee')
def removeTrainee():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template("removeTrainee.html")
@app.route('/displayTrainee')
def displayTrainee():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    obj = adminDbHandler(app.config['HOST'],app.config['USER'],app.config['PASSWORD'],app.config['DATABASE'])
    data = obj.displayTrainee()
    if bool(data) == False:
        return Response(response=render_template('adminHome.html', error="No Trainee Found."))
    print(data)
    return render_template('displayTrainee.html',data=data)
@app.route('/displayTrainer')
def displayTrainer():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template('displayTrainer.html')
@app.route('/logoutAdmin')
def adminLogout():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    session.clear()
    return Response(response=render_template('home.html'))

@app.route("/trainerHome")
def trainerHome():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return render_template('loginAsTrainer.html',error='Please Login or register first.')
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) == True:
        return Response(response=render_template('adminHome.html'))

    name = email.split('@')
    print(name[0])
    return render_template('trainerHome.html',welcome='Welcome '+name[0])
@app.route("/addPicture")
def addPicture():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return render_template('loginAsTrainer.html',error='Please Login or register first.')
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    print(status)
    if bool(status) == True:
        return Response(response=render_template('adminHome.html'))

    name = email.split('@')
    return render_template('trainerPicture.html',error=name[0]+' Please add Your Picture.')
@app.route("/addVideo")
def addVideo():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return render_template('loginAsTrainer.html',error='Please Login or register first.')
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) == True:
        return Response(response=render_template('adminHome.html'))
    name = email.split('@')
    return render_template('trainerVideo.html',error=name[0]+' Please add Your Video.')

@app.route("/logoutTrainer")
def trainerLogout():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsTrainer.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'],app.config['USER'],app.config['PASSWORD'],app.config['DATABASE'])
    status = obj.verifyAdmin(email,password)
    print(status)
    if status == True:
        return Response(response=render_template('adminHome.html'))
    session.clear()
    return Response(response=render_template('home.html'))
@app.route('/traineeHome')
def traineeHome():
    username = session.get('username')
    if username is None:
        return Response(response=render_template('loginAsTrainee.html', error="Pleases Login First."))
    return Response(response=render_template('traineeHome.html',Welcome="Welcome"))
@app.route('/showTrainer')
def showTrainer():
    username = session .get('username')
    if username is None:
        return Response(response=render_template('loginAsTrainee.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'],app.config['USER'],app.config['PASSWORD'],app.config['DATABASE'])
    data = obj.displayTrainer(True)
    print("data",data)
    return Response(response=render_template('showTrainer.html',data=data))
@app.route('/selectTrainer')
def selectTrainer():
    username = session .get('username')
    if username is None:
        return Response(response=render_template('loginAsTrainee.html', error="Pleases Login First."))
    data = resources.trainerData
    print("select Trainer", data)
    resources.trainerData = None
    return Response(response=render_template('selectTrainer.html',data=data))
@app.route("/logoutTrainee")
def traineeLogout():
    username = session.get('username')
    if username is None:
        return Response(response=render_template('loginAsTrainer.html', error="Pleases Login First."))

    session.clear()
    return Response(response=render_template('home.html'))
@app.route('/contactus')
def contactUs():
    return render_template("contactus.html")
@app.route('/features')
def features():
    return render_template("features.html")
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/about us')
def about():
    return render_template("about us.html")


#E-COMMERECE;
@app.route('/addEquipments')
def addEquipments():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template("addequipments.html")
@app.route('/addFoodSupplements')
def addfoodSupplements():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    return render_template("addFoodSupplements.html")
@app.route('/displayEquipments')
def displayequipments():
    return render_template("showEquipments.html")
@app.route('/displayFoodSupplements')
def displayfoodSupplements():
    return render_template("showfoodsupplements.html")

@app.route('/deleteEquipments')
def deleteEquipments():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    data = resources.getEquipments().get()
    print(data)
    return render_template('deleteEquipments.html',data=data)

@app.route('/deleteFoodSupplements')
def deleteFoodSupplements():
    email = session.get('email')
    password = session.get('password')
    if email is None:
        return Response(response=render_template('loginAsAdmin.html', error="Pleases Login First."))
    obj = adminDbHandler(app.config['HOST'], app.config['USER'], app.config['PASSWORD'], app.config['DATABASE'])
    status = obj.verifyAdmin(email, password)
    if bool(status) != True:
        return Response(response=render_template('trainerHome.html'))
    data = resources.getFoodSupplements().get()
    print(data)
    return render_template('deleteFoodSupplements.html',data=data)




@app.route('/orderEquipments')
def orderEquipment():
    username = session.get('username')
    if username is None:
        return render_template("loginAsTrainee.html",error="Please Login or register first.")

    data=resources.getEquipments().get()
    print(data)
    return render_template('orderEquipments.html',data=data)

@app.route('/orderFoodSupplements')
def orderFoodSupplements():
    username = session.get('username')
    if username is None:
        return render_template("loginAsTrainee.html",error="Please Login or register first.")

    data=resources.getFoodSupplements().get()
    return render_template('orderFoodSupplements.html',data=data)
app.run()