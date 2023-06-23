from flask import request,redirect
from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..utils import db
import validators
import string
import random
from ..model.users import User
from ..model.url import Url
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus


url_namespace =Namespace("url" , description="name space for urls")
url_create_model = url_namespace.model(
    'Url',{
        
        "original_url":fields.String(required=True, description= "original_url")
  
    }
)
url_model = url_namespace.model(
    'Url',{
        
        "original_url":fields.String(required=True, description= "original_url"),
        "no_of_clicks" :fields.Integer(required=True, description= "number of clicks on the url"),
        "shortened_url":fields.String(required=True, description= "shortened_url"),
        "date_created":fields.DateTime()
  
    }
)

#url function to shorten url
def generate_short_code(length=6):
    characters= string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

urls ={}

@url_namespace.route('/shorten')
class GenerateValidateShortUrlView(Resource):
    @url_namespace.expect(url_create_model, validate=True)
    @url_namespace.doc(description='Validate url')
    @url_namespace.marshal_with(url_model)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        authenticated_user = User.query.filter_by(email=current_user).first()
        if not authenticated_user:
            return {
                'message':'No record found.'
            }, HTTPStatus.NOT_FOUND
            
        data = request.get_json()
        original_url = data.get('original_url')
        if not validators.url(original_url):
            response= {
                'message':'Invalid URL'
            }
            return response ,HTTPStatus.BAD_REQUEST
        short_code = generate_short_code()
        shortened_url= request.host_url + short_code
        
        url = Url(
            original_url = original_url,
            shortened_url = shortened_url
        )   
        try:
            url.save()    
        except:
            db.session.rollback()
            response = {
                'message': 'An unexpected error occurred'
            }
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
        return url,HTTPStatus.OK
    
@url_namespace.route('/urls')
class GetAllLongShortUrlView(Resource):
    @url_namespace.doc(description='retrieve all URL')
    @url_namespace.marshal_with(url_model)
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        authenticated_user = User.query.filter_by(email=current_user).first()
        if not authenticated_user:
            return {
                'message':'No record found.'
            }, HTTPStatus.NOT_FOUND
        user_url = authenticated_user.url
        return user_url, HTTPStatus.OK
        
        
       
      
@url_namespace.route('/urls/<int:url_id>')
class DeleteLongShortUrlView(Resource):
    @url_namespace.doc(
        description='delete a url by id'
    )
    @jwt_required() 
    def delete(self,url_id):
        current_user = get_jwt_identity()
        authenticated_user = User.query.filter_by(email=current_user).first()
        if not authenticated_user:
            return {
                'message':'No record found.'
            }, HTTPStatus.NOT_FOUND
    
        #delete url by id
        url_to_delete = Url.get_by_id(url_id)
        url_to_delete.delete()
        return {'message': "Url Deleted successfully"},HTTPStatus.NO_CONTENT
@url_namespace.route('/clicks/<shortened_url>')
class GetShortUrlClicksView(Resource):
    @url_namespace.doc(
        description='Get a  short url clicks by id'
    )
    @url_namespace.marshal_with(url_model)
    @jwt_required() 
    def get(self,shortened_url):
        current_user = get_jwt_identity()
        authenticated_user = User.query.filter_by(email=current_user).first()
        if not authenticated_user:
            return {
                'message':'No record found.'
            }, HTTPStatus.NOT_FOUND
        if shortened_url in urls:
            urls[shortened_url]['no_of_clicks'] +=1
            no_of_clicks = urls[shortened_url][no_of_clicks]
            return {
                'no_of_clicks' :no_of_clicks
            }, HTTPStatus.OK
           
        else:
            return{
                'error':'Invalid Url'
            }, HTTPStatus.NOT_FOUND
    
        
       
