from django.core.management import setup_environ
import settings
setup_environ(settings)
from app.models import *
import sys
import os


#def create_price_perhour():
