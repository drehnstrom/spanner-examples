# Deploying Spanner Applications with Cloud Functions and Cloud Run

## Overview

In this lab, you write applications that utilize Spanner databases, and deploy them to both Cloud Functions and Cloud Run. You also install, configure, and enable the Spanner emulator for use in development environments. 

## Objectives

In this lab, you learn how to:
* Deploy Cloud Functions that read and write to Spanner databases.
* Set up and use the Spanner emulator for development.
* Build a REST API that allows you to read and write Spanner data.
* Deploy a REST API to Google Cloud Run.


## Setup and Requirements

![[/fragments/start-qwiklab]]


![[/fragments/cloudshell]]


## Task 1. Create a database with test data

1. On the Google Cloud Console title bar, click __Activate Cloud Shell__ (![cloud shell icon](img/cloud_shell_icon.png)). If prompted, click __Continue__.

2. Run the following command to set your project ID, replacing `<QWIKLABS_PROJECT_ID>` with your Qwiklabs Google Cloud Project ID. <div>If you are asked to __Authorize__ the command, then do so. </div>

```
gcloud config set project <QWIKLABS_PROJECT_ID>

gcloud services enable cloudbuild.googleapis.com
```

3. Run the following Bash command to create a schema file for the Pets database. 

```
mkdir ~/lab-files
cd ~/lab-files

cat > ./pets-db-schema.sql << ENDOFFILE
CREATE TABLE Owners (
     OwnerID STRING(36) NOT NULL, 
     OwnerName STRING(MAX) NOT NULL
) PRIMARY KEY (OwnerID);

CREATE TABLE Pets (
    OwnerID STRING(36) NOT NULL, 
    PetID STRING(MAX) NOT NULL,     
    PetType STRING(MAX) NOT NULL,
    PetName STRING(MAX) NOT NULL,
    Breed STRING(MAX) NOT NULL,
) PRIMARY KEY (OwnerID,PetID),
INTERLEAVE IN PARENT Owners ON DELETE CASCADE
ENDOFFILE
```

4. Run the following commands to create a Spanner instance and database. 

```
gcloud spanner instances create test-spanner-instance --config=regional-us-central1 --description="test-spanner-instance" --processing-units=100

gcloud spanner databases create pets-db --instance=test-spanner-instance --database-dialect=GOOGLE_STANDARD_SQL --ddl-file=./pets-db-schema.sql

```

5. Add a few test records to the database with the following commands. 

```
owner_uuid=$(cat /proc/sys/kernel/random/uuid)

gcloud spanner rows insert --table=Owners --database=pets-db --instance=test-spanner-instance --data=OwnerID=$owner_uuid,OwnerName=Doug

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Noir',PetType='Dog',Breed='Schnoodle'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Bree',PetType='Dog',Breed='Mutt'

gcloud spanner rows insert --table=Pets --database=pets-db --instance=test-spanner-instance --data=PetID=$(cat /proc/sys/kernel/random/uuid),OwnerID=$owner_uuid,PetName='Gigi',PetType='Dog',Breed='Retriever'
```

## Task 2. Create a Cloud Function to read from Spanner

1. Create a folder for your first Cloud Function with the following command.

```
mkdir ~/lab-files/spanner_get_pets
cd ~/lab-files/spanner_get_pets
```

2. Create 2 files for your application: `main.py` and `requirements.txt`.

```
touch main.py requirements.txt
```

3. Click the __Open Editor__ button. In the `lab-files/spanner_get_pets/requirements.txt` file you just created, add the following code. 

```
google-cloud-spanner==3.15.0
```

4. In the `lab-files/spanner_get_pets/main.py` file add the following code that reads from the database and returns the pets. 

```
from google.cloud import spanner

instance_id = 'test-spanner-instance'
database_id = 'pets-db'

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)

def spanner_get_pets(request):
    query = """SELECT OwnerName, PetName, PetType, Breed 
         FROM Owners 
         JOIN Pets ON Owners.OwnerID = Pets.OwnerID;"""

    outputs = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)
        output = '<div>OwnerName,PetName,PetType,Breed</div>'
        outputs.append(output)
        for row in results:
            output = '<div>{},{},{},{}</div>'.format(*row)
            outputs.append(output)

    return '\n'.join(outputs)

```

