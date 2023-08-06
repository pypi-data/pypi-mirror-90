from datetime import datetime
from typing import Any, List, Optional
from fastapiali_classes import WrapperException, RecordException
from sqlalchemy.exc import SQLAlchemyError
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_buonicovid import AcquisizioneBuoniTestata, AcquisizioneBuoniDettagli
from .acquisizione_buoni_dettagli import AcquisizioneDettagli, ACQDetSQLError
from sqlalchemy.orm import contains_eager


class ACQError(Exception):
    pass


class ACQSQLError(WrapperException, ACQError):
    pass


class ACQRcdError(RecordException, ACQError):
    pass


class ACQLoadError(ACQError):
    pass


class AcquisizioneTestata:

    def __init__(self, piva: str):
        self._id = None
        self.piva = piva
        self._dt_creazione = None
        self._dettagli = []
        self._in_db = False
        self._modified = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def piva(self) -> str:
        return self.__piva

    @piva.setter
    def piva(self, value):
        self.__piva = value
        self._modified = True

    @property
    def dt_creazione(self) -> datetime:
        return self._dt_creazione

    @property
    def dettagli(self):
        return self._dettagli

    @dettagli.setter
    def dettagli(self, value: List["AcquisizioneDettagli"]):
        self._dettagli = value
        self._modified = True

    def save(self):
        try:
            if not self._in_db:
                self._insert()
            else:
                if self._modified:
                    self._update()
        except (ACQSQLError, ACQDetSQLError):
            raise ACQLoadError("Errore nel salvataggio dell'acquisizione")

    def _insert(self):
        try:
            rcd = AcquisizioneBuoniTestata(piva=self.piva)
            db.session.add(rcd)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nella creazione della testata.", e)
        else:
            self._id = rcd.id
            self._dt_creazione = rcd.dt_creazione
            self._in_db = True
            self._modified = False

    def _update(self):
        try:
            rcd = db.session.query(AcquisizioneBuoniTestata).filter(AcquisizioneBuoniTestata.id == self.id). \
                with_for_update().one()
            if len(self._dettagli) > 0:
                db.session.query(AcquisizioneBuoniDettagli). \
                    filter(AcquisizioneBuoniDettagli.id_testata_acquisizione == self.id).delete()
                for det in self._dettagli:  # type: AcquisizioneDettagli
                    det.save()
            rcd.piva = self.piva
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nell'aggiornamento della testata acquisizione buoni", e)
        except ACQDetSQLError:
            db.session.rollback()
            raise ACQLoadError("Errore nel salvataggio dei dettagli")
        else:
            self._in_db = True
            self._modified = False

    def delete(self):
        try:
            rcd = db.session.query(AcquisizioneBuoniTestata).filter(AcquisizioneBuoniTestata.id == self.id). \
                with_for_update().one()
            if len(self._dettagli) > 0:
                for det in self._dettagli:  # type: AcquisizioneDettagli
                    det.delete()
            db.session.delete(rcd)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nella cancellazione dell'acquisizione dei buoni.", e)
        except ACQDetSQLError:
            db.session.rollback()
            raise ACQLoadError("Errore nella cancellazione dei dettagli della acquisizione.")
        else:
            self._in_db = False
            self._modified = False

    def load_dettagli(self):
        try:
            db.session.query(AcquisizioneBuoniTestata). \
                filter(AcquisizioneBuoniTestata.id == self.id).with_for_update().one()
            self._dettagli = AcquisizioneDettagli.find(self.id)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nella lettura dei dettagli acqiosizione", e)
        except ACQDetSQLError:
            db.session.rollback()
            raise ACQLoadError("Errore nella lettura dei dettagli acquisizione")

    @classmethod
    def from_record(cls, record: Any) -> "AcquisizioneTestata":
        try:
            testata = cls(record.piva)
            testata._id = record.id
            testata._dt_creazione = record.dt_creazione
            testata._in_db = True
            return testata
        except AttributeError:
            raise ACQRcdError("Errore nella creazione della classe testata acquisizione. Errore interno.", record)

    @classmethod
    def from_id(cls, id_testata: int) -> "AcquisizioneTestata":
        try:
            rcd_testata = db.session.query(AcquisizioneBuoniTestata). \
                options(contains_eager(AcquisizioneBuoniTestata.azienda)). \
                filter(AcquisizioneBuoniTestata.id == id_testata).one()
            return cls.from_record(rcd_testata)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nella lettura della testata acquisizione buoni.", e)
        except ACQRcdError:
            raise

    @classmethod
    def find(cls, piva: Optional[str] = None):
        try:
            if piva:
                rcds_testate = db.session.query(AcquisizioneBuoniTestata). \
                    options(contains_eager(AcquisizioneBuoniTestata.azienda)). \
                    filter(AcquisizioneBuoniTestata.piva == piva). \
                    order_by(AcquisizioneBuoniTestata.id.desc()).all()
                return [cls.from_record(rcd) for rcd in rcds_testate]
            rcds_testate = db.session.query(AcquisizioneBuoniTestata). \
                options(contains_eager(AcquisizioneBuoniTestata.azienda)). \
                order_by(AcquisizioneBuoniTestata.id.desc()).all()
            return [cls.from_record(rcd) for rcd in rcds_testate]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQSQLError("Errore nella lettura delle testate acquisizione buoni.", e)
        except ACQRcdError:
            raise
