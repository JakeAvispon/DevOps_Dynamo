import json

def txt_to_dynamo_json(input_file, output_file):
    data_list = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # Leer encabezados
        lines = f.readlines()
        headers = lines[0].strip().split(',')
        
        # Procesar cada línea
        for line in lines[1:]:
            values = line.strip().split(',')
            # Crear el formato de DynamoDB (S para String, N para Number)
            item = {
                "Estado": {"S": values[0]},
                "Temperatura": {"N": values[1]},
                "Humedad": {"N": values[2]},
                "Costo_Alojamiento": {"N": values[3]},
                "Costo_Transporte": {"N": values[4]},
                "Dias_Promedio": {"N": values[5]},
                "Tiempo_Traslado": {"N": values[6]}
            }
            data_list.append(item)

    with open(output_file, 'w', encoding='utf-8') as json_f:
        json.dump(data_list, json_f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    txt_to_dynamo_json('Estados.txt', 'estados_dynamo.json')
    print("¡Archivo JSON creado con éxito!")