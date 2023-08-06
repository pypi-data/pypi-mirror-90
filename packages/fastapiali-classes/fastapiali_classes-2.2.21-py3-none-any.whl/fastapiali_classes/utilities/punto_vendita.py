from typing import Any
from fastapiali_classes import WrapperException, RecordException
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_ods import DimNegozio
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from sqlalchemy import or_


class PVError(Exception):
    pass


class PVRcdError(RecordException, PVError):
    pass


class PVSQLError(WrapperException, PVError):
    pass


class PuntoVendita:

    def __init__(self, cod_negozio: str, des_negozio: str):
        self._cod_negozio = cod_negozio
        self._des_negozio = des_negozio

    @property
    def cod_negozio(self):
        return self._cod_negozio

    @property
    def des_negozio(self):
        return self._des_negozio

    @classmethod
    def from_record(cls, rcd: Any):
        try:
            return cls(rcd.cod_negozio, rcd.des_negozio)
        except AttributeError:
            raise PVRcdError("Errore nel recod per la creazione classe punto vendita", rcd)

    @classmethod
    def from_codice(cls, cod_negozio: str):
        try:
            rcd_pv = db.session.query(DimNegozio).filter(DimNegozio.cod_negozio == cod_negozio).one()
            return cls.from_record(rcd_pv)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise PVSQLError("Errore nella lettura del negozio.", e)

    @classmethod
    def find(cls, filtro: Optional[str] = None):
        try:
            rcds_pv = db.session.query(DimNegozio)
            if filtro:
                rcds_pv = rcds_pv.\
                    filter(or_(DimNegozio.cod_negozio.ilike(f'%{filtro}%'),
                               DimNegozio.des_negozio.ilike(f'%{filtro}%')))
            rcds_pv = rcds_pv.all()
            return [cls.from_record(rcd) for rcd in rcds_pv]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise PVSQLError("Errore nella lettura dei negozi", e)
        except PVRcdError:
            raise

