# Migrating Data to and from Spanner with Dataflow

## Overview

In this lab, you ...

## Objectives

In this lab, you learn how to:
* ...

## Setup and Requirements

![[/fragments/start-qwiklab]]

![[/fragments/cloudshell]]

## Task 1. Creating an Orders database

1. On the Google Cloud Console title bar, click __Activate Cloud Shell__ (![cloud shell icon](img/cloud_shell_icon.png)). If prompted, click __Continue__.

2. Run the following command to set your project ID, replacing `<QWIKLABS_PROJECT_ID>` with your Qwiklabs Google Cloud Project ID:

```
gcloud config set project <QWIKLABS_PROJECT_ID>
```

3. Clone to following Git respository and then change to the folder with the Dataflow code. 

```
git clone https://github.com/drehnstrom/spanner-examples
cd spanner-examples/dataflow
```
4. Run the following script to create a Spanner database. 

```
bash ./create-spanner-pets-database.sh
```

5. Run the following command to see the Schema. Notice, in this labe there is just one table and the PetID and OwnerID fields are both intergers not strings. 

```
cat pets-db-schema.sql
```

6. Run the following command to see the data you will import. Notice, the Primay and Foreign keys use counters. As you learned earlier in the course, this is an anti-pattern when using Spanner. To solve this, you will use a Dataflow pipeline written in Apache Beam to reverse the bits of the intergers prior to importing the data into Spanner. This will solve the problem of the integers whiile maintaining the relationships. 

```
cat ./pets.csv
```

7. Click the __Open Editer__ button and open the `spanner-examples/dataflow/csv-to-spanner.py` code file. Notice, the pipeliine is create in the main function. The pipeline reads from the CSV file, then reverses the bits on the PetID, and OwnerID fields, before writing the data to Spanner. 

8. Return to the terminal. Let's try to run this pipeline. First, you need to install the Python prerequisites with the following commands. 

```
pip install apache-beam
pip install apache-beam[gcp]
pip install apache-beam[dataframe]
```

9. Now, run the pipeline. (_This code runs the pipeline locally in Cloud Shell._)

```
python csv-to-spanner.py
```

10. When the pipeline completes, navigate to the Spanner service. Using the console run `SELECT * FROM Pets;` to see the results. 




### **Congratulations!** You have created a database with multiple tables, and used both primary-foreign key contraints and interleaved tables to manage relationships.


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

