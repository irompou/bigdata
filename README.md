# Big Data Project

## Overview
This project is part of the 7th semester's course *Business Intelligence and 
Big Data Analysis* of the *Department of Management Science and Technology* 
of the *Athens University of Economics and Business*.

The subject of the project is to emulate a big data analysis scenario, 
containing as many as possible systems and tasks of such a workflow.

In order to construct and analyze this workflow we are going to split the task
into various steps:

1. Selection/Retrieval of a large Dataset
2. ETL actions over this Dataset
3. OLAP Cubes design and implemention
4. OLAP Analysis through MDX queryies and other methods
5. Other Big Data Analysis Methods (Categorization, Regression, Clustering)
6. MapReduce Jobs

### Students

- Valerios Chatzigeorgiou (8100167)
- Ioanna Rompou (8100110)

### Requirements/Dependencies/Build
If you're planning to emulate all the steps taken in order to build the project
and see the results yourself, you have to make sure that you have the following
packages/programs/runtimes installed:

- 7zip installed and the 7z.exe in your PATH
- Python 3.5
  * Install all the requirments by running `pip install -r requirements.txt`
- Oracle's VirtualBox with the following VMs setup:
  * Microsoft Windows Server 2012 w/ SQL Server 2012 Standard Edition installed
    (or any other edition that supports SSAS)
  * Some Linux distribution running a Hadoop cluster

To build everything, `git clone` or download and extract a ZIP of the repository
in a folder and try to follow along the steps described below. This is not 
meant to be a proper step-by-step guide, however most of the tools and 
procedures that are being used are pretty straightforward (everything that we 
run is just scripts, so if you find something that doesn't work as you expected 
you can just see for yourself what happens inside the script, there is no 
recompile or build required).

## 1. Dataset Selection/Retrieval
We are going to use [Stackexchange's annual data dumps](https://archive.org/details/stackexchange) 
as the Dataset we are going to examine and mine our data from.

Stackexchange besides having a main portal/site under [Stackoverflow.com](stackoverflow.com) 
serving general questions of programming community, also contains a plethora of
smaller sub-portals focused on specific areas of Computer Science and other 
fields as well.

We came across various of these sub-portals and ended up selecting three of 
them that are closely related to Data Science:

- [Data Science](datascience.stackexchange.com) ([~5MB compressed / ~25MB decompressed](https://archive.org/download/stackexchange/datascience.stackexchange.com.7z))
- [DBA](dba.stackexchange.com) ([~100MB compressed / ~600MB decompressed](https://archive.org/download/stackexchange/dba.stackexchange.com.7z))
- [Statistics](stats.stackexchange.com) ([~160MB / ~900MB decompressed](https://archive.org/download/stackexchange/stats.stackexchange.com.7z))

It could be possible to analyze the main site (stackoverflow.com), however this
particular data dump is a seperate **7.2GB compressed file**, so it would be 
quite impractical to do so in a contained environment such as the one we 
plan to use (Multiple Virtual Machines).

### Data Description/Schema
The data that Stackoverflow provides closely ressemble the database schema that
is used internally for storage of the content served on the portals. The
detailed schema of the dump is available in a [meta.stackexchange.com post.](http://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede)
The data dumps consist of 8 XML files containing organized data of various 
entities that make up a Stackexchange site:

- Users.xml
- Posts.xml
- Tags.xml
- Comments.xml
- Votes.xml
- Badges.xml
- PostLinks.xml
- PostHistory.xml

## 2. ETL
For the extraction, transformation and loading of the data we are going to use 
mainly Python scripts and TSQL queries. This is actually all we are going to 
need, since most of the data is already in a proper and parsable form (XML).

### Extraction
The main script that is being used for the extraction of the data is [dataset.py](./dataset.py).
Running `python dataset.py --help` gives us the available options for 
downloading and extracting the desired datasets into temporary folders.
These


### Transformation


### Loading

#### XML Import

- [SO 1](http://stackoverflow.com/questions/3989395/convert-xml-to-table-sql-server)
- [SO 2](http://stackoverflow.com/questions/7649301/select-data-from-xml-file-as-table-in-tsql)


## 3. OLAP Cubes

- SSAS Schema/Cubes


## 4. MDX Queries and Other Methods

...


## 5. Other Big Data Analysis Methods

- Categorization
- Regression
- Clustering
 

## 6. MapReduce Jobs

- Hadoop & Spark! :)
