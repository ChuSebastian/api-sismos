import json
import os
import requests
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)

def fetch_and_store(event, context):
    api_url = "https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/2025"

    try:
        response = requests.get(api_url)
        data = response.json()

        # Preparar ítem para DynamoDB
        item = {
            'id': str(datetime.utcnow().timestamp()),  # Clave primaria única
            'fecha': data.get('fecha'),
            'hora': data.get('hora'),
            'magnitud': data.get('magnitud'),
            'profundidad': data.get('profundidad'),
            'epicentro': data.get('epicentro'),
            'fuente': data.get('fuente'),
        }

        # Guardar en DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Sismo guardado exitosamente!', 'item': item})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

