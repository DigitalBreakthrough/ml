import cv2
from ultralytics import YOLO
from shapely.geometry import Polygon, box
import os
import pandas as pd
import telebot

#from bot.config import TOKEN Для включения функциональности бота(рассылка при опасности) раскоментить при надобности
#from db import db_session
#from db.user import User

class MLflex:
    def __init__(self, modelPath, conf_yolo):
        self.modelPath = modelPath
        self.conf_yolo = conf_yolo
        self.model = YOLO(self.modelPath)
        #self.bot = telebot.TeleBot(TOKEN) Для включения функциональности бота(рассылка при опасности) раскоментить при надобности

    def imageanswer(self, image, cam_name):

        intersectionList = []

        predict_yolo = self.model.predict(
            source=image, conf=self.conf_yolo, verbose=False
        )

        image = cv2.imread(image)
        for i in self.giveDictPolygon()[cam_name]:
            for j in range(len(i) - 1):
                cv2.line(image, i[j], i[j + 1], (0, 255, 0), 3)
            cv2.line(image, i[-1], i[0], (0, 255, 0), 3)

        coors = predict_yolo[0].boxes.data

        for i in coors:
            coor = list(map(int, list(i)[:-2]))
            cv2.rectangle(image, (coor[0], coor[1]), (coor[2], coor[3]), (0, 255, 255), 2)
            intersectionListTemp = []
            for j in self.giveDictPolygon()[cam_name]:
                intersectionListTemp.append(self.intersectionArea(j, coor))
            intersectionList.append(max(intersectionListTemp, key=lambda x: x[1]))
            #if intersectionList[-1][0]:  Для включения функциональности бота(рассылка при опасности) раскоментить при надобности
            #    cv2.imwrite('tmp.jpg', image)
            #    session = db_session.create_session()
            #    for i in session.query(User).all():
            #        self.bot.send_message(i.chat_id, f'Опасная ситуация {intersectionList[-1][1]}')
            #        self.bot.send_photo(i.chat_id, photo=open("tmp.jpg", 'rb'))
        return intersectionList, image

    def intersectionArea(self, poly_coords, square_coords):
        poly = Polygon(poly_coords)
        square = box(*square_coords)
        intersection = poly.intersection(square)
        if intersection.area == 0:
            return (False, 0)
        p = intersection.area / square.area
        return (p >= 0.15, round(p, 2))

    def giveDictPolygon(self):
        d = {}
        for i in os.listdir("./data/danger_zones"):
            if i.split('.')[-1] == "txt":
                with open(f"./data/danger_zones/{i}") as r:
                    data = r.read()
                    name = i.split("_")[1].split('.')[0]
                    if name not in d:
                        d[name] = []
                    d[name].append([])
                    for j in data.split(",\n"):
                        d[name][-1].append(list(map(int, j.strip()[1:-1].split(", "))))
        return d

    def makeCSV(path):
        df = pd.read_csv(path)
        df.to_csv("submit.csv", index=False)
