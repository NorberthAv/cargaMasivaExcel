from database.connect import create_connection, close_connection
import base64
import pandas as pd
import io

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.modelos import Udm,EstructuraOrg,Sedes,Ocupacion, EspacioUso, Moneda, Municipios,Parroquias, BienCategoria, BienSubCategoria, BienCategEsp, BienAdquisicion, BienCondicion, BienUso ,Bienes,BienProposito, BienesMuebles,BienInmuebles,BienVehiculos,BienSemovientes, BienMovimiento, Estados



def cargaMasivaMuebles(file,ente_id,user_id):
    try:
        decoded_data = base64.b64decode(file)
        excel_data = io.BytesIO(decoded_data)
        df = pd.read_excel(excel_data, header=9)
        df = df.drop(columns=['Unnamed: 0'])
        engine = create_engine('postgresql://usrsrgbp:123456@192.168.4.64:5432/bd_srgbp')
        Session = sessionmaker(bind=engine)
        session = Session()

        for index, row in df.iterrows():
            moneda = session.query(Moneda).filter(Moneda.is_active==True, Moneda.is_local==True).first()
            codigo = row['CATEGORÍA ESPECÍFICA'][-9:]
            codcat = codigo[:2]
            subcat = codigo[2:5]
            catesp = codigo[5:]
            categ = session.query(BienCategoria).filter(BienCategoria.cod==codcat).first()
            sbcat = session.query(BienSubCategoria).filter(BienSubCategoria.categ_id==categ.id, BienSubCategoria.cod==subcat).first()
            escat = session.query(BienCategEsp).filter(BienCategEsp.subcateg_id==sbcat.id, BienCategEsp.cod==catesp).first()
            frmadq = session.query(BienAdquisicion).filter(BienAdquisicion.name==row['FORMA ADQUISICIÓN']).first()
            unidad = session.query(EstructuraOrg).filter(EstructuraOrg.name==row['UNIDAD ADMINISTRATIVA'], EstructuraOrg.ente_id==ente_id).first()
            
            sede = session.query(Sedes).filter(Sedes.name==row['SEDE'], Sedes.ente_id==ente_id).first()
            
            
            
            condic = session.query(BienCondicion).filter(BienCondicion.name==row['CONDICIÓN FÍSICA']).first()
            uso = session.query(BienUso).filter(BienUso.name==row['ESTADO DEL USO DEL BIEN']).first()
            
            datosBien = {
                'tipobien_id': 1,  # Asegúrate de tener este valor definido
                'categ_id': categ.id if categ else None,
                'subcateg_id': sbcat.id if sbcat else None,
                'categesp_id': escat.id if escat else None,
                'description': str(row['DESCRIPCIÓN']).upper() if 'DESCRIPCIÓN' in row else None,
                'fecha_adquisicion': row['FECHA ADQUISICIÓN'] if 'FECHA ADQUISICIÓN' in row else None,
                'num_documento': str(row['No. DOCUMENTO']).upper() if 'No. DOCUMENTO' in row else None,
                'valor_inicial': row['VALOR ADQUISICIÓN'] if 'VALOR ADQUISICIÓN' in row else None,
                'moneda_id': moneda.id if moneda else None,
                'serial': row['SERIAL'] if 'SERIAL' in row else None,
                'cod_bien': row['CÓDIGO INTERNO DEL BIEN'] if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'user_ref': user_id  # Asegúrate de tener este valor definido
            }
            
            existing_bien = session.query(Bienes).filter(Bienes.cod_bien == str(datosBien['cod_bien'])).first()
       
            if existing_bien is None:
                bien = Bienes(**datosBien)

                # Agregar la nueva instancia de Bienes a la sesión
                session.add(bien)
                session.commit()

                # Confirmar los cambios y cerrar la sesión
                print(df.columns)
                datosMueble = {
                    'bien_id': bien.id,
                    'cod_bien': datosBien['cod_bien'],
                    'marca': str(row.get('MARCA', '')).upper(),
                    'modelo': str(row.get('MODELO', '')).upper(),
                    'color': str(row.get('COLOR', '')).upper(),
                    'serial': str(row.get('SERIAL')).upper(),
                    'user_ref': user_id  # Asegúrate de tener este valor definido
                }
                print(datosMueble)
                mueble = BienesMuebles(**datosMueble)

                # Agregar la nueva instancia de BienesMuebles a la sesión
                session.add(mueble)
                session.commit()
                # Crear una nueva instancia de BienMovimiento con los datos recopilados
                datosMov = {
                    'bien_id': bien.id,
                    'ente_id': ente_id,  # Asegúrate de tener este valor definido
                    'sede_id': sede.id if sede else None,  # Asegúrate de tener este valor definido
                    'adquisicion_id': frmadq.id if frmadq else None,
                    'condicion_id': condic.id if condic else None,
                    'uso_id': uso.id if uso else None,
                    'unidad_id': unidad.id if unidad else None,  # Asegúrate de tener este valor definido
                    'cod_bien': datosBien['cod_bien'],
                    'fecha_movimiento': datosBien['fecha_adquisicion'],
                    'num_documento': datosBien['num_documento'],
                    'observacion': datosBien['description'],
                    'serial': datosBien['serial'],
                    'user_ref': user_id  # Asegúrate de tener este valor definido
                }
                movimiento = BienMovimiento(**datosMov)

                # Agregar la nueva instancia de BienMovimiento a la sesión
                session.add(movimiento)

                # Confirmar los cambios y cerrar la sesión
                session.commit()
                result = { 
                    'type': 'success',
                    'msg': "OK"
                }
            else:
                result = { 
                'type': 'error',
                'msg': "El bien "+datosBien['description']+" ya existe"
                }
        session.close()
        return result
    except Exception as e:
        raise e


