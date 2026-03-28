"""
Scanner Module - Recursively scans directories
"""
import os
from pathlib import Path

class DirectoryScanner:
    def __init__(self, target_path):
        self.target_path = Path(target_path)
        self.files = []
        self.total_files = 0
    
    def scan(self, exclude_hidden=True):
        """Recursively scans directory for all files"""
        self.files = []
        
        try:
            for root, dirs, files in os.walk(self.target_path):
                # Remove hidden directories
                if exclude_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if exclude_hidden and file.startswith('.'):
                        continue
                    
                    file_path = Path(root) / file
                    self.files.append(str(file_path))
            
            self.total_files = len(self.files)
            return self.files
        
        except PermissionError:
            print(f"Permission denied: {self.target_path}")
            return []
    
    def get_total_files(self):
        """Returns total number of files scanned"""
        return self.total_files
