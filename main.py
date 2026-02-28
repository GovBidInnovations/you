from fastapi import FastAPI

# Import the GovBid engine package to ensure it's included in the deployment
import govbid  # noqa: F401

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "GovBid engine is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
