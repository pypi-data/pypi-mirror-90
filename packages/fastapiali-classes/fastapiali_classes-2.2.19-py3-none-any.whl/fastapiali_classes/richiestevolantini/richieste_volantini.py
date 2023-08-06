import datetime
from typing import Optional, Any, List, Union

from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_richiestevolantini import Richieste, RichiesteEmail
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from fastapiali_classes.utilities.punto_vendita import PVRcdError
from fastapiali_classes import WrapperException, RecordException
from .linea_vol import LineaVolantini, LineaVolRcdError
from .offerta_volantini import OffertaVolantini, OfferteVolRcdError
from .vol_PV import VolPV


class RicVolError(Exception):
    pass


class RicVolSQLError(WrapperException, RicVolError):
    pass


class RicVolRcdError(RecordException, RicVolError):
    pass


class RicVolLoadError(RicVolError):
    pass


class RicVolNotFound(RicVolError):
    pass


class RicVolIncompatibilityError(RicVolError):
    pass


class StatoRichiesta:
    def __init__(self, codice: int, descrizione: str):
        self.codice = codice
        self.descrizione = descrizione

    def __str__(self):
        return self.descrizione

    def __eq__(self, other):
        if isinstance(other, StatoRichiesta):
            return self.codice == other.codice
        elif isinstance(other, int):
            return self.codice == other
        else:
            return NotImplemented


