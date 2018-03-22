
# coding: utf-8

# In[12]:


from pyspark.sql import SparkSession
import sys
from datetime import datetime


# In[ ]:


app_name = 'highway_gate_data'

spark = SparkSession.builder.appName(app_name).getOrCreate()


# In[33]:


def GetTime(input_date):
    fmt = '%Y%m%d'
    t1 = datetime.strptime(input_date, fmt)
    t2 = int(t1.timestamp() - 3600)
    day_before = datetime.fromtimestamp(t2)
    year = str(day_before.year)
    month = str(day_before.month)
    if(len(month) < 2):
        month = '0'+month
    day = str(day_before.day)
    return year+month+day


# In[ ]:


input_date = sys.argv[1]
output_path = sys.argv[2]
yesterday = GetTime(input_date)

year = input_date[0:4]
month = input_date[4:6]
day = input_date[6:8]
data1 = spark.read.parquet('/user/rawdata/highway/'+yesterday+'/*')
data2 = spark.read.parquet('/user/rawdata/highway/'+input_date+'/*')
all_data = data1.union(data2)
all_data.registerTempTable('temp')
counts = spark.sql("select time, gate, car, count(*) as c from temp where time like '"+year+'-'+month+'-'+day+"%' group by time, gate, car order by time, gate, car")
gate_statistics = counts.rdd.map(lambda x : x[0]+','+x[1]+','+x[2]+','+str(x[3]))
gate_statistics.coalesce(1).saveAsTextFile(output_path)

