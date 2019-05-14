Material para el taller de Solr
===============================

Contiene las 3 tareas principales cuando se quiere utilizar una instancia de Solr:

1. Instalación y configuración
2. Indexado
3. Clientes para búsqueda

El paquete esta separado también de acuerdo a estas tareas:

/solr
    
Contiene los esquemas y archivo Dockerfile para instalar la instancia de Solr

Al construir y subir la imagen de docker se puede consultar en:

    http://localhost:8984


/index

Contiene el archivo index.py para los 2 métodos explicados de indexado.

Se recomienda la instalación de un ambiente virtual (venv) corriendo la version 3.6+ de Python.
Se ejecuta de la siguiente manera:

.. code-block:: python

   python index.py -i   index_method, available options data/pdf
                   -cp  corpus_path  
                   -u   url of solr instance

/server

Contiene la implemetación de la librería solr-client para nodejs y presenta un ejemplo para
hacer queries a manera de páginas y facet en un escenario de buscador.

Solo basta con instalar los paquetes y subir el servidor para
consultarlo en:

    http://localhost:3000/

