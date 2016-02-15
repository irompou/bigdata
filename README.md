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
in a folder and try to follow along the steps described below.  This is not 
meant to be a proper step-by-step guide, however most of the tools and 
procedures that are being used are pretty straightforward (everything that we 
run is just scripts, so if you find something that doesn't work as you expected 
you can just see for yourself what happens inside the script, there is no 
recompile or build required). 

We assume that all of these scripts/tools are being run from a user that has 
access to the related resources (Databases, Files, Internet Connection, etc.)
in the system that is being used.

## 1. Dataset Selection/Retrieval
We are going to use [Stackexchange's annual data dumps](https://archive.org/details/stackexchange) 
as the Dataset we are going to examine and mine our data from.

Stackexchange besides having a main portal/site under [Stackoverflow.com](https://stackoverflow.com) 
serving general questions of programming community, also contains a plethora of
smaller sub-portals focused on specific areas of Computer Science and other 
fields as well.

We came across various of these sub-portals and ended up selecting three of 
them that are closely related to Data Science:

- [Data Science](https://datascience.stackexchange.com) ([~5MB compressed / ~25MB decompressed](https://archive.org/download/stackexchange/datascience.stackexchange.com.7z))
- [DBA](https://dba.stackexchange.com) ([~100MB compressed / ~600MB decompressed](https://archive.org/download/stackexchange/dba.stackexchange.com.7z))
- [Statistics](https://stats.stackexchange.com) ([~160MB / ~900MB decompressed](https://archive.org/download/stackexchange/stats.stackexchange.com.7z))

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
mainly Python scripts and TSQL queries.  This is actually all we are going to 
need, since most of the data is already in a proper and parsable form (XML).

The Python scripts run much like simple CLI tools with a simple description 
of their usage through the `--help` option.

### Extraction
The main script that is being used for the extraction of the data is [dataset.py](./dataset.py).
Running `python dataset.py --help` gives us the available options for 
downloading and extracting the desired datasets into temporary folders.

The first step should be to `download` the data (either from one of the three
datasets that we chose, or directly from a specified URL with the `-u` option).
At the end of the step the path to the downloaded file is printed out.

The next step is to extract the data through the `extract PATH` command and 
provide the path to the downloaded file.

Depending on how fast or slow your internet connection and CPU is, the 
download and extraction operations should take time relative to the size of the
dataset that you have chosen.

At the end of these two tasks we should have a `data` folder containing 8 XML 
files.  The `tmp` folder is also kept around with the downloaded files.

### Transformation
Our untouched dataset currently is in the perfect state to be imported/loaded to
an RDBMS that supports insertion of data from parsed XML files. Dates are 
represented in the ISO-8601 format, all numeric types are of type integer, 
the files are UTF-8 encode, and long text values (such as question bodies) 
are already represented as processed HTML.  The only *choice* we currently have 
is to only select the data that we are interested in.

We have chosen to use the following data entities from our dataset:

- Users
- Posts
- Comments
- Votes
- Tags
- Badges

This means that we are only going to use the respective XML files only.

*(Note: Claiming that the dataset did not have the need to be 'cleaned' or 
processed in any way is indeed a stretch. Further down we will find ourselves 
with the need to delete some records in order to keep our data consistent, 
but for reasons that we couldn't possibly yet know.)*

### Loading
The RDBMS where we are going to store our data is MS SQL Server 2012. 
Thankfully, it has built-in parsing of XML data and thus, all the insertions can 
be done through TSQL and functions that extract values from the parsed XML.

#### XML Import
Using functions and methods described in the following Stackoverflow links and 
some horrible documentation on SQL Server from the MSDN website, we can see 
that loading an XML file and inserting it to the a table through `INSERT`
statements is done pretty easily if one knows the exact schema of the XML 
data, and the tables that are going to be used.

- [Stackoverflow Question 1](http://stackoverflow.com/questions/3989395/convert-xml-to-table-sql-server)
- [Stackoverflow Question 2](http://stackoverflow.com/questions/7649301/select-data-from-xml-file-as-table-in-tsql)
- [MSDN Documentation](http://msdn.microsoft.com)

We have carefully designed and described the tables that we are going to use 
in the [create_tables.sql](./sql/create_tables.sql) file.

For the import process we have implemented all the necessary steps in the 
[import.sql](./sql/import.sql) file.

##### Temp Tables
One brief note that should be mentioned here, is that in order to import such 
data into a Relational Database that follows certain contraints and rules 
inside and between its various relations (tables), one must be certain that 
there are no inconsistencies present in the raw source dataset.  Entities that 
depend on other entities through foreign key constraints were a kind of 
constraint that this particular dataset had plenty of.  Votes and Comments 
depend on Posts, and Posts depend on Users through their respective primary 
keys.

In order to achieve consistency, we had to clean the data, but this could only
be made possible after the insertion of the data in the database.  Processing 
XML data is a slow task that we can easily avoid, by using temporary tables.

The issue that came up was that some Votes depended on Posts that didn't exist, 
because they had been deleted/moved/edited in such a way that their primary key 
no longer existed.  This issue came up as Foreign Key Constraint Conflict when 
we tried to initially import the Votes data.

For the problematic recordsets, and more particularly the 'Votes' recordset, we
initially imported the dataset into a temporary table, that had exactly the 
same columns as the 'final' table, but didn't include any of the constraints 
that we had issues with (Foreign Key Constraints, in this particular case).

After doing so, we could query the temporary Votes table against the already 
imported Posts and find out which vote records didn't realte to any existing 
Post. We proceeded with deleting these records and then transfering all the 
valid data to the final Votes table.  The temporary votes table was then dropped 
(although SQL Server is supposed to do so automatically after a while).

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
