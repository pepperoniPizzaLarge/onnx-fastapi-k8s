from fastapi import FastAPI, File, Form
from routers import auth, inference
from database.db import engine
from database import sql_models as models

 
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router)
app.include_router(inference.router)


