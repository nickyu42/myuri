// development server
import express from 'express';

const app = express();
const port = 8080;

app.get('/', (req, res) => {
  res.send('Hello world!');
});

app.listen(port, err => {
  if (err) {
    return console.error(err);
  }
  return console.log(`server is listening on ${port}`);
});