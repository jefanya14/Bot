from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from userbot import DB_URI

BASE = declarative_base()


def start() -> scoped_session:
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


def delete_table(table_name):
    metadata = MetaData()
    metadata.reflect(engine)
    table = metadata.tables.get(table_name)
    if table is not None:
        LOGS.info(f"Deleting '{table_name}' table...")
        BASE.metadata.drop_all(engine, [table], checkfirst=True)


SESSION = start()
