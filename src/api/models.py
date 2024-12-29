from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nif = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    web = db.Column(db.String(120), unique=True, nullable=True)
    certificate = db.Column(db.String(120), nullable=True)


    def __init__(self,nif, name, adress):
        self.nif = nif
        self.name = name
        self.adress = adress
        

    def __repr__(self):
        return f'<Company {self.name}>'

    def serialize(self):
        return {
            "nif": self.nif,
            "name": self.name,
            "adress": self.adress,
            
        }
