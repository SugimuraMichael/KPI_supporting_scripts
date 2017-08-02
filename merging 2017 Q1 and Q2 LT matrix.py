import pandas as pd
import glob
import os

'''
The purpose of this document is to merge the Q1 and Q2 lead time matricies to create a finalized version of them...

glob looks at the contents of some file, and extracts names of the csv files. the csv files in the main directory are modified versions
of the lead time matrices produced by ben smith. 

Columns used for lane identification
Origin	Dest	Mode	Client Incoterm	Origin+Dest+Mode+INCO
I currently change the name of the quarter manually  changed to match the year and quarter which it applies to. ex 2017-01 for Q1 2017 etc. Each Quarter can be kept as
its own csv. 
Original lead time column name "Shipment Lead Time: Vendor Fulfilment Date > Delivery (For KPIs 4&5)"


I think I can just do a merge on both so it should contain all of the rows... can pobably just iterate on them by having
them in a file?.... could automate the generation each time within the kpi folder to make it so I have to do less
manually?

Seems reasonable...
'''
#need to set the quarters that are being used. so update once per quarter to account for new columns
quarters = ['2017-01 leadtimes','2017-02 leadtimes','2017-03 leadtimes']

#######################################################################################################
directory = 'C:/Users/585000/Desktop/PCFSM/FLT matrix calculations/quarter_matricies'

os.chdir(directory)

filelist2 = glob.glob(os.path.join('*.csv*'))

first_pass = 0
matrix = pd.DataFrame()

for file in filelist2:
    file_dat = pd.read_csv(directory+'/'+str(file))
    print file_dat.shape
    for index, row in file_dat.iterrows():
        a = str(row['Origin']) + '-' + str(row['Dest']) + '-' + str(row['Mode']).replace('-','') + '-' + str(row['Client Incoterm'])
        file_dat.loc[index, 'lane_id'] = str(a).upper()

    if first_pass == 0:
        first_pass = 1
        matrix = file_dat

    else:
        matrix = pd.merge(matrix,file_dat, how= 'outer',on='lane_id')
        matrix['Origin_x'] = matrix['Origin_x'].fillna('')
        matrix['Dest_x'] = matrix['Dest_x'].fillna('')
        matrix['Mode_x'] = matrix['Mode_x'].fillna('')
        matrix['Client Incoterm_x'] = matrix['Client Incoterm_x'].fillna('')

        matrix['Origin_y'] = matrix['Origin_y'].fillna('')
        matrix['Dest_y'] = matrix['Dest_y'].fillna('')
        matrix['Mode_y'] = matrix['Mode_y'].fillna('')
        matrix['Client Incoterm_y'] = matrix['Client Incoterm_y'].fillna('')
        
        #create that default... this may not be a correct way to handle this. 
        for index, row in matrix.iterrows():
            if row['Origin_x'] != '' and row['Dest_x'] != '' and row['Mode_x']!= '' and row['Client Incoterm_x'] != '':
                matrix.loc[index, 'Origin'] = row['Origin_x']
                matrix.loc[index,'Dest'] = row['Dest_x']
                matrix.loc[index,'Mode'] = row['Mode_x']
                matrix.loc[index,'Client Incoterm'] = row['Client Incoterm_x']
            else:
                matrix.loc[index, 'Origin'] = row['Origin_y']
                matrix.loc[index, 'Dest'] = row['Dest_y']
                matrix.loc[index, 'Mode'] = row['Mode_y']
                matrix.loc[index, 'Client Incoterm'] = row['Client Incoterm_y']

        matrix.drop(['Origin_x', 'Dest_x','Mode_x','Client Incoterm_x',
                     'Origin_y', 'Dest_y', 'Mode_y', 'Client Incoterm_y'
                     ], axis=1, inplace=True)

 #this needs to be adjusted
cols = ['Origin','Dest','Mode','Client Incoterm','lane_id']

cols = cols + quarters

matrix = matrix[cols]
matrix.to_csv(directory+'/matrix_tests/matrix_test_7_27_07.csv',index = False)
