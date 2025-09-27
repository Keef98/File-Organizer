import os
import shutil
import json
import argparse
from pathlib import Path

class FileOrganizer:
    def __init__(self, config_file="organizer_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.log_file = "organizer_log.txt"
        
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "categories": {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
                "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
                "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
                "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".php", ".rb", ".go"],
                "Executables": [".exe", ".msi", ".deb", ".rpm", ".dmg", ".app"]
            },
            "custom_categories": {}
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] Error loading config: {e}")
                return default_config
        return default_config
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARNING] Error saving config: {e}")
    
    def add_custom_category(self, name, extensions):
        """Add a custom category"""
        self.config["custom_categories"][name] = extensions
        self.save_config()
        print(f"[OK] Added custom category: {name}")
    
    def get_file_category(self, filename):
        """Determine which category a file belongs to"""
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Check default categories
        for category, extensions in self.config["categories"].items():
            if file_ext in extensions:
                return category
        
        # Check custom categories
        for category, extensions in self.config["custom_categories"].items():
            if file_ext in extensions:
                return category
        
        return "Other"
    
    def organize_folder(self, folder_path, dry_run=False):
        """Organize files in the specified folder"""
        if not os.path.exists(folder_path):
            print("[WARNING] Folder does not exist!")
            return
        
        print(f"\n[INFO] Organizing folder: {folder_path}")
        if dry_run:
            print("[DRY RUN] No files will be moved")
        
        files_organized = 0
        files_skipped = 0
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Skip directories
                if os.path.isdir(file_path):
                    continue
                
                category = self.get_file_category(filename)
                dest_folder = os.path.join(folder_path, category)
                dest_path = os.path.join(dest_folder, filename)
                
                # Create category folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    if not dry_run:
                        os.makedirs(dest_folder)
                    print(f"[INFO] Created folder: {category}/")
                
                # Move file if it's not already in the right place
                if os.path.dirname(file_path) != dest_folder:
                    if dry_run:
                        print(f"[DRY RUN] Would move: {filename} -> {dest_folder}/")
                    else:
                        shutil.move(file_path, dest_path)
                        print(f"[OK] Moved: {filename} -> {dest_folder}/")
                        self.log_action(f"Moved {filename} -> {dest_folder}/")
                    files_organized += 1
                else:
                    print(f"[SKIP] {filename} already in {category}/")
                    files_skipped += 1
        
        except Exception as e:
            print(f"[ERROR] Error organizing folder: {e}")
            return
        
        print(f"\n[DONE] Check 'organizer_log.txt' for details.")
        print(f"[STATS] Files organized: {files_organized}, Skipped: {files_skipped}")
    
    def log_action(self, action):
        """Log an action to the log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{action}\n")
        except Exception as e:
            print(f"[WARNING] Error writing to log: {e}")

def main():
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("folder", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--add-category", nargs=2, metavar=("NAME", "EXTENSIONS"), 
                       help="Add custom category (extensions as comma-separated list)")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    
    if args.add_category:
        name, extensions = args.add_category
        ext_list = [ext.strip() for ext in extensions.split(',')]
        organizer.add_custom_category(name, ext_list)
        return
    
    organizer.organize_folder(args.folder, args.dry_run)

if __name__ == "__main__":
    main()
