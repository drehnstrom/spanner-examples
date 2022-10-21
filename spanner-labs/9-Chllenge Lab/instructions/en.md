# Challenge Lab: Administering a Spanner Database

## Overview

In this lab, you use what you learned in class to create, administer, and monitor a Spanner database as you would have to in a real-world environment. There are not step-by-step instructions, so you should refer back to the course notes and earlier labs if you get stuck. 

## Objectives

In this lab, you learn how to:
* Create a Spanner database and import existing data
* Backup and restore the database
* Export Spanner data and import it into BigQuery
* Deploy a data access API that allows access to your Spanner data
* Use the Operations monitorin tools for Dashboards, Uptime Checks and Alerts
* Simulate load on your Spanner database


## Setup and Requirements

![[/fragments/start-qwiklab]]


![[/fragments/cloudshell]]



## Task 1. ...


1. Open Cloud Shell and clone the following GitHub repository: `https://github.com/drehnstrom/spanner-examples`. Then, switch to the `bike-database` folder. 

2. In the `bike-database` folder, there are some CSV files. The data includes regions, which have stations, that have trips. The customer wants this data added to a Spanner database. 

3. First, create the database. You need to:
     * Create the Spanner Instance.
     * Write the DDL code for the database schema.
     * Create the database.
     * Import the data. 

     __Note:__ it is up to you how to accommplish these tasks. You can use the Console, write a Shell script, include some Terraform code. It is your choice. 

4. You will need to administrate the database. Using the course notes and documentation as guides, figure out how to backup the database, and document a restore plan. Practice the restore plan using another Spanner instance. 

st5. The customer wants to use Spanner as the OLTP database, and BigQuery as the OLAP data warehouse. Export the data in Avro format format, and then import it into BigQuery tables. ___You get bonus points if you write a script to do this.___ 

6. A database isn't useful if you cant add data to it. Using the Pets API as a guide, create an API that allows you to add trips to the trips table, and query the trips. <div></div>See the code in the `cloud-run` folder as a template. Deploy this to API to Cloud Run. 

7. An API isn't really useful if it breaks. Use the Operations Monitoring tools to create an Uptime Check and Alert yourself via email if the check fails. 

8. Use curl and a Shell script to simulate load on the database. Go back to Operations and check out the Spanner Dashboard. See how the load affects the database metrics.

     __Note:__ Apache Bench is a better program for simulating load. You can install and use it in Cloud Shell with the following code. The first line installs it; the second line would make 100 requests to Google, 5 at a time. Use similar code to invoke your API. 

```
sudo apt install apache2-utils -y

ab -n 100 -c 5 https://www.google.com/
```

### **Congratulations!** You used what you learned in class to create, administer, and monitor a Spanner database as you would have to in a real-world environment..


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

