# Creating Spanner Instances and  Databases (CLI and Terraform)

## Overview

In this lab, you automate the creation of Spanner instances and databases using the Google Cloud SDK, the Command Line Interface (CLI), and Terraform.

## Objectives

In this lab, you learn how to:
* Create instances and databases using the gcloud CLI.
* Automate Spanner infrastructure using Terraform.


## Setup and Requirements

![[/fragments/start-qwiklab]]


![[/fragments/cloudshell]]



## Task 1. Create instances and databases using the gcloud CLI


1. On the Google Cloud Console title bar, click __Activate Cloud Shell__ (![cloud shell icon](img/cloud_shell_icon.png)). If prompted, click __Continue__.

2. Run the following command to set your project ID, replacing `<QWIKLABS_PROJECT_ID>` with your Qwiklabs Google Cloud Project ID (_refer back to the lab instructions, and you will find the Project ID in the pane on the left_.):

```
gcloud config set project <QWIKLABS_PROJECT_ID>
```

3. From the Cloud Shell prompt, run the following command to create a Spanner instance named `test-spanner-instance`. <div>Note the parameters for Spanner configuration and capacity. If you are asked to __Authorize__ the command, then do so. </div>

```
gcloud spanner instances create test-spanner-instance --config=regional-us-central1 --description="test-spanner-instance" --processing-units=100
```

4. The command should not take long. In the Console, navigate to the Spanner service and verify the instance was created. <div>To see the instance, you could also run the command below. Try that now. </div>

```
gcloud spanner instances list
```

5. Before creating the Pets database, you need a file that contains the DDL code. Type the following command to create the file and open it in the nano code editor. 

```
nano pets-db-schema.sql
```

6. Paste the following code into Nano. Type `Ctrl+X`, then `Y`, and then press the ENTER key to save the file. 

```
CREATE TABLE Owners (
     OwnerID STRING(36) NOT NULL, 
     OwnerName STRING(MAX) NOT NULL
) PRIMARY KEY (OwnerID);

CREATE TABLE Pets (
     PetID STRING(36) NOT NULL, 
     OwnerID STRING(36) NOT NULL, 
     PetType STRING(MAX) NOT NULL,
     PetName STRING(MAX) NOT NULL,
     Breed STRING(MAX) NOT NULL,
) PRIMARY KEY (PetID);
```

6. Now that you have the Schema file, run the following command to create the database. 

```
gcloud spanner databases create pets-db --instance=test-spanner-instance --database-dialect=GOOGLE_STANDARD_SQL --ddl-file=./pets-db-schema.sql
```

7. Insert an Owner and all of the dogs owned. The primary keys for Owners and Pets use UUIDs. Enter the following command to create a UUID for the owner and store it in a variable. 

```
owner_uuid=$(cat /proc/sys/kernel/random/uuid)
echo $owner_uuid
```

8. Insert the Owner Doug. <div>__Note:__ the `--data` parameter that allows you to pass the fields in name-value pairs. </div>

```
gcloud spanner rows insert --table=Owners --database=pets-db --instance=test-spanner-instance --data=OwnerID=$owner_uuid,OwnerName=Doug
```

9. Insert all of Doug's dogs with the following commands. 

```
gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Rusty',PetType='Dog',Breed='Poodle'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Duchess',PetType='Dog',Breed='Terrier'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Gretyl',PetType='Dog',Breed='Shepherd'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Gigi',PetType='Dog',Breed='Retriever'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Noir',PetType='Dog',Breed='Schnoodle'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Bree',PetType='Dog',Breed='Mutt'
```

10. Let's see if it worked. Run the following query. 

```
gcloud spanner databases execute-sql pets-db --instance=test-spanner-instance --sql='SELECT o.OwnerName, p.PetName, p.PetType, p.Breed FROM Owners as o JOIN Pets AS p ON o.OwnerID = p.OwnerID' 
```

11. Go to the Console and find the instance, database, tables, and run a query to see the data, or click on the __Data__ menu on the side navigation bar once you select the table.

12. Delete the database with the following command. 

```
gcloud spanner databases delete pets-db --instance=test-spanner-instance 
```

