from google.cloud import spanner
import os

# Get the Instance ID and database ID from environment variables
# Use defaults if they don't exist. 
if "INSTANCE_ID" in os.environ:
    instance_id = os.environ["INSTANCE_ID"]
else:
    instance_id = 'spannerdbsrv'

if "DATABASE_ID" in os.environ:
    database_id = os.environ["DATABASE_ID"]
else:
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

