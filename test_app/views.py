from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app, db, models
from .forms import LoginForm, EditMRM, EditForm
from app.models import mongo_table

import pandas as pd



@app.route('/')
@app.route('/index')
def index():

    runs = models.Runinfo.query
    metadata = pd.read_sql(runs.statement, runs.session.bind)
    stats = pd.DataFrame(metadata.groupby(['species','strain','plate_type','media']).count()['plate_id'])

    # user = {'test': 'test'}  # fake user
    return render_template('index.html', stats=stats.to_html())
    
    
@app.route('/plates_cumulative/json')
def cumulative_plates_json():
    # user = {'test': 'test'}  # fake user
    runs = models.Runinfo.query
    runinfo = pd.read_sql(runs.statement, runs.session.bind)
    runinfo['setup_time'] = pd.to_datetime(runinfo['setup_time'])
    res = runinfo.groupby('setup_time').count()['plate_id']
    monthly = res.resample('M').sum()
    cumulative = monthly.cumsum()
    labels = cumulative.index.astype(str).tolist()
    data = cumulative.values.tolist()
    return jsonify({'labels':labels,'data':data})
    
@app.route('/species_pie/json')
def species_pie():
    # user = {'test': 'test'}  # fake user
    runs = models.Runinfo.query
    runinfo = pd.read_sql(runs.statement, runs.session.bind)
    res = runinfo.groupby('species').count()['plate_id']
    labels = res.index.astype(str).tolist()
    data = res.values.tolist()
    return jsonify({'labels':labels,'data':data})
    
@app.route('/plate_types/json')
def plate_types():
    # user = {'test': 'test'}  # fake user
    runs = models.Runinfo.query
    runinfo = pd.read_sql(runs.statement, runs.session.bind)
    res = runinfo.groupby('plate_type').count()['plate_id']
    labels = res.index.astype(str).tolist()
    data = res.values.tolist()
    return jsonify({'labels':labels,'data':data})
    

    
@app.route('/plates', methods=['GET'])
def plates():
    return render_template('plates.html',plates=True)
    
@app.route('/plates/json', methods=['GET'])
def plates_json():
    
    strain = request.args.get('strain')
    print(strain)
    if strain==None:
        runs = models.Runinfo.query.all()
    else:
        runs = models.Runinfo.query.filter(models.Runinfo.strain==strain).all()
    
    
    out = []
    for r in runs:
        out.append([
            # "<a href="+url_for('fastqs_fastq', fastq=f.fastq_id)+">"+f.filename+"</a>",
            "<a href="+url_for('plates_plate', plate_id=r.plate_id)+">Plate "+str(r.plate_id)+"</a>", 
            r.study, 
            r.plate_type,
            r.species,
            r.strain, 
            r.media,
            r.rep,
            r.setup_time
        ])
    
    return jsonify(data=out)

    
@app.route('/plates/<plate_id>', methods=['GET'])
def plates_plate(plate_id):
    plate = models.Runinfo.query.filter(models.Runinfo.plate_id==plate_id).first()
    
    data_from_db = mongo_table.find_one({"index":str(plate_id)})
    growth = pd.DataFrame(data_from_db['data'])
    wells = growth.columns[:-2].tolist()
    
    return render_template('plates.html',plate=plate, wells=wells)
    
@app.route('/plates/<plate_id>/<well>', methods=['GET'])
def plates_plate_well(plate_id, well):
    plate = models.Runinfo.query.filter(models.Runinfo.plate_id==plate_id).first()
    
    data_from_db = mongo_table.find_one({"index":str(plate_id)})
    # data_from_db = data_from_db['data']
    growth = pd.DataFrame(data_from_db["data"])
    
    return render_template('well.html',plate=plate, well=well, growth=growth[well].to_dict())
    
@app.route('/plates/<plate_id>/<well>/json', methods=['GET'])
def plates_plate_well_json(plate_id, well):
    plate = models.Runinfo.query.filter(models.Runinfo.plate_id==plate_id).first()
    
    data_from_db = mongo_table.find_one({"index":str(plate_id)})
    # data_from_db = data_from_db['data']
    growth = pd.DataFrame(data_from_db["data"])
    labels = pd.to_numeric(growth['hour']).values.tolist()
    growth = pd.to_numeric(growth[well]).values.tolist()
    
    return jsonify({'labels':labels,'growth':growth})
    
@app.route('/strains', methods=['GET'])
def strains():
    runs = models.Runinfo.query
    metadata = pd.read_sql(runs.statement, runs.session.bind)
    # stats = pd.DataFrame(metadata.groupby(['species','strain','plate_type','media']).count()['plate_id'])
    stats = pd.DataFrame(metadata.groupby(['species','strain']).count()['plate_id'])
    # stats = metadata
    
    return render_template('strains.html')
    
