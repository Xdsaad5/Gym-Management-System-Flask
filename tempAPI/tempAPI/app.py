# from flask import Flask,render_template
# from flask_restful import Api
# from database import db
# from Resource import routes
# app=Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {
#     'host':"mongodb://localhost:27017/raza" }
# api =Api(app)
# db.initialize_db(app)
# routes.initialize_routes(api)
# @app.route('/')
# def main():
#     return 'Hello World!'
# if __name__ == '__main__':
#    app.run(debug=True)
'''from flask import Flask,request,render_template
from flask_restful import Api,Resource
from database import db
from Resource import routes,resources
app=Flask(__name__)
app.config.from_pyfile("config.py")
app.secret_key=app.config['SECRET_KEY']
app.config["MONGODB_SETTINGS"]
api=Api(app)
db.initialize_db(app)
resources.copyAppInstance(app)
routes.initialize_routes(api)
@app.route('/')
def home():
    return render_template("addequipments")
@app.route('/addfood')
def addfood():
    return render_template("addfood.html")
@app.route('/displayequipments')
def displayequipments():
    return render_template("showEquipments.html")
@app.route('/displayfood')
def displayfood():
    return render_template("showfoodsupplements.html")

@app.route('/deleteequipment')
def deleteEquipments():
    data = resources.getEquipments().get()
    print(data)
    return render_template('deleteequipments.html',data=data)

@app.route('/deleteFoodSupplements')
def deleteFoodSupplements():
    data = resources.getFoodSupplements().get()
    print(data)
    return render_template('deleteFoodSupplements.html',data=data)

@app.route('/test')
def test():
    return render_template('temp.html')

@app.route('/userInterface')
def userInterface():
    return render_template('userInterface.html')

@app.route('/orderEquipment')
def orderEquipment():
    data=resources.getEquipments().get()
    print(data)
    return render_template('orderEquipments.html',data=data)

@app.route('/orderFoodSupplements')
def orderFoodSupplements():
    data=resources.getFoodSupplements().get()
    return render_template('orderFoodSupplements.html',data=data)

app.run(debug=True)
'''