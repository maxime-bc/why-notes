# from datetime import datetime
#
# from flask_sqlalchemy import Model
# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
# from sqlalchemy.orm import relationship
#
#
# class User(Model):
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     pwd = Column(String, nullable=False)
#     notes = relationship("Note", cascade="all, delete", backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return f"<UserProfile(id={self.id}, email={self.email}, pwd={self.pwd}, " \
#                f"first_name={self.first_name}, last_name={self.last_name})>"
#
#
# class Note(Model):
#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     content = Column(Text, nullable=True)
#     creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
#     edit_date = Column(DateTime, nullable=False)
#     id_user = Column(Integer, ForeignKey('user.id'), nullable=False)
#     is_public = Column(Boolean, nullable=False)
#     uuid = Column(String, nullable=False)
#
#     def __repr__(self):
#         return f"<Note(id={self.id}, title={self.title}, content={self.content}, " \
#                f"creation_date={self.creation_date}, edit_date={self.edit_date}, " \
#                f"id_user={self.id_user}, is_public={self.is_public}, uuid={self.uuid})>"
