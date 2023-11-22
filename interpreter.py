# from fastapi import FastAPI, HTTPException
# import requests
# import pandas as pd
# import matplotlib.pyplot as plt
# import base64
# from io import BytesIO

# app = FastAPI()

# @app.post("/process_excel/")
# async def process_excel(url: str):
#     # Download the Excel file
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # This will raise an error for bad responses
#     except requests.RequestException as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     # Read the Excel file into a DataFrame
#     df = pd.read_excel(BytesIO(response.content))

#     # Generate a graph and convert it to base64
#     graph_base64 = generate_graph_base64(df)

#     # Return 'Hello World' and the graph
#     return {"message": "Hello World", "graph": graph_base64}

# def generate_graph_base64(dataframe):
#     plt.figure()
#     dataframe.plot(kind='line')  # Customize this as per your data
#     plt.tight_layout()

#     img_buffer = BytesIO()
#     plt.savefig(img_buffer, format='png')
#     img_buffer.seek(0)

#     base64_encoded_graph = base64.b64encode(img_buffer.getvalue()).decode()
#     return base64_encoded_graph

from fastapi import FastAPI, HTTPException, Request
import pandas as pd
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import io

app = FastAPI()

@app.post("/process_excel/")
async def process_excel(request: Request):
    try:
        data = await request.json()
        url = data['url']
        python_script = data['python_script']
        print(python_script)

        # Download the Excel file
        df = pd.read_excel(url)
        df.head()
        # Redirect print statements to a variable
        print_output = io.StringIO()
        with redirect_stdout(print_output):

            # Execute the Python script
            local_vars = {}
            exec(python_script, {'df': df, 'plt': plt}, local_vars)
            fig = local_vars.get('fig')

            if not fig:
                raise ValueError("No matplotlib figure found in the executed script.")

            # Convert the figure to base64
            buf = BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            graph_base64 = base64.b64encode(buf.read()).decode()

        return {
            "message": print_output.getvalue(),
            "graph": graph_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/excel_info/")
async def excel_info(url: str):
    try:
        # Download the Excel file
        df = pd.read_excel(url)

        # Redirect the output of df.info() to a string
        info_output = io.StringIO()
        with redirect_stdout(info_output):
            df.info()

        # Get the first row of the DataFrame
        first_row = df.iloc[0].to_dict()

        return {
            "df_info": info_output.getvalue(),
            "first_row": first_row
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



