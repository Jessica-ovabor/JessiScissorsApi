
from ..utils import db

class User(db.Model):
    __tablename__ = 'users'
    id =db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(50), nullable=False,unique=True)
    username=db.Column(db.String(50), nullable=False,unique=True)
    email =db.Column(db.String(50), nullable=False,unique=True)
    password_hash =db.Column(db.Text(), nullable=False)
    url=db.relationship('Url',backref='user',lazy=True)#every user to its url
  
    
    def __repr__(self):
        return f"<User {self.username}>"

    #Add new user every time a request is made
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


   

   
