# import pandas as pd
# data = [[10,'nandy', 1000],[11,'nandy 11', 1001],[12,'nandy 12', 1002]]
# headers = ['id','name','price']
# df = pd.DataFrame(data,columns=headers)
# compression_opts = dict(method='zip',archive_name='result.csv')
# df.to_csv(r'/Users/cb-nandkishor/file4.zip',  index=True,compression=compression_opts)
# #df.to_csv(r'/Users/cb-nandkishor/file5.csv', index=False)
# #print df
from chargebeecli.constants.constants import Export_Formats
from chargebeecli.export.Exporter import Exporter

__headers = ['id', 'name', 'price']
__data = [[10, 'nandy', 1000], [11, 'nandy 11', 1001], [12, 'nandy 12', 1002]]
__export_format = Export_Formats.CSV.value

Exporter(__headers, __data).export_data(_path='/Users/cb-nandkishor', _export_format=__export_format, _file_name='abc')
