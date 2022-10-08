from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField('openid')
    remember_me = BooleanField('remember_me', default=False)
    formula = StringField('formula', validators=[DataRequired()])
    adduct = StringField('adduct', validators=[DataRequired()])


class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    
class EditMRM(Form):
    index = StringField('index', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    Q1 = StringField('Q1', validators=[DataRequired()])
    Q3 = StringField('Q3', validators=[DataRequired()])
    RT = StringField('RT', validators=[DataRequired()])
    BestColumn = StringField('BestColumn', validators=[DataRequired()])
    Group = StringField('RT', validators=[DataRequired()])
    Window = StringField('RT', validators=[DataRequired()])
    Primary_Secondardy = StringField('RT', validators=[DataRequired()])
    Threshold = StringField('RT', validators=[DataRequired()])
    Dwell_weight = StringField('RT', validators=[DataRequired()])
    DP = StringField('RT', validators=[DataRequired()])
    EP = StringField('RT', validators=[DataRequired()])
    CE = StringField('RT', validators=[DataRequired()])
    CXP = StringField('RT', validators=[DataRequired()])
    