# Utility scripts

This folder is created to hold utility scripts for downloading and
preprocessing [PubMed open-access (OA) subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
 and [MEDLINE XML](https://www.nlm.nih.gov/bsd/licensee/) repository using pyspark version 2.1.

## Running and preprocessing Pubmed Open-Access dataset to Spark Dataframe

To run script to download and process Pubmed Open-Access subset,
change directory in `pubmed_oa_spark.py` and simply run

```bash
~/spark-2.1.0/bin/spark-submit pubmed_oa_spark.py
```

or set up Cronjob by running `crontab -e` (**note** that you might have to
  change editor to what you're using, e.g., `export EDITOR="emacs"`) and add
  these lines to an editor

```bash
#!/bin/bash

0 8 * * Sun source ~/.bash_profile;~/spark-2.1.0/bin/spark-submit pubmed_oa_spark.py
```

## Running and preprocessing MEDLINE dataset to Spark Dataframe

Same as Open-Access, we can modify path in `medline_spark.py` then run

```bash
~/spark-2.1.0/bin/spark-submit medline_spark.py
```

to use Cronjob, follows the same instruction as above.
