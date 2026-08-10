# Fermata Python SDK

Python client for Fermata On-Site. Captures greenhouse photos from your robots/cameras and submits them for AI disease and pest detection.

## Installation

```bash
pip install fermata-sdk
```

Requires Python 3.12+. The import name is `fermata`:

```python
from fermata import Fermata, FermataSync
```

## Setup

You will receive the following from Fermata during onboarding:

| Parameter | Description |
|-----------|-------------|
| `url` | Fermata endpoint running on your local machine |
| `username` | Your SDK username |
| `password` | Your SDK password |
| `pipeline_id` | ID of your pipeline schedule (configured in Fermata Cloud) |

You can also discover available pipeline schedules programmatically:

```python
from fermata import FermataSync

with FermataSync(url="http://localhost:3000", username="...", password="...") as fermata:
    for s in fermata.pipelines.list_schedules():
        print(f"{s.id}  scope={s.scope}  scopeId={s.scope_id}")
```

## Quick Start

### Pipeline mode (recommended)

The simplest way to use the SDK. Greenhouse, AI model, and growing cycle are resolved automatically from your pipeline schedule:

```python
from fermata import FermataSync

with FermataSync(
    url="http://localhost:3000",
    username="your-username",
    password="your-password",
    pipeline_id="your-pipeline-id",
    sync_id="robot-run-2026-04-13-slot-2",  # unique string per scan run
) as fermata:
    task_id = fermata.infer(
        image="path/to/photo.jpg",
        captured_at="2026-04-01T10:00:00Z",
        position={"x": 5.2, "y": 3.1, "h": 2.0},
    )
    print(f"Submitted: {task_id}")
```

That's it. The photo is uploaded, inference runs automatically, and results appear in the Fermata Cloud dashboard.

### Manual mode

If you need to specify the greenhouse and model explicitly:

```python
with FermataSync(
    url="http://localhost:3000",
    username="your-username",
    password="your-password",
) as fermata:
    task_id = fermata.infer(
        image="path/to/photo.jpg",
        greenhouse_id="your-greenhouse-id",
        captured_at="2026-04-01T10:00:00Z",
        position={"x": 5.2, "y": 3.1, "h": 2.0},
    )
```

## Pipeline Mode

When `pipeline_id` and `sync_id` are provided, the SDK automatically resolves:

- **Greenhouse** — derived from the growing cycle linked to the schedule
- **AI model** — from the schedule's arguments (or the first available model)
- **Growing cycle** — from the schedule's scope (scope=growing_cycle)
- **Culture** — from the growing cycle

```python
with FermataSync(
    url="http://localhost:3000",
    username="your-username",
    password="your-password",
    pipeline_id="your-pipeline-id",
    sync_id="robot-run-2026-04-13-slot-2",
) as fermata:
    # Resolved context is available via fermata.run
    print(f"Greenhouse: {fermata.run.greenhouse_id}")
    print(f"Model: {fermata.run.model_name}")
    print(f"Cycle: {fermata.run.growing_cycle_id}")
    print(f"Culture: {fermata.run.culture_id}")
    print(f"Run ID: {fermata.run.run_id}")

    # No need to pass greenhouse_id or model_name
    fermata.infer(image="photo.jpg", captured_at="2026-04-01T10:00:00Z")
```

### `sync_id`

A unique string you generate for each scan run (e.g., `"robot-run-2026-04-13-slot-2"`). It is stored with the run for traceability.

In pipeline mode, photo IDs are generated deterministically from the `sync_id`, `captured_at`, and `position`. This means if the robot crashes and retries the same photos, they are automatically deduplicated — no duplicate uploads or inference tasks.

### `PipelineRun` fields

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | `str` | Unique ID for this run (pipeline fire ID) |
| `greenhouse_id` | `str` | Greenhouse derived from the growing cycle |
| `growing_cycle_id` | `str` | Growing cycle from the schedule scope |
| `culture_id` | `str` | Culture from the growing cycle |
| `model_name` | `str` | AI model to use |
| `organization_id` | `str` | Organization ID |

## `fermata.infer()`

Uploads a photo and submits it for AI inference. Returns a task ID.

```python
task_id = fermata.infer(
    image,              # File path (str/Path) or raw image bytes
    captured_at,        # When the photo was taken (ISO 8601 string or datetime)
    *,
    greenhouse_id=None, # Required in manual mode, auto-filled in pipeline mode
    position=None,      # Robot position: {"x": float, "y": float, "h": float}
    ptz=None,           # Camera pan/tilt/zoom: [float, float, float] (default: [0,0,0])
    device_id=None,     # Capturing device ID (UUID)
    model_name=None,    # AI model to use (default: auto-selected)
    photo_id=None,      # Custom photo ID (default: auto-generated)
    metadata=None,      # Arbitrary photo metadata: {"key": value, ...}
)
```

