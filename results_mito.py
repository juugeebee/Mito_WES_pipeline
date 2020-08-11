# Author: Julie BOGOIN

import os
import pandas as pd

###########
#FUNCTIONS#
###########

VCF_HEADER = ['contig', 'start', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'end', 'FORMAT', 'CN']

def _count_comments(filename):
    comments = 0
    fn_open = gzip.open if filename.endswith('.gz') else open
    with fn_open(filename) as fh:
        for line in fh:
            if line.startswith('#'):
                comments += 1
            else:
                break
    return comments

def dataframe(filename, large=True):
    if large:
        # Set the proper argument if the file is compressed.
        comp = 'gzip' if filename.endswith('.gz') else None
        # Count how many comment lines should be skipped.
        comments = _count_comments(filename)
        # Return a simple DataFrame without splitting the INFO column.
        return pd.read_table(filename, compression=comp, skiprows=comments,
                             names=VCF_HEADER, usecols=range(10))

    # Each column is a list stored as a value in this dict. The keys for this
    # dict are the VCF column names and the keys in the INFO column.
    result = OrderedDict()
    # Parse each line in the VCF file into a dict.
    for i, line in enumerate(lines(filename)):
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i
        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))

    return pd.DataFrame(result)


###########
#PRINCIPAL#
###########

print('\npipelinemito results program openning.\n')

if os.path.isfile('mito_results.csv'):
    os.remove('mito_results.csv')
    print('Previous results file removed.\n')

if os.path.isfile('mito_variants_patho.csv'):
    os.remove('mito_variants_patho.csv')
    print('Previous results file removed.\n')


li = []
la = []

path = '.'
folders = os.listdir(path)

for folder in folders:

    if not 'output' in folder:
        if not '.R1.fastq.gz' in folder:
            if not '.R2.fastq.gz' in folder:

                files = os.listdir(folder)

                for file in files:

                    if '.pathogenic.positions.vcf' in file:
                        df = dataframe((folder + '/' + file), large=True)
                        df.dropna(how='all')
                        sample_name = file.split('.')
                        df['sample'] = sample_name[0]
                        li.append(df)

                    if '.mito.GRCh38.report.tsv' in file: 
                        tsv = pd.read_csv(folder + '/' + file, sep='\t',index_col=None, header=[0])
                        tsv.dropna(how='all')
                        sample_name = file.split('.')
                        tsv['sample'] = sample_name[0]
                        la.append(tsv)

concat = pd.concat(li, axis=0, ignore_index=True)

del concat['FILTER']
del concat['ID']
del concat['REF']
del concat['QUAL']
del concat['FORMAT']
del concat['ALT']
del concat['CN']

if concat.empty == True:
    print("AUCUN VARIANT PATHOGENE N'A ETE DETECTE!")

else: 
    concat.to_csv('mito_variants_patho.csv', index=False)
    print('mito_variants_patho.csv generated.')

report = pd.concat(la, axis=0, ignore_index=True)
report.to_csv('mito_results.csv', sep='\t', index=False)
print('mito_results.csv generated.')

print('\npipelinemito results program job done!\n')