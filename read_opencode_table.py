import pandas 

filename = 'opencode_table.csv'
chunksize = 10 ** 6
for chunk in pandas.read_csv(filename, chunksize=chunksize):
    print(chunk)
