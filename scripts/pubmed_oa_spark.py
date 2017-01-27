import os
import re
from glob import glob
from datetime import datetime
import random
import subprocess
import pubmed_parser as pp
from pyspark.sql import Row, SQLContext
from pyspark import SparkConf, SparkContext
from utils import get_update_date

# directory
home_dir = os.path.expanduser('~')
download_dir = os.path.join(home_dir, 'Downloads')
unzip_dir = os.path.join(download_dir, 'pubmed_oa') # path to unzip tar file
save_dir = os.path.join(home_dir, 'Desktop')

def parse_name(p):
    """Turn dataframe from pubmed_parser to list of Spark Row"""
    author_list = p.author_list
    author_table = list()
    if len(author_list) >= 1:
        for author in author_list:
            r = Row(pmc=p.pmc, pmid=p.pmid, last_name=author[0],
                    first_name=author[1], affiliation_id=author[2])
            author_table.append(r)
        return author_table
    else:
        return None

def parse_affiliation(p):
    """Turn dataframe from pubmed_parser to list of Spark Row"""
    affiliation_list = p.affiliation_list
    affiliation_table = list()
    if len(affiliation_list) >= 1:
        for affil in affiliation_list:
            r = Row(pmc=p.pmc, pmid=p.pmid,
                    affiliation_id=affil[0], affiliation=affil[1])
            affiliation_table.append(r)
        return affiliation_table
    else:
        return None

def update():
    """Download and update file"""
    save_file = os.path.join(save_dir, 'pubmed_oa_*_*_*.parquet')
    file_list = list(filter(os.path.isdir, glob(save_file)))
    if file_list:
        d = re.search('[0-9]+_[0-9]+_[0-9]+', file_list[0]).group(0)
        date_file = datetime.strptime(d, '%Y_%m_%d')
        date_update = get_update_date(option='oa')
        # if update is newer
        is_update = date_update > date_file
        if is_update:
            print("MEDLINE update available!")
            subprocess.call(['rm', '-rf', os.path.join(save_dir, 'pubmed_oa_*_*_*.parquet')]) # remove
            subprocess.call(['rm', '-rf', download_dir, 'pubmed_oa'])
            subprocess.call(['wget', 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.A-B.xml.tar.gz', '--directory', download_dir])
            if not os.path.isdir(unzip_dir): os.mkdir(unzip_dir)
            subprocess.call(['tar', '-xzf', os.path.join(download_dir, 'non_comm_use.A-B.xml.tar.gz'), '--directory', unzip_dir])
        else:
            print("No update available")
    else:
        print("Download Pubmed Open-Access for the first time")
        is_update = True
        date_update = get_update_date(option='oa')
        subprocess.call(['wget', 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.A-B.xml.tar.gz', '--directory', download_dir])
        if not os.path.isdir(unzip_dir): os.mkdir(unzip_dir)
        subprocess.call(['tar', '-xzf', os.path.join(download_dir, 'non_comm_use.A-B.xml.tar.gz'), '--directory', unzip_dir])
    return is_update, date_update

def process_file(date_update, fraction=0.01):
    """Process unzipped Pubmed Open-Access folder to parquet file"""
    print("Process Pubmed Open-Access file to parquet with fraction = %s" % str(fraction))
    date_update_str = date_update.strftime("%Y_%m_%d")
    if glob(os.path.join(save_dir, 'pubmed_oa_*.parquet')):
        subprocess.call(['rm', '-rf', 'pubmed_oa_*.parquet']) # remove if folder still exist

    path_all = pp.list_xml_path(unzip_dir)
    if fraction < 1:
        n_sample = int(fraction * len(path_all))
        rand_index = random.sample(range(len(path_all)), n_sample)
        rand_index.sort()
        path_sample = [path_all[i] for i in rand_index]
    else:
        path_sample = path_all

    path_rdd = sc.parallelize(path_sample, numSlices=10000) # use only example path
    parse_results_rdd = path_rdd.map(lambda x: Row(file_name=os.path.basename(x), **pp.parse_pubmed_xml(x)))
    pubmed_oa_df = parse_results_rdd.toDF()
    pubmed_oa_df_sel = pubmed_oa_df[['full_title', 'abstract', 'doi',
                                     'file_name', 'pmc', 'pmid',
                                     'publication_year', 'publisher_id',
                                     'journal', 'subjects']]
    pubmed_oa_df_sel.write.parquet(os.path.join(save_dir, 'pubmed_oa_%s.parquet' % date_update_str),
                                   mode='overwrite')

    parse_name_rdd = parse_results_rdd.map(lambda x: parse_name(x)).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs])
    parse_name_df = parse_name_rdd.toDF()
    parse_name_df.write.parquet(os.path.join(save_dir, 'pubmed_oa_author_%s.parquet' % date_update_str),
                                mode='overwrite')

    parse_affil_rdd = parse_results_rdd.map(lambda x: parse_affiliation(x)).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs])
    parse_affil_df = parse_affil_rdd.toDF()
    parse_name_df.write.parquet(os.path.join(save_dir, 'pubmed_oa_affiliation_%s.parquet' % date_update_str),
                                mode='overwrite')
    print('Finished parsing Pubmed Open-Access subset')

conf = SparkConf().setAppName('pubmed_oa_spark')\
    .setMaster('local[8]')\
    .set('executor.memory', '8g')\
    .set('driver.memory', '8g')\
    .set('spark.driver.maxResultSize', '0')

if __name__ == '__main__':
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    is_update, date_update = update()
    if is_update:
        process_file(date_update)
    sc.stop()
