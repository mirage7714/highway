
# coding: utf-8

from pyspark.sql import SparkSession, Row
from pyspark import SparkConf, SparkContext
import sys

app_name = 'hourly_data'
conf = SparkConf()
conf.setAppName(app_name)
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

input_data = sys.argv[1]
output_data = sys.argv[2]

data = spark.read.text(input_data).rdd.map(lambda x : x[0]).map(lambda x : x.split(',')).map(lambda x : x[0]+','+x[5]+','+str(len(x[7].split(';')))+','+x[7])
list_data = data.collect()
list_data1 = []
for d in list_data:
    gates = d.split(',')[3].split(';')
    count = d.split(',')[2]
    car = d.split(',')[0]
    dist = d.split(',')[1]
    for g in gates:
        gg = g.strip().split('+')[1]
        time = g.strip().split('+')[0]
        hour = time.split(':')[0]
        list_data1.append(car+','+dist+','+count+','+hour+':00:00,'+gg)
o_data = sc.parallelize(list_data1)
df_data = o_data.map(lambda x : x.split(',')).map(lambda x : Row(car = x[0], distance = float(x[1]), counts = int(x[2]), time = x[3], gate = x[4])).toDF()
df_data.write.parquet(output_data)


