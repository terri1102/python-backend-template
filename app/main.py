from fastapi import FastAPI, status
from typing import Dict

app = FastAPI()


@app.get("/health", tags=["healthcheck"], status_code=status.HTTP_200_OK)
def health() -> Dict[str, str]:
    return {"status": "OK"}
