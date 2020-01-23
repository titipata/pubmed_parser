Setting up Pubmed Parser with PySpark
=====================================


Below, we put a small snippet to setup ``Spark 2.1`` on Jupyter Notebook. 
We can use PySpark as a workflow to process MEDLINE XML data to Spark dataframe. 
Using PySpark can reduce parsing time of more than 25 million documents to less than 10 minutes when you have multiple core processors.

**Note** that the ``spark_home`` path to downloaded Spark might be different.

.. code-block:: python

    import os
    import findspark
    findspark.init(spark_home="/opt/spark-2.1.0-bin-cdh5.9.0/")


In Spark 2.1, ``spark`` in this case can use as ``sparkContext`` which has access to ``parallelize`` or ``createDataFrame``.

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


Please see the full implementation details in `scripts <https://github.com/titipata/pubmed_parser/tree/master/scripts>`_ folder on the repository.

We will update the documentation on how to incorporate Pubmed Parser with `dask <https://dask.org/>`_ soon.