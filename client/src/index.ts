import 'normalize.css';

import { Api } from './api';
import { Reader } from './reader';

const root = document.body;

function rootComponent(): HTMLDivElement {
    const element = document.createElement('div');

    const api = new Api('http://myuri.njkyu.com/api');

    const paragraph = document.createElement('p')
    const str = api.get_catalog().then((str) => paragraph.textContent = str.toString());
    element.appendChild(paragraph);

    return element;
}

root.appendChild(rootComponent());
