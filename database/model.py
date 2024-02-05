class admin:
    def __init__(self,email,password):
        self.__email=email
        self.__password=password
class Trainer:
    def __init__(self,name,email,password,speciality,experience,paticipateInComp,fee,contact):
        self.name = name
        self.email=email
        self.password=password
        self.speciality=speciality
        self.experience=experience
        self.participated_in_any_competition = paticipateInComp
        self.consult_fee=fee
        self.mobile_number=contact
class trainee:
    def __init__(self,username,email,password,age,contact,gender,fileUrl):
        self.username = username
        self.email=email
        self.password = password
        self.age = age
        self.mobile_number = contact
        self.gender = gender
        self.imgPath = fileUrl

from .db import db
class equipments(db.Document):
    name=db.StringField(required=True)
    quantity=db.StringField()
    imageUrl=db.StringField()
    price=db.StringField()
    weight = db.StringField()

class foodSuplements(db.Document):
    name=db.StringField(required=True)
    quantity=db.StringField()
    imageUrl=db.StringField()
    price=db.StringField()
