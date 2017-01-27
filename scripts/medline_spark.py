import os
import re
from glob import glob
from datetime import datetime
import subprocess
import pubmed_parser as pp
from pyspark.sql import Row, SQLContext, Window
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import rank, max, sum, desc
from utils import get_update_date

# directory
home_dir = os.path.expanduser('~')
download_dir = os.path.join(home_dir, 'Downloads', 'medline')
save_dir = os.path.join(home_dir, 'Downloads')

def update():
    """Download and update file"""
    save_file = os.path.join(save_dir, 'medline*_*_*_*.parquet')
    file_list = list(filter(os.path.isdir, glob(save_file)))
    if file_list:
        d = re.search('[0-9]+_[0-9]+_[0-9]+', file_list[0]).group(0)
        date_file = datetime.strptime(d, '%Y_%m_%d')
        date_update = get_update_date(option='medline')
        # if update is newer
        is_update = date_update > date_file
        if is_update:
            print("MEDLINE update available!")
            subprocess.call(['rm', '-rf', os.path.join(save_dir, 'medline_*.parquet')]) # remove
            subprocess.call(['rm', '-rf', download_dir])
            # only example for 3 files, change to ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/*.xml.gz to download all
            subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0001.xml.gz', '--directory', download_dir])
            subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0166.xml.gz', '--directory', download_dir])
            subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0718.xml.gz', '--directory', download_dir])
        else:
            print("No update available")
    else:
        print("Download MEDLINE for the first time")
        is_update = True
        date_update = get_update_date(option='medline')
        subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0001.xml.gz', '--directory', download_dir])
        subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0166.xml.gz', '--directory', download_dir])
        subprocess.call(['wget', 'ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/medline16n0718.xml.gz', '--directory', download_dir])
    return is_update, date_update

def process_file(date_update):
    """Process downloaded MEDLINE folder to parquet file"""
    print("Process MEDLINE file to parquet")
    # remove if folder still exist
    if glob(os.path.join(save_dir, 'medline_*.parquet')):
        subprocess.call(['rm', '-rf', 'medline_*.parquet'])

    date_update_str = date_update.strftime("%Y_%m_%d")
    path_rdd = sc.parallelize(glob(os.path.join(download_dir, 'medline*.xml.gz')), numSlices=1000)
    parse_results_rdd = path_rdd.\
        flatMap(lambda x: [Row(file_name=os.path.basename(x), **publication_dict)
                           for publication_dict in pp.parse_medline_xml(x)])
    medline_df = parse_results_rdd.toDF()
    medline_df.write.parquet(os.path.join(save_dir, 'medline_raw_%s.parquet' % date_update_str),
                             mode='overwrite')

    window = Window.partitionBy(['pmid']).orderBy(desc('file_name'))
    windowed_df = medline_df.select(
        max('delete').over(window).alias('is_deleted'),
        rank().over(window).alias('pos'),
        '*')
    windowed_df.\
        where('is_deleted = False and pos = 1').\
        write.parquet(os.path.join(save_dir, 'medline_lastview_%s.parquet' % date_update_str),
                      mode='overwrite')

    # parse grant database
    parse_grant_rdd = path_rdd.flatMap(lambda x: pp.parse_medline_grant_id(x))\
        .filter(lambda x: x is not None)\
        .map(lambda x: Row(**x))
    grant_df = parse_grant_rdd.toDF()
    grant_df.write.parquet(os.path.join(save_dir, 'medline_grant_%s.parquet' % date_update_str),
                           mode='overwrite')

conf = SparkConf().setAppName('medline_spark')\
    .setMaster('local[8]')\
    .set('executor.memory', '8g')\
    .set('driver.memory', '8g')\
    .set('spark.driver.maxResultSize', '0')

if __name__ == '__main__':
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    is_update, date_update = update()
    if is_update or not glob(os.path.join(save_dir, 'medline_*.parquet')):
        process_file(date_update)
    sc.stop()