class RichiesteVolantini:

    STATO_IN_MODIFICA = StatoRichiesta(codice=0, descrizione="In modifica")
    STATO_CREATA = StatoRichiesta(codice=1, descrizione="Creata")
    STATO_PROCESSATA = StatoRichiesta(codice=2, descrizione="Processata")
    _STATI = {
        STATO_IN_MODIFICA.codice: STATO_IN_MODIFICA,
        STATO_CREATA.codice: STATO_CREATA,
        STATO_PROCESSATA.codice: STATO_PROCESSATA
    }

    def __init__(self, anno: str, dt_inizio: datetime, dt_fine: datetime, invio_ora: bool,
                 offerta: Union[OffertaVolantini, int], linea: Union[LineaVolantini, int],
                 punto_vendita: Union[VolPV, str], utente: Optional[str] = None):
        self._id = None
        self._dt_creazione = None
        self.__anno = anno
        self.__offerta = offerta
        self.__linea = linea
        self.__punto_vendita = punto_vendita
        self.__dt_inizio = dt_inizio
        self.__dt_fine = dt_fine
        self.__invio_ora = invio_ora
        self.__utente = utente
        self._emails = []
        self._stato = 1
        self._in_db = False
        self._modified = False

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value
        self._modified = True

    @property
    def anno(self) -> str:
        return self.__anno

    @anno.setter
    def anno(self, value: str):
        self.__anno = value
        self._modified = True

    @property
    def id_offerta(self):
        if type(self.__offerta) == int:
            return self.__offerta
        else:
            return self.__offerta.id

    @property
    def offerta(self) -> Union[OffertaVolantini, int]:
        return self.__offerta

    @offerta.setter
    def offerta(self, value: Union[OffertaVolantini, int]):
        self.__offerta = value
        self._modified = True

    @property
    def id_linea(self):
        if type(self.__linea) == int:
            return self.__linea
        else:
            return self.__linea.id

    @property
    def linea(self) -> Union[LineaVolantini, int]:
        return self.__linea

    @linea.setter
    def linea(self, value: Union[LineaVolantini, int]):
        self.__linea = value
        self._modified = True

    @property
    def cod_negozio(self):
        if type(self.__punto_vendita) == str:
            return self.__punto_vendita
        else:
            return self.__punto_vendita.cod_negozio

    @property
    def punto_vendita(self) -> Union[VolPV, str]:
        return self.__punto_vendita

    @punto_vendita.setter
    def punto_vendita(self, value: Union[VolPV, str]):
        self.__punto_vendita = value
        self._modified = True

    @property
    def dt_inizio(self) -> datetime.date:
        return self.__dt_inizio

    @dt_inizio.setter
    def dt_inizio(self, value: datetime.date):
        self.__dt_inizio = value
        self._modified = True

    @property
    def dt_fine(self) -> datetime.date:
        return self.__dt_fine

    @dt_fine.setter
    def dt_fine(self, value: datetime.date):
        self.__dt_fine = value
        self._modified = True

    @property
    def invio_ora(self) -> bool:
        return self.__invio_ora

    @invio_ora.setter
    def invio_ora(self, value: bool):
        self.__invio_ora = value
        self._modified = True

    @property
    def dt_creazione(self) -> datetime.datetime:
        return self._dt_creazione

    @dt_creazione.setter
    def dt_creazione(self, value: datetime.datetime):
        self._dt_creazione = value
        self._modified = True

    @property
    def emails(self) -> List[str]:
        return self._emails

    @emails.setter
    def emails(self, value: List[str]):
        self._emails = value
        self._modified = True

    @property
    def utente(self) -> str:
        return self.__utente

    @utente.setter
    def utente(self, value: str):
        self.__utente = value
        self._modified = True

    @property
    def stato(self) -> Union['StatoRichiesta', int]:
        return self._stato

    @stato.setter
    def stato(self, value):
        self._stato = self._STATI[value]
        self._modified = True

    def save(self):
        try:
            if not self._in_db:
                self._insert()
            else:
                if self._modified:
                    self._update()
        except (RicVolSQLError, RicVolNotFound):
            raise

    def delete(self):
        qry_ric = db.session.query(Richieste).filter(Richieste.id == self.id)
        qrys_email = db.session.query(RichiesteEmail).filter(RichiesteEmail.id_richiesta == self.id)
        try:
            rcd_ric = qry_ric.with_for_update().one()
            if rcd_ric.stato > self.STATO_IN_MODIFICA.codice:
                qrys_email.delete()
                db.session.delete(rcd_ric)
                db.session.commit()
            else:
                raise RicVolIncompatibilityError("Errore, lo stato non permette l'eliminazione.")
        except RicVolIncompatibilityError:
            db.session.rollback()
            raise
        else:
            del self

    def _insert(self):
        try:
            rcd_ric = Richieste(anno=self.__anno, id_offerta=self.id_offerta, id_linea=self.id_linea,
                                cod_negozio=self.cod_negozio, dt_inizio=self.__dt_inizio, dt_fine=self.__dt_fine,
                                invio_ora=self.__invio_ora, utente=self.__utente)
            db.session.add(rcd_ric)
            db.session.commit()
            self.id = rcd_ric.id
            self._dt_creazione = rcd_ric.dt_creazione
            db.session.bulk_insert_mappings(
                RichiesteEmail,
                [
                    dict(id_richiesta=self._id, email=em)
                    for em in self._emails
                ]
            )
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.commit()
            raise RicVolSQLError("Errore nell'inserimeto della richiesta.", e)
        else:
            self._in_db = True
            self._modified = False

    def _update(self):
        qry_ric = db.session.query(Richieste).filter(Richieste.id == self.id).with_for_update()
        qrys_emails = db.session.query(RichiesteEmail).filter(RichiesteEmail.id_richiesta == self.id)
        try:
            rcd_ric = qry_ric.one()
            qrys_emails.delete()
            db.session.commit()
            rcd_ric.anno = self.__anno
            rcd_ric.id_offerta = self.id_offerta
            rcd_ric.id_linea = self.id_linea
            rcd_ric.cod_negozio = self.cod_negozio
            rcd_ric.dt_inizio = self.__dt_inizio
            rcd_ric.dt_fine = self.__dt_fine
            rcd_ric.invio_ora = self.__invio_ora
            rcd_ric.utente = self.__utente
            db.session.bulk_insert_mappings(
                RichiesteEmail,
                [
                    dict(id_richiesta=self.id, email=em)
                    for em in self._emails
                ]
            )
            rcd_ric.stato = self.stato.codice
            db.session.commit()
        except NoResultFound:
            db.session.rollback()
            raise RicVolNotFound("Nessuna richiesta trovata con l'id fornito")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RicVolSQLError("Errore nell'aggiornamento della richiesta", e)
        else:
            self._in_db = True
            self._modified = False

    @classmethod
    def from_record(cls, rcd: Any) -> 'RichiesteVolantini':
        try:
            offerta = OffertaVolantini.from_record(rcd.offerta)
            linea = LineaVolantini.from_record(rcd.linea)
            punto_vendita = VolPV.from_record(rcd.punto_vendita)
            ric = cls(anno=rcd.anno, offerta=offerta, linea=linea, punto_vendita=punto_vendita, dt_inizio=rcd.dt_inizio,
                      dt_fine=rcd.dt_fine, invio_ora=rcd.invio_ora, utente=rcd.utente)
            ric._id = rcd.id
            ric._dt_creazione = rcd.dt_creazione
            ric._emails = [rcd.email for rcd in rcd.emails]
            ric._stato = cls._STATI[rcd.stato]
            ric._in_db = True
            return ric
        except AttributeError:
            raise RicVolRcdError("Errore nella creazione della classe richiesta volantini.", rcd)
        except (OfferteVolRcdError, LineaVolRcdError, PVRcdError):
            raise RicVolLoadError("Errore nel caricamento dei record offerta o linea o punto vendita")

    @classmethod
    def from_id(cls, id_richiesta: int) -> 'RichiesteVolantini':
        try:
            rcd_ric = db.session.query(Richieste).\
                outerjoin(RichiesteEmail, RichiesteEmail.id_richiesta == Richieste.id).\
                options(joinedload(Richieste.emails)).\
                options(joinedload(Richieste.offerta)).\
                options(joinedload(Richieste.linea)).\
                options(joinedload(Richieste.punto_vendita)).\
                filter(Richieste.id == id_richiesta).one()
            return cls.from_record(rcd_ric)
        except NoResultFound:
            db.session.rollback()
            raise RicVolNotFound("Nessuna richiesta trovata con l'id fornito")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RicVolSQLError("Errore nella lettura delle richiesta", e)
        except (RicVolRcdError, RicVolLoadError):
            raise

    @classmethod
    def find(cls, dt_inizio_creazione: Optional[Union[datetime.datetime, str]] = None,
             dt_fine_creazione: Optional[Union[datetime.datetime, str]] = None,
             dt_inizio_ric: Optional[Union[datetime.datetime, str]] = None,
             dt_fine_ric:  Optional[Union[datetime.datetime, str]] = None) -> List['RichiesteVolantini']:
        try:
            if dt_inizio_creazione and dt_fine_creazione:
                if dt_inizio_creazione < dt_fine_creazione:
                    raise RicVolIncompatibilityError("Data inizio minore di data fine")
                if dt_inizio_ric and dt_fine_ric:
                    raise RicVolIncompatibilityError("Data inizio periodo richiesta minore data fine periodo richiesta")
            rcds_ric = db.session.query(Richieste).\
                outerjoin(RichiesteEmail, RichiesteEmail.id_richiesta == Richieste.id).\
                options(joinedload(Richieste.emails)).\
                options(joinedload(Richieste.offerta)).\
                options(joinedload(Richieste.linea)).\
                options(joinedload(Richieste.punto_vendita))
            if dt_inizio_creazione:
                inizio_creazione = datetime.datetime.strptime(dt_inizio_creazione, "%Y-%M-%d") \
                    if type(dt_inizio_creazione) == str else dt_inizio_creazione
                rcds_ric = rcds_ric.filter(Richieste.dt_creazione >= datetime.datetime.combine(
                    inizio_creazione, datetime.datetime.min.time()))
            if dt_fine_creazione:
                fine_creazione = datetime.datetime.strptime(dt_fine_creazione, "%Y-%M-%d") \
                    if type(dt_fine_creazione) == str else dt_fine_creazione
                rcds_ric = rcds_ric.filter(Richieste.dt_creazione <= datetime.datetime.combine(
                    fine_creazione, datetime.datetime.max.time()))
            if dt_inizio_ric:
                inizio_ric = datetime.datetime.strptime(dt_inizio_ric, "%Y-%M-%d") \
                    if type(dt_inizio_ric) == str else dt_inizio_ric
                rcds_ric = rcds_ric.filter(Richieste.dt_inizio >= datetime.datetime.combine(
                    inizio_ric, datetime.datetime.min.time()))
            if dt_fine_ric:
                fine_ric = datetime.datetime.strptime(dt_fine_ric, "%Y-%M-%d") \
                    if type(dt_fine_ric) == str else dt_fine_ric
                rcds_ric = rcds_ric.filter(Richieste.dt_fine <= datetime.datetime.combine(
                    fine_ric, datetime.datetime.max.time()))
            rcds_ric = rcds_ric.all()
            return [cls.from_record(rcd) for rcd in rcds_ric]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RicVolSQLError("Errore nella lettura delle richieste", e)
        except RicVolIncompatibilityError:
            db.session.rollback()
            raise
        except (RicVolRcdError, RicVolLoadError):
            raise
