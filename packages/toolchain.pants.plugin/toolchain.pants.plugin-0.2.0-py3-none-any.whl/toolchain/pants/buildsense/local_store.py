# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import datetime
import json
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple

from pants.util.dirutil import safe_concurrent_creation

_logger = logging.getLogger(__name__)


class LocalBuildsStore:
    _TIMESTAMP_FMT = "%Y_%m_%d_%H_%M_%S"
    BATCH_VERSION = "1"

    def __init__(self, base_path: Path, max_batch_size_mb: int, enabled: bool) -> None:
        self._enabled = enabled
        self._build_queue = base_path / "queue"
        self._upload_staging = base_path / "upload"
        self._build_queue.mkdir(parents=True, exist_ok=True)
        self._upload_staging.mkdir(parents=True, exist_ok=True)
        self._max_batch_size = 1024 * 1024 * max_batch_size_mb  # keep it in bytes

    def store_build(self, run_id: str, json_build_data: str) -> None:
        if not self._enabled:
            return
        _logger.debug(f"store_build run_id={run_id} data={len(json_build_data)}")
        self._queue_data(run_id, "build_stats", json_build_data)

    def _queue_data(self, run_id: str, data_type: str, json_data: str) -> None:
        fn = self._build_queue / data_type / f"{run_id}.json"
        with safe_concurrent_creation(fn.as_posix()) as tmp_filename:
            with open(tmp_filename, "w") as fl:
                fl.write(json_data)

    def get_upload_batch(self) -> Optional[Path]:
        if not self._enabled:
            return None
        upload_batch = next(self._upload_staging.iterdir(), None)
        if upload_batch:
            return upload_batch
        return self._create_batch()

    def _create_batch(self) -> Optional[Path]:
        timestamp = datetime.datetime.utcnow().strftime(self._TIMESTAMP_FMT)
        batch, files_batch = self._get_batched_data()
        if not files_batch:
            return None

        batch_file = self._upload_staging / f"{timestamp}_{os.getpid()}.json"
        with safe_concurrent_creation(batch_file.as_posix()) as tmp_filename:
            with open(tmp_filename, "w") as fl:
                fl.write(batch)
        for build_file in files_batch:
            build_file.unlink()
        return batch_file

    def _get_batched_data(self) -> Tuple[str, List[Path]]:
        all_files = []
        batch_data = {"version": self.BATCH_VERSION}
        # Doing some work to account for existing files, will remove after everyone runs this version of the plugin
        for sub_dir, key in [("", "build_stats"), ("build_stats", "build_stats")]:
            files_batch = self._get_files_for_batch(sub_dir)
            if not files_batch:
                continue
            all_files.extend(files_batch)
            batch_data[key] = {build_file.stem: json.loads(build_file.read_bytes()) for build_file in files_batch}  # type: ignore[assignment]
        return json.dumps(batch_data), all_files

    def delete_batch_file(self, batch_file: Path) -> None:
        if batch_file.exists():
            batch_file.unlink()

    def _get_files_for_batch(self, sub_dir: str) -> List[Path]:
        # Latest builds first.
        def sort_key(fl: Path) -> Tuple[int, str]:
            last_modification = int(fl.stat().st_mtime / 60)  # Reduce accuracy. mostly to prevent flaky tests
            return last_modification, fl.stem

        queue_dir = self._build_queue
        if sub_dir:
            queue_dir = queue_dir / sub_dir
        if not queue_dir.exists():
            return []
        build_files = sorted(queue_dir.iterdir(), key=sort_key, reverse=True)
        files_to_upload = []
        total_size = 0
        for build_file in build_files:
            if not build_file.is_file():
                continue
            size = build_file.stat().st_size
            if size + total_size > self._max_batch_size:
                break
            total_size += size
            files_to_upload.append(build_file)
        return files_to_upload
