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
    'data': fields.String,
    'variable_name': fields.String(attribute=lambda v: v.variable.name),
    'environment_name': fields.String(attribute=lambda v: v.environment.name)
}

environment_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'in_use': fields.Boolean(attribute=lambda v: v.in_use())
}

instance_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'values': fields.List(fields.Nested(value_fields)),
    'template_name': fields.String(attribute=lambda v: v.template.name),
    'template_id': fields.Integer(attribute=lambda v: v.template.id)
}

pack_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'instances': fields.List(fields.Nested(instance_fields))
}
