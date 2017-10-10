module app.packs {
    import PacksApi = API.Client.PacksApi;
    import Pack = API.Client.Pack;

    class PackController {
        static $inject: string[] = ['PacksApi'];

        constructor(private api: PacksApi = null) {
            api.getPacks().then(d => {
                console.debug(d);
                this.packs = d.data;
            });
        }

        public packs: Array<Pack>;
    }

    confckurator
        .service('PacksApi', PacksApi)
        .controller('PackController', PackController);
}
