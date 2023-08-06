from fastapiali_classes import WrapperException, RecordException
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_buonicovid import BuoniTagli
from sqlalchemy.exc import SQLAlchemyError
from typing import Any


class TaglioBuonoError(Exception):
    pass


class TaglioBuonoRCDError(RecordException, TaglioBuonoError):
    pass


class TaglioBuonoSQLError(WrapperException, TaglioBuonoError):
    pass


class TaglioBuono:

    def __init__(self, cifra: str, numero: int):
        self._id = None
        self.cifra = cifra
        self.numero = numero
        self._in_db = False
        self._modified = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def cifra(self) -> str:
        return self._cifra

    @cifra.setter
    def cifra(self, cifra):
        self._cifra = cifra
        self._modified = True

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero
        self._modified = True

    @classmethod
    def from_record(cls, record: Any) -> "TaglioBuono":
        try:
            taglio = cls(record.cifra, record.numero)
            taglio._id = record.id
            taglio._in_db = True
            return taglio
        except AttributeError:
            raise TaglioBuonoRCDError("Errore nella creazione della classe taglio buono", record)

    @classmethod
    def from_id(cls, id_buono: int):
        try:
            rcd_taglio = db.session.query(BuoniTagli).filter(BuoniTagli.id == id_buono).one()
            return cls.from_record(rcd_taglio)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise TaglioBuonoSQLError("Errore nella lettura del taglio del buono", e)
        except TaglioBuonoRCDError:
            raise

    @classmethod
    def find(cls):
        try:
            rcds_buoni = db.session.query(BuoniTagli).all()
            return [cls.from_record(rcd) for rcd in rcds_buoni]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise TaglioBuonoSQLError("Errore nella lettura dei tagli buoni", e)
