from typing import Union
from fastapi import FastAPI
from lib.db import getDB
import json
from models.measurements import Measurement

app = FastAPI()

def readTemperatures():
    connection = getDB()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM measurements LIMIT 0, 100"
            cursor.execute(sql)
            results = cursor.fetchall()
            # data = json.dumps(results)
            data = []
            for row in results:
                item = Measurement(**{
                    "id": row[0],
                    "temperature": row[1],
                    "humidity": row[2],
                    "pressure": row[3],
                    "created_at": row[4]
                })
                data.append(item)
            return data


@app.get("/")
def read_root():
    results = readTemperatures()
    return results
    # return {"Hello": "World"}



# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}