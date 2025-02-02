from fastapi import FastAPI
from router import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)