def cargaMasivaInmuebles(file,ente_id,user_id):
    try:
        decoded_data = base64.b64decode(file)
        excel_data = io.BytesIO(decoded_data)
        df = pd.read_excel(excel_data, header=9)
        df = df.drop(columns=['Unnamed: 0'])
        engine = create_engine('postgresql://usrsrgbp:123456@192.168.4.64:5432/bd_srgbp')
        Session = sessionmaker(bind=engine)
        session = Session()

        for index, row in df.iterrows():
            
            
            municipio_excel = row['MUNICIPIO'] 
            parroquia_excel = row['PARROQUIA']  

            # Y 'estado_excel' es la cadena que obtienes de tu archivo Excel para el estado
            estado_excel = row['ESTADO']  # Ejemplo: 'DELTA_AMACURO'

            # Reemplaza los guiones bajos por espacios
            estado_excel = estado_excel.replace('_', ' ')

            # Ahora puedes usar 'estado_excel' en tus consultas
            estado = session.query(Estados).filter(Estados.estado.ilike(f"%{estado_excel}%")).first()

            # Si tu municipio contiene '_', lo divides y tomas la última parte como la parroquia
            if '_' in municipio_excel:
                *estado_excel, municipio_excel = municipio_excel.rsplit('_', 1)
                estado_excel = ' '.join(estado_excel)
                municipio_excel = municipio_excel.replace('_', ' ')
            else:
                municipio_excel = municipio_excel

            municipio = session.query(Municipios).filter(Municipios.municipio.ilike(f"%{municipio_excel}%"), Municipios.estado_id==estado.id).first()
            parroquia   = session.query(Parroquias).filter(Parroquias.parroquia.ilike(f"%{parroquia_excel}%"), Parroquias.municipio_id==municipio.id).first()
            
            
            
            moneda = session.query(Moneda).filter(Moneda.is_active==True, Moneda.is_local==True).first()
            codigo = row['CATEGORÍA ESPECÍFICA'][-9:]
            codcat = codigo[:2]
            subcat = codigo[2:5]
            catesp = codigo[5:]
            categ = session.query(BienCategoria).filter(BienCategoria.cod==codcat).first()
            sbcat = session.query(BienSubCategoria).filter(BienSubCategoria.categ_id==categ.id, BienSubCategoria.cod==subcat).first()
            escat = session.query(BienCategEsp).filter(BienCategEsp.subcateg_id==sbcat.id, BienCategEsp.cod==catesp).first()
            frmadq = session.query(BienAdquisicion).filter(BienAdquisicion.name==row['FORMA ADQUISICIÓN']).first()
            condic = session.query(BienCondicion).filter(BienCondicion.name==row['CONDICIÓN FÍSICA']).first()
            uso = session.query(BienUso).filter(BienUso.name==row['ESTADO DEL USO DEL BIEN']).first()
            
            
            

            ocupacion = session.query(Ocupacion).filter(Ocupacion.name.ilike(f"%{row['ESTADO DE OCUPACIÓN']}%")).first()
            espacioUso = session.query(EspacioUso).filter(EspacioUso.name.ilike(f"%{row['PROPOSITO/USO ACTUAL']}%")).first()
            
            
            
            unidad = session.query(EstructuraOrg).filter(EstructuraOrg.name==row['UNIDAD ADMINISTRATIVA'], EstructuraOrg.ente_id==ente_id).first()
            
            sede = session.query(Sedes).filter(Sedes.name==row['SEDE'], Sedes.ente_id==ente_id).first()
            udmconst = session.query(Udm).filter(Udm.name.ilike(row['UNIDAD DE MEDIDA ÁREA DE CONSTRUCCIÓN'])).first()
            udmterre = session.query(Udm).filter(Udm.name.ilike(row['UNIDAD MEDIDA ÁREA DEL TERRENO'])).first()
            
            
            datosBien = {
                'tipobien_id': 2,  # Asegúrate de tener este valor definido
                'categ_id': categ.id if categ else None,
                'subcateg_id': sbcat.id if sbcat else None,
                'categesp_id': escat.id if escat else None,
                'description': str(row['DESCRIPCIÓN']).upper() if 'DESCRIPCIÓN' in row else None,
                'fecha_adquisicion': row['FECHA ADQUISICIÓN'] if 'FECHA ADQUISICIÓN' in row else None,
                'num_documento': str(row['No. DOCUMENTO']).upper() if 'No. DOCUMENTO' in row else None,
                'valor_inicial': row['VALOR ADQUISICIÓN'] if 'VALOR ADQUISICIÓN' in row else None,
                'moneda_id': moneda.id if moneda else None,
                'serial': row['SERIAL'] if 'SERIAL' in row else None,
                'cod_bien': row['CÓDIGO INTERNO DEL BIEN'] if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'user_ref': user_id  # Asegúrate de tener este valor definido
            }
            
            existing_bien = session.query(Bienes).filter(Bienes.cod_bien == str(datosBien['cod_bien'])).first()
       
            if existing_bien is None:
                bien = Bienes(**datosBien)

                # Agregar la nueva instancia de Bienes a la sesión
                session.add(bien)
                session.commit()

                # Confirmar los cambios y cerrar la sesión
                print(df.columns)
                                
                datosInmueble = {
                'bien_id'               : bien.id,
                'estado_id'             : estado.id if estado else None,
                'municipio_id'          : municipio.id if municipio else None,
                'parroquia_id'          : parroquia.id if parroquia else None,
                'cod_bien'              : str(row['CÓDIGO INTERNO DEL BIEN']).upper() if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'rif_comodatario'       : str(row['RIF COMODATARIO']).upper() if 'RIF COMODATARIO' in row else None,
                'fecha_ini_contrato'    : str(row['FECHA INICIO CONTRATO']).upper() if 'FECHA INICIO CONTRATO' in row else None,
                'fecha_fin_contrato'    : str(row['FECHA FIN CONTRATO']).upper() if 'FECHA FIN CONTRATO' in row else None,
                'urbanizacion_sector'   : str(row['URBANIZACIÓN/SECTOR']).upper() if 'URBANIZACIÓN/SECTOR' in row else None,
                'avenida_calle'         : str(row['AVENIDA/CALLE']).upper() if 'AVENIDA/CALLE' in row else None,
                'casa_edificio'         : str(row['CASA/EDIFICIO']).upper() if 'CASA/EDIFICIO' in row else None,
                'piso_numero'           : row['PISO'] if 'PISO' in row else None,
                'lindero_norte'         : str(row['LINDEROS NORTE']).upper()  if 'LINDEROS NORTE' in row else None,
                'lindero_sur'           : str(row['LINDEROS SUR']).upper()  if 'LINDEROS SUR' in row else None,
                'lindero_este'          : str(row['LINDEROS ESTE']).upper()  if 'LINDEROS ESTE' in row else None,
                'lindero_oeste'         : str(row['LINDEROS OESTE']).upper()  if 'LINDEROS OESTE' in row else None,
                'anho_construccion'     : row['AÑO DE CONSTRUCCIÓN'] if 'AÑO DE CONSTRUCCIÓN' in row else None,
                'area_construccion'     : row['ÁREA DE CONSTRUCCIÓN'] if 'ÁREA DE CONSTRUCCIÓN' in row else None,
                'area_terreno'          : row['ÁREA DEL TERRENO'] if 'ÁREA DEL TERRENO' in row else None,
                'udm_construccion_id'   : udmconst.id if udmconst else None,
                'udm_terreno_id'        : udmterre.id if udmterre else None,
                'oficina_registro'      : str(row['OFICINA DE REGISTRO INMUEBLE']).upper()  if 'OFICINA DE REGISTRO INMUEBLE' in row else None,
                'fecha_registro'        : row['FECHA REGISTRO INMUEBLE'] if 'FECHA REGISTRO INMUEBLE' in row else None,
                'numero_registro'       : row['NÚMERO REGISTRO INMUEBLE'] if 'NÚMERO REGISTRO INMUEBLE' in row else None,
                'tomo'                  : row['TOMO'] if 'TOMO' in row else None,
                'folio'                 : row['FOLIO'] if 'FOLIO' in row else None,
                'latitud'               : row['LATITUD (COORDENADAS GEOGRÁFICA)'] if 'LATITUD (COORDENADAS GEOGRÁFICA)' in row else None,
                'longitud'              : row['LONGITUD (COORDENADAS GEOGRÁFICA)'] if 'LONGITUD (COORDENADAS GEOGRÁFICA)' in row else None,
                'user_ref'              : user_id 
                }
                inmueble = BienInmuebles(**datosInmueble)
                session.add(inmueble)
                session.commit()
                
            
                # Crear una nueva instancia de BienMovimiento con los datos recopilados
                   
                datosMov = {
                    'bien_id'               : bien.id,
                    'ente_id'               : ente_id,  # Asegúrate de tener este valor definido
                    'sede_id'               : sede.id if sede else None,  # Asegúrate de tener este valor definido
                    'adquisicion_id'        : frmadq.id if frmadq else None,
                    'condicion_id'          : condic.id if condic else None,
                    'uso_id'                : uso.id if uso else None,
                    'unidad_id'             : unidad.id if unidad else None,  # Asegúrate de tener este valor definido
                    'cod_bien'              : datosBien['cod_bien'],
                    'fecha_movimiento'      : datosBien['fecha_adquisicion'],
                    'num_documento'         : datosBien['num_documento'],
                    'observacion'           : datosBien['description'],
                    'serial'                : datosBien['serial'],
                    'ocupacion_id'          : ocupacion.id if ocupacion else None,
                    'espacio_uso_id'        : espacioUso.id if espacioUso else None,
                    'area_construccion'     : datosInmueble['area_construccion'],
                    'area_terreno'          : datosInmueble['area_terreno'],
                    'udm_construccion_id'   : udmconst.id if udmconst else None,
                    'udm_terreno_id'        : udmterre.id if udmterre else None,
                    'rif_comodatario'       : datosInmueble['rif_comodatario'],         
                    'num_contrato'          : str(row['NÚMERO DEL CONTRATO']).upper() if 'NÚMERO DEL CONTRATO' in row else None,
                    'fecha_ini_contrato'    : datosInmueble['fecha_ini_contrato'],
                    'fecha_fin_contrato'    : datosInmueble['fecha_fin_contrato'],
                    'user_ref': user_id  # Asegúrate de tener este valor definido
                }
                movimiento = BienMovimiento(**datosMov)

                # Agregar la nueva instancia de BienMovimiento a la sesión
                session.add(movimiento)

                # Confirmar los cambios y cerrar la sesión
                session.commit()
                result = { 
                    'type': 'success',
                    'msg': "OK"
                }
            else:
                result = { 
                'type': 'error',
                'msg': "El bien "+datosBien['description']+" ya existe"
                }
        session.close()
        return result
    except Exception as e:
        raise e
    
