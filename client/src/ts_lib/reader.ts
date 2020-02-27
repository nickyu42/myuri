import { ComicFormat } from './types';

/**
 * Comic reader representation
 */
export class Reader {
    private readonly image: HTMLImageElement;

    constructor(public id: number, public viewer: ComicFormat = ComicFormat.RightToLeft) {
        this.image = new Image();
    }

    /**
     * Sets the internal image url
     * @param url the url of the image bytes
     */
    public setImage(url: string) {
        this.image.src = url;
    }

    public getImage(): HTMLImageElement {
        return this.image;
    }
}
