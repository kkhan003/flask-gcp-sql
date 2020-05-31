from app import db
import json

class LeaseInfo(db.Model):
    __tablename__ = 'lease_info'
    lid = db.Column(db.Integer, primary_key = True)
    lease_no = db.Column(db.Integer(), nullable = False)
    lease_co = db.Column(db.String(), nullable = False)
    lease_type = db.Column(db.String(), nullable = False)
    payment_terms = db.Column(db.String(), nullable = False)
    period_desc = db.Column(db.String(), nullable = False)
    start_date = db.Column(db.DateTime, nullable = False)
    end_date = db.Column(db.DateTime, nullable = False)
    rate = db.Column(db.Float(), nullable = False)
    rental = db.Column(db.Integer, nullable = False)
    full_calcs = db.relationship('FullCalcs', backref = 'info', lazy = True, cascade="all, delete-orphan")

class FullCalcs(db.Model):
    __tablename__ = 'full_calcs'
    fcid = db.Column(db.Integer, primary_key = True)
    lease_no = db.Column(db.String(), nullable = False)
    lease_co = db.Column(db.String(), nullable = False)
    lease_type = db.Column(db.String(), nullable = False)
    month = db.Column(db.String(), nullable = False)
    op_lease_liab = db.Column(db.Float(), nullable = True)
    int_exp = db.Column(db.Float(), nullable = True)
    rent_paid = db.Column(db.Float(), nullable = True)
    cl_lease_liab = db.Column(db.Float(), nullable = True)
    op_rou_asset = db.Column(db.Float(), nullable = True)
    amortisation = db.Column(db.Float(), nullable = True)
    cl_rou_asset = db.Column(db.Float(), nullable = True)
    lease_id = db.Column(db.Integer, db.ForeignKey('lease_info.lid'), nullable=False)

db.create_all()