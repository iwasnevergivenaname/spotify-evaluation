from models import db

def create_db():
	db.create_all()


def drop_db():
	db.drop_all()