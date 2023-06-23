from datetime import datetime
from ..utils import db
from ..model.users import User

class Url(db.Model):
    __tablename__ = 'urls'
    id =db.Column(db.Integer(), primary_key=True)
    original_url=db.Column(db.String(500), nullable=False)
    shortened_url=db.Column(db.String(50), nullable=False,unique=True)
    no_of_clicks = db.Column(db.Integer, default=0)
    date_created =db.Column(db.DateTime, default=datetime.now)
    user_id=db.Column(db.Integer(), db.ForeignKey('users.id'),nullable=True)
    
  
    
    def __repr__(self):
        return f"<Url {self.id}>"

    #Add new url every time a request is made
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    @classmethod
    def get_total_clicks(cls,id):
        urls= Url.query.filter_by(user_id=id).count()
    @classmethod
    def get_total_URL(cls,id):
        urls= Url.query.filter_by(user_id=id).count()
        return urls
    @classmethod
    def check_urls(cls,url):
        is_exist = cls.query.filter_by(shortened_url=url).first()
        return True if is_exist else False
    @classmethod
    def get_url_by_user(cls, user_id):
        urls = Url.query.join(User).filter(User.id == user_id).all()
        return urls

    #     students = Used
    # r.query.join(Url).filter(Course.id == course_id).all()
    #     return students
    # # @classmethod
    # def get_total_clicks(cls,id):
    #     cls= cls.query.filter_by(shortened_url=shortened_url).count()    
    
        
        


   

   
