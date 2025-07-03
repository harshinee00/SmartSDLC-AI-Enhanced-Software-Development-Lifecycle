# backend/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import uvicorn

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy classification logic (replace with real AI later)
def classify_line(line):
    line = line.lower()
    if any(keyword in line for keyword in ["login", "submit", "register", "create", "update", "delete"]):
        return "Functional"
    elif any(keyword in line for keyword in ["load time", "responsive", "optimize", "performance"]):
        return "Performance"
    elif any(keyword in line for keyword in ["UI", "interface", "button", "design"]):
        return "UI"
    elif any(keyword in line for keyword in ["secure", "encrypt", "password", "authentication"]):
        return "Security"
    elif any(keyword in line for keyword in ["scalable", "maintainable", "reliable", "available"]):
        return "Non-Functional"
    else:
        return "Unclassified"

@app.post("/classify-requirements/")
async def classify_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        results = []

        for page in pdf:
            lines = page.get_text().split('\n')
            for line in lines:
                if line.strip():
                    category = classify_line(line.strip())
                    results.append({"text": line.strip(), "category": category})

        return JSONResponse(content={"results": results})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run backend with: uvicorn backend.main:app --reload
