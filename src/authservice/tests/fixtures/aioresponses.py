import pytest

from aiohttp import ClientConnectionError

from aioresponses import aioresponses, CallbackResult
from aioresponses.compat import (
    merge_params,
    normalize_url,
)

from services.notification.config import RESET_TOKEN_URL, VERIFICATION_TOKEN_URL


class myaioresponses(aioresponses):
    _last_response_json = None

    # From source code of aioresponses
    async def _request_mock(self, orig_self, method, url, *args, **kwargs):
        if orig_self.closed:
            raise RuntimeError("Session is closed")

        url_origin = url
        url = normalize_url(merge_params(url, kwargs.get("params")))
        url_str = str(url)
        for prefix in self._passthrough:
            if url_str.startswith(prefix):
                return await self.patcher.temp_original(
                    orig_self, method, url_origin, *args, **kwargs
                )

        key = (method, url)
        self.requests.setdefault(key, [])
        request_call = self._build_request_call(method, *args, **kwargs)
        self.requests[key].append(request_call)

        response = await self.match(method, url, **kwargs)

        if response is None:
            raise ClientConnectionError(
                "Connection refused: {} {}".format(method, url)
            )
        self._responses.append(response)

        # New functionality: store the last response JSON
        self._last_response_json = await response.json()

        raise_for_status = kwargs.get("raise_for_status")
        if raise_for_status is None:
            raise_for_status = getattr(orig_self, "_raise_for_status", False)
        if raise_for_status:
            response.raise_for_status()

        return response

    def last_response(self) -> dict:
        return self._last_response_json


@pytest.fixture(autouse=True)
def mocked_responses():
    with myaioresponses() as m:
        m.post(
            RESET_TOKEN_URL,
            status=200,
            repeat=True,
            callback=lambda url, **kwargs: CallbackResult(
                payload=kwargs["json"]
            ),
        )
        m.post(
            VERIFICATION_TOKEN_URL,
            status=200,
            repeat=True,
            callback=lambda url, **kwargs: CallbackResult(
                payload=kwargs["json"]
            ),
        )
        yield m