def cargaMasivaVehiculos(file,ente_id,user_id):
    try:
        decoded_data = base64.b64decode(file)
        excel_data = io.BytesIO(decoded_data)
        df = pd.read_excel(excel_data, header=9)
        df = df.drop(columns=['Unnamed: 0'])
        engine = create_engine('postgresql://usrsrgbp:123456@192.168.4.64:5432/bd_srgbp')
        Session = sessionmaker(bind=engine)
        session = Session()

        for index, row in df.iterrows():
            
            
            
            moneda = session.query(Moneda).filter(Moneda.is_active==True, Moneda.is_local==True).first()
            codigo = row['CATEGORÍA ESPECÍFICA'][-9:]
            codcat = codigo[:2]
            subcat = codigo[2:5]
            catesp = codigo[5:]
            categ = session.query(BienCategoria).filter(BienCategoria.cod==codcat).first()
            sbcat = session.query(BienSubCategoria).filter(BienSubCategoria.categ_id==categ.id, BienSubCategoria.cod==subcat).first()
            escat = session.query(BienCategEsp).filter(BienCategEsp.subcateg_id==sbcat.id, BienCategEsp.cod==catesp).first()
            frmadq = session.query(BienAdquisicion).filter(BienAdquisicion.name==row['FORMA ADQUISICIÓN']).first()
            condic = session.query(BienCondicion).filter(BienCondicion.name==row['CONDICIÓN FÍSICA']).first()
            uso = session.query(BienUso).filter(BienUso.name==row['ESTADO DEL USO DEL BIEN']).first()
            unidad = session.query(EstructuraOrg).filter(EstructuraOrg.name==row['UNIDAD ADMINISTRATIVA'], EstructuraOrg.ente_id==ente_id).first()          
            sede = session.query(Sedes).filter(Sedes.name==row['SEDE'], Sedes.ente_id==ente_id).first()

            
            
            datosBien = {
                'tipobien_id': 2,  # Asegúrate de tener este valor definido
                'categ_id': categ.id if categ else None,
                'subcateg_id': sbcat.id if sbcat else None,
                'categesp_id': escat.id if escat else None,
                'description': str(row['DESCRIPCIÓN']).upper() if 'DESCRIPCIÓN' in row else None,
                'fecha_adquisicion': row['FECHA ADQUISICIÓN'] if 'FECHA ADQUISICIÓN' in row else None,
                'num_documento': str(row['No. DOCUMENTO']).upper() if 'No. DOCUMENTO' in row else None,
                'valor_inicial': row['VALOR ADQUISICIÓN'] if 'VALOR ADQUISICIÓN' in row else None,
                'moneda_id': moneda.id if moneda else None,
                'serial': row['SERIAL'] if 'SERIAL' in row else None,
                'cod_bien': row['CÓDIGO INTERNO DEL BIEN'] if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'user_ref': user_id  # Asegúrate de tener este valor definido
            }
            
            existing_bien = session.query(Bienes).filter(Bienes.cod_bien == str(datosBien['cod_bien'])).first()
       
            if existing_bien is None:
                bien = Bienes(**datosBien)

                # Agregar la nueva instancia de Bienes a la sesión
                session.add(bien)
                session.commit()

                # Confirmar los cambios y cerrar la sesión
                print(df.columns)
                datosVehiculo = {
                'bien_id'               : bien.id,
                'cod_bien'              : str(row['CÓDIGO INTERNO DEL BIEN']).upper() if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'marca'                 : str(row['MARCA']).upper() if 'MARCA' in row else None,
                'modelo'                : str(row['MODELO']).upper() if 'MODELO' in row else None,
                'color'                 : str(row['COLOR']).upper() if 'COLOR' in row else None,
                'anho'                  : str(row['AÑO FABRICACIÓN']).upper() if 'AÑO FABRICACIÓN' in row else None,
                'serial_carr'           : str(row['SERIAL CARROCERÍA']).upper() if 'SERIAL CARROCERÍA' in row else None,
                'serial_motor'          : str(row['SERIAL MOTOR']).upper() if 'SERIAL MOTOR' in row else None,
                'placa'                 : str(row['PLACA']).upper() if 'PLACA' in row else None,
                'user_ref'              : user_id 
                }
                vehiculo = BienVehiculos(**datosVehiculo)
                session.add(vehiculo)
                session.commit()         
                # Crear una nueva instancia de BienMovimiento con los datos recopilados
                
                
                datosMov = {
                    'bien_id'               : bien.id,
                    'ente_id'               : ente_id,  # Asegúrate de tener este valor definido
                    'sede_id'               : sede.id if sede else None,  # Asegúrate de tener este valor definido
                    'adquisicion_id'        : frmadq.id if frmadq else None,
                    'condicion_id'          : condic.id if condic else None,
                    'uso_id'                : uso.id if uso else None,
                    'unidad_id'             : unidad.id if unidad else None,  # Asegúrate de tener este valor definido
                    'cod_bien'              : datosBien['cod_bien'],
                    'fecha_movimiento'      : datosBien['fecha_adquisicion'],
                    'num_documento'         : datosBien['num_documento'],
                    'observacion'           : datosBien['description'],
                    'user_ref': user_id  # Asegúrate de tener este valor definido
                }
                movimiento = BienMovimiento(**datosMov)

                # Agregar la nueva instancia de BienMovimiento a la sesión
                session.add(movimiento)

                # Confirmar los cambios y cerrar la sesión
                session.commit()
                result = { 
                    'type': 'success',
                    'msg': "OK"
                }
            else:
                result = { 
                'type': 'error',
                'msg': "El bien "+datosBien['description']+" ya existe"
                }
        session.close()
        return result
    except Exception as e:
        raise e