5. Click the __Open Terminal__ button. Then, deploy the Cloud Function with the following command. Note, the trigger will be an HTTP trigger, which means a URL will generated for invoking the function. (_It will take a couple minutes for the command to complete._)

```
gcloud functions deploy spanner_get_pets --runtime python310 --trigger-http --allow-unauthenticated --region=us-central1 --quiet
```

6. When the command completes, in the Console, navigate to the __Cloud Functions__ service. Click the __spanner_get_pets__ function, then on __Trigger__. Open the Trigger URL in the browser and the test data should be returned. 

## Task 3. Create a Cloud Function to Write to Spanner

1. Create a folder for your second Cloud Function with the following command.

```
mkdir ~/lab-files/spanner_save_pets
cd ~/lab-files/spanner_save_pets
```

2. Create two files for your application: `main.py` and `requirements.txt`.

```
touch main.py requirements.txt
```

3. Click the __Open Editor__ button. In the `lab-files/spanner_get_pets/requirements.txt` file you just created, add the following code. 

```
google-cloud-spanner==3.15.0
```

4. In the `lab-files/spanner_get_pets/main.py` file, add the following code that reads from the database and returns the pets. 

```
from google.cloud import spanner
import base64
import uuid
import json

instance_id = 'test-spanner-instance'
database_id = 'pets-db'

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)

def spanner_save_pets(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(pubsub_message)

    # Check to see if the Owner already exists
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql("""
            SELECT OwnerID FROM OWNERS 
            WHERE OwnerName = @owner_name""", 
            params={"owner_name": data["OwnerName"]},
            param_types={"owner_name": spanner.param_types.STRING})

    row = results.one_or_none()
    if row != None:
        owner_exists = True
        owner_id = row[0]
    else:
        owner_exists = False
        owner_id = str(uuid.uuid4())

    # Need a UUID for the new pet
    pet_id = str(uuid.uuid4())

    def insert_owner_pet(transaction, data, owner_exists):
        try:
            row_ct = 0
            params = { "owner_id": owner_id,
            "owner_name": data["OwnerName"],
            "pet_id": pet_id,
            "pet_name": data["PetName"],
            "pet_type": data["PetType"],
            "breed": data["Breed"],
                         }

            param_types = { "owner_id": spanner.param_types.STRING,
                            "owner_name": spanner.param_types.STRING,
                            "pet_id": spanner.param_types.STRING,
                            "pet_name": spanner.param_types.STRING,
                            "pet_type": spanner.param_types.STRING,
                            "breed": spanner.param_types.STRING,
                            }

            # Only add the Owner if they don't exist already
            if not owner_exists:
                row_ct = transaction.execute_update(
                    """INSERT Owners (OwnerID, OwnerName) VALUES (@owner_id, @owner_name)""",
                    params=params,
                    param_types=param_types,)

                # Add the pet
            row_ct += transaction.execute_update(
                """INSERT Pets (PetID, OwnerID, PetName, PetType, Breed) VALUES (@pet_id, @owner_id, @pet_name, @pet_type, @breed)
                """,
                params=params,
                param_types=param_types,)
        except:
            row_ct = 0

        return row_ct

    row_ct = database.run_in_transaction(insert_owner_pet, data, owner_exists)

    print("{} record(s) inserted.".format(row_ct))

```

5. Click the __Open Terminal__ button. This Cloud Function triggers on a __Pub/Sub__ message. For it to work, you first need to create the Pub/Sub topic with the following command. 

```
gcloud pubsub topics create new-pet-topic
```

6. Deploy the Cloud Function with the following command. (_It will take a few minutes for the command to complete._)

```
gcloud functions deploy spanner_save_pets --runtime python310 --trigger-topic=new-pet-topic --region=us-central1 --quiet
```

