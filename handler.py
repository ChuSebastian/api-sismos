import json
import uuid
import boto3
import requests
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

def fetch_and_store(event, context):
    try:
        response = requests.get('https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/2025')
        response.raise_for_status()

        data = response.json()  # Esto es una lista
        if not isinstance(data, list) or len(data) == 0:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "No data received from the API"})
            }

        sismo = data[0]  # Primer elemento de la lista

        # Construimos el item a insertar
        item = {
            'id': str(uuid.uuid4()),  # Clave primaria aleatoria
            'fecha': sismo.get('fecha', 'N/A'),
            'hora': sismo.get('hora', 'N/A'),
            'magnitud': sismo.get('magnitud', 'N/A'),
            'profundidad': sismo.get('profundidad', 'N/A'),
            'latitud': sismo.get('latitud', 'N/A'),
            'longitud': sismo.get('longitud', 'N/A'),
            'referencia': sismo.get('referencia', 'N/A')
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Sismo data stored successfully", "item": item})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

