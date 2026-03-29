"""
File Organizer Entry Point
This file goes in: file-organizer-app/run_app.py (ROOT directory)
"""
import sys
import os
import tkinter as tk
from pathlib import Path

# Get absolute paths
root_dir = Path(__file__).parent.absolute()
src_dir = root_dir / 'src'

print(f"🔍 Root directory: {root_dir}")
print(f"🔍 Source directory: {src_dir}")

# Add src to path
sys.path.insert(0, str(src_dir))

print(f"🔍 Python path: {sys.path[:2]}")

# Import and run
try:
    from gui_main import FileOrganizerGUI
    print("✅ Successfully imported FileOrganizerGUI")
    
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
