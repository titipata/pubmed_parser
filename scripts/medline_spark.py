import os
from glob import glob
import pubmed_parser as pp
from pyspark.sql import Row, SQLContext, Window
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import rank, max, sum, desc

# directory
home_dir = os.path.expanduser('~')
save_dir = os.path.join(home_dir, 'Desktop')
data_dir = os.path.join(home_dir, 'Downloads')
spark_dir = os.path.join(home_dir, 'Desktop/spark-2.0.0')

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = spark_dir

conf = SparkConf().setAppName('medline_spark').setMaster('local[8]')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)


if __name__ == '__main__':

    path_rdd = sc.parallelize(glob(os.path.join(data_dir, 'medline*.xml.gz')), numSlices=1000)
    parse_results_rdd = path_rdd.\
        flatMap(lambda x: [Row(file_name=os.path.basename(x), **publication_dict)
                           for publication_dict in pp.parse_medline_xml(x)])
    medline_df = parse_results_rdd.toDF()
    medline_df.write.parquet(os.path.join(save_dir, 'medline_raw.parquet'),
                             compression='gzip')

    window = Window.partitionBy(['pmid']).orderBy(desc('file_name'))
    windowed_df = medline_df.select(
        max('delete').over(window).alias('is_deleted'),
        rank().over(window).alias('pos'),
        '*')
    windowed_df.\
        where('is_deleted = False and pos = 1').\
        write.parquet(os.path.join(save_dir, 'medline_lastview.parquet'), compression='gzip')

    # parse grant database
    parse_grant_rdd = path_rdd.flatMap(lambda x: pp.parse_medline_grant_id(x))\
        .filter(lambda x: x is not None)\
        .map(lambda x: Row(**x))
    grant_df = parse_grant_rdd.toDF()
    grant_df.write.parquet(os.path.join(save_dir, 'medline_grant.parquet'),
                           compression='gzip')
