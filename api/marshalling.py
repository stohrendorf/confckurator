from flask_restful import fields

variable_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'in_use': fields.Boolean(attribute=lambda v: v.in_use())
}

template_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'variables': fields.List(fields.Nested(variable_fields))
}

template_fields_with_text = {
    'id': fields.Integer,
    'name': fields.String,
    'variables': fields.List(fields.Nested(variable_fields)),
    'text': fields.String
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
    'in_use': fields.Boolean(attribute=lambda v: v.in_use())
}

pack_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'values': fields.List(fields.Nested(value_fields))
}
