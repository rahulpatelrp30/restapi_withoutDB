from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from controllers import router
from services import BusinessRuleError, NotFoundError

app = FastAPI(title="Simple Bank API")

# Allows your React frontend (running on another port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(BusinessRuleError)
async def business_rule_handler(request: Request, exc: BusinessRuleError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


app.include_router(router)