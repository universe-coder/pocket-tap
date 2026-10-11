"""Entry point of the standalone build (PyInstaller cannot start a package's __main__)."""

import traceback

from pc_remote.__main__ import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:  # noqa: BLE001 - the window build has no console: show the error
        details = traceback.format_exc()
        try:
            import tkinter
            from tkinter import messagebox
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("PocketTap", details)
        except Exception:  # noqa: BLE001
            print(details)
            input("\nPress Enter to close")
