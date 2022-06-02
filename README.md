# getInfoJira

El objetivo de este codigo es obtener la información de las incidencias de JIRA de una determinadas categorias y obtener por otra parte la información
de las imputaciones (worklog) de los desarroladores.

Esta información es proporcionada por la API de JIRA y es devuelta en JSON.

Desechamos la información que no necesitamos y organizamos en diccionarios la que si necesitamos.

Guardamos la información en CSV en un Bucket de GCP para posteriormente, en otra parte del proyecto, combinar esta información mediante DataFlow y pintar un dashboard en DataStudio. 


Como ejecutarlo en local:


Cd C:\Users\Sergio\Documents\GitHub\getInfoJira

gcloud auth application-default login

py -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

python __main__.py C:\Users\sergio.cobos\AppData\Roaming\gcloud\application_default_credentials.json



El despliegue original de esta solución esta realizado de la siguiente manera:


# AS IS


![image-20220405-094235](https://user-images.githubusercontent.com/46417402/171605682-7764675d-14b1-458a-a3d6-638bdfb09b8b.png)



# TO BE


![image-20220525-085501](https://user-images.githubusercontent.com/46417402/171605707-4e6d810a-4b41-4797-a763-282765efa016.png)
