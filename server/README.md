# Myuri Backend

Flask based server for hosting and storing comics.
An API is exposed for retrieving comics and metadata.

## Development

To setup the server

- Install python >3.7
- ```cd server```
- ```pip install -r requirements.txt``` to install dependencies
- ```flask run``` to start server

To run tests execute ```pytest``` in the server/root project folder

By default the server runs in a development environment.
To run in production change the ```FLASK_ENV``` variable in ```server/.flaskenv``` to ```production```

## Overview

### Dependencies

- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- pytest

### Application Structure

The main entrance to the application is ```wsgi.py```

- ```.flaskenv``` - Flask environment variables
- ```app/database``` - Module for interfacing with the database
- ```app/views``` - All base views are defined here
- ```tests``` - All test files

### Persistence 

The current database used is [SQLite](https://www.sqlite.org/index.html).
In a later version this may be changed.

The comic data is stored inside ```data/```  
A ```data.db``` file is created for storing metadata  
Each comic is stored in its own folder, where each page is named \<page number>.jpeg