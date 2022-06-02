
from incidenciasJira import incidenciasJira
from worklogJira import worklogJira
import os
import google.auth
import sys
from google.cloud import storage

try:
    credentials = google.auth.default()
except:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(sys.argv[1])
    credentials = google.auth.default()


bucket = "xxxxxxxxxxx" # os.getenv("bucket")   --- Introduce el nombre de tu bucket de Google Cloud Storage------
project_id = "xxxxxxxx" # --- Introduce el nombre de tu proyecto de Google Cloud------
gsc_client = storage.Client() 

def getInfoJira(event, context):

    try:
        incidenciasJira("incidenciasJira.csv","incidenciasJira",bucket,gsc_client)
    except Exception as e:
        print("[ERROR]:  {}".format(str(e)))
    try:
        worklogJira("worklogJira",bucket,gsc_client)
    except Exception as e:
        print("[ERROR]:  {}".format(str(e)))



if __name__ == '__main__':
    getInfoJira(None,None)
