"""
    main.py - the start of everything
"""

__maintainer__ = "FireRedz"
__source__ = "TearlessHen"


import asyncio
import json
from pathlib import Path

import aiohttp

from common import encryption, serializers

# TODO: Make this change-able
ASSET_VERSION: str = "2.3.5.15"  # As of 5/11/22 (D/M/Y)
CACHE_FOLDER: Path = Path.cwd() / "cache"
DATA_FOLDER: Path = Path.cwd() / "data"


def ensure_folders() -> None:
    for required_folder in [CACHE_FOLDER, DATA_FOLDER]:
        required_folder.mkdir(exist_ok=True)

    return None


def main_startup() -> int:
    # Checks
    for early_check in [ensure_folders]:
        if ret_code := early_check():
            return ret_code  # Something went wrong.

    # Run in asyncio loop
    asyncio.run(main())
    return 0


async def main() -> int:
    # Get assets file if doesnt exists.
    if not (assets_file := CACHE_FOLDER / "assets.dat").exists():
        async with aiohttp.ClientSession() as http:
            async with http.get(
                f"https://assetbundle-info.sekai.colorfulpalette.org/api/version/{ASSET_VERSION}/os/ios"
            ) as res:
                if not res or res.status != 200:
                    raise RuntimeError(
                        f"Failed to get asset file | {await res.read()=}"
                    )

                # Downloaded normally, save it to cache.
                assets_file.write_bytes(await res.read())

    # Decrypt that fucker
    # and then save it to data
    if decrypted := serializers.deserialize(
        encryption.aes.decrypt(assets_file.read_bytes())  # Forgive me for this
    ):
        (DATA_FOLDER / "assets.json").write_text(json.dumps(decrypted, indent=4))


if __name__ == "__main__":
    raise SystemExit(main_startup())
