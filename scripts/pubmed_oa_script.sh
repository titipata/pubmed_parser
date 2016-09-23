#!/bin/bash

~/Desktop/spark-2.0.0/bin/spark-submit \
  --master local[8] \
  --driver-memory 8g \
  --executor-memory 8g \
  pubmed_oa_spark.py
