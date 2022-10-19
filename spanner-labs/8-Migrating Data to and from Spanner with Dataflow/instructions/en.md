# Migrating Data to and from Spanner with Dataflow

## Overview

In this lab, you use Dataflow and Apache Beam to migrate data into Spanner.

## Objectives

In this lab, you learn how to:
* Write ETL pipelines using Apache Beam
* Run Apache Beam piplines using Google Cloud Dataflow

## Setup and Requirements

![[/fragments/start-qwiklab]]

![[/fragments/cloudshell]]

## Task 1. Creating an Apache Beam Pipeline to import data into Spanner

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

5. Run the following command to see the Schema. Notice, in this lab there is just one table, and the PetID and OwnerID fields are both intergers not strings. 

```
cat pets-db-schema.sql
```

6. Run the following command to see the data you will import. Notice, the Primay and Foreign keys use counters. As you learned earlier in the course, this is an anti-pattern when using Spanner. <div>To solve this, you will use a Dataflow pipeline written in Apache Beam to reverse the bits of the intergers prior to importing the data into Spanner.</div> <div>This will solve the problem of the integers while maintaining the relationships. </div>

```
cat pets.csv
```

7. Click the __Open Editor__ button and open the file `spanner-examples/dataflow/csv-to-spanner.py` code file. Notice, the pipeliine is create in the main function (___lines 53 to 68___). <div>The pipeline reads from the CSV file, then reverses the bits on the PetID, and OwnerID fields, before writing the data to Spanner. </div><div>___The `reverse_bits` function begins at line 21.___</div>  

8. Return to the terminal. Let's try to run this pipeline. First, you need to install the Python prerequisites with the following commands. 

```
pip install apache-beam[gcp]==2.41.0
pip install apache-beam[dataframe]
```

9. Now, run the pipeline. (_This code runs the pipeline locally in Cloud Shell._)

```
python csv-to-spanner.py
```

10. When the pipeline completes, navigate to the Spanner service. Using the console run `SELECT * FROM Pets;` to see the results. 

11. Again using the console, run `DELETE FROM Pets WHERE 1=1;` to delete all the data you just added. Next, you will run the code using the Dataflow service. 

# Task 1. Running a Dataflow Job

1. To run the Job using Dataflow, you will need a Cloud Storage bucket for inputs, staging, and outputs. Use the commange below to create a bucket that contains your Project ID (_this should guarantee a unique name for the bucket_). Also, copy the `pets.csv` file into the bucket. 

```
gsutil mb -l us-central1 gs://$DEVSHELL_PROJECT_ID-data-flow
gsutil cp ./pets.csv gs://$DEVSHELL_PROJECT_ID-data-flow
```

2. Navigate to Cloud Storage in the Console and verify that the bucket was created and the file was copied. 

3. Run the following command to ensure the Dataflow API is enabled in your project. 

```
gcloud services enable dataflow.googleapis.com
```
4. Now, run the pipeline using Dataflow with the following command. 

```
python csv-to-spanner.py \
    --region us-central1 \
    --input gs://$DEVSHELL_PROJECT_ID-data-flow/pets.csv \
    --output gs://$DEVSHELL_PROJECT_ID-data-flow/results/outputs \
    --runner DataflowRunner \
    --project $DEVSHELL_PROJECT_ID \
    --temp_location gs://$DEVSHELL_PROJECT_ID-data-flow/tmp/
```

5. As you did before, check to see if the data was added to your Spanner database. 

6. Delete the Spanner instance so we are no longer being charged for it. 

### **Congratulations!** You used Dataflow and Apache Beam to migrate data into Spanner.


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

