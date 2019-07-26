# Myuri Client

Typescript based application for reading asian/western comics.
Uses the Myuri API to retrieve comics and metadata.
The client is targeted towards mobile and desktop use.

## Development

To run the web client apart from the server

- install Node.js (>11)
- ```cd client``` to change into client app directory 
- ```npm install``` to install dependencies
- ```npm run serve``` to start dev server


To run tests simply execute ```npm test``` after installing dependencies

## Overview

### Dependencies

- typescript - Typescript compiler
- webpack - Bundler
- normalize.css - For cleaner cross platform css
- mocha/chai - For testing the application

### Application Structure

- ```src/``` - All typescript files
- ```src/tests/``` - All test files
- ```public/``` - Client assets