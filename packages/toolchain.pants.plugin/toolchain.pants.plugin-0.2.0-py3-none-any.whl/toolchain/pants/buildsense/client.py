# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import json
import logging
import zlib
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
from pants.goal.run_tracker import RunTrackerOptionEncoder
from requests.exceptions import RequestException

from toolchain.pants.common.network import get_common_request_headers

_logger = logging.getLogger(__name__)
WorkUnits = List[dict]
Artifacts = Dict[str, bytes]


class BuildSenseClient:
    _IMPERSONATE_HEADER = "X-Toolchain-Impersonate"

    @classmethod
    def from_options(cls, client_options, get_access_token_callback, repo):
        return cls(
            base_url=client_options.base_url,
            get_access_token_callback=get_access_token_callback,
            repo=repo,
            timeout=client_options.timeout,
            dry_run=client_options.dry_run,
        )

    def __init__(
        self,
        *,
        base_url: str,
        repo: str,
        get_access_token_callback: Callable,
        timeout: int,
        dry_run: bool,
    ):
        self._base_url = base_url
        self._successful_calls = 0
        self._dry_run = dry_run
        self._timeout = timeout
        self._get_access_token_callback = get_access_token_callback
        self._repo = repo
        self._compression_threshold = 10 * 1024  # 10kb
        self._session = requests.Session()
        self._session.mount(self._base_url, requests.adapters.HTTPAdapter(max_retries=3))

    def _get_headers(self, user_api_id: Optional[str]) -> Dict[str, str]:
        headers = get_common_request_headers()
        headers.update(self._get_access_token_callback().get_headers())
        headers["X-Pants-Stats-Version"] = "3"
        if user_api_id:
            headers[self._IMPERSONATE_HEADER] = user_api_id
        return headers

    @property
    def has_successful_calls(self) -> bool:
        return self._successful_calls > 0

    def _prepare_request(self, api_call_desc: str, data: str, as_file: bool) -> Tuple[dict, dict, int]:
        req_kwargs = {}
        headers = {}
        compression = len(data) > self._compression_threshold
        file_upload = compression and as_file
        uncompressed_size = len(data)
        if compression:
            headers["Content-Encoding"] = "compress"
            data = zlib.compress(data.encode())  # type: ignore
            if file_upload:
                req_kwargs = {"files": {"buildsense": data}}
        if not req_kwargs:
            headers["Content-Type"] = "application/json"
            req_kwargs = {"data": data}  # type: ignore[dict-item]
        if compression:
            compressed_size = len(data)
            rate = compressed_size / uncompressed_size
            compression_str = f" file={file_upload} compressed={compressed_size:,} rate={rate:.2%}"
        else:
            compression_str = ""
            compressed_size = len(data)

        _logger.debug(
            f"send_json_data {api_call_desc}. compression={compression} payload_size={uncompressed_size:,}{compression_str}"
        )
        return req_kwargs, headers, compressed_size

    def _send_json_data(
        self,
        *,
        api_call_desc: str,
        method: str,
        path: str,
        data: str,
        user_api_id: Optional[str],
        as_file: bool = False,
    ) -> Optional[dict]:
        url = urljoin(self._base_url, path)
        req_kwargs, headers, compressed_size = self._prepare_request(api_call_desc, data, as_file)
        headers.update(self._get_headers(user_api_id))
        if self._dry_run:
            return None
        try:
            response = self._session.request(
                method=method, url=url, headers=headers, timeout=self._timeout, **req_kwargs  # type: ignore[arg-type]
            )
            response.raise_for_status()
        except RequestException as error:
            self._process_error(api_call_desc, compressed_size, error)
            return None
        # Only returning a response if we got a HTTP 20x
        self._successful_calls += 1
        return response.json()

    def _process_error(self, api_call_desc: str, payload_size: int, error: RequestException) -> None:
        # TODO: handle errors better.
        response = error.response
        if response is not None:  # bool(response) will return False for failed requests.
            request_id = response.headers.get("X-Request-ID", "N/A")
            error_message = f" request id: {request_id} error message: {error.response.text}"
        else:
            error_message = error.request.url
        _logger.warning(f"Error reporting {api_call_desc}. payload_size={payload_size:,}: {error!r} {error_message}")

    def submit_workunits(self, *, run_id: str, call_num: int, user_api_id: Optional[str], workunits: WorkUnits):
        wu_json = json.dumps({"workunits": workunits, "run_id": run_id})
        _logger.debug(f"workunits(call_num={call_num}, work_units={len(workunits)})")
        self._send_json_data(
            api_call_desc=f"workunits(call_num={call_num}, work_units={len(workunits)})",
            method="post",
            path=f"{self._repo}/buildsense/{run_id}/workunits/",
            data=wu_json,
            user_api_id=user_api_id,
        )

    def submit_run_start(self, *, run_id: str, build_stats: dict) -> Optional[str]:
        data = json.dumps(build_stats, cls=RunTrackerOptionEncoder)
        json_response = self._send_json_data(
            api_call_desc="run_start",
            method="post",
            path=f"{self._repo}/buildsense/{run_id}/",
            data=data,
            user_api_id=None,
            as_file=True,
        )
        return json_response["ci_user_api_id"] if json_response else None

    def submit_run_end(self, *, run_id: str, user_api_id: Optional[str], build_stats: dict) -> Optional[str]:
        """Sends the final build report to the service.

        If it fails to upload, it returns the data so it can be queued for upload at a later time.
        """
        data = json.dumps(build_stats, cls=RunTrackerOptionEncoder)
        response = self._send_json_data(
            api_call_desc="run_end",
            method="patch",
            path=f"{self._repo}/buildsense/{run_id}/",
            data=data,
            user_api_id=user_api_id,
            as_file=True,
        )
        return None if response else data

    def submit_batch(self, *, batched_data: str, batch_name: str, user_api_id: Optional[str]) -> bool:
        response = self._send_json_data(
            api_call_desc=f"batch_upload={batch_name}",
            method="post",
            path=f"{self._repo}/buildsense/batch/",
            data=batched_data,
            user_api_id=user_api_id,
            as_file=True,
        )
        return bool(response)

    def upload_artifacts(self, *, run_id, artifacts: Dict[str, bytes], user_api_id: Optional[str]) -> bool:
        url = urljoin(self._base_url, f"{self._repo}/buildsense/{run_id}/artifacts/")
        headers = self._get_headers(user_api_id)
        headers["Content-Encoding"] = "compress"
        compressed_artifacts = {name: zlib.compress(data) for name, data in artifacts.items()}
        if self._dry_run:
            return True
        try:
            response = self._session.post(url=url, headers=headers, timeout=self._timeout, files=compressed_artifacts)
            response.raise_for_status()
        except RequestException as error:
            self._process_error(f"upload_files={len(artifacts)}", sum(len(fl) for fl in artifacts.values()), error)
            return False
        # Only returning a response if we got a HTTP 20x
        self._successful_calls += 1
        return True
