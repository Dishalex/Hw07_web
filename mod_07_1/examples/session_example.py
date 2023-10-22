"""
Session
"""
from sqlalchemy import create_engine, Table, Column,Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)

class Address(Base):
    __tablename__ = 'addreses'
    id = Column(Integer, primary_key=True)
    user_email = Column(String(130), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

Base.metadata.create_all(engine)



if __name__ == '__main__':
    new_user = User(fullname='Oleksandr Druzhko')
    session.add(new_user)
    new_address = Address(user_email='abc@mail.ua', user=new_user)
    session.add(new_address)
    session.commit()

    u = session.query(User).first()
    print(u.id, u.fullname)

    adrs = session.query(Address).join(Address.user).all()
    print(adrs)                                         # --> [<__main__.Address object at 0x7f23d3d17750>]
    for a in adrs:
        print(a.id, a.user_email, a.user.fullname)      #--> 1 abc@mail.ua Oleksandr Druzhko

    session.close()