### Parameters

**`image`** — The photo to analyze. Either a file path or raw bytes:

```python
# From file
fermata.infer(image="photos/row3_pos12.jpg", ...)

# From bytes (e.g., from camera API)
fermata.infer(image=camera.capture(), ...)
```

**`greenhouse_id`** — Identifies which greenhouse this photo belongs to. Required in manual mode, auto-filled from the pipeline schedule in pipeline mode. Explicit values always override the pipeline context.

**`captured_at`** — Timestamp of when the photo was taken. Use ISO 8601 format:

```python
# String
fermata.infer(..., captured_at="2026-04-01T10:30:00Z")

# datetime
from datetime import datetime, timezone
fermata.infer(..., captured_at=datetime.now(timezone.utc))
```

**`position`** — Where in the greenhouse the photo was taken. Coordinates match your greenhouse layout in Fermata Cloud:

```python
fermata.infer(
    ...,
    position={
        "x": 5.2,   # meters from origin (width axis)
        "y": 3.1,   # meters from origin (length axis)
        "h": 2.0,   # height in meters
    },
)
```

**`ptz`** — Camera pan/tilt/zoom settings. Optional, defaults to `[0, 0, 0]`:

```python
fermata.infer(..., ptz=[0.5, 0.3, 1.0])  # [pan, tilt, zoom]
```

**`metadata`** — Arbitrary key/value metadata to store alongside the photo (e.g. resolution, format, sensor info). Stored on the photo in Fermata Cloud and returned when reading it back. Optional:

```python
fermata.infer(
    ...,
    metadata={
        "resolution": "4000x3000",
        "format": "jpeg",
        "exposure_ms": 12.5,
    },
)
```

## Robot Scan Example

Upload all photos from a scan directory:

```python
from pathlib import Path
from datetime import datetime, timezone
from fermata import FermataSync

FERMATA_URL = "http://localhost:3000"
USERNAME = "your-username"
PASSWORD = "your-password"
PIPELINE_ID = "your-pipeline-id"

def scan(photo_dir):
    sync_id = f"scan-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    with FermataSync(
        url=FERMATA_URL, username=USERNAME, password=PASSWORD,
        pipeline_id=PIPELINE_ID, sync_id=sync_id,
    ) as fermata:
        print(f"Starting scan {fermata.run.run_id} for {fermata.run.greenhouse_id}")

        for photo in sorted(Path(photo_dir).glob("*.jpg")):
            task_id = fermata.infer(
                image=photo,
                captured_at=datetime.fromtimestamp(photo.stat().st_mtime, tz=timezone.utc),
                position=parse_position(photo.name),  # your position parser
            )
            print(f"{photo.name} -> {task_id}")

    print("Scan complete")

scan("./today_scan/")
```

If the robot crashes mid-scan, restart with the same `sync_id` — photos already uploaded are automatically skipped.

## Scan Progress

Inference is asynchronous: `infer()` returns as soon as the task is queued. To follow a whole
batch, poll `scan_progress()` — that is one request per tick regardless of batch size, instead
of one request per task.

```python
import time

with FermataSync(url=FERMATA_URL, username=USERNAME, password=PASSWORD) as fermata:
    for photo in photos:
        fermata.infer(image=photo, captured_at=..., greenhouse_id=...)

    while not (progress := fermata.scan_progress()).finished:
        print(f"{progress.pending} tasks still pending")
        time.sleep(2)

    print("all tasks finished")
```

With no argument the method reports on the client's own scan (`fermata.scan_id`, which is the
fire id in pipeline mode). Pass a scan id to check a different one:

```python
progress = fermata.scan_progress("01920000-0000-7000-8000-000000000001")
```

The async client exposes the same method:

```python
progress = await fermata.scan_progress()
```

`pending` counts only what is still in flight — done, failed and canceled tasks are
indistinguishable once they finish. Fetch individual tasks with `fermata.inference.get(task_id)`
if you need per-task outcomes.

The SDK ships no built-in wait helper on purpose: poll interval, timeout and any progress
display belong to your application, as in the loop above.

Polling a scan with no photos in your organization raises `NotFoundError`. The same error
covers servers older than aivision 3.1.0, which do not serve this endpoint at all.

