from flask_sqlalchemy import SQLAlchemy

"""
Init SQLAlchemy instance, create base and metadata
"""

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata
