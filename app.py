from flask import Flask, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
# Habilitamos CORS para que tu página en S3 pueda consultar a la EC2 sin bloqueos
CORS(app)

# Configuración de DynamoDB
# No necesitas poner llaves de acceso si tu EC2 tiene el Rol de IAM correcto
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Cambia a tu región
tabla = dynamodb.Table('TablaEstados')

@app.route('/api/estados', methods=['GET'])
def obtener_estados():
    try:
        # Escaneamos la tabla para traer todos los registros de los estados
        respuesta = tabla.scan()
        datos = respuesta.get('Items', [])
        
        # Si la tabla es muy grande y hay más datos (LastEvaluatedKey)
        while 'LastEvaluatedKey' in respuesta:
            respuesta = tabla.scan(ExclusiveStartKey=respuesta['LastEvaluatedKey'])
            datos.extend(respuesta.get('Items', []))
            
        return jsonify(datos)
    
    except ClientError as e:
        print(f"Error al consultar los pergaminos: {e.response['Error']['Message']}")
        return jsonify({"error": "No se pudo leer la base de datos"}), 500

if __name__ == '__main__':
    # Corremos el servidor en el puerto 5000, visible para todos (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)