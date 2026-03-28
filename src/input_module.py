"""
Input Module - Handles user input and validation
"""
from pathlib import Path

class InputHandler:
    @staticmethod
    def get_directory_path():
        """Gets and validates directory path from user"""
        while True:
            path = input("Enter the target directory path: ").strip()
            
            if not path:
                print("Path cannot be empty. Please try again.")
                continue
            
            path_obj = Path(path)
            
            if not path_obj.exists():
                print(f"Path does not exist: {path}")
                continue
            
            if not path_obj.is_dir():
                print(f"Path is not a directory: {path}")
                continue
            
            try:
                list(path_obj.iterdir())
                return str(path_obj)
            except PermissionError:
                print(f"Permission denied: {path}")
                continue
    
    @staticmethod
    def get_mode():
        """Gets mode from user (dry-run or execute)"""
        while True:
            print("\nSelect mode:")
            print("1. Dry-run (preview changes without moving files)")
            print("2. Execute (actually move files)")
            
            choice = input("Enter choice (1 or 2): ").strip()
            
            if choice == '1':
                return 'dry-run'
            elif choice == '2':
                return 'execute'
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    @staticmethod
    def confirm_operation():
        """Gets confirmation from user"""
        response = input("Do you want to proceed? (yes/no): ").strip().lower()
        return response in ['yes', 'y']
