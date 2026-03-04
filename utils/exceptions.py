from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class CarbonSakthiException(Exception):
    """Base exception for CarbonSakthi AI"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class FarmerNotFoundException(CarbonSakthiException):
    """Exception raised when farmer is not found"""
    def __init__(self, farmer_id: str):
        super().__init__(
            message=f"Farmer with ID {farmer_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class DuplicateFarmerException(CarbonSakthiException):
    """Exception raised when trying to create duplicate farmer"""
    def __init__(self, message: str = "Farmer already exists"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )

class DatabaseException(CarbonSakthiException):
    """Exception raised for database operations"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class AuthenticationException(CarbonSakthiException):
    """Exception raised for authentication failures"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthorizationException(CarbonSakthiException):
    """Exception raised for authorization failures"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