6. When the command completes, in the Console, navigate to the __Pub/Sub__ service. Click the __new-pet-topic__ topic to view its details. <div>On the Details page, click the __Messages__ tab, then click the __Publish Message__ button. </div><div>Enter the message below, then click the __Publish__ button. __Note__: the message is in JSON format and must use the correct schema as shown for the function to work. </div>

```
{"OwnerName": "Jean", "PetName": "Sally", "PetType": "Frog", "Breed": "Green"}
```

7. Go to the web page you used to test the read function. Refresh it in the browser and check if the new owner, Jean, and her frog, Sally, were added. 

## Task 4. Starting the Spanner emulator

1. In the Cloud Shell terminal, run the following command to install and start the Spanner emulator. 

```
sudo apt-get install google-cloud-sdk-spanner-emulator
gcloud emulators spanner start
```

2. The emulator takes over the terminal, so in the Cloud Shell toolbar, click the __+__ icon to open a new terminal tab. Run the following commands to configure the Cloud SDK to use the emulator. 

```
gcloud config configurations create emulator
gcloud config set auth/disable_credentials true
gcloud config set project $GOOGLE_CLOUD_PROJECT
gcloud config set api_endpoint_overrides/spanner http://localhost:9020/

```

3. Create the instance and database using gcloud, but note that these commands are using the emulator now, not Spanner in the cloud. Run each separately not as a whole.

```
cd ~/lab-files

gcloud spanner instances create emulator-instance --config=emulator-config --description="EmulatorInstance" --nodes=1

gcloud spanner databases create pets-db --instance=emulator-instance --database-dialect=GOOGLE_STANDARD_SQL --ddl-file=./pets-db-schema.sql
```

4. To have the code from the Python client library use the emulator, the `SPANNER_EMULATOR_HOST` environment variable must be set. Run the following code now to do that. 

```
export SPANNER_EMULATOR_HOST=localhost:9010
```

## Task 5. Writing a REST API for the Spanner Pets database

1. Create create a folder for the Cloud Run program files and add the files needed. 

```
mkdir ~/lab-files/cloud-run
cd ~/lab-files/cloud-run

touch Dockerfile main.py requirements.txt
```

2. Click the __Open Editor__ button. In the `lab-files/cloud-run/requirements.txt` file you just created, add the following code. 

```
google-cloud-spanner==3.15.0
Flask
Flask-RESTful
```

3. In `main.py`, add the following. This code uses Python Flask and the Flask-RESTful library to build a REST API for the Pets database. <div>__Note__: the use of the environment variables near the top of the file (_lines 11 to 20_). When you deploy to Cloud Run, you set these variables to point to the real Spanner database. When the variables are not set, it defaults to the emulator. 

