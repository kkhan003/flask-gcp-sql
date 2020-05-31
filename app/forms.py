from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectField
# val err to build validations - these work with the 2 functions below..
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LeaseDetails(FlaskForm):
    lease_no = IntegerField(validators=[DataRequired()])
    lease_co = SelectField(choices=['Company 1','Company 2','Company 3'],validators=[DataRequired()], validate_choice=False)
    lease_type = SelectField(choices=['Land','Building','Equipment','Vehicles'],validators=[DataRequired()], validate_choice=False)
    payment_terms = SelectField(choices=['Advance','Arrears'],validators=[DataRequired()], validate_choice=False)
    period_desc = SelectField(choices=['Yearly','Semi-annual','Quarterly','Tri-annual','Bi-monthly','Monthly'],validators=[DataRequired()], validate_choice=False)
    start_date = DateField(validators=[DataRequired()])
    end_date = DateField(validators=[DataRequired()])
    rate = FloatField(validators=[DataRequired()])
    rental = IntegerField(validators=[DataRequired()])
    submit = SubmitField('New')