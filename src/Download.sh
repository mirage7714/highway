#!/bin/bash
source /home/hadoop/.bashrc
HADOOP_HOME=/usr/local/hadoop
SPARK_HOME=/usr/local/spark
source /usr/local/hadoop/etc/hadoop/hadoop-env.sh
source /usr/local/spark/conf/spark-env.sh

t=`date -d'1 days ago' +"%Y%m%d"`
year=${t:0:4}
m=${t:4:2}
d=${t:6:2}
main=/home/hadoop/code/highway
data_dir=${main}/data
lib_dir=${main}/lib
d_dir=${main}/data/highway_traffic
hdfs_dir=/user/rawdata/highway
log=${main}/logs/process.log

mkdir -p ${data_dir}/${t}
hdfs dfs -mkdir -p ${hdfs_dir}/${t}
cd ${main}
for hour in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
do
url=http://tisvcloud.freeway.gov.tw/history/TDCS/M06A/${t}/${hour}
file=TDCS_M06A_${t}_${hour}0000.csv

wget ${url}/${file}

/usr/local/spark/bin/spark-submit --master local[*] ${lib_dir}/CalHourly.py file:///home/hadoop/code/highway/${file} hdfs:/user/rawdata/highway/${t}/${hour}
mv ${file} ${t}${hour}.csv
gzip ${t}${hour}.csv

mv ${t}${hour}.csv.gz ${data_dir}/${t}

done

bash ${lib_dir}/GateList.sh
