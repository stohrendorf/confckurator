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

import * as models from './models';

export interface UpdateTemplateVariables {
    /**
     * Variable IDs that should be removed from the template.
     */
    delete?: Array<number>;

    /**
     * Variables to update.
     */
    update?: Array<models.UpdateTemplateVariablesUpdate>;

    /**
     * Variables to create.
     */
    create?: Array<models.UpdateTemplateVariablesCreate>;

}
