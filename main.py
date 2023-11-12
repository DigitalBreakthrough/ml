from MLFlex import MLflex
import cv2
# from db import db_session Для включения функциональности бота(рассылка при опасности) раскоментить при надобности
# db_session.global_init("db/users.db")  Для включения функциональности бота(рассылка при опасности) раскоментить при надобности


MODELPATH = "myyolov8l.pt"
CONF_YOLO = 0.45
MLflex = MLflex(MODELPATH, CONF_YOLO)

image = "example/DpR-Csp-uipv-ShV-V15d56b754-3f8a-4665-8b2e-1d0b340be4bb.jpg"
cam_name = "DpR-Csp-uipv-ShV-V1"
#image =  "example/Pgp-lpc2-K-0-1-38&Pgp-lpc2-K-0-1-38_Nepreryvnaya_podgruppa_(kleti_3-5)_2021-11-17_15_40_09.481.Png"
#cam_name = "Pgp-lpc2-K-0-1-38"
#image = "example/Php-Angc-K3-8&Php-Angc-K3-8_angc4test1144.jpg"
#cam_name = "Php-Angc-K3-8"

data = MLflex.imageanswer(image, cam_name)
print(data[0])
cv2.imwrite('example3.jpg', data[1])
