from fastapi import FastAPI, File, UploadFile, WebSocket, HTTPException, Request, WebSocketDisconnect
from fastapi.param_functions import Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from io import BytesIO
from langchain.llms import OpenAI

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")



class State:
    """Holds the application state, including the extracted PDF text."""
    VectorStore=""

class Key:
    openai_api_key=""


# Initialize OpenAI instance
openai = OpenAI(api_key=Key.openai_api_key)


async def get_pdf_text(file: UploadFile):
    """Extracts text from a PDF file, handling potential encoding issues."""
    try:
        contents = await file.read()
        pdf = PdfReader(BytesIO(contents))
        text = ''
        for page in pdf.pages:   
            text += page.extract_text()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        return chunks

    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF")
    

      


class MessageRequest(BaseModel):
    """Pydantic model for validating message, PDF text, and API key."""
    message: str
    api_key: str


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Handles PDF uploads, checking file format and returning extracted text."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        pdf_text = await get_pdf_text(file)
        # Create embeddings using OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        State.VectorStore = FAISS.from_texts(pdf_text, embedding=embeddings)

        return {"filename": file.filename, "pdf_text": pdf_text}

    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF")


@app.post("/send-message/")
async def send_message(request_data: MessageRequest):
    """Handles sending messages, validating API key and using OpenAI API."""
    Key.openai_api_key=request_data.api_key

    try:
        if not State.VectorStore:
            raise HTTPException(status_code=400, detail="No PDF text available")

        docs = State.VectorStore.similarity_search(query=request_data.message)
        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=request_data.message, k=3)
        return {"response": response}

    except Exception as e:
        print(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing message")

# WebSocket route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()

            # Check if PDF text is available
            if not State.VectorStore:
                await websocket.send_text("No PDF text available")
                continue

            # Process the received message
            docs = State.VectorStore.similarity_search(query=data)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=data,k=3)

            # Send the response back to the client
            await websocket.send_text(response)
    except WebSocketDisconnect:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
