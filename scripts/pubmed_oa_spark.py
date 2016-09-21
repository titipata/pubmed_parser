import os
import pubmed_parser as pp
from pyspark.sql import Row, SQLContext
from pyspark import SparkConf, SparkContext

# directory
home_dir = os.path.expanduser('~')
save_dir = os.path.join(home_dir, 'Desktop')
data_dir = os.path.join(home_dir, 'Downloads/data/')
spark_dir = os.path.join(home_dir, 'Desktop/spark-2.0.0')

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = spark_dir

conf = SparkConf().setAppName('pubmed_oa_spark').setMaster('local[8]')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def parse_name(p):
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


if __name__ == '__main__':

    path_all = pp.list_xml_path(data_dir)
    path_rdd = sc.parallelize(path_all[0:1000], numSlices=10000) # example path
    print(path_all[0:10])
    parse_results_rdd = path_rdd.map(lambda x: Row(file_name=os.path.basename(x), **pp.parse_pubmed_xml(x)))
    pubmed_oa_df = parse_results_rdd.toDF()
    pubmed_oa_df_sel = pubmed_oa_df[['full_title', 'abstract', 'doi',
                                     'file_name', 'pmc', 'pmid',
                                     'publication_year', 'publisher_id',
                                     'journal', 'subjects']]
    pubmed_oa_df_sel.write.parquet(os.path.join(save_dir, 'pubmed_oa.parquet'),
                                   compression='gzip')

    parse_name_rdd = parse_results_rdd.map(lambda x: parse_name(x)).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs])
    parse_name_df = parse_name_rdd.toDF()
    parse_name_df.write.parquet(os.path.join(save_dir, 'pubmed_oa_author.parquet'),
                                compression='gzip')

    parse_affil_rdd = parse_results_rdd.map(lambda x: parse_affiliation(x)).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs])
    parse_affil_df = parse_affil_rdd.toDF()
    parse_name_df.write.parquet(os.path.join(save_dir, 'pubmed_oa_affiliation.parquet'),
                                compression='gzip')
    print('Finished parsing Pubmed Open-Access subset')
