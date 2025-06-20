import os
import json
import uuid
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

API_URL = 'https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/2025'

def lambda_handler(event, context):
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        data = resp.json()

        if not isinstance(data, list):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Respuesta de API no es una lista"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    items_to_store = data[:10]  # Tomar los 10 más recientes
    stored = []

    for sismo in items_to_store:
        item = {
            'id': sismo.get('codigo', str(uuid.uuid4())),
            'codigo': sismo.get('codigo'),
            'reporte_acelerometrico_pdf': sismo.get('reporte_acelerometrico_pdf'),
            'idlistasismos': sismo.get('idlistasismos'),
            'fecha_local': sismo.get('fecha_local'),
            'hora_local': sismo.get('hora_local'),
            'fecha_utc': sismo.get('fecha_utc'),
            'hora_utc': sismo.get('hora_utc'),
            'latitud': sismo.get('latitud'),
            'longitud': sismo.get('longitud'),
            'magnitud': sismo.get('magnitud'),
            'profundidad': sismo.get('profundidad'),
            'referencia': sismo.get('referencia'),
            'referencia2': sismo.get('referencia2'),
            'referencia3': sismo.get('referencia3'),
            'tipomagnitud': sismo.get('tipomagnitud'),
            'mapa': sismo.get('mapa'),
            'informe': sismo.get('informe'),
            'publicado': sismo.get('publicado'),
            'numero_reporte': sismo.get('numero_reporte'),
            'id_pdf_tematico': sismo.get('id_pdf_tematico'),
            'createdAt': sismo.get('createdAt'),
            'updatedAt': sismo.get('updatedAt'),
            'intensidad': sismo.get('intensidad'),
        }
        table.put_item(Item=item)
        stored.append(item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Se almacenaron {len(stored)} sismos",
            "items": stored
        }, default=str)
    }

