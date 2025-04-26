from fastapi.responses import JSONResponse
from typing import Dict, Any
from utils.logging_config import logger

# Success Response
def success_response(data: Any, message: str = "Request successful", code: int = 200, headers: Dict[str, str] = None) -> JSONResponse:
    try:
        if headers is None:
            headers = {}
        
        response = {
            "status": "success",
            "message": message,
            "data": data
        }

        logger.info(f"Success: {message}")
        return JSONResponse(content=response, status_code=code, headers=headers)

    except Exception as e:
        logger.error(f"Error in success_response: {str(e)}", exc_info=True)
        return error_response("An error occurred while generating the success response.", 500)


# Error Response with logging and error code
def error_response(message: str, error_code: int = 400, headers: Dict[str, str] = None) -> JSONResponse:
    try:
        if headers is None:
            headers = {}

        # Log the error with the message and status code
        logger.error(f"Error {error_code}: {message}")

        response = {
            "status": "error",
            "message": message,
            "error": {
                "code": error_code,
                "detail": message
            }
        }

        return JSONResponse(content=response, status_code=error_code, headers=headers)

    except Exception as e:
        logger.critical(f"Critical failure in error_response: {str(e)}", exc_info=True)
        return JSONResponse(
            content={
                "status": "error",
                "message": "An unexpected error occurred while processing the error response.",
                "error": {"code": 500, "detail": str(e)}
            },
            status_code=500
        )
