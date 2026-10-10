"""Entry point of the standalone build (PyInstaller cannot start a package's __main__)."""

import traceback

from pc_remote.__main__ import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:  # noqa: BLE001 - keep the console open so the error can be read
        traceback.print_exc()
        input("\nPress Enter to close")
