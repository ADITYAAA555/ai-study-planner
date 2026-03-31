import os

class Config:
    SECRET_KEY = "supersecretkey"
    JWT_SECRET_KEY = "jwtsecretkey"
    MONGO_URI = "mongodb://localhost:27017/academic_twin"