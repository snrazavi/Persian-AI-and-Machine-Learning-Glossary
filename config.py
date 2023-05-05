"""This file contains the configuration for the Flask app."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

@dataclass
class Config:
    """A class for the Flask app configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_ENDPOINT')}:3306/{os.environ.get('RDS_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
