# Choosing Primary Keys

## Overview

In this lab, you examine and run the Python code for generating Spanner primary keys in various formats. 

## Objectives

In this lab, you learn how to:
* Generate Spanner primary keys as UUIDs.
* Convert counters and timestamps into values appropriate for Spanner primary keys.

## Setup and Requirements

![[/fragments/start-qwiklab]]


![[/fragments/cloudshell]]


## Task 1. Generating Primary Keys for Spanner Tables

1. Using the Navigation menu in the Google Cloud Console, select  __Dataflow | Workbench__ from the Analytics section. If prompted, __Enable__ the Notebooks API.<div>__Tip:__ You can also search for `Dataflow Workbench` using the Search box in the Console toolbar.

2. From the Workbench page, click the __New Notebook__ button and choose __Apache Beam | Without GPUs__. <div>Name the notebook `my-notebook`, choose the `us-central1` region, and click the __Create__ button.</div><div>___It will take a few minutes for the Notebook instance to be created.___</div>

3. When the instance is ready, click on the __Open Jupyter__ link. This will open Jupyter in another browser tab. <div>From the Jupyter menu, choose __Git__ and __Clone Repository__, paste in the following URL `https://github.com/drehnstrom/spanner-examples`, and click __Clone__.

4. In the file explorer on the left, navigate to `/spanner-examples/colab-notebooks/Spanner_Generating_PK_Values.ipynb` and open that file. 

5. This is a Jupyter notebook with the code for generating primary keys in various formats using Python. Read the text and run the code in each code cell. To run the code in a cell, select it and click the run button from the toolbar. 

### **Congratulations!** You have examined and run the Python code for generating Spanner primary keys in various formats. 


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

