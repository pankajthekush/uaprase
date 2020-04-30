#import local methods
from shelp import copy_file_to
from shelp import pgconnstring

#import sqlachemy data
from sqlalchemy import MetaData
from sqlalchemy import Column,String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#code startsz

Base = declarative_base()

#create engine and session


#user agent class
class UserAgent(Base):
    __tablename__ = 'user_agent_table'
    user_agent = Column(String, primary_key=True)
    browser_name = Column(String)
    browser_version = Column(String)
    os_name = Column(String)
    os_version = Column(String)
    device_name = Column(String)
    device_brand = Column(String)
    device_model = Column(String)
    remarks = Column(String)

#create table


def return_session():
    connection_string = pgconnstring()
    engine = create_engine(connection_string,echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session




if __name__ == "__main__":
    session = return_session()
    new_user_agent = UserAgent(user_agent='test')
    session.merge(new_user_agent)  #user merge inseted of add ,to handle primary, key conflict
    session.commit()


