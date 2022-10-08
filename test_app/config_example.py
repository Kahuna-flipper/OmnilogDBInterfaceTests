import os
basedir = os.path.abspath(os.path.dirname(__file__))

# LOCAL:
''
DB_NAME='phenom'
HOST='localhost'
USER='phenom'
PASS='phenom'
DIALECT='mysql'
DRIVER='mysqlconnector'

MONGOCLIENT = "mongodb://localhost:27017/"


# MONGO
MONGO_CNX = {
    'client':MONGOCLIENT,
    'db': "phenom",
    'collection':"growth_profiles"
}    
