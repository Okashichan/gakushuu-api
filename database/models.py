from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship


class DbRole(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    user = relationship('DbUser', back_populates='role')


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    avatar = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime)
    role_id = Column(Integer, ForeignKey('role.id'))

    role = relationship('DbRole', back_populates='user')
    lessons = relationship('DbLesson', back_populates='author')
    dictionary = relationship(
        'DbDictionary', back_populates='author')
    dictionary_proposals = relationship(
        'DbDictionaryProposal', back_populates='author')


class DbLesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    cover = Column(String)
    created_at = Column(DateTime)
    last_modified = Column(DateTime)
    is_published = Column(Boolean)
    author_id = Column(Integer, ForeignKey('user.id'))

    author = relationship('DbUser', back_populates='lessons')
    tests = relationship('DbTest', back_populates='lesson')


class DbDictionary(Base):
    __tablename__ = 'dictionary'
    id = Column(Integer, primary_key=True)
    original = Column(String)
    en_translation = Column(String)
    ua_translation = Column(String)
    romanization = Column(String)
    transliteration = Column(String)
    comment = Column(String)
    created_at = Column(DateTime)
    last_modified = Column(DateTime)

    author_id = Column(Integer, ForeignKey('user.id'))

    author = relationship('DbUser', back_populates='dictionary')


class DbDictionaryProposal(Base):
    __tablename__ = 'dictionary_proposal'
    id = Column(Integer, primary_key=True)
    original = Column(String)
    en_translation = Column(String)
    ua_translation = Column(String)
    romanization = Column(String)
    transliteration = Column(String)
    comment = Column(String)
    created_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey('user.id'))

    author = relationship('DbUser', back_populates='dictionary_proposals')


class DbTest(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    questions = Column(String)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('DbLesson', back_populates='tests')
