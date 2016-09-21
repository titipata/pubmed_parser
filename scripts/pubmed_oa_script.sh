#!/bin/bash

echo "\n##########################\n" >> pubmed_oa.log
# wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/comm_use.A-B.xml.tar.gz
# tar -xzf comm_use.A-B.xml.tar.gz --directory data/
# rm comm_use.A-B.xml.tar.gz
echo "Download Open-Access subset $(date)" >> pubmed_oa.log

~/Desktop/spark-2.0.0/bin/spark-submit \
  --master local[8] \
  --driver-memory 8g \
  --executor-memory 8g \
  pubmed_oa_spark.py

echo "Finish saving to parquet file" >> pubmed_oa.log
