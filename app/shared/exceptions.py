from fastapi import HTTPException, status


class GitHubAPIException(HTTPException):
    """Exception for GitHub API errors."""

    def __init__(self, detail: str = "GitHub API error"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )


class ResourceNotFoundException(HTTPException):
    """Exception for resource not found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )


class ValidationException(HTTPException):
    """Exception for validation errors."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class RateLimitException(HTTPException):
    """Exception for rate limiting."""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        )
