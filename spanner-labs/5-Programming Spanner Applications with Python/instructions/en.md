# Programming Spanner Applications with Python

## Overview

In this lab, you run the Python code to create Spanner instances and databases. You also see how to create, retrieve, and delete records from databases using both the Google Standard SQL and PostgreSQL dialects. 

## Objectives

In this lab, you learn how to:
* Use Python to create and delete Spanner instances and databases.
* Program Spanner databases that use the PostgreSQL dialect.

## Setup and Requirements

![[/fragments/start-qwiklab]]


![[/fragments/cloudshell]]


## Task 1. Programming Spanner databases with Python

1. Using the Navigation menu in the Google Cloud Console, select  __Dataflow | Workbench__ from the Analytics section. If prompted, __Enable__ the Notebooks API.<div>__Tip:__ You can also search for `Dataflow Workbench` using the Search box in the Console toolbar.

2. From the Workbench page, click the __New Notebook__ button and choose __Apache Beam | Without GPUs__. <div>Name the notebook `my-notebook`, choose the `us-central1` region, and click the __Create__ button.</div><div>___It will take a few minutes for the Notebook instance to be created.___</div>

3. When the instance is ready, click on the __Open Jupyter__ link. This will open Jupyter in another browser tab. <div>From the Jupyter menu, choose __Git__ and __Clone Repository__, paste in the following URL `https://github.com/drehnstrom/spanner-examples`, and click __Clone__.

4. In the file explorer on the left, navigate to `/spanner-examples/colab-notebooks/Spanner_Samples_Python.ipynb` and open that file. 

4. Run the first cell to install the Python Spanner client library. 

5. In the second cell, change the `project_id` variable to your Qwiklabs project ID, and then run the cell. In this cell, some variables are created and the Spanner API is enabled. 

8. Read the text prior to each code cell and run each one. Take the time to understand what the code is doing. 

## Task 2. Programming Spanner databases using the PostgreSQL dialect

1. Open the file: `/spanner-examples/colab-notebooks/Spanner_PostgeSQL.ipynb`.

2. Examine and run each of the steps in the notebook.

### **Congratulations!** You have run the Python code to create Spanner instances and databases. You also saw how to create, retrieve, and delete records from databases using both the Google Standard SQL and PostgreSQL dialects. 


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

