from app.config import Base

from datetime import datetime, timedelta
from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index)

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_email', 'email'),
        {'schema': 'access'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(350), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Integer, nullable=False, default=9)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime(timezone=True))

    # Relationships
    refresh_tokens = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
    password_resets = relationship('PasswordReset', back_populates='user', cascade='all, delete-orphan')
    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='author', cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = (
        Index('ix_refresh_tokens_user_id_created_at', 'user_id', 'created_at'),
        Index('ix_refresh_tokens_token', 'token'),
        Index('ix_refresh_tokens_expires_at', 'expires_at'),
        {'schema': 'access'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('access.users.id'), nullable=False)
    token = Column(Text, unique=True, nullable=False)
    token_type = Column(String(50), nullable=False, default='long')
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.utcnow() + timedelta(days=3))
    revoked = Column(Boolean, nullable=False, default=False)
    ip = Column(INET)
    user_agent = Column(Text)
    last_used_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship('User', back_populates='refresh_tokens')


class PasswordReset(Base):
    __tablename__ = 'password_resets'
    __table_args__ = (
        Index('ix_password_resets_user_id_created_at', 'user_id', 'created_at'),
        Index('ix_password_resets_reset_token', 'reset_token'),
        Index('ix_password_resets_expires_at', 'expires_at'),
        {'schema': 'access'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('access.users.id'), nullable=False)
    reset_token = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=1))
    used = Column(Boolean, nullable=False, default=False)
    used_at = Column(DateTime(timezone=True))
    ip = Column(INET)
    user_agent = Column(Text)

    # Relationships
    user = relationship('User', back_populates='password_resets')


class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = (
        Index('ix_posts_author_id', 'author_id'),
        Index('ix_posts_created_at', 'created_at'),
        {'schema': 'content'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('access.users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_mime = Column(String(50), default='text/html')
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = (
        Index('ix_comments_post_id_created_at', 'post_id', 'created_at'),
        Index('ix_comments_author_id_created_at', 'author_id', 'created_at'),
        {'schema': 'content'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('content.posts.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('access.users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')