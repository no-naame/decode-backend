from datetime import datetime, timedelta
from typing import Optional


def parse_github_repo(repo_url: str) -> tuple[str, str]:
    """
    Parse GitHub repository URL to extract owner and repo name.

    Args:
        repo_url: GitHub repository URL

    Returns:
        Tuple of (owner, repo_name)

    Example:
        parse_github_repo("https://github.com/owner/repo") -> ("owner", "repo")
    """
    parts = repo_url.rstrip("/").split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    raise ValueError(f"Invalid GitHub repository URL: {repo_url}")


def calculate_date_range(days: int) -> tuple[datetime, datetime]:
    """
    Calculate date range from today going back N days.

    Args:
        days: Number of days to go back

    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format float as percentage string.

    Args:
        value: Float value (0 to 1)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string

    Example:
        format_percentage(0.856) -> "85.60%"
    """
    return f"{value * 100:.{decimals}f}%"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate cache key from prefix and arguments.

    Args:
        prefix: Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Cache key string

    Example:
        generate_cache_key("user", "username", days=30) -> "user:username:days=30"
    """
    parts = [prefix] + [str(arg) for arg in args]

    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        kwargs_str = ":".join([f"{k}={v}" for k, v in sorted_kwargs])
        parts.append(kwargs_str)

    return ":".join(parts)
