/**
 * Confckurator
 * Confckurator Client/Server API
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */

/* tslint:disable:no-unused-variable member-ordering */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { Http, Headers, URLSearchParams }                    from '@angular/http';
import { RequestMethod, RequestOptions, RequestOptionsArgs } from '@angular/http';
import { Response, ResponseContentType }                     from '@angular/http';

import { Observable }                                        from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import * as models                                           from '../model/models';
import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';


@Injectable()
export class TemplatesApi {

    protected basePath = 'https://localhost/api';
    public defaultHeaders: Headers = new Headers();
    public configuration: Configuration = new Configuration();

    constructor(protected http: Http, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {
        if (basePath) {
            this.basePath = basePath;
        }
        if (configuration) {
            this.configuration = configuration;
        }
    }

    /**
     * 
     * @summary Create a new template
     * @param postTemplatesBody Template creation properties.
     */
    public createTemplate(postTemplatesBody?: models.NewTemplate, extraHttpRequestParams?: any): Observable<models.IdResponse> {
        return this.createTemplateWithHttpInfo(postTemplatesBody, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary Create a new variable
     * @param templateId The template ID.
     * @param postTemplateVariablesBody Variable creation properties.
     */
    public createTemplateVariable(templateId: number, postTemplateVariablesBody?: models.NewVariable, extraHttpRequestParams?: any): Observable<models.IdResponse> {
        return this.createTemplateVariableWithHttpInfo(templateId, postTemplateVariablesBody, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary Delete a template
     * @param templateId The template ID.
     */
    public deleteTemplate(templateId: number, extraHttpRequestParams?: any): Observable<any> {
        return this.deleteTemplateWithHttpInfo(templateId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary Delete a variable
     * @param templateId The template ID.
     * @param variableId The variable ID.
     */
    public deleteTemplateVariable(templateId: number, variableId: number, extraHttpRequestParams?: any): Observable<any> {
        return this.deleteTemplateVariableWithHttpInfo(templateId, variableId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary Get details about a template
     * @param templateId The template ID.
     */
    public getTemplate(templateId: number, extraHttpRequestParams?: any): Observable<models.Template> {
        return this.getTemplateWithHttpInfo(templateId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary List all variables of a template
     * @param templateId The template ID.
     */
    public getTemplateVariables(templateId: number, extraHttpRequestParams?: any): Observable<models.Variable> {
        return this.getTemplateVariablesWithHttpInfo(templateId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }

    /**
     * 
     * @summary List all templates
     */
    public getTemplates(extraHttpRequestParams?: any): Observable<Array<models.Template>> {
        return this.getTemplatesWithHttpInfo(extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json() || {};
                }
            });
    }


    /**
     * Create a new template
     * 
     * @param postTemplatesBody Template creation properties.
     */
    public createTemplateWithHttpInfo(postTemplatesBody?: models.NewTemplate, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/';

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        headers.set('Content-Type', 'application/json');

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Post,
            headers: headers,
            body: postTemplatesBody == null ? '' : JSON.stringify(postTemplatesBody), // https://github.com/angular/angular/issues/10612
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Create a new variable
     * 
     * @param templateId The template ID.
     * @param postTemplateVariablesBody Variable creation properties.
     */
    public createTemplateVariableWithHttpInfo(templateId: number, postTemplateVariablesBody?: models.NewVariable, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/${templateId}/variable'
                    .replace('${' + 'templateId' + '}', String(templateId));

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'templateId' is not null or undefined
        if (templateId === null || templateId === undefined) {
            throw new Error('Required parameter templateId was null or undefined when calling createTemplateVariable.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        headers.set('Content-Type', 'application/json');

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Post,
            headers: headers,
            body: postTemplateVariablesBody == null ? '' : JSON.stringify(postTemplateVariablesBody), // https://github.com/angular/angular/issues/10612
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Delete a template
     * 
     * @param templateId The template ID.
     */
    public deleteTemplateWithHttpInfo(templateId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/${templateId}'
                    .replace('${' + 'templateId' + '}', String(templateId));

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'templateId' is not null or undefined
        if (templateId === null || templateId === undefined) {
            throw new Error('Required parameter templateId was null or undefined when calling deleteTemplate.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Delete,
            headers: headers,
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Delete a variable
     * 
     * @param templateId The template ID.
     * @param variableId The variable ID.
     */
    public deleteTemplateVariableWithHttpInfo(templateId: number, variableId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/${templateId}/variable/${variableId}'
                    .replace('${' + 'templateId' + '}', String(templateId))
                    .replace('${' + 'variableId' + '}', String(variableId));

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'templateId' is not null or undefined
        if (templateId === null || templateId === undefined) {
            throw new Error('Required parameter templateId was null or undefined when calling deleteTemplateVariable.');
        }
        // verify required parameter 'variableId' is not null or undefined
        if (variableId === null || variableId === undefined) {
            throw new Error('Required parameter variableId was null or undefined when calling deleteTemplateVariable.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Delete,
            headers: headers,
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Get details about a template
     * 
     * @param templateId The template ID.
     */
    public getTemplateWithHttpInfo(templateId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/${templateId}'
                    .replace('${' + 'templateId' + '}', String(templateId));

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'templateId' is not null or undefined
        if (templateId === null || templateId === undefined) {
            throw new Error('Required parameter templateId was null or undefined when calling getTemplate.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Get,
            headers: headers,
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * List all variables of a template
     * 
     * @param templateId The template ID.
     */
    public getTemplateVariablesWithHttpInfo(templateId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/${templateId}/variable'
                    .replace('${' + 'templateId' + '}', String(templateId));

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'templateId' is not null or undefined
        if (templateId === null || templateId === undefined) {
            throw new Error('Required parameter templateId was null or undefined when calling getTemplateVariables.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Get,
            headers: headers,
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * List all templates
     * 
     */
    public getTemplatesWithHttpInfo(extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + '/template/';

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Get,
            headers: headers,
            search: queryParameters,
            withCredentials:this.configuration.withCredentials
        });
        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

}
