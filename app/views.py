import logging
from flask import abort, json, request, render_template, redirect, url_for
from app import app, db, models, forms
from google.auth.transport import requests
import google.oauth2.id_token
from app.calcs import single_lease, pd

firebase_request_adapter = requests.Request()
@app.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
        # Verify the token against the Firebase Auth API. This example
        # verifies the token on each page load. For improved performance,
        # some applications may wish to cache results in an encrypted
        # session store (see for instance
        # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    leasedet = models.LeaseInfo.query.order_by('lid').all()
    form = forms.LeaseDetails()            
    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, form=form, data=leasedet)

# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     leasedet = models.LeaseInfo.query.order_by('lid').all()
#     form = forms.LeaseDetails()
#     return render_template('home.html', title='Home', form=form, data=leasedet)

@app.route("/output", methods=['GET', 'POST'])
def output():
    fullcalcs = models.FullCalcs.query.order_by('fcid').all()
    return render_template('output.html', title='Output', data=fullcalcs)

@app.route("/new", methods=['GET', 'POST'])
def newleases():
    form = forms.LeaseDetails()
    if form.validate_on_submit():
        newlease = models.LeaseInfo(lease_no=form.lease_no.data, lease_co=form.lease_co.data, lease_type=form.lease_type.data, payment_terms=form.payment_terms.data, period_desc=form.period_desc.data,
                            start_date=form.start_date.data, end_date=form.end_date.data, rate=form.rate.data, rental=form.rental.data)
        db.session.add(newlease)
        db.session.commit()
        df = pd.read_sql('SELECT * FROM lease_info WHERE lid=(SELECT max(lid) FROM lease_info)', con=db.engine)
        df_db = single_lease(df)
        df_db.to_sql(name='full_calcs', con=db.engine, index=False, if_exists='append')
        db.session.commit()
        return redirect(url_for('root'))


@app.route("/<int:leaseid>/delete", methods=['GET', 'POST'])
def yourleasesdelete(leaseid):
    deletedItem = models.LeaseInfo.query.filter_by(lid=leaseid).one()
    db.session.delete(deletedItem)
    db.session.commit()
    return redirect(url_for('root'))


@app.route("/<int:leaseid>/edit", methods=['GET', 'POST'])
def yourleasesedit(leaseid):
    editlease = models.LeaseInfo.query.filter_by(lid=leaseid).one()
    form = forms.LeaseDetails(obj=editlease)
    if form.validate_on_submit():
        editlease.lease_no = form.lease_no.data
        editlease.lease_co = form.lease_co.data
        editlease.lease_type = form.lease_type.data
        editlease.payment_terms = form.payment_terms.data
        editlease.period_desc = form.period_desc.data
        editlease.start_date = form.start_date.data
        editlease.end_date = form.end_date.data
        editlease.rate = form.rate.data
        editlease.rental = form.rental.data
        db.session.commit()
        return redirect(url_for('root'))
    else:
        return render_template('edit.html', title='Edit', data=editlease, form=form)




