from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ ='user'

    username = Column(String(80),nullable = False)
    password = Column(String(10),nullable = False)

    id = Column(Integer,primary_key = True)

class LoginSessions(Base):
    __tablename__ = 'login_session'
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    id = Column(Integer,primary_key = True)


class Restaurant(Base):

    __tablename__ = 'restaurant'

    name = Column(
            String(80),nullable = False)

    id = Column(
            Integer,primary_key = True)

class MenuItem(Base):

    __tablename__ = 'menu_item'

    name = Column(
            String(80),nullable = False)

    id = Column(
            Integer,primary_key = True)

    description = Column(String(250))

    price = Column(String(8))

    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)



# Insert at the end of file for engine
engine = create_engine(
        'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
