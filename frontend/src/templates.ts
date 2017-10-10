module app.templates {
    import TemplatesApi = API.Client.TemplatesApi;
    import Template = API.Client.Template;

    class TemplateController {
        static $inject: string[] = ['TemplatesApi'];

        constructor(private api: TemplatesApi = null) {
            api.getTemplates().then(d => {
                console.debug(d);
                this.templates = d.data;
                this.templates.forEach(value => this.templatesVisible[value.id] = false);
            });
        }

        public templates: Array<Template>;
        public templatesVisible: boolean[] = [];
    }

    confckurator
        .service('TemplatesApi', TemplatesApi)
        .controller('TemplateController', TemplateController);
}
