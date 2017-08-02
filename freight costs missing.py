import pandas as pd
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('latin-1')
#doesnt change
MC_directory = 'C:/Users/585000/Desktop/PCFSM/2017 KPIs/'

#ADJUST: FILE NAME

### USE PAD COR not pad cor ppm
matrix_file = 'PAD COR 6_01_17.csv'
month_period = ['2017-04','2017-03']

save_loc = 'C:/Users/585000/Desktop/PCFSM/2017 KPIs/ASNs for google drive/'
save_name = "March_April_ASNS_test_6_6_v2.csv"
save_yes_no = 'no'

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
cols = ['Order Last Delivery Recorded Year - Month','Freight Forwarder','PE#',"PQ#","Order#","Shipment#",'Shipment Mode',
        'Vendor INCO Term','Sub Vendor Name','Order Pick Up Country Name','Client INCO Term','Ship To Country Name',
        'Shipment Total Item Weight','Shipment Total Item Volume']
dat = dat[cols]

dat.to_csv(save_loc+save_name,index=False)

nik = pd.read_excel('C:/Users/585000/Downloads/Planned costs for PMU March.xlsx')


#test = pd.merge(nik,dat,how='left',on= 'Shipment#',indicator=True)


nik['Mode of transport'] =nik['Mode of transport'].fillna('-99')

for index, row in nik.iterrows():
    nik_asn = str(row['Shipment#'])
    check = str(row['Mode of transport'])

    if check == '-99':
        for index2, row2 in dat.iterrows():
            if nik_asn == str(row2['Shipment#']):

                nik.loc[index,'Freight Forwarder'] = row2['Freight Forwarder']
                nik.loc[index,'Mode of transport'] = row2['Shipment Mode']
                nik.loc[index,'Vendor Inco'] = row2['Vendor INCO Term']
                nik.loc[index,'Vendor name'] = row2['Sub Vendor Name']
                nik.loc[index,'Origin'] = row2['Order Pick Up Country Name']
                nik.loc[index,'Client Inco'] = row2['Client INCO Term']
                nik.loc[index,'Desrination country'] = row2['Ship To Country Name']
                nik.loc[index,'weight'] = row2['Shipment Total Item Weight']
                nik.loc[index,'volume'] = row2['Shipment Total Item Volume']


nik.to_excel('C:/Users/585000/Downloads/Planned costs for PMU March_2.xlsx',index=False)










