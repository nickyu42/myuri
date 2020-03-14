/**
 * Class for interfacing with backend api
 */
export class Api {

    private static instance: Api;
    private static host: string;

    // constructor() {}

    /**
     * Returns the instance
     */
    public static getInstance(host: string): Api {
        if (!Api.instance) {
            Api.instance = new Api();
            Api.host = host;
        }
        return Api.instance;
    }

    public static readonly endpoints: { [id: string]: string } = {
        catalog: '/c/catalog',
        cover: '/c/cover/',
        info: '/c/info/',
        page: '/c/',
    };

    /**
     * Uses fetch api to make a GET request
     * @param endpoint which endpoint to fetch from
     * @param args parameters to add after the endpoint
     * @returns Promise<Response> object
     */
    public get(endpoint: string, ...args: (number | string)[]): Promise<Response> {
        return fetch(
            Api.host + Api.endpoints[endpoint] + args.join('/'),
            {
                mode: 'no-cors'
            }
        );
    }

    /**
     * Get single page of a comic
     * @param id internal id
     * @param chapter which chapter to get
     * @param page which page to get
     */
    public getPage(id: number, chapter: string, page: number): Promise<Blob> {
        return this.get('page', id, chapter, page)
        .then((response) => response.blob());
    }

    /**
     * Get info about a comic
     * @param id internal id to get
     */
    public getInfo(id: number): Promise<JSON> {
        return this.get('info', id).then(
            (response) => response.json()
        );
    }

    /**
     * Get cover of a comic
     * @param id internal id
     */
    public getCover(id: number): Promise<Blob> {
        return this.get('cover', id).then((response) => response.blob());
    }

    /**
     * Get the comic catalog
     */
    public getCatalog(): Promise<string> {
        return this.get('catalog').then((response) => response.text());
    }
}

export function dummy(): number {
    return 42;
}
