from typing import Any, Optional, List
from fastapiali_classes import WrapperException, RecordException
from sqlalchemy.exc import SQLAlchemyError
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_richiestevolantini import Linee, OfferteLinee


class LineaVolError(Exception):
    pass


class LineaVolRcdError(RecordException, LineaVolError):
    pass


class LineaVolSQLError(WrapperException, LineaVolError):
    pass


class LineaVolantini:

    def __init__(self, id_linea: int, descrizione: str):
        self._id = id_linea
        self._descrizione = descrizione

    @property
    def id(self) -> int:
        return self._id

    @property
    def descrizione(self) -> str:
        return self._descrizione

    @classmethod
    def from_record(cls, rcd: Any) -> 'LineaVolantini':
        try:
            return cls(rcd.id, rcd.descrizione)
        except AttributeError:
            raise LineaVolRcdError("Errore nei parametri del record classe linea volantini", rcd)

    @classmethod
    def from_id(cls, id_linea: int) -> 'LineaVolantini':
        try:
            rcd_linea = db.session.query(Linee).filter(Linee.id == id_linea).one()
            return cls.from_record(rcd_linea)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise LineaVolRcdError("Errore nella lettura della linea volantini", e)
        except LineaVolRcdError:
            raise

    # Metodo per trovare le linee
    @classmethod
    def find(cls, id_offerta: Optional[int] = None) -> List['LineaVolantini']:
        try:
            rcds_linee = db.session.query(Linee)
            if id_offerta:
                rcds_linee = rcds_linee.join(OfferteLinee, OfferteLinee.id_linea == Linee.id).\
                    filter(OfferteLinee.id_offerta == id_offerta)
            rcds_linee = rcds_linee.all()
            return [cls.from_record(rcd) for rcd in rcds_linee]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise LineaVolSQLError("Errore nella lettura delle line volantino", e)
        except LineaVolRcdError:
            raise
