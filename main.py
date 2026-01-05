from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
  return {"message": "Hello"}

@app.get('/predict/{value}')
def predict(value: int):
  result = 2 * value
  return {"input": value,
          "prediction": result,
          "status": "success"}