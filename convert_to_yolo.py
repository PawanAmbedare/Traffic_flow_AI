import os
import xml.etree.ElementTree as ET

classes = ["ambulance", "fire_truck"]

def convert(xml_file, txt_file, img_width, img_height):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(txt_file, "w") as f:
        for obj in root.iter("object"):
            cls = obj.find("name").text
            if cls not in classes:
                continue

            cls_id = classes.index(cls)
            xmlbox = obj.find("bndbox")
            xmin = int(xmlbox.find("xmin").text)
            xmax = int(xmlbox.find("xmax").text)
            ymin = int(xmlbox.find("ymin").text)
            ymax = int(xmlbox.find("ymax").text)

            x = ((xmin + xmax) / 2) / img_width
            y = ((ymin + ymax) / 2) / img_height
            w = (xmax - xmin) / img_width
            h = (ymax - ymin) / img_height

            f.write(f"{cls_id} {x} {y} {w} {h}\n")