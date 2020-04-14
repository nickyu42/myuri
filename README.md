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
The full application (server + web client) can be setup using docker-compose  
it is setup to spawn 3 containers:
- Nginx - main entrypoint for the application, acts as a reverse proxy
- Server - Flask based server for API
- Client - NodeJS based web client for interfacing with the server