def cargaMasivaSemovientes(file,ente_id,user_id):
    try:
        decoded_data = base64.b64decode(file)
        excel_data = io.BytesIO(decoded_data)
        df = pd.read_excel(excel_data, header=9)
        df = df.drop(columns=['Unnamed: 0'])
        engine = create_engine('postgresql://usrsrgbp:123456@192.168.4.64:5432/bd_srgbp')
        Session = sessionmaker(bind=engine)
        session = Session()

        for index, row in df.iterrows():
            
            
            
            moneda = session.query(Moneda).filter(Moneda.is_active==True, Moneda.is_local==True).first()
            codigo = row['CATEGORÍA ESPECÍFICA'][-9:]
            codcat = codigo[:2]
            subcat = codigo[2:5]
            catesp = codigo[5:]
            categ = session.query(BienCategoria).filter(BienCategoria.cod==codcat).first()
            sbcat = session.query(BienSubCategoria).filter(BienSubCategoria.categ_id==categ.id, BienSubCategoria.cod==subcat).first()
            escat = session.query(BienCategEsp).filter(BienCategEsp.subcateg_id==sbcat.id, BienCategEsp.cod==catesp).first()
            frmadq = session.query(BienAdquisicion).filter(BienAdquisicion.name==row['FORMA ADQUISICIÓN']).first()
            condic = session.query(BienCondicion).filter(BienCondicion.name==row['CONDICIÓN FÍSICA']).first()
            uso = session.query(BienUso).filter(BienUso.name==row['ESTADO DEL USO DEL BIEN']).first()
            unidad = session.query(EstructuraOrg).filter(EstructuraOrg.name==row['UNIDAD ADMINISTRATIVA'], EstructuraOrg.ente_id==ente_id).first()          
            sede = session.query(Sedes).filter(Sedes.name==row['SEDE'], Sedes.ente_id==ente_id).first()

            proposito = session.query(BienProposito).filter(BienProposito.name.ilike(f"%{row['PROPOSITO']}%")).first()
            udm = session.query(Udm).filter(Udm.name.ilike(row['UNIDAD DE MEDIDA'])).first()
            
            datosBien = {
                'tipobien_id': 2,  # Asegúrate de tener este valor definido
                'categ_id': categ.id if categ else None,
                'subcateg_id': sbcat.id if sbcat else None,
                'categesp_id': escat.id if escat else None,
                'description': str(row['DESCRIPCIÓN']).upper() if 'DESCRIPCIÓN' in row else None,
                'fecha_adquisicion': row['FECHA ADQUISICIÓN'] if 'FECHA ADQUISICIÓN' in row else None,
                'num_documento': str(row['No. DOCUMENTO']).upper() if 'No. DOCUMENTO' in row else None,
                'valor_inicial': row['VALOR ADQUISICIÓN'] if 'VALOR ADQUISICIÓN' in row else None,
                'moneda_id': moneda.id if moneda else None,
                'serial': row['SERIAL'] if 'SERIAL' in row else None,
                'cod_bien': row['CÓDIGO INTERNO DEL BIEN'] if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'user_ref': user_id  # Asegúrate de tener este valor definido
            }
            
            existing_bien = session.query(Bienes).filter(Bienes.cod_bien == str(datosBien['cod_bien'])).first()
       
            if existing_bien is None:
                bien = Bienes(**datosBien)

                # Agregar la nueva instancia de Bienes a la sesión
                session.add(bien)
                session.commit()

                # Confirmar los cambios y cerrar la sesión
                print(df.columns)
                
                datosSemoviente = {
                'bien_id'               : bien.id,
                'cod_bien'              : str(row['CÓDIGO INTERNO DEL BIEN']).upper() if 'CÓDIGO INTERNO DEL BIEN' in row else None,
                'proposito_id'          : proposito.id if proposito else None,
                'magnitud_id'           : 3,
                'udm_id'                : udm.id if udm else None,
                'raza'                  : str(row['RAZA']).upper() if 'RAZA' in row else None,
                'cantidad'              : row['PESO'] if 'PESO' in row else None,
                'fecha_nacimiento'      : row['FECHA NACIMIENTO'] if 'FECHA NACIMIENTO' in row else None,
                'in_genero'             : row['HEMBRA'] == 'H' if 'HEMBRA' in row else 'M' if 'MACHO' in row else None,
                'hierro'                : row['NÚMERO DE HIERRO'] if 'NÚMERO DE HIERRO' in row else None,
                'user_ref'              : user_id 
                }
                
                semoviente = BienSemovientes(**datosSemoviente)
                session.add(semoviente)
                session.commit()         
                # Crear una nueva instancia de BienMovimiento con los datos recopilados
                
                
                datosMov = {
                    'bien_id'               : bien.id,
                    'ente_id'               : ente_id,  # Asegúrate de tener este valor definido
                    'sede_id'               : sede.id if sede else None,  # Asegúrate de tener este valor definido
                    'adquisicion_id'        : frmadq.id if frmadq else None,
                    'condicion_id'          : condic.id if condic else None,
                    'uso_id'                : uso.id if uso else None,
                    'unidad_id'             : unidad.id if unidad else None,  # Asegúrate de tener este valor definido
                    'cod_bien'              : datosBien['cod_bien'],
                    'fecha_movimiento'      : datosBien['fecha_adquisicion'],
                    'num_documento'         : datosBien['num_documento'],
                    'observacion'           : datosBien['description'],
                    'user_ref': user_id  # Asegúrate de tener este valor definido
                }
                movimiento = BienMovimiento(**datosMov)

                # Agregar la nueva instancia de BienMovimiento a la sesión
                session.add(movimiento)

                # Confirmar los cambios y cerrar la sesión
                session.commit()
                result = { 
                    'type': 'success',
                    'msg': "OK"
                }
            else:
                result = { 
                'type': 'error',
                'msg': "El bien "+datosBien['description']+" ya existe"
                }
        session.close()
        return result
    except Exception as e:
        raise e