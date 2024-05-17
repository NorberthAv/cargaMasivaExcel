from flask import Flask, jsonify, request
from dotenv import load_dotenv


import controllers.cargaMasiva as masiveSave

app= Flask(__name__)

load_dotenv()

# @app.route("/hello")
@app.route('/excel/cargaMasiva', methods=['POST'])
def name():  
    try:
        result = None
        file = request.json.get('archivo', None)
        tipo_excel = request.json.get('tipoExcel', None)
        if file is None or tipo_excel is None:
            return jsonify({'type': 'error', 'response': 'Faltan parámetros para procesar la petición'}), 400
        else:
            if tipo_excel == 1:
                result = masiveSave.cargaMasivaMuebles(file)
            if tipo_excel == 2:
                result = masiveSave.cargaMasivaInmuebles(file)
            if tipo_excel == 3:
                result = masiveSave.cargaMasivaVehiculos(file)
            if tipo_excel == 4:
                result = masiveSave.cargaMasivaSemovientes(file)

            if result != None and result['type'] == 'success':
                return jsonify({'type': 'ok', 'response': 'Operación completada'}),200
            else:
                return jsonify({'type': result['type'], 'response': result['msg']}), 400
    except Exception as e:
        return jsonify({'type': 'error', 'response': str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9300)