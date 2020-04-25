<img align="left" src="https://i.imgur.com/n8shdOD.png" width=230 height=100/>
<img src="https://i.imgur.com/X2xkpSE.png" width=200 height=100/>

[![Build Status](https://travis-ci.com/nickyu42/Myuri.svg?branch=master)](https://travis-ci.com/nickyu42/Myuri)

Self hosted Man(ga/hwa/hua) server with accompanying web client

## Development Roadmap
- Automated indexing of library and metadata storing
- API to serve pages from indexed comics
- Web interface for reading comics
- Admin web interface for modifying and viewing comic metadata

## Installation
The full application (server + web client) can be setup using docker-compose. 
By default it runs in development mode (no https, debug logging), 
but can be run can started in production using `docker-compose.prod.yml`  

compose is setup to spawn 2 containers:  
- myuri_nginx - Main entrypoint for the application, acts as a reverse proxy
- myuri_backend - Flask based server for API  

### Run in development
```
docker-compose up -d
```

### Run in production
```
docker-compose -f docker-compose.prod.yml up -d
```
