from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, UniqueConstraint, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, configure_mappers
from sqlalchemy_continuum import make_versioned
from sqlalchemy_continuum.plugins import FlaskPlugin, PropertyModTrackerPlugin

make_versioned(plugins=[FlaskPlugin(), PropertyModTrackerPlugin()], user_cls=None)
Schema = declarative_base()


class Pack(Schema):
    """
    :type id: int
    :type name: str
    :type instances: List[Instance]
    :type parent_id: int
    :type parent: Pack|None
    """

    __tablename__ = 'packs'
    __versioned__ = {}

    id = Column(Integer, Sequence('pack_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    instances = relationship('Instance', backref='pack', cascade="all, delete-orphan")

    parent_id = Column(Integer, ForeignKey(id), nullable=True, default=None)
    parent = relationship('Pack', remote_side=[id])

    def __repr__(self):
        return "<Pack(name='{}', id='{}')>".format(self.name, self.id)

    def get_templates(self):
        """
        :rtype: Set[Template]
        """
        ids = set()
        for instance in self.instances:
            for value in instance.values:
                ids.add(value.variable.template)
        return ids


class Environment(Schema):
    """
    :type id: int
    :type name: str
    :type values: List[Value]
    """

    __tablename__ = 'environments'
    __versioned__ = {}

    id = Column(Integer, Sequence('environment_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    values = relationship('Value', backref='environment')

    def __repr__(self):
        return "<Environment(name='{}', id='{}')>".format(self.name, self.id)

    def in_use(self):
        return len(self.values) != 0


class Template(Schema):
    """
    :type id: int
    :type name: str
    :type text: str
    :type variables: List[Variable]
    """

    __tablename__ = 'templates'
    __versioned__ = {}

    id = Column(Integer, Sequence('template_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    text = Column(Unicode, nullable=False)

    variables = relationship('Variable', backref='template')
    instances = relationship('Instance', backref='template')

    def __repr__(self):
        return "<Template(name='{}', id='{}')>".format(self.name, self.id)


class Variable(Schema):
    """
    :type id: int
    :type template_id: int
    :type template: Template
    :type name: str
    :type description: str
    :type values: List[Value]
    """

    __tablename__ = 'variables'
    __versioned__ = {}

    id = Column(Integer, Sequence('variable_id_seq'), primary_key=True)
    template_id = Column(Integer, ForeignKey(Template.id))
    name = Column(String(255), nullable=False)
    description = Column(Unicode, nullable=False)

    values = relationship('Value', backref='variable')

    __table_args__ = (
        UniqueConstraint('template_id', 'name'),
    )

    def __repr__(self):
        return "<Variable(name='{}', id='{}', template_id='{}')>".format(self.name,
                                                                         self.id,
                                                                         self.template_id)

    def get_value(self, pack: Pack, environment: Environment):
        default_value = None
        for value in pack.values:
            if value.pack_id != pack.id:
                continue
            if value.variable_id != self.id:
                continue
            if value.environment_id is None:
                default_value = value
            elif value.environment_id == environment.id:
                return value

        return default_value

    def in_use(self):
        return len(self.values) != 0


class Value(Schema):
    """
    :type variable_id: int
    :type variable: Variable
    :type environment_id: int
    :type environment: Environment
    :type instance_id: int
    :type instance: Instance
    :type data: str
    """

    __tablename__ = 'values'
    __versioned__ = {}

    variable_id = Column(Integer, ForeignKey(Variable.id), primary_key=True)
    environment_id = Column(Integer, ForeignKey(Environment.id), primary_key=True, nullable=True)
    instance_id = Column(Integer, ForeignKey('instances.id'), primary_key=True)
    data = Column(Unicode, nullable=False)

    def __repr__(self):
        return "<Value(variable_id='{}', environment_id='{}', pack_id='{}')>".format(self.variable_id,
                                                                                     self.environment_id,
                                                                                     self.pack_id)


class Instance(Schema):
    """
    :type id: int
    :type name: str
    :type values: List[Value]
    :type pack_id: int
    :type pack: Pack
    :type template_id: int
    :type template: Template
    """

    __tablename__ = 'instances'
    __versioned__ = {}

    id = Column(Integer, Sequence('instance_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)

    values = relationship(Value, backref='instance', cascade="all, delete-orphan")
    pack_id = Column(Integer, ForeignKey(Pack.id), nullable=False)
    template_id = Column(Integer, ForeignKey(Template.id), nullable=False)

    __table_args__ = (
        UniqueConstraint(pack_id, name),
    )

    def __repr__(self):
        return "<Instance(name='{}', id='{}')>".format(self.name, self.id)

    # noinspection PyUnusedLocal
    @validates(values)
    def validate_values(self, key, value: Value):
        if value.variable.template_id != self.template_id:
            raise ValueError('Non-transitive instance-value-variable-template association')
        return value


configure_mappers()
