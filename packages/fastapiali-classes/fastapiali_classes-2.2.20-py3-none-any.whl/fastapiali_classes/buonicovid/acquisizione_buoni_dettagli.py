from typing import Any, List
from fastapiali_classes import WrapperException, RecordException
from sqlalchemy.exc import SQLAlchemyError
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_buonicovid import AcquisizioneBuoniDettagli


class ACQDetError(Exception):
    pass


class ACQDetSQLError(WrapperException, ACQDetError):
    pass


class ACQDetRcdError(RecordException, ACQDetError):
    pass


class AcquisizioneDettagli:

    def __init__(self, id_buono: int, qta: int, id_testata: int):
        self._id = None
        self.id_buono = id_buono
        self.qta = qta
        self.id_testata = id_testata
        self._dt_inserimento = None
        self._in_db = False
        self._modified = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def dt_inserimento(self):
        return self._dt_inserimento

    @property
    def id_buono(self):
        return self.__id_buono

    @id_buono.setter
    def id_buono(self, value: int):
        self.__id_buono = value
        self._modified = True

    @property
    def qta(self) -> int:
        return self.__qta

    @qta.setter
    def qta(self, value: int):
        self.__qta = value
        self._modified = True

    @property
    def id_testata(self) -> int:
        return self.__id_testata

    @id_testata.setter
    def id_testata(self, value: int):
        self.__id_testata = value
        self._modified = True

    def save(self):
        try:
            if not self._in_db:
                self._insert()
            else:
                if self._modified:
                    self._update()
        except ACQDetSQLError:
            raise

    def _insert(self):
        try:
            rcd = AcquisizioneBuoniDettagli(id_taglio_buono=self.id_buono, qta_buono=self.qta,
                                            id_testata_acquisizione=self.id_testata)
            db.session.add(rcd)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQDetSQLError("Errore nell'inserimento del dettaglio.", e)
        else:
            self._id = rcd.id
            self._dt_inserimento = rcd.dt_inserimento
            self._in_db = True
            self._modified = False

    def _update(self):
        try:
            rcd = db.session.query(AcquisizioneBuoniDettagli).filter(AcquisizioneBuoniDettagli.id == self.id). \
                with_for_update().one()
            rcd.id_taglio_buono = self.id_buono
            rcd.qta_buono = self.qta
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQDetSQLError("Errore nell'aggiornamento del dettaglio", e)
        else:
            self._in_db = True
            self._modified = False

    def delete(self):
        try:
            db.session.query(AcquisizioneBuoniDettagli).filter(AcquisizioneBuoniDettagli.id == self.id).delete()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQDetSQLError("Errore nella eliminazione del dettaglio.", e)
        else:
            self._in_db = False
            self._modified = False

    @classmethod
    def from_record(cls, record: Any) -> "AcquisizioneDettagli":
        try:
            dettaglio = cls(record.id_taglio_buono, record.qta_buono, record.id_testata_acquisizione)
            dettaglio._id = record.id
            dettaglio._dt_inserimento = record.dt_inserimento
            dettaglio._in_db = True
            return dettaglio
        except AttributeError:
            raise ACQDetRcdError("Errore nella creazione della classe dettaglio acquisizione.", record)

    @classmethod
    def from_id(cls, id_dettaglio: int) -> "AcquisizioneDettagli":
        try:
            rcd_dettaglio = db.session.query(AcquisizioneBuoniDettagli). \
                filter(AcquisizioneBuoniDettagli.id == id_dettaglio).one()
            return cls.from_record(rcd_dettaglio)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQDetSQLError("Errore nella lettura del dettaglio", e)
        except ACQDetRcdError:
            raise

    @classmethod
    def find(cls, id_testata: int) -> List["AcquisizioneDettagli"]:
        try:
            rcds_dettagli = db.session.query(AcquisizioneBuoniDettagli). \
                filter(AcquisizioneBuoniDettagli.id_testata_acquisizione == id_testata).all()
            return [cls.from_record(rcd) for rcd in rcds_dettagli]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ACQDetSQLError("Errore nella lettura dei dettagli.", e)
        except ACQDetRcdError:
            raise