import logging
import os
import sqlite3

from lxml import etree

from db import DBConnect

xml_file = 'answer.xml'
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    db = DBConnect("test")
    db.create_table("test")

    if os.path.isfile(xml_file):
        root_element = etree.parse(xml_file).getroot()

        for date_elem in root_element.find("importStatus"):
            for type_elem in date_elem.findall("type"):
                for label_elem in type_elem.findall("label"):
                    label = label_elem.get("value")
                    status = label_elem.find("importedStatus").text
                    db.update_status(label=label, status=status)
                    logging.info(f"Статус {label} обновлен {status} ")

        with sqlite3.connect("test") as conn:
            cursor = conn.cursor()
            result = cursor.execute("""SELECT * FROM test""")
            logging.info(f"Записи из бд {result.fetchall()}")
    else:
        logging.error("XML-файл не найден.")
