from fastapiali_classes.utilities.punto_vendita import PuntoVendita, PVRcdError, PVSQLError
from typing import Optional
from fastapi_sqlalchemy import db
from fastapi_modules.sqlalchemy.pgsql_ods import DimNegozio
from fastapi_modules.sqlalchemy.pgsql_richiestevolantini import LineeNegozi
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from fastapiali_classes import WrapperException


class VolPVError(Exception):
    pass


class VolPVSQLError(WrapperException, VolPVError):
    pass


class VolPVLoadError(VolPVError):
    pass


class VolPV(PuntoVendita):
    
    def __init__(self, cod_negozio: str, des_negozio: str):
        super().__init__(cod_negozio, des_negozio)

    @classmethod
    def find(cls, filtro: Optional[str] = None, id_linea: Optional[int] = None):
        try:
            rcds_pv = db.session.query(DimNegozio)
            if filtro:
                rcds_pv = rcds_pv. \
                    filter(or_(DimNegozio.cod_negozio.ilike(f'%{filtro}%'),
                               DimNegozio.des_negozio.ilike(f'%{filtro}%')))
            if id_linea:
                rcds_pv = rcds_pv.\
                    join(LineeNegozi, LineeNegozi.cod_negozio == DimNegozio.cod_negozio).\
                    filter(LineeNegozi.id_linea == id_linea)
            rcds_pv = rcds_pv.all()
            return [cls.from_record(rcd) for rcd in rcds_pv]
        except SQLAlchemyError as e:
            db.session.rollback()
            raise VolPVSQLError("Errore nella lettura dei negozi", e)
        except (PVSQLError, PVRcdError):
            raise VolPVLoadError("Errore nella lettura dei punti vendita")
