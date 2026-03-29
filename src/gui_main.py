"""
File Organizer GUI - Simple Version with Custom Sounds
"""
import sys
import os
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import winsound  # Windows only - for sound alerts

from scanner_module import DirectoryScanner
from metadata_module import FileMetadata
from classifier_module import FileClassifier
from organizer_module import FileOrganizer


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x700")
        
        # Title
        title = tk.Label(root, text="FILE ORGANIZER", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Directory selection
        dir_frame = tk.Frame(root)
        dir_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(dir_frame, text="Directory:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.dir_entry = tk.Entry(dir_frame, font=("Arial", 10))
        self.dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_btn = tk.Button(dir_frame, text="BROWSE", command=self.browse, font=("Arial", 10, "bold"), bg="green", fg="white", padx=20)
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Mode selection
        mode_frame = tk.LabelFrame(root, text="Mode", font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.mode_var = tk.StringVar(value="dry-run")
        
        tk.Radiobutton(mode_frame, text="DRY-RUN (Preview Only)", variable=self.mode_var, value="dry-run", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="EXECUTE (Move Files)", variable=self.mode_var, value="execute", font=("Arial", 10)).pack(anchor=tk.W)
        
        # Log
        log_frame = tk.LabelFrame(root, text="Log", font=("Arial", 10, "bold"), padx=5, pady=5)
        log_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.start_btn = tk.Button(btn_frame, text="START", command=self.start, font=("Arial", 12, "bold"), bg="blue", fg="white", padx=30, pady=10)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(btn_frame, text="CLEAR", command=self.clear, font=("Arial", 12, "bold"), bg="red", fg="white", padx=30, pady=10)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.log("Welcome! Follow these steps:\n1. Click BROWSE to select a folder\n2. Choose DRY-RUN or EXECUTE\n3. Click START button\n")
    
    def browse(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, folder)
            self.log(f"Selected: {folder}\n")
    
    def log(self, msg):
        self.log_text.insert(tk.END, msg)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear(self):
        self.log_text.delete("1.0", tk.END)
    
    def play_success_sound(self):
        """Play a soft, pleasant success sound"""
        try:
            # Windows beep: frequency=1000Hz, duration=300ms
            winsound.Beep(1000, 300)  # High pitch, moderate duration
            # Add a second beep for more pleasant sound
            import time
            time.sleep(0.1)
            winsound.Beep(1200, 300)  # Slightly higher pitch
        except Exception as e:
            self.log(f"Note: Sound playback not available\n")
    
    def play_error_sound(self):
        """Play an error/warning sound (slightly annoying)"""
        try:
            # Lower frequency beeps for error
            winsound.Beep(500, 200)   # Low pitch, short
            import time
            time.sleep(0.1)
            winsound.Beep(400, 200)   # Even lower pitch
        except Exception as e:
            self.log(f"Note: Sound playback not available\n")
    
    def play_info_sound(self):
        """Play a neutral info sound"""
        try:
            # Single moderate beep
            winsound.Beep(800, 200)
        except Exception as e:
            self.log(f"Note: Sound playback not available\n")
    
    def start(self):
        folder = self.dir_entry.get().strip()
        
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            self.play_error_sound()
            return
        
        if not Path(folder).exists():
            messagebox.showerror("Error", "Folder does not exist!")
            self.play_error_sound()
            return
        
        mode = self.mode_var.get()
        self.log(f"\n{'='*50}\n")
        self.log(f"Starting {mode} mode...\n")
        self.log(f"Folder: {folder}\n")
        self.play_info_sound()
        
        thread = threading.Thread(target=self.organize, args=(folder, mode))
        thread.daemon = True
        thread.start()
    
    def organize(self, folder, mode):
        try:
            self.log("Scanning files...\n")
            scanner = DirectoryScanner(folder)
            files = scanner.scan()
            count = len(files)
            
            self.log(f"Found {count} files\n")
            
            if count == 0:
                self.log("No files found!\n")
                messagebox.showwarning("Warning", "No files found!")
                self.play_error_sound()
                return
            
            dry_run = (mode == "dry-run")
            organizer = FileOrganizer(folder, dry_run=dry_run)
            classifier = FileClassifier()
            
            self.log(f"Organizing files...\n")
            
            for i, file in enumerate(files, 1):
                try:
                    meta = FileMetadata(file)
                    year = meta.get_year()
                    ftype = classifier.classify(Path(file).name)
                    
                    dest_dir = Path(folder) / year / ftype
                    organizer.ensure_directory(dest_dir)
                    dest_file = dest_dir / Path(file).name
                    organizer.move_file(file, dest_file)
                    
                    self.log(f"{i}. {Path(file).name} -> {year}/{ftype}/\n")
                except Exception as e:
                    self.log(f"{i}. Error: {Path(file).name}\n")
            
            stats = organizer.get_stats()
            self.log(f"\n{'='*50}\n")
            self.log(f"Results:\n")
            self.log(f"  Moved: {stats['moved']}\n")
            self.log(f"  Skipped: {stats['skipped']}\n")
            self.log(f"  Errors: {stats['errors']}\n")
            self.log(f"{'='*50}\n")
            
            if dry_run:
                self.log("DRY-RUN COMPLETE (No files moved)\n")
                self.play_success_sound()
                messagebox.showinfo("Success", "Dry-run complete!")
            else:
                if stats['errors'] == 0:
                    self.log("ORGANIZATION COMPLETE!\n")
                    self.play_success_sound()
                    messagebox.showinfo("Success", "Files organized successfully!")
                else:
                    self.log(f"ORGANIZATION COMPLETE WITH {stats['errors']} ERRORS!\n")
                    self.play_error_sound()
                    messagebox.showwarning("Completed with Errors", f"Organization complete but {stats['errors']} errors occurred!")
        
        except Exception as e:
            self.log(f"\nERROR: {e}\n")
            self.play_error_sound()
            messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()