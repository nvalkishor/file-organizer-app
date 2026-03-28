"""
Main Application - File Organizer
"""
import logging
import sys
from pathlib import Path

# Import custom modules
from scanner_module import DirectoryScanner
from metadata_module import FileMetadata
from classifier_module import FileClassifier
from organizer_module import FileOrganizer
from input_module import InputHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main application flow"""
    print("=" * 60)
    print("         FILE ORGANIZER APPLICATION")
    print("=" * 60)
    
    # Get directory path
    target_dir = InputHandler.get_directory_path()
    print(f"\nTarget directory: {target_dir}")
    
    # Scan directory
    print("\nScanning directory...")
    scanner = DirectoryScanner(target_dir)
    files = scanner.scan()
    print(f"Found {scanner.get_total_files()} files")
    
    # Get mode
    mode = InputHandler.get_mode()
    print(f"\nMode: {mode}")
    
    # Confirm operation
    if not InputHandler.confirm_operation():
        print("Operation cancelled.")
        return
    
    # Initialize components
    dry_run = (mode == 'dry-run')
    organizer = FileOrganizer(target_dir, dry_run=dry_run)
    classifier = FileClassifier()
    
    # Organize files
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Organizing files...")
    organizer.organize_files(files, classifier, FileMetadata)
    
    # Display statistics
    stats = organizer.get_stats()
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(f"Files moved: {stats['moved']}")
    print(f"Files skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
