"""This file contains the configuration for the Flask app."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

# load RDS credentials from environment variables
RDS_USERNAME = os.environ.get('RDS_USERNAME')
RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
RDS_ENDPOINT = os.environ.get('RDS_ENDPOINT')
RDS_PORT = os.environ.get('RDS_PORT')
RDS_DB_NAME = os.environ.get('RDS_DB_NAME')

# read access key and secret access key from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')



@dataclass
class Config:
    """A class for the Flask app configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
