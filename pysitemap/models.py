from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, exists
from sqlalchemy.orm import relationship
import hashlib
from db import Model, db_endine, session
import uuid
from validators import domain as domain_validator

groups_domains = Table(
    'groups_domains',
    Model.metadata,
    Column('domain_id', Integer, ForeignKey('domain_groups.id')),
    Column('group_id', Integer, ForeignKey('domains.id'))
)


class DomainGroup(Model):
    __tablename__ = 'domain_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    domains = relationship("Domain", secondary=groups_domains, back_populates="groups")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Domain group {}: {}>".format(self.id, self.name)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class Domain(Model):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    domain = Column(String(200), nullable=False)
    domains = relationship("DomainGroup", secondary=groups_domains, back_populates="domains")

    def __init__(self, domain):
        self.validate_domain(domain)
        self.domain = domain

    def validate_domain(self, domain=None):
        domain = domain or self.domain
        return domain_validator(domain, raise_errors=True)

    def __repr__(self):
        return "<Domain {}: {}>".format(self.id, self.domain)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    token = Column(String(250), default='Unknown')
    is_active = Column(Boolean, default=False)

    def __init__(self, username: str):
        self.username = username
        m = hashlib.sha256()
        m.update('{}{}'.format(username, uuid.uuid4()).encode('utf-8'))
        self.token = m.hexdigest()

    @classmethod
    def validate(cls, username, token):
        return session.query(cls).filter(cls.username == username, cls.token == token).count() == 1

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


Model.metadata.create_all(db_endine)
