# Fermata Python SDK

Python client for Fermata On-Site. Captures greenhouse photos from your robots/cameras and submits them for AI disease and pest detection.

## Installation

```bash
pip install fermata
```

Requires Python 3.12+.

## Setup

You will receive the following from Fermata during onboarding:

| Parameter | Description |
|-----------|-------------|
| `url` | Fermata endpoint running on your local machine |
| `username` | Your SDK username |
| `password` | Your SDK password |
| `greenhouse_id` | ID of your greenhouse (configured in Fermata Cloud) |

## Quick Start

```python
from fermata import FermataSync

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
    print(f"Submitted: {task_id}")
```

That's it. The photo is uploaded, inference runs automatically, and results appear in the Fermata Cloud dashboard.

## Scan Sessions

Each client instance represents a single scan session. All photos submitted through the same instance are automatically grouped together. The scan ID is generated when the client is created.

```python
# Scan 1
with FermataSync(...) as fermata:
    print(f"Scan: {fermata.scan_id}")
    fermata.infer(image="photo1.jpg", ...)
    fermata.infer(image="photo2.jpg", ...)  # same scan

# Scan 2 — new instance, new scan_id
with FermataSync(...) as fermata:
    print(f"Scan: {fermata.scan_id}")
    fermata.infer(image="photo3.jpg", ...)  # different scan
```

Use `fermata.scan_id` to log or correlate the scan in your own systems.

## `fermata.infer()`

Uploads a photo and submits it for AI inference. Returns a task ID.

```python
task_id = fermata.infer(
    image,              # File path (str/Path) or raw image bytes
    greenhouse_id,      # Your greenhouse ID
    captured_at,        # When the photo was taken (ISO 8601 string or datetime)
    *,
    position=None,      # Robot position: {"x": float, "y": float, "h": float}
    model_name=None,    # AI model to use (default: auto-selected)
    photo_id=None,      # Custom photo ID (default: auto-generated)
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

**`greenhouse_id`** — Identifies which greenhouse this photo belongs to. Provided by Fermata during setup.

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

## Robot Scan Example

Upload all photos from a scan directory:

```python
from pathlib import Path
from fermata import FermataSync

FERMATA_URL = "http://localhost:3000"
USERNAME = "your-username"
PASSWORD = "your-password"
GREENHOUSE_ID = "your-greenhouse-id"

def scan(photo_dir):
    with FermataSync(url=FERMATA_URL, username=USERNAME, password=PASSWORD) as fermata:
        print(f"Starting scan {fermata.scan_id}")

        for photo in sorted(Path(photo_dir).glob("*.jpg")):
            task_id = fermata.infer(
                image=photo,
                greenhouse_id=GREENHOUSE_ID,
                captured_at=photo.stat().st_mtime,
                position=parse_position(photo.name),  # your position parser
            )
            print(f"{photo.name} -> {task_id}")

    print("Scan complete")

scan("./today_scan/")
```

## Async Client

For applications that use asyncio (e.g., FastAPI backends), use the async client:

```python
import asyncio
from fermata import Fermata

async def main():
    async with Fermata(url="...", username="...", password="...") as fermata:
        task_id = await fermata.infer(
            image="photo.jpg",
            greenhouse_id="gh-01",
            captured_at="2026-04-01T10:00:00Z",
        )

asyncio.run(main())
```

### Concurrent uploads

```python
async with Fermata(url="...", username="...", password="...") as fermata:
    photos = [
        ("img1.jpg", {"x": 1.0, "y": 2.0, "h": 0.5}),
        ("img2.jpg", {"x": 3.0, "y": 4.0, "h": 0.5}),
        ("img3.jpg", {"x": 5.0, "y": 6.0, "h": 0.5}),
    ]

    task_ids = await asyncio.gather(*[
        fermata.infer(
            image=img,
            greenhouse_id="gh-01",
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
    photo = fermata.photos.create(
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
| `fermata.photos.create(photo_id, *, greenhouse_id, captured_at, position)` | `Photo` | Register photo metadata |
| `fermata.inference.submit(photo_id, model_name)` | `str` | Submit photo for inference, returns task_id |
| `fermata.inference.get(task_id)` | `InferenceTask` | Get task status and details |

### `UploadLink` fields

| Field | Type | Description |
|-------|------|-------------|
| `upload_url` | `str` | Presigned URL — `PUT` your image bytes here |
| `download_url` | `str` | Presigned URL — `GET` to preview the uploaded image |
| `delete_url` | `str` | Presigned URL — `DELETE` to remove an orphaned upload |
| `expires_at` | `datetime` | When the presigned URLs expire |

### `InferenceTask` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `UUID` | Task ID |
| `status` | `str` | `"new"`, `"pending"`, `"done"`, or `"failed"` |
| `attempts` | `int` | Number of processing attempts |
| `created_at` | `datetime` | When the task was created |
| `error_reason` | `str \| None` | Error message if task failed |

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

Network errors and temporary outages are automatically retried (3 attempts with backoff).

## Support

Contact your Fermata representative for assistance with setup, credentials, or integration questions.
