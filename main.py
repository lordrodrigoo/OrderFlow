from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.api.controllers.user_controller import router as user_router
from src.exceptions.exception_handlers import EmailAlreadyExistsException, email_exception_handler, validation_exception_handler




app = FastAPI(title="API Food Delivery", version="1.0.0")

# Register exception handlers
app.add_exception_handler(EmailAlreadyExistsException, email_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Include routers
app.include_router(user_router)


# Route for health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
