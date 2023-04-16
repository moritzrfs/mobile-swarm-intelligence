import json
import requests
import math

upload_url = 'http://192.168.1.211:8080/uploadfile/'
start_url = 'http://192.168.1.211:8080/start/'
api_key = 'QB7n3XjRxvrYRSq3sR4J21rRyrzoAKrwi4u5A8T5yKPmpwmifi3OxCBBYOXz6hLBzO5Vjt1lRKu74L0XZ0WrNt99'

headers = {'X-API-Key': api_key}

path = [(0, 0), (4, 9), (4, 9), (13, 9), (15, 13), (16, 16)]

instructions = {"instructions": []}

def drive_path(path, upload_url, start_url, headers):
    for i in range(len(path)-1):
        current_pos = path[i]
        next_pos = path[i+1]
        
        if current_pos != next_pos:
            # berechne Steigung
            m = (next_pos[1] - current_pos[1])/(next_pos[0] - current_pos[0])
            print(m)
            
            #drehe roboter um die Gradzahl der Steigung
            instructions["instructions"].append({"action": "turn_right", "degree": m*10})
            
            #Länge der Stecke berechnen
            distance = math.sqrt((next_pos[0] - current_pos[0])**2 + (next_pos[1] - current_pos[1])**2)
            instructions["instructions"].append({"action": "drive_straight", "seconds": distance})
            print(distance)


    print(instructions)
    with open('instruc.json', 'w') as f:
        json.dump(instructions, f)

    # Datei als Tupel aus Dateiname und geöffnetem Dateiobjekt definieren
    files = [('file', open('instruc.json', 'rb'))]

    # Anfrage senden und Antwort erhalten
    upload_response = requests.post(upload_url, headers=headers, files=files)

    response = requests.post(start_url, headers=headers)

    # Antwort ausgeben
    print(upload_response.text)

drive_path(path, upload_url, start_url, headers)