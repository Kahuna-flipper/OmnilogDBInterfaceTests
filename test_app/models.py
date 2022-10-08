
from app import db
from phenom_db import *
from sqlalchemy.orm import relationship
from phenom_db import *

import pymongo
from config import MONGO_CNX
myclient = pymongo.MongoClient(MONGO_CNX['client'])
# database
mydb = myclient[MONGO_CNX['db']]
# collection
mongo_table= mydb[MONGO_CNX['collection']]


class Runinfo(db.Model):
    plate_id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    study =  db.Column(db.String(64), nullable=False) 
    plate_type=  db.Column(db.String(64), nullable=False)
    species =  db.Column(db.String(64), nullable=False)
    strain =  db.Column(db.String(64), nullable=False)
    media =  db.Column(db.String(64), nullable=False)
    rep =  db.Column(db.String(64), nullable=False)
    setup_time =  db.Column(db.String(64), nullable=False)

class Plateinfo(db.Model):
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(64), nullable=False) 
    well= db.Column(db.String(64), nullable=False) 
    cas = db.Column(db.String(64), nullable=True) 
    kegg= db.Column(db.String(64), nullable=True) 
    name= db.Column(db.String(64), nullable=False) 
    type= db.Column(db.String(64), nullable=False) 
    
class Pca(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # TO match all growth results on plate & well
    dim1 = db.Column(db.Float, nullable=False)
    dim2 = db.Column(db.Float, nullable=False)
    dim3 = db.Column(db.Float, nullable=False)
    type= db.Column(db.String(64), nullable=False) 
    name= db.Column(db.String(64), nullable=False) 
    comparator= db.Column(db.String(64), nullable=False) 
    
    study_id = db.Column(db.Integer, db.ForeignKey('studies.study_id'),nullable=False)
    
    
class Growth(db.Model):
    auc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auc = db.Column(db.String(64), nullable=False) 
    well= db.Column(db.String(64), nullable=False) 
    auc_ratio= db.Column(db.Float, nullable=False)
    fold_change = db.Column(db.Float, nullable=False)
    log2FC = db.Column(db.Float, nullable=False)
    plate_id = db.Column(db.Integer, nullable=False)
    
class Studies(db.Model):
    study_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_name = db.Column(db.String(64), nullable=False)
    study_description= db.Column(db.String(64), nullable=True)
    # pc1= db.Column(db.Float, nullable=True)
    # pc2= db.Column(db.Float, nullable=True)
    # pc3= db.Column(db.Float, nullable=True)
    
    
class Study2runinfo(db.Model):
    s2r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_id = db.Column(db.Integer, db.ForeignKey('studies.study_id'),nullable=False)
    plate_id = db.Column(db.Integer, db.ForeignKey('runinfo.plate_id'), nullable=False)
    