```
from google.cloud import spanner
from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import uuid
import os
 
# Get the Instance ID and database ID from environment variables
# Use the emulator if the env variables are not set.
# Requires the start-spanner-emulator.sh script be run. 
if "INSTANCE_ID" in os.environ:
    instance_id = os.environ["INSTANCE_ID"]
else:
    instance_id = 'emulator-instance'

if "DATABASE_ID" in os.environ:
    database_id = os.environ["DATABASE_ID"]
else:
    database_id = 'pets-db'

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)

app = Flask(__name__)
api = Api(app)

class PetsList(Resource):
    def get(self):
        query = """SELECT Owners.OwnerID, OwnerName,
                   PetID, PetName, PetType, Breed
                   FROM Owners
                   JOIN Pets ON Owners.OwnerID = Pets.OwnerID;"""

        pets = []
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(query)
            for row in results:
                pet = {'OwnerID': row[0],
                       'OwnerName': row[1],
                       'PetID': row[2],
                       'PetName': row[3],
                       'PetType': row[4],
                       'Breed': row[5], }
                pets.append(pet)
            return pets, 200

    def post(self):
        # Check to see if the Owner already exists
        data = request.get_json(True)
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql("""
               SELECT OwnerID FROM OWNERS 
               WHERE OwnerName = @owner_name""", 
               params={"owner_name": data["OwnerName"]},
               param_types={"owner_name": spanner.param_types.STRING})

        row = results.one_or_none()
        if row != None:
            owner_exists = True
            owner_id = row[0]
        else:
            owner_exists = False
            owner_id = str(uuid.uuid4())

        # Need a UUID for the new pet
        pet_id = str(uuid.uuid4())
        
        def insert_owner_pet(transaction, data, owner_exists):
            try:
                row_ct = 0
                params = {"owner_id": owner_id,
                          "owner_name": data["OwnerName"],
                          "pet_id": pet_id,
                          "pet_name": data["PetName"],
                          "pet_type": data["PetType"],
                          "breed": data["Breed"],
                         }

                param_types = { "owner_id": spanner.param_types.STRING,
                                "owner_name": spanner.param_types.STRING,
                                "pet_id": spanner.param_types.STRING,
                                "pet_name": spanner.param_types.STRING,
                                "pet_type": spanner.param_types.STRING,
                                "breed": spanner.param_types.STRING,
                              }

                # Only add the Owner if they don't exist already
                if not owner_exists:
                    row_ct = transaction.execute_update(
                    """INSERT Owners (OwnerID, OwnerName)
                       VALUES (@owner_id, @owner_name)""",
                    params=params,
                    param_types=param_types,)

                # Add the pet
                row_ct += transaction.execute_update(
                    """INSERT Pets (PetID, OwnerID, PetName, PetType, Breed)
                        VALUES (@pet_id, @owner_id, @pet_name, @pet_type, @breed)""",
                    params=params,
                    param_types=param_types,)

            except:
                row_ct = 0

            return row_ct

        row_ct = database.run_in_transaction(insert_owner_pet, data, owner_exists)

        return "{} record(s) inserted.".format(row_ct), 201

    def delete(self):

        # This delete all the Owners and Pets
        # Uses Cascading Delete on interleaved Pets table
        def delete_owners(transaction):
            row_ct = transaction.execute_update(
            "DELETE FROM Owners WHERE true = true")

            return row_ct


        row_ct = database.run_in_transaction(delete_owners)
        return "{} record(s) deleted.".format(row_ct), 201
        
class Pet(Resource):
    def get(self, pet_id):

        params = {"pet_id": pet_id}
        param_types = {
            "pet_id": spanner.param_types.STRING,
        }

        query = """SELECT Owners.OwnerID, OwnerName,
                   PetID, PetName, PetType, Breed
                   FROM Owners
                   JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                   WHERE PetID = @pet_id; """

        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                    query, params=params, param_types=param_types,)
            
            pet = None
            for row in results:
                pet = {'OwnerID': row[0],
                       'OwnerName': row[1],
                       'PetID': row[2],
                       'PetName': row[3],
                       'PetType': row[4],
                       'Breed': row[5], }
            
            if pet:
                return pet, 200
            else:
                return "Not found", 404


    def patch(self, pet_id):
        # This woud be for an Update
        return "Not Implemented", 500

    def delete(self, pet_id):
        # This woud be for a Delete
        return "Not Implemented", 500


api.add_resource(PetsList, '/pets')
api.add_resource(Pet, '/pets/<pet_id>')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


```

4. Click the __Open Terminal__ button, and then run the following code to start the program. 

```
python main.py
```

5. In the Cloud Shell toolbar, click the __+__ icon again to open a third terminal tab. 

6. You can use curl to test the API. First, add some records using HTTP POST commands. 

```
curl -X POST --data '{"OwnerName": "Sue", "PetName": "Sparky", "PetType": "Cat", "Breed": "Alley"}'  http://localhost:8080/pets
curl -X POST --data '{"OwnerName": "Sue", "PetName": "Pickles", "PetType": "Dog", "Breed": "Shepherd"}'  http://localhost:8080/pets
curl -X POST --data '{"OwnerName": "Doug", "PetName": "Noir", "PetType": "Dog", "Breed": "Schnoodle"}'  http://localhost:8080/pets
curl -X POST --data '{"OwnerName": "Doug", "PetName": "Bree", "PetType": "Dog", "Breed": "Mutt"}'  http://localhost:8080/pets
curl -X POST --data '{"OwnerName": "Joey", "PetName": "Felix", "PetType": "Cat", "Breed": "Tabby"}'  http://localhost:8080/pets

```

