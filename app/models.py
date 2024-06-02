#every model represents a table in the database
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# class must extend Base, requirement for any SQLAlchemy Model
class Post(Base):
    __tablename__ = "posts"
    # define columns
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable=False)
    content = Column(String, nullable = False)
    priv = Column(Boolean, server_default= 'TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False)
    # create another property for our post, fetch the User(Base) class and find the relationship between the two db's
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    # unique prevents the same email registering twice
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


