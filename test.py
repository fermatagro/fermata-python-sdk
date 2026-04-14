import asyncio
import os

from fermata._client import Fermata

APP_ID = os.getenv("HERA_APP_ID")
APP_SECRET_KEY = os.getenv("HERA_APP_SECRET")

_missing = [name for name, val in [("HERA_APP_ID", APP_ID), ("HERA_APP_SECRET", APP_SECRET_KEY)] if val is None]
if _missing:
	raise SystemExit(f"Error: required environment variables are not set: {', '.join(_missing)}")

assert APP_ID is not None
assert APP_SECRET_KEY is not None

async def main() -> None:
	async with Fermata(
		url="http://172.28.0.10:3000",
		username=str(APP_ID),
		password=str(APP_SECRET_KEY),
	) as fermata:
		print(f"Auth OK, scan_id={fermata.scan_id}")

		try:
			ghs = await fermata.greenhouses.list()
			print(f"Greenhouses: {ghs}")
		except Exception as e:
			print(f"greenhouses.list(): {e}")

		try:
			models = await fermata.models.list()
			print(f"Models: {models}")
		except Exception as e:
			print(f"models.list(): {e}")

		# try:
		# except:
		# 	print("oops")

if __name__ == "__main__":
	asyncio.run(main())
