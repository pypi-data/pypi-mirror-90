from typing import Any, List, Optional
from fastapiali_classes import WrapperException, RecordException
from fastapi_sqlalchemy import db
from sqlalchemy.exc import SQLAlchemyError
from fastapi_modules.sqlalchemy.pgsql_richiestevolantini import Offerte, OfferteAnni


class OfferteVolError(Exception):
    pass


class OfferteVolRcdError(RecordException, OfferteVolError):
    pass


class OfferteVolSQLError(WrapperException, OfferteVolError):
    pass


class OffertaVolantini:

    def __init__(self, id_offerta: int, descrizione: str):
        self._id = id_offerta
        self._descrizione = descrizione

    @property
    def id(self) -> int:
        return self._id

    @property
    def descrizione(self) -> str:
        return self._descrizione

    @classmethod
    def from_record(cls, rcd: Any) -> 'OffertaVolantini':
        try:
            return cls(rcd.id, rcd.descrizione)
        except AttributeError:
            raise OfferteVolRcdError("Errore nei parametri del record offerta", rcd)

    @classmethod
    def from_id(cls, id_offerta: int):
        try:
            rcd_offerta = db.session.query(Offerte).filter(Offerte.id == id_offerta).one()
            return cls.from_record(rcd_offerta)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise OfferteVolSQLError("Errore nella lettura dell'offerta volantino.", e)
        except OfferteVolRcdError:
            raise

    @classmethod
    def find(cls, anno: Optional[str] = None) -> List['OffertaVolantini']:
        try:
            rcds_offerte = db.session.query(Offerte)
            if anno:
                rcds_offerte = rcds_offerte.\
                    join(OfferteAnni, OfferteAnni.id_offerta == Offerte.id).\
                    filter(OfferteAnni.anno == anno)
            rcds_offerte = rcds_offerte.all()
            return [cls.from_record(rcd) for rcd in rcds_offerte]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise OfferteVolSQLError("Errore nella lettura delle offerte volantino", e)
        except OfferteVolRcdError:
            raise
