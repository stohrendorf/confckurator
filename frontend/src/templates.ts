module app.templates {
    import TemplatesApi = API.Client.TemplatesApi;
    import Template = API.Client.Template;

    class TemplateController {
        static $inject: string[] = ['TemplatesApi'];

        constructor(private api: TemplatesApi = null) {
            api.getTemplates().then(d => {
                console.debug(d);
                this.templates = d.data;
            });
        }

        public templates: Array<Template>;
    }

    confckurator
        .service('TemplatesApi', TemplatesApi)
        .controller('TemplateController', TemplateController);
}
