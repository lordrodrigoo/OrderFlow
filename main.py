#pylint: disable=unused-import
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.auth_controller import router as auth_router
from src.api.controllers.auth_controller import router as auth_router
from src.exceptions.exception_handlers import EmailAlreadyExistsException, email_exception_handler, validation_exception_handler

load_dotenv()
app = FastAPI(
    title=os.getenv("API_TITLE"),
    version=os.getenv("API_VERSION")
)

# Register exception handlers
app.add_exception_handler(EmailAlreadyExistsException, email_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)



# Include routers

app.include_router(user_router)
app.include_router(auth_router)


# Route for health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint para testar compressão GZip
@app.get("/test-gzip")
def test_gzip():
    big_content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50
    return {"content": big_content}


# MIDDLEWARES
app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=5)
