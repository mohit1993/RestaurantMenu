from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant,MenuItem,User,LoginSessions

engine = create_engine('sqlite:///restaurantmenu.db')
dbsession = sessionmaker(bind = engine)

session = dbsession()


