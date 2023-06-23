from flask import request,redirect,url_for
from flask_restx import Namespace,Resource,fields
from ..utils import db
import validators
import string
import random
from ..model.url import Url
from http import HTTPStatus


demo_namespace =Namespace("demo" , description="name space for demonstration for unsigned user")
demo_create_model = demo_namespace.model(
    'Url',{
        
        "original_url":fields.String(required=True, description= "original_url"),
       
  
    }
)
demo_model = demo_namespace.model(
    'Url',{
        
      
        "shortened_url":fields.String(required=True, description= "shortened_url"),
        
  
    }
)

#url function to shorten url
def generate_short_code(length=6):
    characters= string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

urls ={}

@demo_namespace.route('/trial')
class GenerateValidateShortUrlView(Resource):
    @demo_namespace.expect(demo_create_model, validate=True)
    @demo_namespace.doc(description='Validate url')
    @demo_namespace.marshal_with(demo_model)
    def post(self):
        data = request.get_json()
        original_url = data.get('original_url')
        if not validators.url(original_url):
            response= {
                'message':'Invalid URL'
            }
            return response ,HTTPStatus.BAD_REQUEST
        short_code = generate_short_code()
        shortened_url= request.host_url + short_code
        return shortened_url
        # url = Url(
        #     original_url = original_url,
        #     shortened_url = shortened_url
        # )   
        # try:
        #     url.save()    
        # except:
        #     db.session.rollback()
        #     response = {
        #         'message': 'An unexpected error occurred'
        #     }
        #     return response, HTTPStatus.INTERNAL_SERVER_ERROR
        # return url,HTTPStatus.OK
    
