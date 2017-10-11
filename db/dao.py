from sqlalchemy import Column, Integer, String, Text, ForeignKey, Sequence, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Schema = declarative_base()


class Pack(Schema):
    """
    :type id: int
    :type name: str
    :type values: list[Value]
    """

    __tablename__ = 'packs'

    id = Column(Integer, Sequence('pack_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    values = relationship('Value', backref='pack')

    def __repr__(self):
        return "<Pack(name='{}', id='{}')>".format(self.name, self.id)


class Environment(Schema):
    """
    :type id: int
    :type name: str
    :type values: list[Value]
    """

    __tablename__ = 'environments'

    id = Column(Integer, Sequence('environment_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    values = relationship('Value', backref='environment')

    def __repr__(self):
        return "<Environment(name='{}', id='{}')>".format(self.name, self.id)


template_tags = Table('template_tags', Schema.metadata,
                      Column('tag_id', ForeignKey('tags.id'), primary_key=True),
                      Column('template_id', ForeignKey('templates.id'), primary_key=True)
                      )


class Tag(Schema):
    """
    :type id: int
    :type name: str
    :type templates: list[Template]
    """

    __tablename__ = 'tags'

    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    templates = relationship('Template', secondary=template_tags, back_populates='tags')

    def __repr__(self):
        return "<Tag(name='{}', id='{}')>".format(self.name, self.id)


class Template(Schema):
    """
    :type id: int
    :type name: str
    :type text: str
    :type tags: list[Tag]
    :type variables: list[Variable]
    """

    __tablename__ = 'templates'

    id = Column(Integer, Sequence('template_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    text = Column(Text, nullable=False)

    tags = relationship('Tag', secondary=template_tags, back_populates='templates')
    variables = relationship('Variable', backref='template')

    def __repr__(self):
        return "<Template(name='{}', id='{}')>".format(self.name, self.id)


class Variable(Schema):
    """
    :type id: int
    :type template_id: int
    :type name: str
    :type description: str
    :type values: list[Value]
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


class Value(Schema):
    """
    :type variable_id: int
    :type environment_id: int
    :type pack_id: int
    :type data: str
    """

    __tablename__ = 'values'

    variable_id = Column(Integer, ForeignKey('variables.id'), primary_key=True)
    environment_id = Column(Integer, ForeignKey('environments.id'), primary_key=True)
    pack_id = Column(Integer, ForeignKey('packs.id'), primary_key=True)
    data = Column(Text, nullable=False)

    def __repr__(self):
        return "<Value(variable_id='{}', environment_id='{}', pack_id='{}')>".format(self.variable_id,
                                                                                     self.environment_id,
                                                                                     self.pack_id)
