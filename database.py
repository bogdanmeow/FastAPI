from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select, insert, UUID, ForeignKey, Relationship
import uuid
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel

# Нерешённые вопросы:
# - когда необходимо указывать link_model?
# - как указывать link_model, чтобы не выдало ошибки?
# - каких строк кода не хватает?

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    username: str
    email: str
    phone: str

    reserved_link: list['User'] = Relationship(back_populates='user_link', link_model=None) # Добавлять ли link_model? Как это сделать без ощибки?
    reviews_link: list['Review'] = Relationship(back_populates='user_link')

class Room(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(default=None, foreign_key='user.id')
    hotel_id: uuid.UUID = Field(default=None, foreign_key='hotel_id')
    number: str
    floor: str

    user_link: list['User'] = Relationship(back_populates='reserved_link', link_model=None) # Добавлять ли link_model? Как это сделать без ощибки?
    hotel_link: list['Hotel'] = Relationship(back_populates='room_link', link_model=None) # Добавлять ли link_model? Как это сделать без ощибки?

class UserRoomLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, primary_key=True, foreign_key='user.id')
    room_id: uuid.UUID = Field(default=None, primary_key=True, foreign_key='hotel.id')

class Hotel(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    name: str
    city_id: uuid.UUID = Field(default=None, foreign_key='city.id')
    review_id: uuid.UUID = Field(default=None, foreign_key='review.id')
    hotelrating: uuid.UUID = Field(default=None, foreign_key='hoterating.id')

    city_link: list['City'] = Relationship(back_populates='hotel_link', link_model=None) # Указать ли созданную CityHotelLink? - как указать, чтобы не возникало ошибки?
    room_link: list['Hotel'] = Relationship(back_populates='hotel_link', link_model=None)  # Добавлять ли link_model? Как это сделать без ощибки?

class City(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    name: str
    hotel_id: uuid.UUID = Field(foreign_key='hotel.id')

    hotel_link: list['City'] = Relationship(back_populates='city_link', link_model=None) # Указать ли созданную CityHotelLink? - как указать, чтобы не возникало ошибки?

class CityHotelLink(SQLModel, table=True):
    city_id: uuid.UUID = Field(primary_key=True, foreign_key='city.id')
    hotel_id: uuid.UUID = Field(primary_key=True, foreign_key='hotel.id')

class Review(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    hotel_id: uuid.UUID = Field(default=None, foreign_key='hotel.id')
    user_id: uuid.UUID = Field(foreign_key='user.id')
    rating_id: uuid.UUID = Field(foreign_key='rating.id')

    user_link: list['User'] = Relationship(back_populates='reviews_link')

class Rating(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    rating: int

class HotelRating(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    hotelrating: int

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)

user1 = User(id = uuid.uuid4(), description='Данила')
user2 = User(id = uuid.uuid4(), description='Филипп')
user3 = User(id = uuid.uuid4(), description='Сарибек')

room1 = Room(id = uuid.uuid4(), description='room1', user_id= user1.id)
room2 = Room(id = uuid.uuid4(), description='room1', user_id= user2.id)
room3 = Room(id = uuid.uuid4(), description='room1', user_id= user3.id)

with Session(engine) as session:
    user = session.exec(select(User).where(User.description == 'Данила')).first()
    print(user.articles)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
