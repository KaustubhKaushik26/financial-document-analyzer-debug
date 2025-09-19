from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import verification, analyze_financial_document, risk_assessment, investment_analysis

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    """Initializes and runs the financial analysis crew."""
    print('1')
    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks=[verification, analyze_financial_document, risk_assessment, investment_analysis],
        process=Process.sequential,
        verbose=True # For detailed logs
    )
    print("Printing financial_crew", financial_crew)
    
    # Inputs for kickoff
    inputs = {
        'query': query,
        'file_path': file_path
    }
    print("Printing inputs", inputs)
    
    result = financial_crew.kickoff(inputs=inputs)
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a detailed analysis of this financial document, including key metrics, trends, and a final investment recommendation based on the findings.")
):
    """Analyzes the uploaded financial document."""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # Process the document with the crew
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log cleanup errors if necessary
                print(f"Error cleaning up file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)