import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
from organizer import FileOrganizer

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.settings = {
            "default_folder": os.path.join(os.path.expanduser("~"), "Desktop"),
            "file_type_filters": "*.*",
            "theme": "dark",
            "log_file_location": "file_organizer.log"
        }
        self.load_settings()
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.setup_ui()
        self.load_config()
        self.setup_keyboard_shortcuts()
        self.setup_drag_drop()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🗂️ Modern File Organizer Pro")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#1e1e1e")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1200x900+{x}+{y}")
        
    def setup_styles(self):
        """Setup modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Card.TFrame', background='#2d2d2d', relief='raised', borderwidth=1)
        style.configure('Title.TLabel', background='#2d2d2d', foreground='#ffffff', font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background='#2d2d2d', foreground='#cccccc', font=('Segoe UI', 10))
        style.configure('Info.TLabel', background='#1e1e1e', foreground='#ffffff', font=('Segoe UI', 9))
        style.configure('Success.TLabel', background='#1e1e1e', foreground='#4CAF50', font=('Segoe UI', 9))
        style.configure('Warning.TLabel', background='#1e1e1e', foreground='#FF9800', font=('Segoe UI', 9))
        style.configure('Error.TLabel', background='#1e1e1e', foreground='#F44336', font=('Segoe UI', 9))
        
        # Button styles
        style.configure('Primary.TButton', background='#2196F3', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', background='#4CAF50', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Warning.TButton', background='#FF9800', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton', background='#F44336', foreground='white', font=('Segoe UI', 10, 'bold'))
        
        # Entry styles
        style.configure('Modern.TEntry', fieldbackground='#3d3d3d', foreground='#ffffff', insertcolor='#ffffff')
        
        # Progress bar style - using default style for compatibility
        # style.configure('Custom.TProgressbar', background='#2196F3', troughcolor='#3d3d3d')
        
    def setup_variables(self):
        """Setup tkinter variables"""
        self.folder_var = tk.StringVar(value=self.settings.get("default_folder", os.path.join(os.path.expanduser("~"), "Desktop")))
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        self.dry_run_var = tk.BooleanVar(value=False)
        self.scanned_files = {}
        self.custom_categories = {}
        self.organizer = FileOrganizer()
        self.is_organizing = False
        self.file_type_filters = self.settings.get("file_type_filters", "*.*")
        self.log_file_location = self.settings.get("log_file_location", "file_organizer.log")
    def load_settings(self):
        """Load settings from settings.json"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to settings.json"""
        try:
            with open("settings.json", 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Card.TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🗂️ Modern File Organizer Pro", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Professional File Organization Tool", style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Folder selection card
        folder_card = ttk.LabelFrame(main_frame, text="📁 Folder Selection", style='Card.TFrame', padding=15)
        folder_card.pack(fill=tk.X, pady=(0, 15))
        
        folder_frame = ttk.Frame(folder_card)
        folder_frame.pack(fill=tk.X)
        
        ttk.Label(folder_frame, text="Select folder to organize:", style='Info.TLabel').pack(anchor=tk.W)
        
        folder_input_frame = ttk.Frame(folder_frame)
        folder_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.folder_entry = ttk.Entry(folder_input_frame, textvariable=self.folder_var, style='Modern.TEntry', font=('Segoe UI', 10))
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(folder_input_frame, text="Browse", command=self.browse_folder, style='Primary.TButton').pack(side=tk.RIGHT)
        ttk.Button(folder_input_frame, text="Scan", command=self.scan_folder, style='Success.TButton').pack(side=tk.RIGHT, padx=(0, 10))
        
        # Options card
        options_card = ttk.LabelFrame(main_frame, text="⚙️ Options", style='Card.TFrame', padding=15)
        options_card.pack(fill=tk.X, pady=(0, 15))
        
        options_frame = ttk.Frame(options_card)
        options_frame.pack(fill=tk.X)
        
        ttk.Checkbutton(options_frame, text="Dry Run (Preview only)", variable=self.dry_run_var, style='Info.TLabel').pack(anchor=tk.W)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.organize_btn = ttk.Button(action_frame, text="🚀 Organize Files", command=self.start_organize, style='Success.TButton')
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ Stop", command=self.stop_organize, style='Danger.TButton', state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text="📊 Custom Categories", command=self.edit_custom_categories, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="⚙️ Settings", command=self.show_settings, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="❓ Help", command=self.show_help, style='Primary.TButton').pack(side=tk.LEFT)
        
        # Progress card
        progress_card = ttk.LabelFrame(main_frame, text="📈 Progress", style='Card.TFrame', padding=15)
        progress_card.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(progress_card, variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(progress_card, textvariable=self.status_var, style='Info.TLabel')
        self.status_label.pack()
        
        # Statistics card
        stats_card = ttk.LabelFrame(main_frame, text="📊 Statistics", style='Card.TFrame', padding=15)
        stats_card.pack(fill=tk.X, pady=(0, 15))
        
        self.stats_frame = ttk.Frame(stats_card)
        self.stats_frame.pack(fill=tk.X)
        
        # Log card
        log_card = ttk.LabelFrame(main_frame, text="📝 Activity Log", style='Card.TFrame', padding=15)
        log_card.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_card, height=8, bg='#2d2d2d', fg='#ffffff', 
                                                insertbackground='#ffffff', font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial log message
        self.log_message("File Organizer Pro started. Select a folder to begin.")
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.browse_folder())
        self.root.bind('<Control-s>', lambda e: self.scan_folder())
        self.root.bind('<Control-r>', lambda e: self.start_organize())
        self.root.bind('<Escape>', lambda e: self.stop_organize())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Control-h>', lambda e: self.show_help())
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            self.root = TkinterDnD.Tk() if not hasattr(self, '_dnd_setup') else self.root
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
            self._dnd_setup = True
        except ImportError:
            self.log_message("Drag & drop not available. Install tkinterdnd2 for full functionality.")
            
    def on_drop(self, event):
        """Handle drag and drop events"""
        try:
            files = self.root.tk.splitlist(event.data)
            if files and os.path.isdir(files[0]):
                self.folder_var.set(files[0])
                self.status_var.set(f"Selected folder: {os.path.basename(files[0])}")
                self.update_statistics()
                self.scan_folder()
                self.log_message(f"Folder dropped: {files[0]}")
        except Exception as e:
            self.log_message(f"Error handling drag & drop: {str(e)}")
        
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Select folder to organize")
        if folder:
            self.folder_var.set(folder)
            self.status_var.set(f"Selected folder: {os.path.basename(folder)}")
            self.update_statistics()
            self.scan_folder()
            self.log_message(f"Selected folder: {folder}")
    
    def scan_folder(self):
        """Scan folder and categorize files"""
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return
        
        self.log_message(f"Scanning folder: {folder}")
        self.status_var.set("Scanning folder...")

        try:
            self.scanned_files = {}
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

            if not files:
                self.log_message("No files found in the selected folder.")
                self.status_var.set("No files found")
                self.update_statistics()
                return

            for filename in files:
                try:
                    category = self.organizer.get_file_category(filename)
                except Exception as e:
                    category = "Unknown"
                    self.log_message(f"Error categorizing '{filename}': {str(e)}")

                if category not in self.scanned_files:
                    self.scanned_files[category] = []
                self.scanned_files[category].append(filename)

            self.update_statistics()
            self.log_message(f"Scan complete. Found {len(files)} files in {len(self.scanned_files)} categories.")
            self.status_var.set("Scan complete")
            
        except Exception as e:
            self.log_message(f"Error scanning folder: {str(e)}")
            self.status_var.set("Scan failed")
    
    def update_statistics(self):
        """Update the statistics display"""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not self.scanned_files:
            ttk.Label(self.stats_frame, text="No files scanned yet", style='Info.TLabel').pack(anchor=tk.W)
            return
        
        total_files = sum(len(files) for files in self.scanned_files.values())
        ttk.Label(self.stats_frame, text=f"Total files: {total_files}", style='Info.TLabel').pack(anchor=tk.W)
        
        for category, files in self.scanned_files.items():
            ttk.Label(self.stats_frame, text=f"{category}: {len(files)} files", style='Info.TLabel').pack(anchor=tk.W)
    
    def start_organize(self):
        """Start the organization process"""
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return
        
        if self.is_organizing:
            messagebox.showwarning("Warning", "Organization is already in progress.")
            return
        
        self.is_organizing = True
        self.organize_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start organization directly (no threading for now)
        self.organize_files_direct()
    
    def organize_files_direct(self):
        """Organize files directly without threading"""
        try:
            folder = self.folder_var.get()
            dry_run = self.dry_run_var.get()
            
            self.log_message(f"Starting organization: {folder}")
            self.status_var.set("Organizing files...")
            self.root.update()
            
            # Get all files in the folder
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total_files = len(files)
            
            if total_files == 0:
                self.log_message("No files to organize.")
                self.status_var.set("No files found")
                return
            
            files_organized = 0
            files_skipped = 0
            
            for i, filename in enumerate(files):
                if not self.is_organizing:  # Check for stop signal
                    break
                
                file_path = os.path.join(folder, filename)
                category = self.organizer.get_file_category(filename)
                dest_folder = os.path.join(folder, category)
                dest_path = os.path.join(dest_folder, filename)
                
                # Create category folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    if not dry_run:
                        os.makedirs(dest_folder)
                    self.log_message(f"Created folder: {category}/")
                
                # Move file if it's not already in the right place
                if os.path.dirname(file_path) != dest_folder:
                    if dry_run:
                        self.log_message(f"[DRY RUN] Would move: {filename} -> {category}/")
                    else:
                        try:
                            import shutil
                            shutil.move(file_path, dest_path)
                            self.log_message(f"Moved: {filename} -> {category}/")
                        except Exception as e:
                            self.log_message(f"Error moving {filename}: {str(e)}")
                            continue
                    files_organized += 1
                else:
                    self.log_message(f"Skipped: {filename} (already in {category}/)")
                    files_skipped += 1
                
                # Update progress
                progress = (i + 1) / total_files * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing: {filename}")
                self.root.update()  # Update GUI
            
            if self.is_organizing:
                self.log_message(f"Organization complete! Files organized: {files_organized}, Skipped: {files_skipped}")
                self.status_var.set("Organization complete")
            else:
                self.log_message("Organization stopped by user")
                self.status_var.set("Organization stopped")
            
        except Exception as e:
            self.log_message(f"Error during organization: {str(e)}")
            self.status_var.set("Organization failed")
        finally:
            self.is_organizing = False
            self.organize_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.progress_var.set(0)
    
    def organize_worker(self):
        """Worker thread for organization"""
        try:
            folder = self.folder_var.get()
            dry_run = self.dry_run_var.get()
            
            # Store messages for batch processing
            messages = []
            
            messages.append(f"Starting organization: {folder}")
            messages.append("Organizing files...")
            
            # Get all files in the folder
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total_files = len(files)
            
            if total_files == 0:
                messages.append("No files to organize.")
                messages.append("No files found")
                self.batch_update_gui(messages)
                return
            
            files_organized = 0
            files_skipped = 0
            
            for i, filename in enumerate(files):
                if not self.is_organizing:  # Check for stop signal
                    break
                
                file_path = os.path.join(folder, filename)
                category = self.organizer.get_file_category(filename)
                dest_folder = os.path.join(folder, category)
                dest_path = os.path.join(dest_folder, filename)
                
                # Create category folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    if not dry_run:
                        os.makedirs(dest_folder)
                    messages.append(f"Created folder: {category}/")
                
                # Move file if it's not already in the right place
                if os.path.dirname(file_path) != dest_folder:
                    if dry_run:
                        messages.append(f"[DRY RUN] Would move: {filename} -> {category}/")
                    else:
                        try:
                            import shutil
                            shutil.move(file_path, dest_path)
                            messages.append(f"Moved: {filename} -> {category}/")
                        except Exception as e:
                            messages.append(f"Error moving {filename}: {str(e)}")
                            continue
                    files_organized += 1
                else:
                    messages.append(f"Skipped: {filename} (already in {category}/)")
                    files_skipped += 1
                
                # Update progress every 5 files or at the end
                if (i + 1) % 5 == 0 or (i + 1) == total_files:
                    progress = (i + 1) / total_files * 100
                    self.batch_update_gui(messages, progress, f"Processing: {filename}")
                    messages = []  # Clear messages after updating
            
            if self.is_organizing:
                messages.append(f"Organization complete! Files organized: {files_organized}, Skipped: {files_skipped}")
                messages.append("Organization complete")
            else:
                messages.append("Organization stopped by user")
                messages.append("Organization stopped")
            
            self.batch_update_gui(messages)
            
        except Exception as e:
            messages = [f"Error during organization: {str(e)}", "Organization failed"]
            self.batch_update_gui(messages)
        finally:
            self.is_organizing = False
            self.batch_update_gui([], 0, "", final_state=True)
    
    def batch_update_gui(self, messages, progress=None, status=None, final_state=False):
        """Update GUI from worker thread using a queue"""
        try:
            # Store updates in a thread-safe way
            if hasattr(self, 'root') and self.root.winfo_exists():
                # Use a simple approach - just print to console for now
                for message in messages:
                    print(f"[LOG] {message}")
                
                if progress is not None:
                    print(f"[PROGRESS] {progress}%")
                if status is not None:
                    print(f"[STATUS] {status}")
                
                if final_state:
                    print("[FINAL] Organization complete")
                    # Reset button states
                    self.organize_btn.config(state=tk.NORMAL)
                    self.stop_btn.config(state=tk.DISABLED)
                    self.progress_var.set(0)
        except:
            pass  # Ignore errors if GUI is destroyed
    
# Removed unused methods - using root.after() for thread-safe updates
    
    def stop_organize(self):
        """Stop the organization process"""
        self.is_organizing = False
        self.log_message("Stopping organization...")
        self.status_var.set("Stopping...")
    
    def edit_custom_categories(self):
        """Open custom categories editor"""
        try:
            # Simple input dialog for now
            from tkinter import simpledialog
            
            # Get category name
            name = simpledialog.askstring("Add Category", "Enter category name:")
            if not name:
                return
                
            # Get extensions
            extensions = simpledialog.askstring("Add Category", f"Enter file extensions for '{name}' (comma-separated):")
            if not extensions:
                return
                
            # Add category
            ext_list = [ext.strip() for ext in extensions.split(',')]
            self.organizer.add_custom_category(name, ext_list)
            self.log_message(f"Added custom category: {name}")
            self.update_statistics()
            
        except Exception as e:
            self.log_message(f"Error adding custom category: {str(e)}")
    
    def show_settings(self):
        """Show settings dialog"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("400x350")
        settings_win.transient(self.root)
        settings_win.grab_set()

        # Default folder
        tk.Label(settings_win, text="Default Folder:").pack(anchor=tk.W, padx=10, pady=(10,0))
        default_folder_var = tk.StringVar(value=self.settings.get("default_folder", os.path.join(os.path.expanduser("~"), "Desktop")))
        default_folder_entry = ttk.Entry(settings_win, textvariable=default_folder_var, width=40)
        default_folder_entry.pack(padx=10, pady=2)
        def browse_default_folder():
            folder = filedialog.askdirectory()
            if folder:
                default_folder_var.set(folder)
        ttk.Button(settings_win, text="Browse", command=browse_default_folder).pack(padx=10, pady=2)

        # File type filters
        tk.Label(settings_win, text="File Type Filters (e.g. *.jpg;*.png;*.mp4):").pack(anchor=tk.W, padx=10, pady=(10,0))
        file_type_var = tk.StringVar(value=self.settings.get("file_type_filters", "*.*"))
        ttk.Entry(settings_win, textvariable=file_type_var, width=40).pack(padx=10, pady=2)

        # Theme
        tk.Label(settings_win, text="Theme:").pack(anchor=tk.W, padx=10, pady=(10,0))
        theme_var = tk.StringVar(value=self.settings.get("theme", "dark"))
        ttk.Combobox(settings_win, textvariable=theme_var, values=["dark", "light"], state="readonly").pack(padx=10, pady=2)

        # Log file location
        tk.Label(settings_win, text="Log File Location:").pack(anchor=tk.W, padx=10, pady=(10,0))
        log_file_var = tk.StringVar(value=self.settings.get("log_file_location", "file_organizer.log"))
        log_file_entry = ttk.Entry(settings_win, textvariable=log_file_var, width=40)
        log_file_entry.pack(padx=10, pady=2)
        def browse_log_file():
            file = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log"), ("All Files", "*.*")])
            if file:
                log_file_var.set(file)
        ttk.Button(settings_win, text="Browse", command=browse_log_file).pack(padx=10, pady=2)

        # Save/cancel buttons
        btn_frame = ttk.Frame(settings_win)
        btn_frame.pack(pady=15)
        def save_and_close():
            self.settings["default_folder"] = default_folder_var.get()
            self.settings["file_type_filters"] = file_type_var.get()
            self.settings["theme"] = theme_var.get()
            self.settings["log_file_location"] = log_file_var.get()
            self.save_settings()
            # Apply settings immediately
            self.folder_var.set(self.settings["default_folder"])
            self.file_type_filters = self.settings["file_type_filters"]
            self.log_file_location = self.settings["log_file_location"]
            # Theme switching (simple)
            if self.settings["theme"] == "light":
                self.root.configure(bg="#f0f0f0")
            else:
                self.root.configure(bg="#1e1e1e")
            settings_win.destroy()
        ttk.Button(btn_frame, text="Save", command=save_and_close).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=settings_win.destroy).pack(side=tk.LEFT, padx=10)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
File Organizer Pro - Help

Keyboard Shortcuts:
- Ctrl+O: Browse for folder
- Ctrl+S: Scan folder
- Ctrl+R: Start organization
- Escape: Stop organization
- F1 or Ctrl+H: Show this help

Features:
- Drag & drop folders onto the window
- Preview mode (dry run) to test before organizing
- Custom category creation
- Real-time progress tracking
- Activity logging

Usage:
1. Select a folder to organize
2. Click 'Scan' to preview file categories
3. Enable 'Dry Run' to preview changes
4. Click 'Organize Files' to start
5. Check the log for detailed information
        """
        messagebox.showinfo("Help", help_text)
    
    def log_message(self, message):
        """Add a message to the log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        # Only update GUI from main thread
        if threading.current_thread() is threading.main_thread():
            self.root.update_idletasks()
    
    def load_config(self):
        """Load configuration"""
        try:
            if os.path.exists("organizer_config.json"):
                with open("organizer_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.custom_categories = config.get("custom_categories", {})
        except Exception as e:
            self.log_message(f"Error loading config: {str(e)}")

# CustomCategoriesDialog class removed - using simple input dialogs instead

def main():
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
