from flask import request,session
from flask_restx import Namespace,Resource,fields
from ..utils import db
from ..model.users import User
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,unset_jwt_cookies,get_jwt
import validators

auth_namespace =Namespace("auth" , description="name space for authentication")
user_signup_model = auth_namespace.model(
    'Signup',{
        
        "name":fields.String(required=True, description= "A name"),
        "username": fields.String(required=True, description= "A username"),
        "password": fields.String(required=True, description= "A password for admin"),
        "email": fields.String(required=True, description= "An email for admin"),
  
    }
)
user_model = auth_namespace.model(
    'User',{
        "id": fields.Integer(),
        "name":fields.String(description= "A name"),
        "username": fields.String( description= "A username"),
        "email": fields.String( description= "An email"),
        "password_hash": fields.String(description= "A password"),
       
       
       
    }        
) 

    
@auth_namespace.route('/register/user')
class SignupUserView(Resource):
    
    @auth_namespace.expect(user_signup_model, validate=True)
    @auth_namespace.marshal_with(user_model)#marshal_with return json rather than object in db we use it to serialise
    @auth_namespace.doc(
        description="Sign up a user"
    )
    def post(self):
        """
        Sign up a user
        
        """
         
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            response = {'Message':'User with this email already exists'}
            return response,HTTPStatus.CONFLICT
       
        
        new_user = User(
         
                email = data.get('email'),
                name = data.get('name'),
                username=data.get('username'),
                password_hash = generate_password_hash(data.get('password')),
                
            )
        try:
            
            new_user.save()
        except:
            db.session.rollback()
            response ={'Message':'Unexpected error occurred while saving'}
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
      
        return new_user,HTTPStatus.CREATED       
#login model serialiser       
login_model = auth_namespace.model(
    'Login',{
       
        "email": fields.String(required=True, description= "email"),
        "password": fields.String(required=True, description= "A password")
  
        
        
    }
) 
 
@auth_namespace.route('/login')
@auth_namespace.expect(login_model)
@auth_namespace.doc(description='Token required')
class LoginUserView(Resource):
    def post(self):
        """
        Login an user  and Generate token
        
        """
        
       
        data= request.get_json()
        email=data.get('email')
        password=data.get('password')
        
        #checks if in the database if for instance ovaj@gmail.com exixts in our dable it grabs the whole info about that note emailmis set to be unique
        user = User.query.filter_by(email=email).first()
     
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity= user.email)
            refresh_token = create_refresh_token(identity= user.email)  
            
            
            response ={
                
                'access_token':access_token,
                'refresh_token':refresh_token,
                'message':'logged in successfully',
                
            }
        else:
            response={
                'message':'Oops incorrect password'
            }
            return response,HTTPStatus.BAD_REQUEST
        return response, HTTPStatus.CREATED
@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
        Logout a User
       
        """
        unset_jwt_cookies
        db.session.commit()
        return {"message":"Logged out successfully"},HTTPStatus.OK
#delete user account by user
@auth_namespace.route('')
class DeleteUserAccountView(Resource):
    @auth_namespace.doc(description='delete a user by id',
    params ={
        'user_id':'User Id'
    })
    @jwt_required()
    def delete(self):
        """
        delete a user by ID
        
        """
        current_user = get_jwt_identity()
        authenticated_user = User.query.filter_by(email=current_user).first()
        if not authenticated_user or authenticated_user is None:
            return {
                'message':'User does not exists. '
            }, HTTPStatus.NOT_FOUND
        authenticated_user.delete()
        try:
           db.session.commit()
        except:
            db.session.rollback()
        return {'message':'User accounts has successfully been deleted'},HTTPStatus.OK
#it refreshes and return a username  and our authentication endpoint     
@auth_namespace.route('/refresh')
class Refresh(Resource):    
    @jwt_required(refresh=True)
    def post(self):
        """
        refresh token
       
        """
        username =get_jwt_identity()
        
        access_token = create_access_token(identity=username)
        
        return{"access_token":access_token }, HTTPStatus.OK
