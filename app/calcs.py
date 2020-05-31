# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


# %%
def single_lease(m_df):
    m_df.columns = m_df.columns.str.lower().str.replace(".","").str.replace(" ","_")
    m_df.head()


    # %%
    m_df['start_date'] = pd.to_datetime(m_df['start_date'])
    m_df['end_date'] = pd.to_datetime(m_df['end_date'])


    # %%
    calcs = m_df
    calcs


    # %%
    # Defining relevant variables

    s_date = calcs.start_date[0]
    e_date = calcs.end_date[0]
    p_terms = calcs.payment_terms[0]
    per_desc = calcs.period_desc[0]
    int_rate = calcs.rate[0]
    rent = calcs.rental[0]
    tot_days = (e_date-s_date).days+1


    # %%
    # Coming up with number of payments based on frequency

    if per_desc == 'Yearly':
        payment_period = relativedelta(years=1)
    elif per_desc == 'Semi-annual':
        payment_period = relativedelta(months=6)
    elif per_desc == 'Quarterly':
        payment_period = relativedelta(months=3)
    elif per_desc == 'Tri-annual':
        payment_period = relativedelta(months=4)
    elif per_desc == 'Bi-monthly':
        payment_period = relativedelta(months=2)
    elif per_desc == 'Monthly':
        payment_period = relativedelta(months=1)


    # %%
    payment_dates = []
    if p_terms == 'Advance':
        p_date = s_date
        payment_dates = [p_date]
        while p_date + payment_period < e_date:
            p_date = p_date + payment_period
            payment_dates.append(p_date) 
    else:
        p_date = s_date - timedelta(days=1)
        while p_date + payment_period <= e_date:
            p_date = p_date + payment_period
            payment_dates.append(p_date) 


    # %%
    calcs2 = pd.DataFrame(payment_dates,columns=['payment_date'])
    calcs2['rental'] = rent
    calcs2


    # %%
    ((e_date - calcs2.loc[len(calcs2)-1,'payment_date'])/(calcs2.loc[len(calcs2)-1,'payment_date']-calcs2.loc[len(calcs2)-2,'payment_date']))


    # %%
    payment_period.days


    # %%
    if p_terms == 'Advance':
        calcs2.loc[len(calcs2)-1,'rental'] = calcs2.loc[len(calcs2)-1,'rental'] * ((e_date - calcs2.loc[len(calcs2)-1,'payment_date'])/     (calcs2.loc[len(calcs2)-1,'payment_date']-calcs2.loc[len(calcs2)-2,'payment_date']))
    else:
        if calcs2.loc[len(calcs2)-1,'payment_date'] != e_date:
            calcs2.loc[len(calcs2),'payment_date'] = e_date
            calcs2.loc[len(calcs2)-1,'rental'] = rent * ((e_date - calcs2.loc[len(calcs2)-2,'payment_date'])/(calcs2.loc[len(calcs2)-2,         'payment_date']-calcs2.loc[len(calcs2)-3,'payment_date']))


    # %%
    e_date - calcs2.loc[len(calcs2)-2,'payment_date']


    # %%
    calcs2['xnpv'] = ''
    calcs2.xnpv = calcs2.rental/((1+int_rate)**(((calcs2.payment_date-s_date).dt.days)/365))
    sum_xnpv = calcs2.xnpv.sum()
    calcs2


    # %%
    # Create full lease day wise table

    calcs1 = pd.DataFrame(calcs.values.repeat(tot_days,axis=0),columns=calcs.columns)
    calcs1


    # %%
    # Add a new column 'period_date'

    calcs1['period_date'] = ''
    calcs1['period_date'][0] = s_date
    calcs1.head()


    # %%
    # Add dates in the 'period_date' column

    for i in range(1, len(calcs1)):
        calcs1.loc[i, 'period_date'] = calcs1.loc[i-1, 'period_date'] + timedelta(days=1)
    calcs1['period_date'] = pd.to_datetime(calcs1['period_date'])
    calcs1.drop(columns='rental', inplace = True)
    calcs1.tail()


    # %%
    calcs3 = calcs1.merge(calcs2, left_on='period_date', right_on='payment_date', how='left')
    calcs3['rental'] = calcs3['rental'].fillna(0)
    calcs3


    # %%
    calcs3['sum_xnpv_pd'] = sum_xnpv


    # %%
    calcs3['int_exp'] = 0.0


    # %%
    calcs3['int_exp'][0] = round(sum_xnpv * int_rate / 365,2)


    # %%
    calcs3['lease_liab'] = 0.0
    calcs3['lease_liab'][0] = round(sum_xnpv,2)

    calcs3['rou_asset'] = 0.0
    calcs3['rou_asset'][0] = round(sum_xnpv,2)
    calcs3['amortisation'] = round(sum_xnpv/(tot_days-1),2)


    # %%
    calcs3.convert_dtypes().dtypes


    # %%
    for i in range(1, len(calcs3)):
        calcs3.loc[i, 'lease_liab'] = (calcs3.loc[i-1, 'lease_liab']+calcs3.loc[i-1, 'int_exp'] - calcs3.loc[i, 'rental']).round(2)
        calcs3.loc[i, 'rou_asset'] = (calcs3.loc[i-1, 'rou_asset'] - calcs3.loc[i, 'amortisation']).round(2)
        if calcs3.loc[i-1, 'rental'] == 0:
            calcs3.loc[i, 'int_exp'] = calcs3.loc[i-1, 'int_exp']
        else:
            calcs3.loc[i, 'int_exp'] = (calcs3.loc[i-1, 'lease_liab']*int_rate/365).round(2)
    calcs3


    # %%
    calcs3['month'] = calcs3.period_date.map(lambda x: x.strftime('%b-%Y'))


    # %%
    calcs4 = calcs3.groupby(['lid','lease_no','lease_co','lease_type','month'],sort=False).agg(op_lease_liab=('lease_liab','first'),int_exp=('int_exp','sum'),rent_paid=('rental','sum'),cl_lease_liab=('lease_liab','last'),op_rou_asset=('rou_asset','first'),amortisation=('amortisation','sum'),cl_rou_asset=('rou_asset','last'))
    calcs4 = calcs4.reset_index()
    calcs4.rename(columns={'lid': 'lease_id'},inplace=True)


    # %%
    return calcs4

if __name__ == "__main__":
    single_lease()