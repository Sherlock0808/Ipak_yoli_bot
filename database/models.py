from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String)
    username = Column(String)
    language = Column(String(10))
    created_at = Column(TIMESTAMP, server_default=func.now())


class FAQ(Base):
    __tablename__ = 'faqs'

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50))
    lang = Column(String(50))
    is_active = Column(Boolean, default=True)


class Service(Base):
    __tablename__ = 'services_json'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    type = Column(String(50))
    link = Column(Text)


class SupportMessage(Base):
    __tablename__ = 'support_messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    message_text = Column(Text)
    status = Column(String(20), default='open')  # open, closed, in_progress
    created_at = Column(TIMESTAMP, server_default=func.now())
    handled_by = Column(String(100), nullable=True)


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    message_text = Column(Text)
    response_text = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())
