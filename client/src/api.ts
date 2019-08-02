/**
 * Class for interfacing with backend api
 */
export class Api {

    public static readonly endpoints: { [id: string]: string } = {
        catalog: '/c/catalog/',
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
    public static get(endpoint: string, ...args: any[]): Promise<Response> {
        return fetch(
            Api.endpoints[endpoint] + args.join('/'),
        );
    }

    /**
     * Get single page of a comic
     * @param id internal id
     * @param chapter which chapter to get
     * @param page which page to get
     */
    public static get_page(id: number, chapter: string, page: number): Promise<Blob> {
        return Api.get('page', id, chapter, page)
        .then((response) => response.blob());
    }

    /**
     * Get info about a comic
     * @param id internal id to get
     */
    public static get_info(id: number): Promise<JSON> {
        return Api.get('info', id).then((response) => response.json());
    }

    /**
     * Get cover of a comic
     * @param id internal id
     */
    public static get_cover(id: number): Promise<Blob> {
        return Api.get('cover', id).then((response) => response.blob());
    }
}

export function dummy(): number {
    return 42;
}
