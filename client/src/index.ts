import 'normalize.css';
import { isNull } from 'util';

const root = document.getElementById('root');

function component(): HTMLDivElement {
    const element = document.createElement('div');
  
    element.innerHTML = 'Hello World';
  
    return element;
}

if (!isNull(root)) {
  root.appendChild(component())
}
