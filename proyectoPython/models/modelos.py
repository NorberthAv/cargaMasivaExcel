from sqlalchemy import Column, Integer,Float, String, Boolean,Numeric,Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bienes(Base):
    __tablename__ = 'bienes'

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
    inmuebles = relationship('BienInmuebles', back_populates='bien')
    vehiculos = relationship('BienVehiculos', back_populates='bien')
    semoviente = relationship('BienSemovientes', back_populates='bien')
    
    
    

class BienMovimiento(Base):
    __tablename__ = 'bien_movimiento'

    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes.id'))
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


class BienVehiculos(Base):
    __tablename__ = 'bien_vehiculos'
    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes.id'), nullable=False)
    propietario = Column(String(20))
    tramite = Column(String(20))
    marca = Column(String(80))
    modelo = Column(String(80))
    color = Column(String(20))
    anho = Column(Integer)
    clase = Column(String(40))
    tipo = Column(String(40))
    uso = Column(String(40))
    servicio = Column(String(40))
    serial_carr = Column(String(40))
    serial_chas = Column(String(40))
    serial_motor = Column(String(40))
    placa = Column(String(10))
    cod_bien = Column(String(40))
    user_ref = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    bien = relationship('Bienes', back_populates='vehiculos')

class BienesMuebles(Base):
    __tablename__ = 'bien_muebles'
    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes.id'))
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
    
class BienInmuebles(Base):
    __tablename__ = 'bien_inmuebles'

    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    municipio_id = Column(Integer, ForeignKey('municipios.id'))
    parroquia_id = Column(Integer, ForeignKey('parroquias.id'))
    cod_bien = Column(String(40))
    urbanizacion_sector = Column(String(255))
    avenida_calle = Column(String(255))
    casa_edificio = Column(String(255))
    piso_numero = Column(String(255))
    localizacion = Column(String(255))
    lindero_norte = Column(Text)
    lindero_sur = Column(Text)
    lindero_este = Column(Text)
    lindero_oeste = Column(Text)
    anho_construccion = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rif_comodatario = Column(String(15))
    ocupacion_id = Column(Integer)
    espacio_uso_id = Column(Integer)
    area_construccion = Column(Numeric(255,0))
    area_terreno = Column(Numeric(255,2))
    udm_construccion_id = Column(Integer)
    udm_terreno_id = Column(Integer)
    oficina_registro = Column(Text)
    fecha_registro = Column(Date)
    numero_registro = Column(String(255))
    tomo = Column(String(20))
    folio = Column(String(25))
    latitud = Column(String(255))
    longitud = Column(String(255))
    poligono = Column(Text)
    user_ref = Column(Integer)
    fecha_ini_contrato = Column(Date)
    fecha_fin_contrato = Column(Date)
    protocolo = Column(String(80))
    pais_id = Column(Integer)
    
    bien = relationship('Bienes', back_populates='inmuebles')
    # estado = relationship('Estados', back_populates='inmuebles')
    # municipio = relationship('Municipios', back_populates='inmuebles')
    # parroquia = relationship('Parroquias', back_populates='inmuebles')
    
    
class BienSemovientes(Base):
    __tablename__ = 'bien_semovientes'
    id = Column(Integer, primary_key=True)
    bien_id = Column(Integer, ForeignKey('bienes.id'), nullable=False)
    proposito_id = Column(Integer, ForeignKey('bien_proposito.id'), nullable=False)
    magnitud_id = Column(Integer, ForeignKey('magnitud.id'), nullable=False)
    udm_id = Column(Integer, ForeignKey('udm.id'), nullable=False)
    cod_bien = Column(String(40))
    raza = Column(String(255))
    cantidad = Column(Float)
    user_ref = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    fecha_nacimiento = Column(Date)
    in_genero = Column(String(1))
    hierro = Column(String(10))
    bien = relationship('Bienes', back_populates='semoviente')
    # proposito = relationship('BienProposito', back_populates='semoviente')
    # magnitud = relationship('Magnitud', back_populates='semoviente')
    # udm = relationship('Udm', back_populates='semoviente')
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
    
class Estados(Base):
    __tablename__ = 'estados'
    id = Column(Integer, primary_key=True)
    estado = Column(String(80))
    iso_3166 = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
class Municipios(Base):
    __tablename__ = 'municipios'
    id = Column(Integer, primary_key=True)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    municipio = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    estado_municipio = relationship('Estados')

class Parroquias(Base):
    __tablename__ = 'parroquias'
    id = Column(Integer, primary_key=True)
    municipio_id = Column(Integer, ForeignKey('municipios.id'))
    parroquia = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    municipio_parroquia = relationship('Municipios')
    
class Udm(Base):
    __tablename__ = 'udm'
    id = Column(Integer, primary_key=True)
    cod = Column(String(5))
    name = Column(String(40))
    description = Column(String(255))
    ref_id = Column(Integer)
    ref_cant = Column(Float)
    magnitud_id = Column(Integer)

class Sedes(Base):
    __tablename__ = 'sedes' 
    id = Column(Integer, primary_key=True)
    ente_id = Column(Integer, nullable=False)
    tipo_sede_id = Column(Integer, nullable=False)
    estado_id = Column(Integer, nullable=False)
    municipio_id = Column(Integer, nullable=False)
    parroquia_id = Column(Integer, nullable=False)
    name = Column(String(80))
    address = Column(String(255))
    phone1 = Column(String(15))
    phone2 = Column(String(15))
    longitud = Column(Float)
    latitud = Column(Float)
    user_ref = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    estatus = Column(Boolean, nullable=False)
    
class EstructuraOrg(Base):
    __tablename__ = 'estructura_org'
    id = Column(Integer, primary_key=True)
    ente_id = Column(Integer, nullable=False)
    sede_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    in_padre = Column(Integer, default=0, nullable=False)
    in_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Ocupacion(Base):
    __tablename__ = 'ocupacion'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    is_active = Column(Boolean)

class BienProposito(Base):
    __tablename__ = 'bien_proposito'
    id = Column(Integer, primary_key=True)
    cod = Column(String(30))
    name = Column(String(30))
    is_active = Column(Boolean)
class EspacioUso(Base):
    __tablename__ = 'espacio_uso'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    is_active = Column(Boolean, default=True)