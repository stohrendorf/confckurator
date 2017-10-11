from flask_restful import fields

variable_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

tag_fields = {
    'id': fields.Integer,
    'name': fields.String
}

template_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tags': fields.List(fields.Nested(tag_fields)),
    'variables': fields.List(fields.Nested(variable_fields))
}

value_fields = {
    'variable_id': fields.Integer,
    'environment_id': fields.Integer,
    'pack_id': fields.Integer,
    'data': fields.String
}

environment_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'values': fields.List(fields.Nested(value_fields))
}

pack_fields = {
    'id': fields.Integer,
    'name': fields.String
}