13. In the Console, verify the database was deleted. 

14. Lastly, delete the instance with the following command. 

```
gcloud spanner instances delete test-spanner-instance --quiet
```

__Note:__ The `--quiet` parameter runs the command without prompting the user. This could have been added to the prior command as well. This is usefull if you are writing an automated pipeline and there would be no user to ask. 

15. In the Console, verify that the instance was deleted. 

## Task 2. Automate Spanner infrastructure using Terraform

1. Create a folder for your Terraform files and change to it using the following commands.

```
mkdir terraform-spanner
cd terraform-spanner
```

2. You need a number of files for the Terraform module. Run the following command to create the empty files. 

```
touch main.tf provider.tf terraform.tfvars variables.tf
```

3. Click the __Open Editor__ button to open the code editor. From the Explorer pane on the left, find the `terraform-spanner` folder you just created and expand it. Select the `provider.tf` file to open it in the editor and add the following code to it. 

```
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```
__Note:__ The code in the Terraform block downloads the Google provider from Hashicorp's website. The code in the provider block configures the provider to use the correct Project ID and Region which you set as variables later. 

4. Open the file `main.tf` and add the following resource block. This code creates the Spanner instance. 

```
resource "google_spanner_instance" "db-instance" {
  name             = "terraform-spanner-instance"
  config           = "regional-${var.region}"
  display_name     = "TF Spanner Instance"
  processing_units = var.processing_units
  force_destroy = var.force_destroy
}
```

5. In the same file, below the previous code, add the following which creates the Pets database. Note the DDL code which defines the tables. 

```
resource "google_spanner_database" "test-database" {
  instance            = google_spanner_instance.db-instance.name
  name                = "pets-db"
  # Can't run destroy unless set to false
  deletion_protection = var.deletion_protection 

  ddl = [
    "CREATE TABLE Owners (OwnerID STRING(36) NOT NULL, OwnerName STRING(MAX) NOT NULL) PRIMARY KEY (OwnerID)",
    "CREATE TABLE Pets (PetID STRING(36) NOT NULL, OwnerID STRING(36) NOT NULL, PetType STRING(MAX) NOT NULL, PetName STRING(MAX) NOT NULL, Breed STRING(MAX) NOT NULL) PRIMARY KEY (PetID)",
  ]
}
```

5. Open the file `variables.tf`. In this file, you declare the variables used in the Terraform module. Add the following code. 

```
variable "deletion_protection" {
  description = "If set to true, you cannot run terraform destroy if there are databases created."
  type        = bool
  default     = false
}

variable "force_destroy" {
    description = "If set to true, running terraform destroy will delete all backups."
  type    = bool
  default = true
}

variable "processing_units" {
  type    = number
  default = 100
}

variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "region" {
  type = string
}
```

6. All the variables except for `project_id` and `region` have defaults. You use the `terraform.tfvars` file to set those variable values. Open that file and add the following. 

```
project_id = "YOUR-PROJECT-ID-HERE"
region = "us-central1"
```

__Note:__ You must enter your Google Cloud Project ID where indicated. You can find your Project ID in the Console by navigating to the __Cloud overview__ page. It will start with "qwiklabs-" not your User ID that starts with "student-".


7. Let's see if it works. Click the __Open Terminal__ button. Note, you may have to switch back to the original tab first if your Editor opened a new tab or window. At the command prompt, enter the following. 

```
terraform init
```

8. Assuming there were no errors with the previous command, enter the following and analyze the output. It should say that two resources will be added. 

```
terraform plan
```

9. Lasty, enter the following command to create the Spanner instance and Pets database. You must type `yes` when prompted. 

```
terraform apply 
```

10. Wait for the Terraform command to complete. In the Console, navigate to the Spanner service and verify that the instance and database were created. There is no refresh button, so you may need to click on another product and then return to Spanner to refresh the instances list.

11. Return to the terminal and enter the following command to delete the Spanner instance. 

```
terraform destroy -auto-approve
```

### **Congratulations!** You have automated the creation of Spanner instances and databases using the Google Cloud SDK, the Command Line Interface (CLI), and Terraform.


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

