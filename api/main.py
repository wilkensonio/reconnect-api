from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import (user_routes, available_routes,
                      appointment_routes, app_token, pi_message_routes,
                      notifications_routes, ws_routes)
from .utils import validate_api_key
from fastapi import Depends


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # Allow requests from this origin
    allow_origins=["http://localhost:3000",
                   "http://localhost:8000",
                   "http://localhost",
                   'http://ec2-3-82-206-23.compute-1.amazonaws.com/',
                   'http://ec2-3-82-206-23.compute-1.amazonaws.com'
                   'http://ec2-3-82-206-23.compute-1.amazonaws.com:80/',
                   'http://ec2-3-82-206-23.compute-1.amazonaws.com:80',
                   'https://reconnect-faculty.s3.us-east-1.amazonaws.com/index.html'
                   ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


models.Base.metadata.create_all(bind=database.engine)
app.include_router(app_token.router, prefix="/api/v1")
app.include_router(ws_routes.router, prefix="/api/v1")

app.include_router(user_routes.router, prefix="/api/v1",
                   dependencies=[Depends(validate_api_key.validate_api_key)])
app.include_router(available_routes.router, prefix="/api/v1",
                   dependencies=[Depends(validate_api_key.validate_api_key)])
app.include_router(appointment_routes.router, prefix="/api/v1",
                   dependencies=[Depends(validate_api_key.validate_api_key)])
app.include_router(pi_message_routes.router, prefix="/api/v1",
                   dependencies=[Depends(validate_api_key.validate_api_key)])
app.include_router(notifications_routes.router, prefix="/api/v1",
                   dependencies=[Depends(validate_api_key.validate_api_key)])
