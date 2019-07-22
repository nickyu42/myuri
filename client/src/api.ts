import { Comic } from './types'

/**
 * Class for interfacing with backend api
 */
export class Api {

    static readonly endpoints: { [id: string]: string } = {
        catalog: '/c/catalog/',
        info: '/c/info/',
        page: '/c/'
    };

    /**
     * Create url object from image and pushes it onto the given list
     * @param comic types.Comic object
     * @param queue list of chapter number and possibly url object
     */
    get_page(comic: Comic) {
        return this.get('page', [comic.id, comic.chapter, comic.page])
        .then((response) => response.blob)
    }

    /**
     * Get info about a comic
     * @param id internal id to get
     */
    get_info(id: number): Promise<JSON> {
        return this.get('info').then((response) => response.json())
    }

    /**
     * Uses fetch api to make a GET request
     * @param endpoint which endpoint to fetch from
     * @param args parameters to add after the endpoint
     * @returns Promise<Response> object
     */
    private get(endpoint: string, ...args: any[]): Promise<Response> {
        return fetch(
            Api.endpoints[endpoint] + args.map(toString).join('/')
        );
    }
}

export function dummy(): number {
    return 42;
}