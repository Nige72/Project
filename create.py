# Create the db
from hello import db
db.drop_all()
db.create_all()