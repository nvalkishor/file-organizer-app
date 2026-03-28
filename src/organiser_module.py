"""
Organizer Module - Handles file organization
"""
import shutil
from pathlib import Path
import logging

class FileOrganizer:
    def __init__(self, target_dir, dry_run=True):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)
        self.stats = {
            'moved': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def ensure_directory(self, path):
        """Creates directory if it doesn't exist"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    def move_file(self, source, destination):
        """Safely moves a file to destination"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            # Handle duplicates
            if dest_path.exists():
                name, ext = dest_path.stem, dest_path.suffix
                counter = 1
                while dest_path.exists():
                    dest_path = dest_path.parent / f"{name}_{counter}{ext}"
                    counter += 1
            
            if not self.dry_run:
                shutil.move(str(source_path), str(dest_path))
            
            self.logger.info(f"Moved: {source} -> {dest_path}")
            self.stats['moved'] += 1
            return True
        
        except Exception as e:
            self.logger.error(f"Error moving {source}: {e}")
            self.stats['errors'] += 1
            return False
    
    def organize_files(self, files, classifier, metadata):
        """Organizes files by year and type"""
        for file in files:
            try:
                meta = metadata(file)
                year = meta.get_year()
                file_type = classifier.classify(Path(file).name)
                
                # Create directory structure
                dest_dir = self.target_dir / year / file_type
                self.ensure_directory(dest_dir)
                
                # Move file
                dest_file = dest_dir / Path(file).name
                self.move_file(file, dest_file)
            
            except Exception as e:
                self.logger.error(f"Failed to organize {file}: {e}")
                self.stats['skipped'] += 1
    
    def get_stats(self):
        """Returns organization statistics"""
        return self.stats
