import argparse
from pathlib import Path

from src.patcher.utils import current_patches


def filetype(value: str) -> Path:
    try:
        file = Path(value)
        if not file.exists():
            raise ValueError("File doesn't exist")
        return file
    except Exception as e:
        raise ValueError("Invalid value") from e


def parse_cli() -> tuple[argparse.Namespace, "dict[str, PatchFunction]"]:
    parser = argparse.ArgumentParser(
        prog="kpp_patcher",
        description="Patch different behaviours of the Kindle KPP app",
    )

    parser.add_argument(
        "filename",
        type=filetype,
        help="Path to the KPPMainApp.js.hbc file",
    )

    parser.add_argument(
        "--interactive",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Use interactive mode to select patches. If this option is set, cli "
            "choices are ignored. Disable with --no-interactive."
        ),
    )

    patches = current_patches()

    for name in patches.keys():
        parser.add_argument(
            f"--{name}", action=argparse.BooleanOptionalAction, default=True
        )

    args = parser.parse_args()

    selected_patches = {k: v for k, v in patches.items() if getattr(args, k, False)}

    return args, selected_patches
