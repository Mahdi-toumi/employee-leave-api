import uuid
import sys  
import logging 
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import structlog

# 1. Setup Logging (File + Terminal)
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),   # Writes to file inside container
        logging.StreamHandler(sys.stdout) # Writes to terminal (Kubernetes logs)
    ]
)

structlog.configure(
    processors=[structlog.processors.JSONRenderer()],
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()

app = FastAPI(title="Employee Leave API")

# 2. Setup Metrics (Prometheus)
Instrumentator().instrument(app).expose(app)

# 3. Database & Models
class Leave(BaseModel):
    employee_id: str
    reason: str
    days: int
    status: str = "Pending"

# Simple in-memory database
db: Dict[str, Leave] = {}

# 4. Middleware: Logs every request automatically
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    log = logger.bind(method=request.method, path=request.url.path, req_id=request_id)
    
    try:
        response = await call_next(request)
        log.info("request_processed", status=response.status_code)
        return response
    except Exception as e:
        log.error("request_failed", error=str(e))
        raise e

# 5. API Routes
@app.post("/leaves/", status_code=201)
def apply_leave(leave: Leave):
    leave_id = str(uuid.uuid4())
    db[leave_id] = leave
    logger.info("leave_created", leave_id=leave_id, emp_id=leave.employee_id)
    return {"id": leave_id, **leave.model_dump()}

@app.get("/leaves/")
def list_leaves():
    return db

@app.get("/leaves/{leave_id}")
def get_leave(leave_id: str):
    if leave_id not in db:
        raise HTTPException(status_code=404, detail="Leave not found")
    return db[leave_id]

@app.delete("/leaves/{leave_id}")
def delete_leave(leave_id: str):
    if leave_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    del db[leave_id]
    logger.info("leave_deleted", leave_id=leave_id)
    return {"status": "deleted"}

@app.get("/health")
def health_check():
    return {"status": "ok"}