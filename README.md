## Web Scrapping para Youtube

# Sobre el código

Este código busca extraer las estadísticas básicas de cada video subido por un perfil de Youtube. Está proyectado 100% en Python (aunque es posible realizarlo con R) .

# ¿Qué se necesita?

- Un ambiente para ejecutar Python. El código fue preparado en un Jupyter Notebook pero puede ser ejecutado con recursos locales. Para eso se recomienda la preparación de dos archivos .py como se indica al interior del código.
- Una Key API de Google Youtube.
- El ID de un canal de Youtube para ser analizado.

# ¿Cómo generar una Key API en Google Youtube?
- Contar con una cuenta Gmail y estar logeado en ella.
- Entrar a este link: https://console.cloud.google.com/
- En la parte superior izquierda, junto con el logo de GoogleAPI, se encontrará el botom "Proyecto Nuevo" (o el nombre de un proyecto en una lista desplegable si ya ha sido usado en el pasado).
- Generar un proyecto nuevo con el nombre deseado.
- Asegurarse que en el botom mencionado ahora salga el nombre del proyecto.
- En la aprte superior de la pantalla, seleccionar "+ HABILITAR API Y SERVICIOS".
- Seleccionar la opción "Youtube Data API V3".
- Seleciconar la opción "Habilitar" o "Enable".
- Luego de que cargue, en la parte izquierda observará la opción "Credenciales" (con el ícono de una llave). Seleccionela.
- En la parte superior seleccione la opción "+CREAR CREDENCIALES" y luego "API Key".
- Guarde el token generado e incluyalo en el string del código llamado "API_KEY" en la sección de Código de Ejecución.

# ¿Cómo identificar el ID de un canal de Youtube?
- Entre directamente a cualquier canal de youtube.
- Click derecho, código fuente
- CTRL + F, buscar "channel_id"
- Copiar los caracteres que suelen ser del tipo "UCECJDeK0MNapZbpaOzxrUPA" (esta es la de Luisito Comunica).
- Incluir en el string Channel_ID del código.

# Para tener en cuenta
- El código solo extraerá los últimos 50 videos. Para aumentar el alcance, revisar la linea 53 donde dice limit="50".
- La API tiene un límite de request por día. Para más información consultar: https://developers.google.com/youtube/v3/getting-started

# Disclaimer
- El código no es 100% de autoría propia. Fue construido apartir de retazos.
