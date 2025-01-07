import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

router = APIRouter(prefix="/user_registered")


class UserRegisteredWebhook(BaseModel):
    user_id: str
    email: str


@router.post("/")
async def user_registered(user: UserRegisteredWebhook):  # pragma: no cover
    """
    Handles the user registration webhook.

    This function is triggered when a user registration webhook is received.
    It logs the event details, evaluates the email validity, and returns an
    appropriate HTTP response based on the validation. If the user's email
    is invalid, it returns an error response along with a structured error
    message. Otherwise, it confirms successful processing with no additional
    content.

    Args:
        user (UserRegisteredWebhook): The webhook payload received when a user
            registers, containing user details such as email and traits.

    Returns:
        Response: An HTTP response with a 403 Forbidden status and structured
            error message if the user email is invalid.
            Otherwise, an HTTP 204 No Content response to confirm successful
            processing.
    """
    logging.info("User registered", extra={"user": user.model_dump()})

    error_message = {
        "messages": [
            {
                "instance_ptr": "#/traits/email",
                "messages": [
                    {
                        "id": 123,  # Error id to be evaluated in frontend
                        "text": "You are not allowed to register.",
                        "type": "error",
                        "context": {  # Additional context we can send to the Frontend
                            "value": "short value",
                            "any": "additional information",
                        },
                    }
                ],
            }
        ]
    }

    if user.email == "invalid@test.com":
        return JSONResponse(
            error_message,
            status.HTTP_403_FORBIDDEN,
        )
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
