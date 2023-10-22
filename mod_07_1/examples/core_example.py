"""
Core
"""
from sqlalchemy import create_engine, Table, Column,Integer, String, ForeignKey, MetaData
from sqlalchemy.sql import select

engine = create_engine('sqlite:///:memory:', echo=False, future=True)
metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('fullname', String),
              )    


addreses = Table('addreses', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String(130), nullable=False, index=True),
              Column('user_id', Integer, ForeignKey('users.id'))
              )    


metadata.create_all(engine)


if __name__ == '__main__':
    with engine.connect() as conn:

        r_user = users.insert().values(fullname='Andriy Dorozhniy')
        print(r_user)                   #-->INSERT INTO users (fullname) VALUES (:fullname)
        result_user = conn.execute(r_user)      
        print(result_user.lastrowid)
        u = conn.execute(select(users))
        print(u.fetchall())


        r_address = addreses.insert().values(email='abc@mail.ua', user_id=result_user.lastrowid)
        print(r_address)                #--> INSERT INTO addreses (email, user_id) VALUES (:email, :user_id)
        conn.execute(r_address)
        a = conn.execute(select(addreses))
        print(a.fetchall())

        # make JOIN
        a_u = select(users.c.fullname, addreses.c.email).select_from(addreses).join(users)
        print(a_u)                  #-->    SELECT users.fullname, addreses.email
                                    #       FROM addreses JOIN users ON users.id = addreses.user_id
        result = conn.execute(a_u)
        print(result.fetchall())