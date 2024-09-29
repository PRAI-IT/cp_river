from typing import Union
import random
from typing import Annotated
from datetime import datetime as dt
import pyarrow.parquet as pq
from fastapi import FastAPI, Header, Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import tensorflow as tf
import tensorflow_recommenders as tfrs
from pydantic import BaseModel


class Video(BaseModel):
    id: list


model_vtv = tf.saved_model.load("models/video_to_video")
model_time = tf.saved_model.load("models/time")
df_video = pq.read_table("dataset/video_stat.parquet", columns=['video_id', 'title', 'description',
                                                                'category_id', 'v_pub_datetime',
                                                                'v_year_views']).to_pandas()
df_video['video_id'] = df_video['video_id'].astype(str)

_, get_ml_time = model_time(["10"])
get_ml_time = get_ml_time.numpy().tolist()
s_ml = []
for s in get_ml_time:
    for ids in s:
        s_ml.append(ids)
get_ml_time = s_ml.copy()


app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
])

users = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/video/{video_id}")
def get_video_data(video_id: str, q: Union[str, None] = None):
    return df_video.loc[df_video['video_id'] == video_id].to_dict()


@app.options("/video", status_code=200)
@app.post("/video")
def get_recommendation(data: Video, user_agent: Annotated[str | None, Header()] = None,
                       real_ip: str = Header(None, alias='X-Real-IP')):
    agent = str(user_agent) + "|" + str(real_ip)
    result = []
    if agent not in users:
        users[agent] = {"reserve": [], "block": [], "send": []}
        users[agent]["reserve"].extend(get_ml_time)
        users[agent]["reserve"] = list(dict.fromkeys(users[agent]["reserve"]))
    else:
        if len(data.id):
            _, get_ml_video = model_vtv(tf.constant(data.id))
            get_ml_video = get_ml_video.numpy().tolist()
            for s in get_ml_video:
                sn = s.copy()
                for ids in s:
                    if ids in users[agent]["block"]:
                        sn.remove(ids)
                users[agent]["send"].extend(sn)
                users[agent]["send"] = list(dict.fromkeys(users[agent]["send"]))
    if len(users[agent]["send"]) > 8:
        for idx in range(8):
            ids = users[agent]["send"][random.randint(0, len(users[agent]["send"]) - 1)]
            users[agent]["send"].remove(ids)
            result.append(ids)
    else:
        result = users[agent]["send"].copy()
        users[agent]["send"] = []
    for idx in range(10 - len(result)):
        # if len(users[agent]["reserve"])
        ids = users[agent]["reserve"][random.randint(0, len(users[agent]["reserve"]) - 1)]
        users[agent]["reserve"].remove(ids)
        result.append(ids)
    users[agent]["block"].extend(result)
    users[agent]["block"] = list(dict.fromkeys(users[agent]["block"]))
    return result
