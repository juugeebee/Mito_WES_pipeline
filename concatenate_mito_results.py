# Author: Julie BOGOIN

import os
import pandas
from os import listdir
from os.path import isfile, join

path_Data1 = '/media/Data1/jbogoin/Donnees_brutes/hg38/'
path_Data2 = '/media/Data1/jbogoin/Donnees_brutes/hg38/'
path_Data3 = '/media/Data3/jbogoin/Donnees_brutes/hg38/'


folders_Data1 = os.listdir(path_Data1)
folders_Data2 = os.listdir(path_Data2)
folders_Data3 = os.listdir(path_Data3)

li = []

print('\nconcatenate_mito_results program openning.\n')

if os.path.isfile('~/Documents/concat_mito.csv'):
    os.remove('~/Documents/concat_mito.csv')
    print('Previous results file removed.')


for folder in folders_Data1:

    if '_fastq' in folder:
        
        mypath = path_Data1 + folder
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for result in onlyfiles:

            if 'mito_results' in result:

                df = pandas.read_csv((mypath + '/' + result), sep='\t',index_col=None, header=[0])
                df.dropna(how='all')
                run_name = folder.split('_')
                df['run_date'] = run_name[3]
                li.append(df)


for folder in folders_Data2:

    if '_fastq' in folder:
        
        mypath = path_Data2 + folder
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for result in onlyfiles:

            if 'mito_results' in result:

                df = pandas.read_csv((mypath + '/' + result), sep='\t',index_col=None, header=[0])
                df.dropna(how='all')
                run_name = folder.split('_')
                df['run_date'] = run_name[3]
                li.append(df)


for folder in folders_Data3:

    if '_fastq' in folder:
        
        mypath = path_Data3 + folder
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for result in onlyfiles:

            if 'mito_results' in result:

                df = pandas.read_csv((mypath + '/' + result), sep='\t',index_col=None, header=[0])
                df.dropna(how='all')
                run_name = folder.split('_')
                df['run_date'] = run_name[3]
                li.append(df)

concat = pandas.concat(li, axis=0, ignore_index=True)
concat.sort_values(by=['run_date','sample', 'MitoTIP_score'], inplace=True)
concat.reset_index(inplace=True)
del concat['index']

concat['MTscore'] = 'i'
concat.loc[concat.MitoTIP_score=='.', 'MTscore'] = 0
concat.loc[concat.MitoTIP_score!='.', 'MTscore'] = 1

cols = ['run_date', 'sample', 'MitoTIP_score', 'MTscore']
concat = concat[cols]

# pour chaque sample: 
# compter le nombre de variants avec un score MitoTIP:

final = concat.groupby(['run_date','sample'])\
    .agg({'sample' : ['count'], \
    'MTscore' : ['sum']}).reset_index()

print(final)

final.to_csv('~/Documents/concat_mito.csv',index=False)
print("concat_mito.csv generated.\n")

print('concatenate_mito_results program job done.\n')


                
