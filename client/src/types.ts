export class Comic {

    constructor(public id: number, 
                public name: string[], 
                public chapter: string, 
                public page: number,
                public totalPages: number,
                public type: Comic.Type) {}

    /**
     * Parses the given string into a JSON object and checks if the parameters match
     * @param jsonString String representation of comic json object
     */
    static fromJSON(jsonString: string): Comic {
        const obj = JSON.parse(jsonString);

        const containsAll = Object.keys(this.prototype).every((prop) => 
            prop in obj && typeof prop == typeof obj[prop]
        );

        if (containsAll) {
            return Object.assign(new this(
                obj.id,
                obj.name,
                obj.chapter,
                obj.page,
                obj.totalPages,
                obj.type
            ), obj)
        } 

        throw "Could not parse string into Comic";
    }

    /**
     * Checks if the comic has reached final page, otherwise advances
     * @returns true if comic has moved to next page
     */
    nextPage(): boolean {
        if (this.page < this.totalPages) {
            this.page += 1
            return true;
        } 

        return false;
    }

    /**
     * Checks if the comic is at the first page, otherwise goes to previous page
     * @returns true if comic has moved to previous page
     */
    prevPage(): boolean {
        if (this.page > 0) {
            this.page += 1
            return true;
        } 

        return false;
    }
}

export namespace Comic {
    export enum Type {
        Manga,
        Manhwa,
        Manhua
    }
}