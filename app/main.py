from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def init_fastapi():
    return {"FastAPI" : "Success"}