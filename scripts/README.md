# Utility scripts

This folder is created to hold utility scripts for downloading and
preprocessing [PubMed open-access (OA) subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
 and [MEDLINE XML](https://www.nlm.nih.gov/bsd/licensee/) repository using pyspark.

## Running and preprocessing Pubmed Open-Access dataset to Spark Dataframe

To run script to download and process Pubmed Open-Access subset,
change directory in `pubmed_oa_spark.py` and simply run

```bash
source pubmed_oa_script.sh
```

or set up Cronjob by running `crontab -e` (**note** that you might have to
  change editor to what you're using, e.g., `export EDITOR="emacs"`) and add
  these lines to an editor

```bash
#!/bin/bash

0 8 * * Sun source ~/.bash_profile;source pubmed_oa_script.sh
```

## Running and preprocessing MEDLINE dataset to Spark Dataframe

Same as Open-Access, we can modify path in `medline_spark.py` then run

```bash
source medline_script.sh
```

to use Cronjob, follows the same instruction as above.
