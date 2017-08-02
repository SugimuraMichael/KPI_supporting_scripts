import pandas as pd
import numpy as np

#doesnt change
MC_directory = 'C:/Users/585000/Desktop/PCFSM/2017 KPIs/'

#ADJUST: FILE NAME

### USE PAD COR not pad cor ppm
matrix_file = 'PAD COR 6_26_17.csv'
month_period = ['2017-05']

save_loc = 'C:/Users/585000/Desktop/PCFSM/2017 KPIs/ASNs for google drive/'
save_name = "may_ASNS_test_6_26_v2.csv"
save_yes_no = 'yes'

dat = pd.read_csv(MC_directory+matrix_file)

# part 1: Remove rows as required
#remove the Ta0 items
dat['Ta0'] = 0
for index, row in dat.iterrows():
    a = str(row['Project Code'])
    a = a[-3:]
    if a == 'TA0':
        dat.loc[index, 'Ta0'] = 1

dat = dat[dat['Ta0'] == 0]

## NEED TO FIX
dat = dat[dat['Client Type'] != 'NGF']

dat = dat[dat['Managed By - Project']!= 'SCMS']
dat = dat[dat['Order Short Closed'] != "Yes"]

#'2017-04'
pattern = '|'.join(month_period)
dat['Order Last Delivery Recorded Year - Month']=dat['Order Last Delivery Recorded Year - Month'].fillna("")
dat = dat[dat['Order Last Delivery Recorded Year - Month'].str.contains(pattern)]

'''
Order Last Delivery Recorded Year-Month	Freight Forwarder	PE#	PQ#	Order#	Shipment#
'''

cols = ['Order Last Delivery Recorded Year - Month','Freight Forwarder','PE#',"PQ#","Order#","Shipment#"]

dat = dat[cols]

dat.to_csv(save_loc+save_name,index=False)