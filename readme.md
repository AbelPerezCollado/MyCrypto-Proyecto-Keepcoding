# mYCRYPTO 馃挸
Aplicaci贸n web con la cual podr谩s simular el registro de inversiones y compra/venta de Criptomonedas y controlar el estado de nuestra inversi贸n.

## Demo 馃枼
Si quieres ver una demo del proyecto, puedes solicitar un enlace en la siguiente direcci贸n de correo electr贸nico: iabel83@gmail.com

## Instalaci贸n 鈿欙笍
Para un correcto funcionamiento de la app, sigue los siguientes pasos:

* **1. Clonar repositorio**: 
``` git clone https://github.com/AbelPerezCollado/flask_proyecto.git ```

* **2. Creaci贸n y activaci贸n de entorno virtual**:
```python -m venv <nombre del entorno virtual> ``` 
```. <nombre del entorno virtual>/bin/activate ```

* **3. Instalaci贸n del entorno**:

	```pip install -r requeriments.txt```
	
* **4. Variables de entorno**:

	Renombrar el archivo ```.env_template``` como ```env```
	
	Definir las variables de entorno: ```FLASK_APP=balance ```
										```FLASK_ENV=production```
										
* **5. Obtener APIKey**:

	Visitar la p谩gina [CoinAPI](https://www.coinapi.io/) para conseguir tu 	APIkey(	[obtener gratis aqu铆](https://www.coinapi.io/pricing?apikey))
	
	
* **6. Creaci贸n de BBDD**:	

	Descargar gestor de BBDD sqlite en el siguiente enlace: [sqlitebrowser](https://sqlitebrowser.org/dl/)
	
	Abrir el archivo ```..balance/data/crea_tablas.sql ``` en el programa y ejecutarlo.
	
	
	
		
* **7. Archivo de configuraci贸n**:

	Renombrar archivo ```config_template.py``` como ```config.py```
	 
	Solo definir las siguientes variables: 
	
	```RUTA_BBDD = "ruta base de datos"```
	
	```	SECRET_KEY = "tu SECRET KEY"``` (puedes usar [RandomKeygen](https://randomkeygen.com/))
	
	
	
	``` HEADERS = {'X-CoinAPI-Key' : 'tu apikey aqu铆'} ```  											 
 
## Ejecutar aplicaci贸n 馃殌
Escribir en la terminal ``` flask run ```  
## Tecnologia empleada 馃洜锔?

* [Python](https://www.python.org/) - v.3.10.1
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web develoment
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - Form library
* [Pico.css](https://picocss.com/) - Minimal CSS Framework
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - Web template engine
* [SQLite](https://www.sqlite.org/index.html) - Database engine
* [AWS](https://aws.amazon.com/es/) - Amazon Web Services


## Desarrollador 鈱笍

* **Abel P茅rez** | [GitHub](https://github.com/AbelPerezCollado)  	