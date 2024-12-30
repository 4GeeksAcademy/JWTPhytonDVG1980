"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Company
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import re
import bcrypt

def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register_user():
    body = request.get_json()
    name = body.get('name', None)
    email = body.get('email', None)
    password = body.get('password', None)
    if name is None or email is None or password is None:
        return {'message': 'Missing arguments'}      
    bpassword = bytes(password, 'utf-8')
    salt = bcrypt.gensalt(14)
    hashed_password = bcrypt.hashpw(password=bpassword, salt=salt)       
    user = User(name, email,hashed_password.decode('utf-8'))    
    #return {'message': f'name: {user.name} email: {user.email} password: {password}'}
    db.session.add(user)
    db.session.commit()
    return {'message': f'User {user.email} was created'}

@api.route('/token', methods=['POST'])
def create_token():
    body = request.get_json()
    email = body.get('email', None)
    password = body.get('password', None)
    if password is None or email is None:
        return {'message': f'missing parameters {email} {password}', 'authorize': False}, 400
    if check(email) is not True:
        return {'message': 'email is not valid', 'authorize': False}, 400
    user = User.query.filter_by(email=email).one_or_none()    
    if user is None:
        return {'mesasge': 'User doesnt exist', 'authorize': False}, 400
    password_byte =bytes(password, 'utf-8')
    if bcrypt.checkpw(password_byte, user.password.encode('utf-8')):
        return {'token': create_access_token(identity = email), 'authorize': True},200
    return {'message': 'Unauthorized', 'authorize': False}, 401
       

# *************************************USER********************************************

@api.route('/profile/user')
@jwt_required()
def validate_user():
    email = get_jwt_identity()    
    user = User.query.filter_by(email=email).one_or_none()
    if user is None:
        return {'message': 'Unauthorized'}, 401
    return user.serialize(), 200
    
# **************************************COMPANY*******************************************

@api.route('/companies', methods=['GET'])
def get_companies():
    """Obtiene todas las compañías"""
    companies = Company.query.all()
    companies_serialized = [company.serialize() for company in companies]
    return jsonify(companies_serialized), 200


@api.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Obtiene una compañía por ID"""
    company = Company.query.get(company_id)
    if company is None:
        return jsonify({"message": "Company not found"}), 404
    return jsonify(company.serialize()), 200


@api.route('/companies', methods=['POST'])
def create_company():
    """Crea una nueva compañía"""
    body = request.get_json()
    nif = body.get('nif', None)
    name = body.get('name', None)
    sector = body.get('sector', None)
    address = body.get('address', None)
   
    
    if not nif or not name or not address:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Verificar si ya existe una compañía con el mismo NIF
    existing_company = Company.query.filter_by(nif=nif).first()
    if existing_company:
        return jsonify({"message": "Company with this NIF already exists"}), 400

    company = Company(nif=nif, name=name, adress=adress)
    db.session.add(company)
    db.session.commit()
    return jsonify(company.serialize()), 201


@api.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """Actualiza los datos de una compañía existente"""
    body = request.get_json()
    company = Company.query.get(company_id)
    
    if company is None:
        return jsonify({"message": "Company not found"}), 404

    company.nif = body.get('nif', company.nif)
    company.name = body.get('name', company.name)
    company.address = body.get('address', company.adress)
    

    db.session.commit()
    return jsonify(company.serialize()), 200


@api.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Elimina una compañía por ID"""
    company = Company.query.get(company_id)
    if company is None:
        return jsonify({"message": "Company not found"}), 404

    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": f"Company {company_id} deleted"}), 200

# *************************************FAVORITES******************************************

# **************************************RATINGS*******************************************

# ************************************TYPESERVICES****************************************


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200