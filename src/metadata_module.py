"""
Metadata Module - Extracts file metadata
"""
import os
from datetime import datetime
from pathlib import Path

class FileMetadata:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.name = self.file_path.name
        self.extension = self.file_path.suffix.lower()
    
    def get_date(self):
        """
        Gets file date with fallback chain:
        1. Creation time (ctime)
        2. Modification time (mtime)
        3. Access time (atime)
        4. Current year
        """
        try:
            stat = self.file_path.stat()
            
            # Try creation time first
            if hasattr(stat, 'st_birthtime'):
                return datetime.fromtimestamp(stat.st_birthtime)
            
            # Fallback to modification time
            if stat.st_mtime:
                return datetime.fromtimestamp(stat.st_mtime)
            
            # Fallback to access time
            if stat.st_atime:
                return datetime.fromtimestamp(stat.st_atime)
        
        except (OSError, AttributeError):
            pass
        
        # Default to current date
        return datetime.now()
    
    def get_year(self):
        """Returns year as string (YYYY)"""
        date = self.get_date()
        return str(date.year)
    
    def get_extension(self):
        """Returns file extension"""
        return self.extension.lstrip('.')

