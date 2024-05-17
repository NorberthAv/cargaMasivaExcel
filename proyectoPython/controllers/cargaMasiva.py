from database.connect import create_connection, close_connection
import base64
import pandas as pd
import io

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.modelos import Moneda, BienCategoria, BienSubCategoria, BienCategEsp, BienAdquisicion, BienCondicion, BienUso ,Bienes, BienesMuebles, BienMovimiento



def cargaMasivaMuebles(file):
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
                'user_ref': 1  # Asegúrate de tener este valor definido
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
                    'user_ref': 1  # Asegúrate de tener este valor definido
                }
                print(datosMueble)
                mueble = BienesMuebles(**datosMueble)

                # Agregar la nueva instancia de BienesMuebles a la sesión
                session.add(mueble)
                session.commit()
                # Crear una nueva instancia de BienMovimiento con los datos recopilados
                datosMov = {
                    'bien_id': bien.id,
                    'ente_id': 1,  # Asegúrate de tener este valor definido
                    'sede_id': 1,  # Asegúrate de tener este valor definido
                    'adquisicion_id': frmadq.id if frmadq else None,
                    'condicion_id': condic.id if condic else None,
                    'uso_id': uso.id if uso else None,
                    'unidad_id': 1,  # Asegúrate de tener este valor definido
                    'cod_bien': datosBien['cod_bien'],
                    'fecha_movimiento': datosBien['fecha_adquisicion'],
                    'num_documento': datosBien['num_documento'],
                    'observacion': datosBien['description'],
                    'serial': datosBien['serial'],
                    'user_ref': 1  # Asegúrate de tener este valor definido
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


def cargaMasivaInmuebles(file):
    print(file)
    result = { 
        'type': 'success',
        'msg': "OK"
    }
    return result
def cargaMasivaVehiculos(file):
    print(file)
    result = { 
        'type': 'success',
        'msg': "OK"
    }
    return result
def cargaMasivaSemovientes(file):
    print(file)
    result = { 
        'type': 'success',
        'msg': "OK"
    }
    return result