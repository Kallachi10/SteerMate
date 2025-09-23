from fastapi import FastAPI

app = FastAPI(title="SteerMate Backend")

@app.get("/")
async def root():
    return {"message": "SteerMate Backend"}