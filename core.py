import json, urllib.request, urllib.parse, urllib.error
from typing import Dict, Optional, Any


class NeonAPI:
    """Powerful API interaction engine."""

    def __init__(self, base_url: str = "", headers: Optional[Dict] = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json", "User-Agent": "NeonAPI/1.0"}
        if headers:
            self.headers.update(headers)
        self.timeout = timeout
        self._last_response: Optional[Dict] = None

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = self._build_url(endpoint, params)
        return self._request("GET", url)

    def post(self, endpoint: str, data: Any = None) -> Dict:
        return self._request("POST", self._build_url(endpoint), data=data)

    def put(self, endpoint: str, data: Any = None) -> Dict:
        return self._request("PUT", self._build_url(endpoint), data=data)

    def delete(self, endpoint: str) -> Dict:
        return self._request("DELETE", self._build_url(endpoint))

    def patch(self, endpoint: str, data: Any = None) -> Dict:
        return self._request("PATCH", self._build_url(endpoint), data=data)

    def _build_url(self, endpoint: str, params: Optional[Dict] = None) -> str:
        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = self.base_url + "/" + endpoint.lstrip("/")
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return url

    def _request(self, method: str, url: str, data: Any = None) -> Dict:
        try:
            body = json.dumps(data).encode() if data else None
            req = urllib.request.Request(url, data=body, headers=self.headers, method=method)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode()
                try:
                    body_out = json.loads(raw)
                except Exception:
                    body_out = raw
                result = {"status": resp.status, "ok": resp.status < 400, "data": body_out, "url": url, "method": method}
                self._last_response = result
                return result
        except urllib.error.HTTPError as e:
            return {"status": e.code, "ok": False, "error": str(e), "url": url}
        except Exception as e:
            return {"status": 0, "ok": False, "error": str(e), "url": url}

    def set_auth(self, token: str, scheme: str = "Bearer"):
        self.headers["Authorization"] = f"{scheme} {token}"

    def set_header(self, key: str, value: str):
        self.headers[key] = value

    def last(self) -> Optional[Dict]:
        return self._last_response
