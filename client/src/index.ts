import 'normalize.css';

import { Api } from './api';
import { Reader } from './reader';

const root = document.body;

function rootComponent(): HTMLDivElement {
    const element = document.createElement('div');

    const api = new Api();

    Api.get_info(1).then((j) => {
        element.innerHTML = JSON.stringify(j);

        try {
            const reader = new Reader(1);

            Api.get_cover(1).then((blob) => {
                const url = URL.createObjectURL(blob);
                reader.setImage(url);
            });

            element.appendChild(reader.getImage());

        } catch (error) {
            console.log(error);
        }
    });

    return element;
}

root.appendChild(rootComponent());
