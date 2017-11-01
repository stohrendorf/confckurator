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

export interface Value {
    /**
     * Variable ID
     */
    variable_id: number;

  /**
   * Variable name
   */
  variable_name: string;

    /**
     * Environment ID
     */
    environment_id: number;

  /**
   * Environment name
   */
  environment_name: string;

    /**
     * Pack ID
     */
    pack_id: number;

    /**
     * Value data
     */
    data?: string;

}
