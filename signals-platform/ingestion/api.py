# ingestion/api.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_api_session(retries=3, backoff_factor=1.0):
    """Returns a requests Session with automatic retries for failed/rate-limited calls."""
    session = requests.Session()
    
    # Configure retry logic for rate limits (429) and server errors (500, 502, 503, 504)
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session