from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#*******************************************USER***************************************************

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "is_active" : True
            # do not serialize the password, its a security breach
        }
    
#*******************************************COMPANY****************************************************

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nif = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    web = db.Column(db.String(120), unique=True, nullable=False)
    certificate = db.Column(db.String(120), nullable=True)


    def __init__(self,nif,name,sector,address,email,description,web,certificate):
        self.nif = nif
        self.name = name
        self.sector = sector
        self.address = address
        self.email = email
        self.description = description
        self.web = web
        self.certificate = certificate
        

    def __repr__(self):
        return f'<Company {self.name}>'

    def serialize(self):
        return {
            "nif": self.nif,
            "name": self.name,
            "sector": self.sector,
            "address": self.address,
            "email": self.email,
            "description": self.description,
            "web": self.web,
            "certificate": self.certificate,
            
        }
    
#***********************************FAVORITES***********************************************
