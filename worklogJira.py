
# 1. IMPORTS Y DECLARACIONES

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import csv
import os
import google.auth
import sys, traceback
from datetime import datetime
from google.cloud import storage
import common

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def worklogJira(filepath,bucket,gsc_client):

    filename1 = "IMPUTACIONES_XXX_WORKLOG_ID_1.csv"
    filename2 = "IMPUTACIONES_XXX_ISSUE_ID_2.csv"
    filename3 = "IMPUTACIONES_XXX_ISSUE_KEY_3.csv"
 


    dict_agg = []
    dict_arr_agg = []
    arr_agg = []
    arr_issueId = []
    arr_issueId_unique = []
    dict_arr_id_key = []


    # 2. Llamada API paginada "Get IDs of updated worklogs"


    self = "https://XXXXXXXXXXXXXX.atlassian.net/rest/api/2/worklog/updated?since=1640991600000"  
    lastPage = False

    while lastPage == False:

        url = self
        auth = HTTPBasicAuth("XXXXXX@XXXXXXX.XX", "XXXXXXXXXXXXXXX")

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



        for value in llamada['values']:
            try:
                    worklogId = value['worklogId']
            except KeyError:
                    worklogId = ""
            except TypeError:
                    worklogId = ""
            try:
                    lastPage = llamada['lastPage']
            except KeyError:
                    lastPage = ""
            except TypeError:
                    lastPage = ""
            try:
                    self = llamada['nextPage']
            except KeyError:
                    self = ""
            except TypeError:
                    self = ""
            try:
                    
                    updatedTime = int(value['updatedTime']/1000)
                    dt = datetime.fromtimestamp(updatedTime)
            except KeyError:
                    updatedTime = ""
            except TypeError:
                    updatedTime = ""
            
            dict_agg.append({"worklogId": worklogId,
                            "lastPage": lastPage,
                            "self": self,
                            "updatedTime": updatedTime,
                            "dt": dt
                            })
            arr_agg.append(worklogId)
    
    df = pd.DataFrame(dict_agg)
    df.to_csv('IMPUTACIONES_XXX_WORKLOG_ID_1.csv', index=False)

    # 3. Llamada API POST Array de Woklogs IDs paginados "Get worklogs"




    for result_batch in batch(arr_agg, 1000):
            
        url = "https://XXXXXXXXXXXXXX.atlassian.net/rest/api/3/worklog/list"
        auth = HTTPBasicAuth("XXXXXXXXXX@XXXXXXXX.XX", "XXXXXXXXXXX")

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        payload = json.dumps( {
        "ids": result_batch
        
        } )

        response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
        )

        llamadaIDs = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        llamadaIDs=json.loads(llamadaIDs)



        for value in llamadaIDs:
            
                try:
                    author = value['author']['displayName']
                except KeyError:
                    author = ""
                except TypeError:
                    author = ""
                try:
                    issueId = value['issueId']
                except KeyError:
                    issueId = ""
                except TypeError:
                    issueId = ""
                try:
                    created = value['created']
                except KeyError:
                    created = ""
                except TypeError:
                    created = ""
                try:
                    started = value['started']
                except KeyError:
                    started = ""
                except TypeError:
                    started = ""
                try:
                    updated = value['updated']
                except KeyError:
                    updated = ""
                except TypeError:
                    updated = ""
                try:
                    id = value['id']
                except KeyError:
                    id = ""
                except TypeError:
                    id = ""
                try:
                    timeSpent = value['timeSpent']
                except KeyError:
                    timeSpent = ""
                except TypeError:
                    timeSpent = ""
                try:
                    timeSpentSeconds = value['timeSpentSeconds']
                    timeSpentSeconds_minutos = timeSpentSeconds/60
                    timeSpentSeconds_horas = timeSpentSeconds_minutos/60
                except KeyError:
                    timeSpentSeconds = ""
                except TypeError:
                    timeSpentSeconds = ""
                try:
                    comment = "" 
                except KeyError:
                    comment = ""
                except TypeError:
                    comment = ""
            
            
                dict_arr_agg.append({"author": author,
                                    "issueId": issueId,
                                    "created": created,
                                    "started": started,
                                    "updated": updated,
                                    "id": id,
                                    "timeSpent": timeSpent,
                                    "timeSpentSeconds": timeSpentSeconds,
                                    "timeSpentSeconds_minutos": timeSpentSeconds_minutos,
                                    "timeSpentSeconds_horas": timeSpentSeconds_horas,
                                    "comment": comment
                            })
                arr_issueId.append(issueId)
                
    df = pd.DataFrame(dict_arr_agg)
    df.to_csv('IMPUTACIONES_XXX_ISSUE_ID_2.csv', index=False)

    #4. Tercera llamada API JQL Array de Issues sin duplicados


    counter = 0
    contador = 0
    
    for element in arr_issueId:
        if element not in arr_issueId_unique:
            arr_issueId_unique.append(element)
            counter = counter + 1

    total=len(arr_issueId_unique) 
    maxResults=1 

    x = range(0, total, maxResults)

    for x in range(2,len(arr_issueId_unique)-1):
        url = "https://XXXXXXXXXXXXXX.atlassian.net/rest/api/2/search?jql= (category = XXXXXXXX) OR (category = XXXXXXXX)) and issue in (" + arr_issueId_unique[x] + ") ORDER BY status ASC, resolved ASC, issuetype DESC, Rank ASC"
        auth = HTTPBasicAuth("XXXXXXX@XXXXXXXX.XX", "XXXXXXXXXXXXXX")
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

        llamadaIssueIdKey = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        llamadaIssueIdKey=json.loads(llamadaIssueIdKey)

        contador = contador + 1
        print(contador)

        for item in llamadaIssueIdKey['issues']:  
                try:
                    id = item["id"]
                except KeyError:
                    id = ""
                try:
                    Issue = item["key"]
                except KeyError:
                    Issue = ""
                try:
                    Summary = item["fields"]["summary"]
                except KeyError:
                    Summary = ""


                dict_arr_id_key.append({"id": id,
                                        "Issue": Issue,
                                        "Summary": Summary
                                })
    
    df = pd.DataFrame(dict_arr_id_key)
    df.to_csv('IMPUTACIONES_XXX_ISSUE_KEY_3.csv', index=False)
                        
    # 5. Subir CSV a GCS 

    common.upload_blob(bucket, filename1, "export/" + filepath + "/" + filename1, gsc_client)
    common.upload_blob(bucket, filename2, "export/" + filepath + "/" + filename2, gsc_client)
    common.upload_blob(bucket, filename3, "export/" + filepath + "/" + filename3, gsc_client)

