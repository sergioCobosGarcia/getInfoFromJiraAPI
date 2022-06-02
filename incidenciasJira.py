
# 1. Imports y declaraciones 

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import csv
import os
import google.auth
import sys, traceback
from google.cloud import storage
import common




def incidenciasJira(filename,filepath,bucket,gsc_client):

    # 2. Atributos total y maxResult API 

    #Este paso es necesario para obtener los atributos de la llamada y poder iterar en los resultados.

    url = "https://XXXXXXXXXXXX.atlassian.net/rest/api/2/search?jql=(category = XXXXXXXXXX) AND (resolved is EMPTY OR resolved >= 2020-09-01 OR resolved <= 2020-09-01 AND status not in (Resolved, Closed)) ORDER BY resolved ASC, status DESC,  ASC"
    auth = HTTPBasicAuth("XXXXXXX@XXXXX.XXX", "XXXXXXXXXXXXXXXXXXXXXX") #email,token

    headers = {
        "Accept": "application/json"
        }

    response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

    attr_llamada = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    attr_llamada=json.loads(attr_llamada)


        
    total = attr_llamada['total']  
    startAt=0 # utilizar esta variable en la llamada si se desea parametrizar este valor.
    maxResults=100 # utilizar esta variable en la llamada si se desea parametrizar este valor.
    dict_agg = []

    #3. Bucle llamada API paginada 


    x = range(0, total, maxResults)

    for n in x:
        
        url = "https://XXXXXXXXXXXX.atlassian.net/rest/api/2/search?jql=(category = XXXXXXXXXX) AND (resolved is EMPTY OR resolved >= 2020-09-01 OR resolved <= 2020-09-01 AND status not in (Resolved, Closed)) ORDER BY resolved ASC, status DESC,  ASC&maxResults=100&startAt=" + str(n) + ""
        auth = HTTPBasicAuth("XXXXXXX@XXXXX.XXX", "XXXXXXXXXXXXXXXXXXXXXX") #email,token

        headers = {
        "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

        print("respones is:", response)
        print("json is:", json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

        llamada = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        llamada=json.loads(llamada)

    

    # 4. Bucle anidado construccion diccionario API paginada 

        for item in llamada['issues']:  
                try:
                    Clave = item["key"]
                except KeyError:
                    Clave = ""
                try:
                    Tipo_Incidencia = item["fields"]["issuetype"]['name']
                except KeyError:
                    Tipo_Incidencia = ""
                try:
                    Epic_Link = item["fields"]["customfield_10007"]
                except KeyError:
                    Epic_Link = ""
                try:
                    parent = item['fields']['parent']['key'] 
                except KeyError:
                    parent = ""
            
                try:
                    Tiempo_Trabajado = item["fields"]["timespent"]
                except KeyError:
                    Tiempo_Trabajado = ""
                try:
                    Codigo_Proyecto = item["fields"]["customfield_13707"]
                except KeyError:
                    Codigo_Proyecto = ""
                Incidencias_Enlazadas = ""
                for issue_link in item['fields']['issuelinks']:
                    try:
                        Incidencias_Enlazadas = Incidencias_Enlazadas + issue_link['inwardIssue']['key'] + " "
                    except KeyError:
                        pass
                    except TypeError:
                        pass
                    try:
                        Incidencias_Enlazadas = Incidencias_Enlazadas + issue_link['outwardIssue']['key'] + " "
                    except KeyError:
                        pass
                    except TypeError:
                        pass
            
                dict_agg.append({"Clave": Clave,
                            "Clave": Clave,
                            "Tipo_Incidencia":  Tipo_Incidencia,
                            "Epic_Link":  Epic_Link,
                            "parent":  parent,
                            "Tiempo_Trabajado":  Tiempo_Trabajado,
                            "Codigo_Proyecto":  Codigo_Proyecto,
                            "Incidencias_Enlazadas":  Incidencias_Enlazadas,
                            "Parent": "",
                            "Link_Issues": "",
                            "BS_Link_Issues": "",
                            "Issue_type_BS_Link_Issues": "",
                            "Epik_Link": "",
                            "BS_Link_Issues": "",
                            })

    # 5. Creación del CSV 
    
    df = pd.DataFrame(dict_agg)
    df.to_csv('incidenciasJira.csv', index=False)


    # 6. Subir CSV a GCS 

            # Copy with gsutil to destination bucket, file name and file destination name will be the same
    common.upload_blob(bucket, filename, "export/" + filepath + "/" + filename, gsc_client)
