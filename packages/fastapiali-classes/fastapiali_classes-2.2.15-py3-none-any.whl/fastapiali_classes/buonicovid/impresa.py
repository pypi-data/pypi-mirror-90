from typing import Any, List
from fastapi_sqlalchemy import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from fastapiali_classes import RecordException, WrapperException
from fastapi_modules.sqlalchemy.pgsql_buonicovid import AziendeEsterne
from sqlalchemy import or_
from .acquisizione_buoni_testata import AcquisizioneTestata, ACQSQLError, ACQLoadError, ACQRcdError


class ImpresaError(Exception):
    pass


class ImpresaNotFaund(ImpresaError):
    pass


class ImpresaRecordError(RecordException, ImpresaError):
    pass


class ImpresaSQLError(WrapperException, ImpresaError):
    pass


class ImpresaLoadError(ImpresaError):
    pass


class Imprasa:

    def __init__(self, piva: str, rag_soc: str):
        self.piva = piva
        self.rag_soc = rag_soc
        self._acqusizioni = []
        self._in_db = False

    @property
    def partita_iva(self):
        return self.piva

    @property
    def ragione_sociale(self):
        return self.rag_soc

    @property
    def acquisizioni(self):
        return self._acqusizioni

    def load_acquisizioni(self):
        try:
            self._acqusizioni = AcquisizioneTestata.find(self.piva)
        except (ACQSQLError, ACQRcdError):
            raise ACQLoadError("Errore nel caricamento delle acquisizioni dell'azionda")

    @classmethod
    def from_piva(cls, piva: str) -> "Imprasa":
        try:
            rcd_impresa = db.session.query(AziendeEsterne). \
                filter(AziendeEsterne.piva == piva).one()
            return cls.from_record(rcd_impresa)
        except NoResultFound:
            db.session.rollback()
            raise ImpresaNotFaund("Impresa non trovata col codice fornito.")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ImpresaSQLError("Errore durante la ricerca dell'azienda.", e)
        except ImpresaRecordError:
            raise

    @classmethod
    def from_record(cls, record: Any) -> "Imprasa":
        try:
            impresa = cls(record.piva, record.rag_soc)
            impresa._in_db = True
            return impresa
        except AttributeError:
            raise ImpresaRecordError("Errore nella creazione della classe impresa", record)

    @classmethod
    def find(cls, filtro: str = None) -> List["Imprasa"]:
        try:
            if filtro:
                rcds_aziende = db.session.query(AziendeEsterne). \
                    filter(or_(AziendeEsterne.piva.ilike("%" + filtro + "%"),
                               AziendeEsterne.rag_soc.ilike("%" + filtro + "%"))).all()
            else:
                rcds_aziende = db.session.query(AziendeEsterne).all()

            return [cls.from_record(rcd_azienda) for rcd_azienda in rcds_aziende]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ImpresaSQLError("Errore nella lettura delle azinde.", e)
        except ImpresaRecordError:
            raise
