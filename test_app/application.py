from flask import Flask, render_template, url_for, jsonify
''' CONNECTING TO DATABASES '''
# MYSQL - for metadata
from ex_config import SQLALCHEMY_DATABASE_URI, MONGO_CNX
from sqlalchemy import create_engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Mongo for growth data
import pymongo
# Making a Connection with MongoClient
myclient = pymongo.MongoClient(MONGO_CNX['client'])
# database
mydb = myclient[MONGO_CNX['db']]
# collection
mongo_table= mydb[MONGO_CNX['collection']]
data = mongo_table.find()
from phenom_db import *
import pandas as pd





app = Flask(__name__,template_folder='templates',static_url_path='/static')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/ecoli')
def ecoli():
    return render_template('ecoli.html')


@app.route('/strains/json', methods=['GET'])
def strains_json():
    strain_data = pd.read_csv('./static/data/OrganismsData/ecoli.csv')
    #strain_data = pd.read_csv(url_for('static',filename='data/OrganismsData/ecoli.csv'))
    # from ex_config import SQLALCHEMY_DATABASE_URI, MONGO_CNX
    # from sqlalchemy import create_engine
    # engine = create_engine(SQLALCHEMY_DATABASE_URI)
    # from sqlalchemy.orm import sessionmaker
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # from phenom_db import Runinfo

    # metadata = session.query(Runinfo)
    # metadata = pd.read_sql(metadata.statement, metadata.session.bind)
    # #runs = models.Runinfo.query
    # #metadata = pd.read_sql(runs.statement, runs.sessio n.bind)
    # # Adding specie filter here temporarily
    # metadata = metadata[metadata['species']=='E. coli']
    # # stats = pd.DataFrame(metadata.groupby(['species','strain','plate_type','media']).count()['plate_id'])
    # stats = pd.DataFrame(metadata.groupby(['species','strain']).count()['plate_id']).reset_index()
    # out = []
    out2 = []

    for i in strain_data.index:
        specie = strain_data.loc[i,'Specie']
        strain = strain_data.loc[i,'Strain']
        studies = strain_data.loc[i,'Studies']
        media = strain_data.loc[i,'Media Types']


    # for i in metadata.index:
    #     strain = metadata.loc[i,'strain']
    #     species = metadata.loc[i,'species']
    #     count = metadata.loc[i,'plate_id']
    #     plate_type = metadata.loc[i,'plate_type']
    #     study = metadata.loc[i,'study']
    #     media = metadata.loc[i,'media']
    #     rep = metadata.loc[i,'rep']
    #     setup_time = metadata.loc[i,'setup_time']
    #     out.append([
    #         # "<a href="+url_for('fastqs_fastq', fastq=f.fastq_id)+">"+f.filename+"</a>",
    #         #"<a href="+url_for('strains_strain', strain=strain)+">"+species+ ' '+strain+"</a>", 
    #         #str(strain)+''+str(species),
    #         str(count),
    #         str(study),
    #         str(plate_type),
    #         str(species),
    #         str(strain),
    #         str(media),
    #         str(rep),
    #         str(setup_time)            
    #     ])

        out2.append([
            str(specie),
            str(strain),
            str(studies),
            str(media)
        ])

    #return jsonify(data=out)
    return jsonify(data=out2)

if __name__=="__main__":
    app.run(debug=True)