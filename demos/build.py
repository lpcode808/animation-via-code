"""Usage: python3 build.py <demo>   e.g. python3 build.py bouncing_ball
Renders frames, writes the soundtrack, muxes to <demo>.mp4 and makes a contact sheet."""
import sys, os, importlib

# The guard matters: on macOS and Windows, worker processes re-import this file.
if __name__ == "__main__":
    name = sys.argv[1]
    os.environ.setdefault("WORK", f"work/{name}")
    import common
    common.WORK = os.environ["WORK"]
    mod = importlib.import_module(name)
    if hasattr(mod, "checks"): mod.checks()                  # assertions run before any frame
    common.render(name, mod.DURATION, workers=int(os.environ.get("WORKERS", 4)))
    mod.soundtrack(f"{common.WORK}/audio.wav")
    common.mux(f"{name}.mp4", f"{common.WORK}/audio.wav")
    common.contact_sheet(f"{name}.mp4", f"{name}-sheet.jpg")
    print("wrote", f"{name}.mp4", f"{name}-sheet.jpg")
