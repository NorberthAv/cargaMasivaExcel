from sqlalchemy import Column, Integer, String, Boolean,Numeric,Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bienes(Base):
    __tablename__ = 'bienes_prueba222'

    id = Column(Integer, primary_key=True)
    tipobien_id = Column(Integer, nullable=False)
    categ_id = Column(Integer, nullable=False)
    subcateg_id = Column(Integer, nullable=False)
    categesp_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    fecha_adquisicion = Column(Date)
    num_documento = Column(String(255))
    valor_inicial = Column(Numeric(20,2))
    moneda_id = Column(Integer, nullable=False)
    user_ref = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    serial = Column(String(80))
    cod_bien = Column(String(80))
    fec_cierre = Column(DateTime)
    bienstatus_id = Column(Integer, default=1)
    observacion = Column(Text)
    cod_categ = Column(String(15))
    depreciacion = Column(Numeric(20,2))
    valor_contable = Column(Numeric(20,2))
    conforme = Column(Boolean, default=True)

    # Relación con BienesMuebles
    muebles = relationship('BienesMuebles', back_populates='bien')

class BienMovimiento(Base):
    __tablename__ = 'bien_movimiento'

    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes_prueba222.id'))
    ente_id = Column(Integer)
    sede_id = Column(Integer)
    adquisicion_id = Column(Integer)
    condicion_id = Column(Integer)
    uso_id = Column(Integer)
    unidad_id = Column(Integer)
    cod_bien = Column(String(40))
    fecha_movimiento = Column(Date)
    num_documento = Column(String(255))
    observacion = Column(String(255))
    user_ref = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    serial = Column(String(80))
    ocupacion_id = Column(Integer)
    espacio_uso_id = Column(Integer)
    rif_comodatario = Column(String(15))
    udm_construccion_id = Column(Integer)
    area_construccion = Column(Numeric(255,2))
    fecha_ini_contrato = Column(Date)
    fecha_fin_contrato = Column(Date)
    num_contrato = Column(String(40))
    udm_terreno_id = Column(Integer)
    area_terreno = Column(Numeric(255,2))



class BienesMuebles(Base):
    __tablename__ = 'bien_muebles_prueba'
    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes_prueba222.id'))
    cod_bien = Column(String(40))
    marca = Column(String(80))
    modelo = Column(String(80))
    color = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    serial = Column(String(80))
    user_ref = Column(Integer)

    # Relación con Bienes
    bien = relationship('Bienes', back_populates='muebles')
class Moneda(Base):
    __tablename__ = 'moneda'
    id = Column(Integer, primary_key=True)
    cod_iso = Column(String(3))
    simbol = Column(String(5))
    name = Column(String(40))
    decimales = Column(Integer, default=2)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, default=False)
    is_local = Column(Boolean, default=False)

class BienCategoria(Base):
    __tablename__ = 'bien_categoria'
    id = Column(Integer, primary_key=True)
    cod = Column(String(3))
    name = Column(String(80))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    tipobien_id = Column(Integer)

class BienSubCategoria(Base):
    __tablename__ = 'bien_subcateg'
    id = Column(Integer, primary_key=True)
    categ_id = Column(Integer, ForeignKey('bien_categoria.id'))
    cod = Column(String(3))
    name = Column(String(80))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    categoria = relationship('BienCategoria')

class BienCategEsp(Base):
    __tablename__ = 'bien_categesp'
    id = Column(Integer, primary_key=True)
    subcateg_id = Column(Integer, ForeignKey('bien_subcateg.id'))
    cod = Column(String(4))
    name = Column(String(80))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    subcategoria = relationship('BienSubCategoria')

class BienAdquisicion(Base):
    __tablename__ = 'bien_adquisicion'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class BienCondicion(Base):
    __tablename__ = 'bien_condicion'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    inm = Column(Boolean, default=False)

class BienUso(Base):
    __tablename__ = 'bien_uso'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(255))
    in_active = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, default=True)