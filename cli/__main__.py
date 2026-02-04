"""
Allow running cli as a module: python -m cli
"""

import sys
import os

# Fix Windows console encoding to UTF-8
# This prevents UnicodeEncodeError when outputting non-ASCII characters
if sys.platform == "win32":
    # Set environment variable for child processes
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    # Reconfigure stdout/stderr to use UTF-8 with error handling
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from cli.main import main

if __name__ == "__main__":
    main()
