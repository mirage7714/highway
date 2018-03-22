#!/bin/bash
main_dir=/home/hadoop/code/highway/
lib_dir=${main_dir}/lib
data_dir=${main_dir}/data/gates
day=`date +"%Y%m%d"`

url="https://www.freeway.gov.tw/Upload/DownloadFiles/%e5%9c%8b%e9%81%93%e8%a8%88%e8%b2%bb%e9%96%80%e6%9e%b6%e5%ba%a7%e6%a8%99%e5%8f%8a%e9%87%8c%e7%a8%8b%e7%89%8c%e5%83%b9%e8%a1%a8.csv"
cd ${main_dir}
wget ${url} -O ${day}.csv

mv ${day}.csv ${data_dir}/
