import base64
import shutil
import requests
from fastapi import Request, FastAPI
import cv2
from MLflex import MLflex

# from db import db_session Для включения функциональности бота(рассылка при опасности) раскоментить при надобности

app = FastAPI()
BACK = "здесь должен быть адресс на бэк"
#db_session.global_init("../db/users.db") Для включения функциональности бота(рассылка при опасности) раскоментить при надобности
MODELPATH = "myyolov8l.pt"
CONF_YOLO = 0.45
MLflex = MLflex(MODELPATH, CONF_YOLO)


@app.post("/uploadImage")  # Фото
async def root(request: Request):
    data = await request.json()
    for i in data['attachments']:
        r = requests.get(i['downloadURL'], stream=True)
        if r.status_code == 200:
            with open("data.jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        intersectionList, img = MLflex.imageanswer("data.jpg", i["camName"])
        status = intersectionList[0][0]
        percent = intersectionList[0][1]
        camName = i['camName']

        cv2.imwrite("send.jpg", img)

        with open("send.jpg", "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            params = {
                "fileId": i['id'],
                "status": str(status).upper(),
                "percent": percent,
                "camName": camName,
                "bytes": base64_image
            }

        a = requests.post(f"{BACK}/attachments", params=params)
        i["percent"] = percent
        i["status"] = str(status).upper()
    return data
