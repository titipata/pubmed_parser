#!/bin/bash

echo "\n##########################\n" >> medline.log
# wget ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/*.gz
# wget ftp://ftp.nlm.nih.gov/nlmdata/.medlease/gz/*.gz
echo "Download MEDLINE $(date)" >> medline.log

~/Desktop/spark-2.0.0/bin/spark-submit \
  --master local[8] \
  --driver-memory 8g \
  --executor-memory 8g \
  medline_spark.py

echo "Finish saving to parquet file" >> medline.log
