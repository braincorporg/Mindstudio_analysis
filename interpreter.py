from fastapi import FastAPI, HTTPException
import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = FastAPI()

@app.post("/process_excel/")
async def process_excel(url: str):
    # Download the Excel file
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an error for bad responses
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Read the Excel file into a DataFrame
    df = pd.read_excel(BytesIO(response.content))

    # Generate a graph and convert it to base64
    graph_base64 = generate_graph_base64(df)

    # Return 'Hello World' and the graph
    return {"message": "Hello World", "graph": graph_base64}

def generate_graph_base64(dataframe):
    plt.figure()
    dataframe.plot(kind='line')  # Customize this as per your data
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    base64_encoded_graph = base64.b64encode(img_buffer.getvalue()).decode()
    return base64_encoded_graph
