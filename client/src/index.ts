import 'normalize.css';
import { isNull } from 'util';

import { Comic } from './types'
import { Api } from './api'

const root = document.body;

enum Viewer {
  LeftToRight,
  RightToLeft,
  Vertical,
  Webtoom
}

class Reader {
  image: HTMLImageElement;

  constructor(public state: Comic, viewer: Viewer = Viewer.RightToLeft) {
    this.image = new Image()
  }

  setImage(url: string) {
    this.image.src = url
  }
}

function rootComponent(): HTMLDivElement {
    const element = document.createElement('div');

    const api = new Api()
    
    api.get_info(0).then((j) => {
      const comicRepr = JSON.stringify(j);
      element.innerHTML = comicRepr;

      try {
        const comic = Comic.fromJSON(comicRepr);
        const reader = new Reader(comic);

        api.get_page(comic).then((blob) => {
          const url = URL.createObjectURL(blob);
          reader.setImage(url);
        })

        element.appendChild(reader.image);

      } catch (error) {
        console.log(error)
      }
    })
  
    return element;
}

// root.appendChild(rootComponent())