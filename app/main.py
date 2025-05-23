from fastapi import FastAPI, File, Form
from routers import auth, inference
from database.db import engine
from database import sql_models as models
from rate_limit import RateLimitMiddleware

# Create database and tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# add rate limit middleware to limit requests to 30 per minutes
app.add_middleware(RateLimitMiddleware, throttle_rate=30)

# add routers endpoints
app.include_router(auth.router)
app.include_router(inference.router)


