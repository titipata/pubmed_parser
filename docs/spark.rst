Setting up PySpark with Pubmed Parser
=====================================


We put small snippet to setup Spark 2.1 on Jupyter Notebook here for initializing the notebook. 
We use Spark workflow to process MEDLINE XML data to Spark dataframe. **Note** that the path to downloaded Spark might be different.

.. code-block:: python

    import os
    import findspark
    findspark.init(spark_home="/opt/spark-2.1.0-bin-cdh5.9.0/")


In Spark 2.1, `spark` in this case can use as `sparkContext` and has access to `parallelize` or `createDataFrame` already.

.. code-block:: python

    from pyspark.sql import SparkSession
    from pyspark.conf import SparkConf

    conf = SparkConf().\
        setAppName('map').\
        setMaster('local[5]').\
        set('spark.yarn.appMasterEnv.PYSPARK_PYTHON', '~/anaconda3/bin/python').\
        set('spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON', '~/anaconda3/bin/python').\
        set('executor.memory', '8g').\
        set('spark.yarn.executor.memoryOverhead', '16g').\
        set('spark.sql.codegen', 'true').\
        set('spark.yarn.executor.memory', '16g').\
        set('yarn.scheduler.minimum-allocation-mb', '500m').\
        set('spark.dynamicAllocation.maxExecutors', '3').\
        set('spark.driver.maxResultSize', '0')

    spark = SparkSession.builder.\
        appName("testing").\
        config(conf=conf).\
        getOrCreate()