## Async Client

For applications that use asyncio (e.g., FastAPI backends), use the async client:

```python
import asyncio
from fermata import Fermata

async def main():
    async with Fermata(
        url="...", username="...", password="...",
        pipeline_id="your-pipeline-id", sync_id="run-001",
    ) as fermata:
        task_id = await fermata.infer(
            image="photo.jpg",
            captured_at="2026-04-01T10:00:00Z",
        )

asyncio.run(main())
```

### Concurrent uploads

```python
async with Fermata(
    url="...", username="...", password="...",
    pipeline_id="your-pipeline-id", sync_id="run-001",
) as fermata:
    photos = [
        ("img1.jpg", {"x": 1.0, "y": 2.0, "h": 0.5}),
        ("img2.jpg", {"x": 3.0, "y": 4.0, "h": 0.5}),
        ("img3.jpg", {"x": 5.0, "y": 6.0, "h": 0.5}),
    ]

    task_ids = await asyncio.gather(*[
        fermata.infer(
            image=img,
            captured_at="2026-04-01T10:00:00Z",
            position=pos,
        )
        for img, pos in photos
    ])
```

## Low-Level API

`fermata.infer()` is a convenience that combines four steps. You can call each step individually for more control:

```python
with FermataSync(url="...", username="...", password="...") as fermata:
    photo_id = "your-photo-id"  # UUIDv7 string

    # Step 1 — Get a presigned upload URL
    link = fermata.photos.upload_link(photo_id, captured_at="2026-04-01T10:00:00Z")
    print(link.upload_url)    # presigned PUT URL
    print(link.download_url)  # presigned GET URL
    print(link.expires_at)    # URL expiration time

    # Step 2 — Upload image to storage via presigned URL
    fermata.photos.upload(link.upload_url, "path/to/photo.jpg")  # file path or bytes

    # Step 3 — Register photo metadata
    fermata.photos.create(
        photo_id,
        greenhouse_id="gh-01",
        captured_at="2026-04-01T10:00:00Z",
        position={"x": 5.2, "y": 3.1, "h": 2.0},
    )

    # Step 4 — Submit for inference
    task_id = fermata.inference.submit(photo_id, model_name="tomato-v3")

    # Check result
    task = fermata.inference.get(task_id)
    print(task.status)  # "new" -> "pending" -> "done" or "failed"
```

This is useful when you need to:
- Separate upload from inference (e.g., upload now, infer later)
- Handle errors at each step individually
- Reuse an already-uploaded photo for multiple models
- Generate your own photo IDs for correlation with external systems

### Methods reference

| Method | Returns | Description |
|--------|---------|-------------|
| `fermata.photos.upload_link(photo_id, captured_at)` | `UploadLink` | Get presigned upload/download URLs |
| `fermata.photos.upload(upload_url, image)` | — | Upload image bytes to storage |
| `fermata.photos.create(photo_id, *, greenhouse_id, captured_at, ...)` | — | Register photo metadata |
| `fermata.inference.submit(photo_id, model_name)` | `str` | Submit photo for inference, returns task_id |
| `fermata.inference.get(task_id)` | `InferenceTask` | Get task status and details |
| `fermata.scan_progress(scan_id=None)` | `ScanProgress` | Pending inference-task count for a scan; defaults to the current scan |
| `fermata.inference.scan_progress(scan_id)` | `ScanProgress` | Same, for an explicit scan id |
| `fermata.pipelines.list_schedules()` | `list[Schedule]` | List available pipeline schedules |
| `fermata.pipelines.get_schedule(schedule_id)` | `Schedule` | Get a pipeline schedule by ID |
| `fermata.greenhouses.list()` | `list[Greenhouse]` | List greenhouses in the organization |
| `fermata.greenhouse_objects.list(greenhouse_id)` | `list[GreenhouseObject]` | List a greenhouse's layout objects (rows, blocks, exits); follows pagination |
| `fermata.greenhouse_objects.get(greenhouse_id, object_id)` | `GreenhouseObject` | Get a single greenhouse object by its numeric ID |

### `UploadLink` fields

| Field | Type | Description |
|-------|------|-------------|
| `upload_url` | `str` | Presigned URL — `PUT` your image bytes here |
| `download_url` | `str` | Presigned URL — `GET` to preview the uploaded image |
| `delete_url` | `str` | Presigned URL — `DELETE` to remove an orphaned upload |
| `expires_at` | `datetime` | When the presigned URLs expire |

### `ScanProgress` fields

