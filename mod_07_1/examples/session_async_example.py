"""
ASYNC SESSION
"""
import asyncio
from sqlalchemy import create_engine, Column,Integer, String, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker    
from sqlalchemy.orm import relationship, declarative_base, sessionmaker




engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
AsyncDBSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

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

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_models()
    async with AsyncDBSession() as session:
        new_user = User(fullname='Oleksandr Druzhko')
        session.add(new_user)
        new_address = Address(user_email='abc@mail.ua', user=new_user)
        session.add(new_address)
        await session.commit()

        new_user = User(fullname='Denys Gupalo')
        session.add(new_user)
        new_address = Address(user_email='den@mail.ua', user=new_user)
        session.add(new_address)
        await session.commit()

        u = session.execute(select(User))
        r_u = u.scalars_one().all()
        for u in r_u:
            print(u.id, u.fullname)

        await session.close()

    # adrs = session.execute(select(Address)).join(Address.user).scalars().all()
    # print(adrs)                                         # --> [<__main__.Address object at 0x7f23d3d17750>]
    # for a in adrs:
    #     print(a.id, a.user_email, a.user.fullname)      #--> 1 abc@mail.ua Oleksandr Druzhko

if __name__ == '__main__':
    asyncio.run(main())
