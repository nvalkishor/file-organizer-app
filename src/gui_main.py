"""
File Organizer GUI - Windows-friendly GUI application
Double-click to run!
"""
import sys
from pathlib import Path

# Fix module imports for PyInstaller
sys.path.insert(0, str(Path(__file__).parent))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from scanner_module import DirectoryScanner
from metadata_module import FileMetadata
from classifier_module import FileClassifier
from organizer_module import FileOrganizer

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer App")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        self.root.configure(bg='#f0f0f0')
        
        # Title
        title_label = tk.Label(
            root, 
            text="📁 File Organizer", 
            font=("Arial", 18, "bold"),
            bg='#f0f0f0'
        )
        title_label.pack(pady=20)
        
        # Directory selection frame
        frame1 = tk.Frame(root, bg='#f0f0f0')
        frame1.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame1, text="Target Directory:", font=("Arial", 10), bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.dir_entry = tk.Entry(frame1, width=40, font=("Arial", 9))
        self.dir_entry.pack(side=tk.LEFT, padx=10)
        
        browse_btn = tk.Button(frame1, text="Browse", command=self.browse_directory, bg='#4CAF50', fg='white', cursor="hand2")
        browse_btn.pack(side=tk.LEFT)
        
        # Mode selection frame
        frame2 = tk.LabelFrame(root, text="Select Mode", font=("Arial", 10, "bold"), bg='#f0f0f0', padx=20, pady=15)
        frame2.pack(pady=15, padx=20, fill=tk.X)
        
        self.mode_var = tk.StringVar(value="dry-run")
        
        tk.Radiobutton(
            frame2, 
            text="🔍 Dry-run (Preview - No changes)", 
            variable=self.mode_var, 
            value="dry-run",
            font=("Arial", 9),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=8)
        
        tk.Radiobutton(
            frame2, 
            text="✂️ Execute (Actually move files)", 
            variable=self.mode_var, 
            value="execute",
            font=("Arial", 9),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=8)
        
        # Status frame
        frame3 = tk.LabelFrame(root, text="Status", font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame3.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(frame3, height=8, width=50, font=("Courier", 8), bg='white', fg='#333')
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame3, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(pady=10, padx=20, fill=tk.X)
        
        # Buttons frame
        frame4 = tk.Frame(root, bg='#f0f0f0')
        frame4.pack(pady=15)
        
        start_btn = tk.Button(
            frame4, 
            text="▶ Start Organization", 
            command=self.start_organization,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            frame4, 
            text="🗑️ Clear Log", 
            command=self.clear_log,
            bg='#f44336',
            fg='white',
            font=("Arial", 10),
            cursor="hand2",
            padx=15,
            pady=10
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Footer
        footer = tk.Label(
            root, 
            text="© 2026 File Organizer | Organize files by Year & Type",
            font=("Arial", 8),
            bg='#f0f0f0',
            fg='#666'
        )
        footer.pack(pady=5)
    
    def browse_directory(self):
        """Open directory browser"""
        directory = filedialog.askdirectory(title="Select Directory to Organize")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.log(f"✅ Directory selected: {directory}")
    
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Clear the log"""
        self.status_text.delete(1.0, tk.END)
    
    def start_organization(self):
        """Start file organization in separate thread"""
        directory = self.dir_entry.get().strip()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory!")
            return
        
        if not Path(directory).exists():
            messagebox.showerror("Error", "Directory does not exist!")
            return
        
        mode = self.mode_var.get()
        self.log(f"\n{'='*50}")
        self.log(f"Starting file organization...")
        self.log(f"Directory: {directory}")
        self.log(f"Mode: {mode}")
        self.log(f"{'='*50}\n")
        
        # Run in separate thread to prevent GUI freeze
        thread = threading.Thread(target=self.organize_files, args=(directory, mode))
        thread.start()
    
    def organize_files(self, directory, mode):
        """Organize files (runs in background thread)"""
        try:
            self.progress.start()
            
            # Scan directory
            self.log("📁 Scanning directory...")
            scanner = DirectoryScanner(directory)
            files = scanner.scan()
            self.log(f"✅ Found {scanner.get_total_files()} files\n")
            
            # Initialize organizer
            dry_run = (mode == 'dry-run')
            organizer = FileOrganizer(directory, dry_run=dry_run)
            classifier = FileClassifier()
            
            # Organize files
            self.log(f"⏳ Organizing files...")
            for i, file in enumerate(files):
                try:
                    meta = FileMetadata(file)
                    year = meta.get_year()
                    file_type = classifier.classify(Path(file).name)
                    
                    dest_dir = Path(directory) / year / file_type
                    organizer.ensure_directory(dest_dir)
                    
                    dest_file = dest_dir / Path(file).name
                    organizer.move_file(file, dest_file)
                    
                    self.log(f"  {i+1}. {Path(file).name} → {year}/{file_type}/")
                except Exception as e:
                    self.log(f"  ⚠️ Error: {Path(file).name} - {str(e)}")
            
            # Display statistics
            stats = organizer.get_stats()
            self.log(f"\n{'='*50}")
            self.log(f"📊 STATISTICS")
            self.log(f"{'='*50}")
            self.log(f"Files moved: {stats['moved']}")
            self.log(f"Files skipped: {stats['skipped']}")
            self.log(f"Errors: {stats['errors']}")
            self.log(f"{'='*50}\n")
            
            if dry_run:
                self.log("✅ Dry-run completed! (No files were actually moved)")
            else:
                self.log("✅ Organization completed!")
            
            messagebox.showinfo("Success", "File organization completed!")
        
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.progress.stop()

if __name__ == '__main__':
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()# File: src/gui_main.py