| Field | Type | Description |
|-------|------|-------------|
| `scan_id` | `str` | Scan the count refers to (sent to the server as `pipelineId`) |
| `pending` | `int` | Inference tasks not yet in a terminal state (queued + in-flight) |
| `finished` | `bool` | `True` once `pending` reaches zero |

### `InferenceTask` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `UUID` | Task ID |
| `status` | `str` | `"new"`, `"pending"`, `"done"`, or `"failed"` |
| `attempts` | `int` | Number of processing attempts |
| `created_at` | `datetime` | When the task was created |
| `error_reason` | `str \| None` | Error message if task failed |

### `GreenhouseObject` fields

Physical layout elements of a greenhouse (rows, blocks, exits). Import the model types with `from fermata.types import GreenhouseObject, GreenhouseObjectType`. Fields marked optional may be unset on a given object.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Object number, unique within the greenhouse |
| `greenhouse_id` | `UUID` | Greenhouse the object belongs to |
| `kind` | `GreenhouseObjectType` | `"row"`, `"block"`, or `"exit"` |
| `description` | `str` | Optional. Human-readable label |
| `pos` | point | Optional. Point location on the greenhouse grid (`x`, `y`) — set for point-shaped objects |
| `rect` | rect | Optional. Rectangular area (`x1`, `y1`, `x2`, `y2`) — set for area-shaped objects |
| `height` | `float` | Optional. Height above the greenhouse floor |
| `created_at` | `datetime` | When the object was created |
| `updated_at` | `datetime` | When the object was last modified |

## Error Handling

```python
from fermata import FermataSync, FermataError, AuthError, ConnectionError

with FermataSync(...) as fermata:
    try:
        fermata.infer(image="photo.jpg", ...)
    except AuthError:
        print("Check your username and password")
    except ConnectionError:
        print("Cannot reach Fermata — is the service running?")
    except FermataError as e:
        print(f"Error: {e}")
```

| Exception | When |
|-----------|------|
| `AuthError` | Invalid username/password |
| `ConnectionError` | Fermata service unreachable or timed out |
| `ValidationError` | Invalid parameters (e.g., bad greenhouse_id) |
| `ServerError` | Internal server error |
| `FermataError` | Base class for all SDK errors |

Auth (401) is auto-refreshed and retried once. Server outages (502/503) are retried with backoff (up to 3 attempts). Network errors (connection refused, timeout) are **not** retried — they surface as `ConnectionError` immediately.

### Debugging connection errors

By default, `ConnectionError` shows a clean one-line message and hides the underlying httpx/httpcore traceback. Uncaught `FermataError` tracebacks are also filtered to drop SDK + transport internal frames, leaving only your code + the error message:

```
Traceback (most recent call last):
  File "scan_images.py", line 16, in <module>
    asyncio.run(main())
  File "scan_images.py", line 12, in main
    await client.list_schedules()
fermata.exceptions.ConnectionError: Cannot reach http://hera:3000/auth/token: connection timed out
```

The original httpx exception is still available on `__context__` for inspection (caught-exception paths are not filtered):

```python
except ConnectionError as e:
    print(e.__context__)  # the original httpx.ConnectTimeout
```

For the full chained traceback including SDK + httpx frames (useful when debugging transport-level issues), set `FERMATA_DEBUG=1`:

```bash
FERMATA_DEBUG=1 python my_script.py
```

The original exception is also always logged at DEBUG on the `fermata` logger — enable via `logging.basicConfig(level=logging.DEBUG)`.

## Releasing

Releases are automated by [release-please](https://github.com/googleapis/release-please). The flow:

1. Land conventional-commit changes on `master` (`feat:`, `fix:`, `refactor:`, etc. — see `release-please-config.json`)
2. `release-please.yml` opens/updates a **Release PR** that bumps `pyproject.toml` version, updates `CHANGELOG.md`, and updates `.release-please-manifest.json`
3. Review the Release PR. When ready, merge it
4. On merge, release-please creates a git tag (`vX.Y.Z`) and a GitHub Release
5. `release.yml` runs on the published release, builds wheel + sdist, and uploads to https://pypi.org/p/fermata-sdk via Trusted Publishing

No manual version bumps, no manual tagging.

## License

Proprietary — Copyright © 2025-2026 Fermatagro Technology Limited. All rights reserved. See [LICENSE](LICENSE).

Use of this SDK requires explicit written authorization from Fermatagro Technology Limited. Contact your Fermata representative for licensing.

## Support

Contact your Fermata representative for assistance with setup, credentials, or integration questions.
