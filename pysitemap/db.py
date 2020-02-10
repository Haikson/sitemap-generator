from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import ClauseElement

DB_URI = 'sqlite:///stuff.db'

db_endine = create_engine(DB_URI)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_endine
    )
)

Model = declarative_base()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True






