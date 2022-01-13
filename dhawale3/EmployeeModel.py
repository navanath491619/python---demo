from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class EmployeeModel(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    gender= db.Column(db.Integer())
    age = db.Column(db.Integer())
    mobile = db.Column(db.String(80))
 
    def __init__(self, employee_id,name,gender,age,mobile):
        self.employee_id = employee_id
        self.name = name
        self.gender = gender
        self.age = age
        self.mobile = mobile
 
    def __repr__(self):
        return f"{self.name}:{self.employee_id}"
