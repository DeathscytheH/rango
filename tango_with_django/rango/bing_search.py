#bing_search.py

import json
import urllib, urllib2
from keys import BING_API_KEY

def run_query(search_terms):
    #especificamos la base
    root_url="https://api.datamarket.azure.com/Bing/Search/"
    source = "Web"

    #Especificar la cantidad de resultados que queremos
    #Offset especifuca donde en la lista de resultados iniciamos.
    #Con results_per_page = 10 y offset = 11, iniciaremos en la pagina 2.
    results_per_page = 10
    offset = 0

    #Envolvemos la query en comillas como lo pide el API de Bing
    #Luego se guardara en la variable query
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)
    
    #Contruyendo la siguiete parte de la URL
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
            root_url,
            source,
            results_per_page,
            offset,
            query
        )
    #Autenticacion con los servidores de bing
    #El username debe estar vacio.
    username = ''
    bing_api_key = BING_API_KEY

    #Crear un passwordmanager el cual manejara la Autenticacion por nosotros.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)

    #Creamos una lista donde estaran los resultados
    results = [ ]

    try:
        #Prepar la coneccion con bing
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        #Conectarse al server y leer la respuesta
        response = urllib2.urlopen(search_url).read()

        #Convertir la respuesta a un diccionario
        json_response = json.loads(response)

        #Ciclamos por cada pagina y populamos la lista de resultados.
        for result in json_response['d']['results']:
            results.append({
                'title':result['Title'],
                'link':result['Url'],
                'summary':result['Description']
                })
    #Algo fallo a la hora de la coneccion
    except urllib2.URLError, e:
        print "Error al mandar la query a Bing", e
    #Regresamos los resultados
    return results

def main():
    # Query, get the results and create a variable to store rank.
    query = raw_input("Please enter a query: ")
    results = run_query(query)
    rank = 1
    
    # Loop through our results.
    for result in results:
        # Print details.
        print "Rank {0}".format(rank)
        print result['title']
        print result['link']
        print
        
        # Increment our rank counter by 1.
        rank += 1

if __name__ == '__main__':
    main()