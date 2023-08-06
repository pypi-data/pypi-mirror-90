"""
Utilities for making external web requests.
"""
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from dada_utils import path

DEFAULT_TIMEOUT = 20  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_session(**kwargs):
    """
    Get an http session with retry/timeout logic.
    """
    retries = Retry(
        total=kwargs.pop("max_retries", 3),
        backoff_factor=kwargs.pop("backoff", 1.2),
        status_forcelist=kwargs.pop("retry_on", [429, 500, 502, 503, 504]),
    )
    http = requests.Session(**kwargs)
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    return http


def download_file(url, local_path: Optional[str] = None, **kwargs) -> str:
    """download a public url locally"""
    chunk_size = kwargs.get("chunk_size")
    session = get_session(**kwargs)

    # create a temp path
    if not local_path:
        # create output path
        ext = path.get_ext(url)
        name = path.get_name(url)
        local_path = path.join(path.get_tempdir(), f"{name}.{ext}")

    with session.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path


def exists(url) -> bool:
    """
    Check if a URL exists via HEAD request
    """
    r = requests.head(url)
    return int(r.status_code) < 400
