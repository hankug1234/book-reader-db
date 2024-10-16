import os, secrets, sys
sys.path.extend(["./tables/book_reader_tables.py","./conneection/connection.py","./crud/repository.py"])
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from app.connection.connection import Init_db
from app.data_type import Rvc_data_set_meta, Tts_data_set_meta, Rvc_model_meta, Tts_model_meta
import logging

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Init_db(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]) + os.sep + "app_config.json")
rvc_model_repository, tts_model_repository, rvc_data_set_repository, tts_data_set_repository = db.get_repository()

logger = logging.getLogger("main")

# 2. logger 레벨 설정
logger.setLevel(logging.DEBUG)
# 또는
logging.basicConfig(level=logging.DEBUG)

# 3. formatting 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 4. handler 설정
# console 출력
stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    
    logging.info(await request.body())
    response = await call_next(request)
    
    return response


@app.post("/train/rvc",status_code=200)
async def save_rvc_model_meta_data(meta: Rvc_model_meta):
    table = db.tables.rvc_model
    model_id = secrets.token_urlsafe(16)
    data = table(id = model_id, name = meta.name,
                 batch_size = meta.batch_size, save_epoch = meta.save_epoch,
                 total_epoch = meta.total_epoch, image = meta.image, image_name = meta.image_name,
                 data_set_id = meta.data_set_id, test_script = meta.test_script)
    try:
        rvc_model_repository.insert([data])
        return data.asJson
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalidate data format {e}")
    
@app.get("/model/rvc/{type}",status_code=200)
async def get_rvc_model_meta_data(type: Annotated[str,Path(title="search type (specific model id | all)")]):
    try:
        if type == "all":
            return [d.asJson() for d in rvc_model_repository.select_all()]
        else:
            return [d.asJson() for d in rvc_model_repository.select_by_id(type)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")

@app.get("/model/page/rvc/{start}/{offset}",status_code=200)
async def get_rvc_model_meta_data_by_page(start: Annotated[int|None,Path(title="search start point")],
                                  offset: Annotated[int|None,Path(title="search offset from start")]):
    try:
        return [d.asJson() for d in rvc_model_repository.select_by_page(start,offset)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")
 
    

@app.post("/train/tts",status_code=200)
async def save_tts_model_meta_data(meta: Tts_model_meta):
    table = db.tables.tts_model
    model_id = secrets.token_urlsafe(16)
    data = table(id = model_id, name = meta.name,
                 batch_size = meta.batch_size, save_epoch = meta.save_epoch,
                 total_epoch = meta.total_epoch, image = meta.image, image_name = meta.image_name,
                 data_set_id = meta.data_set_id, test_script = meta.test_script, language=meta.language)
    try:
        tts_model_repository.insert([data])
        return data.asJson
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")

@app.get("/model/tts/{type}",status_code=200)
async def get_tts_model_meta_data(type: Annotated[str,Path(title="search type (specific model id | all)")]):
    try:
        if type == "all":
            return [d.asJson() for d in tts_model_repository.select_all()]
        else:
            return [d.asJson() for d in tts_model_repository.select_by_id(type)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")

@app.get("/model/page/tts/{start}/{offset}",status_code=200)
async def get_tts_model_meta_data_by_page(start: Annotated[int|None,Path(title="search start point")],
                                  offset: Annotated[int|None,Path(title="search offset from start")]):
    try:
        return [d.asJson() for d in tts_model_repository.select_by_page(start,offset)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")




@app.post("/regist/rvc_data",status_code=200)
async def save_rvc_data_set_meta_data(meta:Rvc_data_set_meta):
    table = db.tables.rvc_data_set
    data_set_id = secrets.token_urlsafe(16)
    data = table(data_set_id = data_set_id, data_set_name = meta.data_set_name,
                 description= meta.description, data_set = meta.data_set)
    
    try:
        rvc_data_set_repository.insert([data])
        return {"detail" : "insert success"}
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")

@app.get("/data/rvc/{type}",status_code=200)
async def get_rvc_data_set_meta_data(type: Annotated[str,Path(title="search type (specific data set id | all)")]):
    try:
        if type == "all":
            return [d.asJson() for d in rvc_data_set_repository.select_all()]
        else:
            return [d.asJson() for d in rvc_data_set_repository.select_by_id(type)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")
    
@app.get("/data/page/rvc/{start}/{offset}",status_code=200)
async def get_rvc_data_set_meta_data_by_page(start: Annotated[int|None,Path(title="search start point")],
                                  offset: Annotated[int|None,Path(title="search offset from start")]):
    try:
        return [d.asJson() for d in rvc_data_set_repository.select_by_page(start,offset)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")    
    
    
@app.post("/regist/tts_data",status_code=200)
async def save_rvc_data_set_meta_data(meta:Tts_data_set_meta):
    table = db.tables.tts_data_set
    data_set_id = secrets.token_urlsafe(16)
    data = table(data_set_id = data_set_id, data_set_name = meta.data_set_name,
                 description= meta.description, data_set = meta.data_set)
    
    try:
        tts_data_set_repository.insert([data])
        return {"detail" : "insert success"}
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")
    
@app.get("/data/tts/{type}",status_code=200)
async def get_tts_data_set_meta_data(type: Annotated[str,Path(title="search type (specific data set id | all)")]):
    try:
        if type == "all":
            return [d.asJson() for d in tts_data_set_repository.select_all()]
        else:
            return [d.asJson() for d in tts_data_set_repository.select_by_id(type)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")

@app.get("/data/page/tts/{start}/{offset}",status_code=200)
async def get_tts_data_set_meta_data_by_page(start: Annotated[int|None,Path(title="search start point")],
                                  offset: Annotated[int|None,Path(title="search offset from start")]):
    try:
        return [d.asJson() for d in tts_data_set_repository.select_by_page(start,offset)]
    except Exception as _:
        raise HTTPException(status_code=400, detail="invalidate data format ")  
        