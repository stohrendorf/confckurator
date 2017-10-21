from sqlalchemy import Column, Integer, String, Text, ForeignKey, Sequence, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Schema = declarative_base()


class Pack(Schema):
    """
    :type id: int
    :type name: str
    :type values: List[Value]
    :type parent_id: int
    :type parent: Pack|None
    """

    __tablename__ = 'packs'

    id = Column(Integer, Sequence('pack_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    values = relationship('Value', backref='pack')

    parent_id = Column(Integer, ForeignKey('packs.id'), nullable=True, default=None)
    parent = relationship('Pack', remote_side=[id])

    def __repr__(self):
        return "<Pack(name='{}', id='{}')>".format(self.name, self.id)

    def get_templates(self):
        """
        :rtype: Set[Template]
        """
        ids = set()
        for value in self.values:
            ids.add(value.variable.template)
        return ids


class Environment(Schema):
    """
    :type id: int
    :type name: str
    :type values: List[Value]
    """

    __tablename__ = 'environments'

    id = Column(Integer, Sequence('environment_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    values = relationship('Value', backref='environment')

    def __repr__(self):
        return "<Environment(name='{}', id='{}')>".format(self.name, self.id)


class Template(Schema):
    """
    :type id: int
    :type name: str
    :type text: str
    :type variables: List[Variable]
    """

    __tablename__ = 'templates'

    id = Column(Integer, Sequence('template_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    text = Column(Text, nullable=False)

    variables = relationship('Variable', backref='template')

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

    id = Column(Integer, Sequence('variable_id_seq'), primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.id'))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    UniqueConstraint('template_id', 'name')

    values = relationship('Value', backref='variable')

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
        if len(self.values) == 0:
            return False

        return True


class Value(Schema):
    """
    :type variable_id: int
    :type variable: Variable
    :type environment_id: int
    :type environment: Environment
    :type pack_id: int
    :type pack: Pack
    :type data: str
    """

    __tablename__ = 'values'

    variable_id = Column(Integer, ForeignKey('variables.id'), primary_key=True)
    environment_id = Column(Integer, ForeignKey('environments.id'), primary_key=True, nullable=True)
    pack_id = Column(Integer, ForeignKey('packs.id'), primary_key=True)
    data = Column(Text, nullable=False)

    def __repr__(self):
        return "<Value(variable_id='{}', environment_id='{}', pack_id='{}')>".format(self.variable_id,
                                                                                     self.environment_id,
                                                                                     self.pack_id)