@app.route('/strains/json', methods=['GET'])
def strains_json():
    runs = models.Runinfo.query
    metadata = pd.read_sql(runs.statement, runs.session.bind)
    # stats = pd.DataFrame(metadata.groupby(['species','strain','plate_type','media']).count()['plate_id'])
    stats = pd.DataFrame(metadata.groupby(['species','strain']).count()['plate_id']).reset_index()
    out = []
    for i in stats.index:
        strain = stats.loc[i,'strain']
        species = stats.loc[i,'species']
        count = stats.loc[i,'plate_id']
        out.append([
            # "<a href="+url_for('fastqs_fastq', fastq=f.fastq_id)+">"+f.filename+"</a>",
            "<a href="+url_for('strains_strain', strain=strain)+">"+species+ ' '+strain+"</a>", 
            str(count)
            
        ])
    
    return jsonify(data=out)
    
    
@app.route('/strains/<strain>', methods=['GET'])
def strains_strain(strain):
    runs = models.Runinfo.query.filter(models.Runinfo.strain==strain)
    metadata = pd.read_sql(runs.statement, runs.session.bind)
    stats = pd.DataFrame(metadata.groupby(['species','strain','plate_type','media']).count()['plate_id'])
    
    return render_template('strains.html',strains=stats.to_html(), strain=strain)
'''    
@app.route('/phenomes', methods=['GET'])
def phenomes():
    aucs = models.Growth.query.all()
    return render_template('phenomes.html',aucs=aucs)
'''
    
@app.route('/compounds', methods=['GET'])
def compounds():
    info = models.Plateinfo.query
    # info = pd.read_sql(info.statement, info.session.bind)
    # info = info['name'].unique()
    return render_template('compounds.html',info=info)
    
@app.route('/compounds/json', methods=['GET'])
def compounds_json():
    info = models.Plateinfo.query
    info = pd.read_sql(info.statement, info.session.bind)
    info = info[['name','type','kegg','cas','plate','well']]
    data = info.values.tolist()
    for d in data:
        name = d[0]
        d[0] = "<a href="+url_for('compounds_compound', compound=name)+">"+name+"</a>"
    
    
    return jsonify({'labels':info.index.tolist(), 'data':data})
    
    
@app.route('/compounds/<compound>', methods=['GET'])
def compounds_compound(compound):
    info = models.Plateinfo.query.filter(models.Plateinfo.name==compound)
    info = pd.read_sql(info.statement, info.session.bind)
    # plates = 
    aucs = models.Growth.query.filter(models.Growth.well.in_(info['well'].tolist())).all()
    # aucs = models.Growth.query.filter(models.Growth.well==compound.well).all()
    # aucs = pd.read_sql(aucs.statement, aucs.session.bind)
    # aucs = aucs['name'].unique()
    return render_template('compounds.html',aucs=aucs, compound=compound, info=info.to_html())
    
@app.route('/compounds/<compound>/json/<metric>', methods=['GET'])
def compounds_compound_json(compound, metric):
    
    # compound = compound.replace('%25','%').replace('%20',' ')
    print(compound)
    
    info = models.Plateinfo.query.filter(models.Plateinfo.name==compound)
    info = pd.read_sql(info.statement, info.session.bind)
    
    aucs = models.Growth.query.filter(models.Growth.well.in_(info['well'].tolist()))
    aucs = pd.read_sql(aucs.statement, aucs.session.bind)
    
    runs = models.Runinfo.query
    runinfo = pd.read_sql(runs.statement, runs.session.bind)
    aucs = pd.merge(aucs, runinfo)
    aucs = aucs[aucs['plate_type'].isin(info['plate'].tolist())]
    grouped = aucs.groupby(['species','strain','media']).mean()[metric] # TODO separate these into species?
    
    return jsonify({'labels':grouped.index.tolist(), 'data':grouped.values.tolist()})
    #TODO add error bars: https://github.com/datavisyn/chartjs-plugin-error-bars
    
    
@app.route('/studies', methods=['GET'])
def studies():
    studies = models.Studies.query.all()
    return render_template('studies.html',studies=studies)
    
@app.route('/studies/json', methods=['GET'])
def studies_json():
    studies = models.Studies.query.all()
    out = []
    for study in studies:
        out.append([
            "<a href="+url_for('studies_study', study=study.study_id)+">"+study.study_name+"</a>", 
            study.study_description]
        )
    return jsonify({'data':out})
    
