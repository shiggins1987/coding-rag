from fastapi import FastAPI

models = {}

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": "artifacts" in models}

@app.get("/parse")
def parse_book(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