7. See if the records were added using an HTTP GET command. The records should be returned in JSON format. 

```
curl http://localhost:8080/pets
```

__Note__: These records were added to the emulator. Next, you deploy to Cloud Run and use the real Spanner instance. 

8. Type `exit` to close the third terminal tab, then type `Ctrl + C` to stop the Python program in the second terminal tab. Close the second tab by typing `exit`. <div>Return to the first terminal tab and stop the emulator by typing `Ctrl + C`.</div>

## Task 6. Deploying an app to Cloud Run

1. To deploy to Cloud Run, you need a Docker image. To create the image, you need a Dockerfile. Click the __Open Editor__ button and open the `Dockerfile` file you created earlier. Paste the following code into it. 

```
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install gunicorn
RUN pip install -r requirements.txt
ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
```

2. Return to the terminal and run the following code to create the Docker image. (_Make sure you are in the ~/lab-files/cloud-run folder._)

```
cd ~/lab-files/cloud-run

gcloud builds submit --tag=gcr.io/$GOOGLE_CLOUD_PROJECT/spanner-pets-api:v1.0 .
```

3. Make sure Cloud Run is enabled in your project. 

```
gcloud services enable run.googleapis.com
```

4. Now, deploy the Cloud Run application using the following command. __Note__ how the environment variables are set in the command, so the code will use the Cloud Spanner instance, not the emulator. It takes a couple minutes for the command to complete. 

```
gcloud run deploy spanner-pets-api --image gcr.io/$GOOGLE_CLOUD_PROJECT/spanner-pets-api:v1.0 --update-env-vars INSTANCE_ID=test-spanner-instance,DATABASE_ID=pets-db --allow-unauthenticated --region=us-central1
```

5. When the command completes, note the service URL and copy it to the clipboard. As you did with the emulator, you can use curl commands to test the API. First, create a variable to store the URL as shown below. Make sure you paste your full URL including the `https://...`

```
pets_url=<YOUR_SERVICE_URL HERE>
```

6. Add some records using curl. 

```
curl -X POST --data '{"OwnerName": "Sue", "PetName": "Sparky", "PetType": "Cat", "Breed": "Alley"}'  $pets_url/pets
curl -X POST --data '{"OwnerName": "Sue", "PetName": "Pickles", "PetType": "Dog", "Breed": "Shepherd"}'  $pets_url/pets
curl -X POST --data '{"OwnerName": "Doug", "PetName": "Noir", "PetType": "Dog", "Breed": "Schnoodle"}'  $pets_url/pets
curl -X POST --data '{"OwnerName": "Doug", "PetName": "Bree", "PetType": "Dog", "Breed": "Mutt"}'  $pets_url/pets
curl -X POST --data '{"OwnerName": "Joey", "PetName": "Felix", "PetType": "Cat", "Breed": "Tabby"}'  $pets_url/pets
```

7. See if the records were added. 

```
curl $pets_url/pets
```

8. In the Console, navigate to the __Cloud Run__ service and click your service to view its details and look at the logs. You will see each request you made logged there.

9. Navigate to Spanner and explore the instance and the database. 

10. The API implements DELETE as well. Return to the terminal and enter the following command to delete all the data. 

```
curl -X DELETE $pets_url/pets
```

11. From the Console, delete the Spanner instance so you are no longer being charged for it. 


### **Congratulations!** You have written applications that utilize Spanner databases and deployed them to both Cloud Functions and Cloud Run. You also installed, configured, and enabled the Spanner emulator for use in development environments. 


![[/fragments/endqwiklab]]

![[/fragments/copyright]]