@app.route('/studies/<study>', methods=['GET'])
def studies_study(study):
    study_info = models.Study2runinfo.query.filter(models.Study2runinfo.study_id==study).all()
    pca = models.Pca.query.filter(models.Pca.study_id==study)
    pca = pd.read_sql(pca.statement, pca.session.bind)
    
    return render_template('studies.html',study=study_info, pca=pca.to_html(), study_id=study)
    
@app.route('/studies/<study>/pca/<type>/json', methods=['GET'])
def studies_study_pca(study, type):
    from sqlalchemy import and_
    study_info = models.Study2runinfo.query.filter(models.Study2runinfo.study_id==study).all()
    # pca = models.PCA.query.filter(and_(models.PCA.study_id==study,models.PCA.type=='loadings'))
    # pca = models.PCA.query.filter(and_(models.PCA.study_id==study,models.PCA.type=='coordinates'))
    pca = models.Pca.query.filter(and_(models.Pca.study_id==study,models.Pca.type==type))
    pca = pd.read_sql(pca.statement, pca.session.bind)
    labels = []
    datasets = []
    colors=['rgb(255, 99, 132)','rgb(255, 159, 64)','rgb(255, 205, 86)','rgb(75, 192, 192)','rgb(54, 162, 235)','rgb(153, 102, 255)','rgb(201, 203, 207)']
    color_cnt=0
    link=''
    for comp in pca['comparator'].unique():
        
        comp_data = pca[pca['comparator']==comp]
        dataset = {}
        data = []
        for i in comp_data.index:
            x = comp_data.loc[i,'dim1']
            y = comp_data.loc[i,'dim2']
            z = comp_data.loc[i,'dim3']
            name = comp_data.loc[i,'name']
            if type=='loadings':
                link='../compounds/'+name.split(';')[0].strip()
            elif type=='coordinates':
                link='../strains/'+name.split(';')[1].strip()
            data.append({'x':x,'y':y,'z':z,'name':name,'link':link})
            # labels.append(name)
        dataset['data']=data
        dataset['label']=comp
        dataset['backgroundColor']=colors[color_cnt%len(colors)]
        dataset['borderColor']=colors[color_cnt%len(colors)]
        dataset['pointRadius']=10
        dataset['pointHoverRadius']=8
        datasets.append(dataset)
        color_cnt+=1
        
    return jsonify({'datasets':datasets})
    

    
'''
@app.route('/fastqs/json', methods=['GET'])
def fastqs_json():
    fastqs = models.Fastq.query.all()
    out = []
    for f in fastqs:
        out.append([
            "<a href="+url_for('fastqs_fastq', fastq=f.fastq_id)+">"+f.filename+"</a>",
            f.size_kb, 
            f.total_bps, 
            f.total_seqs, 
            f.fastq_id
        ])
    
    return jsonify(data=out)
    
@app.route('/fastqs', methods=['GET'])
def fastqs():
    return render_template('fastqs.html',fastqs=True)
    
@app.route('/fastqs/<fastq>', methods=['GET'])
def fastqs_fastq(fastq):
    # session = Session()
    fastq = models.Fastq.query.filter(models.Fastq.fastq_id==fastq).first()
    # fastq = fastq.__dict__
    # del fastq['_sa_instance_state']
    return render_template('fastqs.html',fastq=fastq)
    
@app.route('/genomes', methods=['GET'])
def genomes():
    
    return render_template('genomes.html',genomes=True)
    
@app.route('/genomes/json', methods=['GET'])
def genomes_json():
    genomes = models.Assembly.query.all()
    out = []
    for g in genomes:
        out.append([
            "<a href="+url_for('genomes_genome', genome=g.assembly_id)+">"+g.name+"</a>",
            g.name, 
            g.total_length, 
            g.num_contigs, 
            g.N50
        ])
    
    return jsonify(data=out)
    
@app.route('/genomes/<genome>', methods=['GET'])
def genomes_genome(genome):
    genome = models.Assembly.query.filter(models.Assembly.assembly_id==genome).first()
    # genome = genome.__dict__
    # del genome['_sa_instance_state']
    
    # return jsonify({
        # 'status': 'success',
        # 'genome': genome
    # })
    return render_template('genomes.html',genome=genome)
    
@app.route('/projects', methods=['GET'])
def projects():
    session = Session()
    projects = session.query(Projects).all()
    project_list = []
    for p in projects:
        project_list.applicationend({'name':p.name})
    return jsonify({
        'status': 'success',
        'genomes': project_list
    })
    
'''
                           