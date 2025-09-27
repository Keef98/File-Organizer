#!/usr/bin/env python3
"""
GUI Installer for File Organizer Pro
Provides a graphical interface for choosing installation options
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import sys
from pathlib import Path

class InstallerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.setup_ui()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("File Organizer Pro - Installer")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        self.root.configure(bg="#1e1e1e")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
    def setup_styles(self):
        """Setup modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Card.TFrame', background='#2d2d2d', relief='raised', borderwidth=1)
        style.configure('Title.TLabel', background='#2d2d2d', foreground='#ffffff', font=('Segoe UI', 18, 'bold'))
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
        
    def setup_variables(self):
        """Setup tkinter variables"""
        self.install_path_var = tk.StringVar(value="D:/Programs")
        self.create_desktop_shortcut_var = tk.BooleanVar(value=True)
        self.create_start_menu_var = tk.BooleanVar(value=True)
        self.launch_after_install_var = tk.BooleanVar(value=True)
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Card.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Icon and title
        title_frame = ttk.Frame(header_frame)
        title_frame.pack()
        
        # Simple icon using text
        icon_label = ttk.Label(title_frame, text="📁", font=('Segoe UI', 48))
        icon_label.pack()
        
        title_label = ttk.Label(title_frame, text="File Organizer Pro", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Professional File Organization Tool", style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Installation Path section
        path_card = ttk.LabelFrame(main_frame, text="Installation Path", style='Card.TFrame', padding=15)
        path_card.pack(fill=tk.X, pady=(0, 20))
        
        path_frame = ttk.Frame(path_card)
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="Choose where to install File Organizer Pro:", style='Info.TLabel').pack(anchor=tk.W)
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.install_path_var, style='Modern.TEntry', font=('Segoe UI', 10))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(path_input_frame, text="Browse", command=self.browse_path, style='Primary.TButton').pack(side=tk.RIGHT)
        
        # Installation Options section
        options_card = ttk.LabelFrame(main_frame, text="Installation Options", style='Card.TFrame', padding=15)
        options_card.pack(fill=tk.X, pady=(0, 20))
        
        options_frame = ttk.Frame(options_card)
        options_frame.pack(fill=tk.X)
        
        ttk.Checkbutton(options_frame, text="Create Desktop Shortcut", variable=self.create_desktop_shortcut_var, style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Create Start Menu Shortcut", variable=self.create_start_menu_var, style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Launch after installation", variable=self.launch_after_install_var, style='Info.TLabel').pack(anchor=tk.W, pady=2)
        
        # Features section
        features_card = ttk.LabelFrame(main_frame, text="Features", style='Card.TFrame', padding=15)
        features_card.pack(fill=tk.X, pady=(0, 30))
        
        features_frame = ttk.Frame(features_card)
        features_frame.pack(fill=tk.X)
        
        features_text = """• Preview mode (test before organizing)
• Real-time progress tracking
• Custom category creation
• Drag & drop support
• Keyboard shortcuts
• Modern dark theme
• Activity logging"""
        
        ttk.Label(features_frame, text=features_text, style='Info.TLabel', justify=tk.LEFT).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel_install, style='Danger.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Install", command=self.start_install, style='Success.TButton').pack(side=tk.RIGHT)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to install", style='Info.TLabel')
        self.status_label.pack(pady=(20, 0))
        
    def browse_path(self):
        """Open folder selection dialog for installation path"""
        folder = filedialog.askdirectory(title="Select installation directory")
        if folder:
            self.install_path_var.set(folder)
    
    def cancel_install(self):
        """Cancel installation and close installer"""
        if messagebox.askyesno("Cancel Installation", "Are you sure you want to cancel the installation?"):
            self.root.destroy()
    
    def start_install(self):
        """Start the installation process"""
        install_path = self.install_path_var.get().strip()
        
        if not install_path:
            messagebox.showerror("Error", "Please select an installation path.")
            return
        
        # Validate path
        try:
            Path(install_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create installation directory:\n{str(e)}")
            return
        
        # Check if executable exists
        exe_path = Path("FileOrganizerPro.exe")
        if not exe_path.exists():
            messagebox.showerror("Error", "FileOrganizerPro.exe not found in current directory.")
            return
        
        # Start installation in a separate thread
        import threading
        thread = threading.Thread(target=self.install_worker, daemon=True)
        thread.start()
    
    def install_worker(self):
        """Worker thread for installation"""
        try:
            install_path = Path(self.install_path_var.get())
            
            # Update status
            self.status_label.config(text="Installing files...")
            self.root.update_idletasks()
            
            # Create installation directory
            install_path.mkdir(parents=True, exist_ok=True)
            
            # Copy executable
            exe_path = Path("FileOrganizerPro.exe")
            dest_exe = install_path / "FileOrganizerPro.exe"
            shutil.copy2(exe_path, dest_exe)
            
            # Copy additional files if they exist
            files_to_copy = ["README.txt", "icon.ico"]
            for file_name in files_to_copy:
                if os.path.exists(file_name):
                    shutil.copy2(file_name, install_path / file_name)
            
            # Create shortcuts
            if self.create_desktop_shortcut_var.get():
                self.create_desktop_shortcut(install_path)
            
            if self.create_start_menu_var.get():
                self.create_start_menu_shortcut(install_path)
            
            # Update status
            self.status_label.config(text="Installation complete!")
            self.root.update_idletasks()
            
            # Show success message
            messagebox.showinfo("Installation Complete", 
                              f"File Organizer Pro has been successfully installed to:\n{install_path}\n\n"
                              f"You can now run the application from the installed location.")
            
            # Launch application if requested
            if self.launch_after_install_var.get():
                try:
                    os.startfile(str(dest_exe))
                except Exception as e:
                    messagebox.showwarning("Launch Error", f"Could not launch application:\n{str(e)}")
            
            # Close installer
            self.root.destroy()
            
        except Exception as e:
            self.status_label.config(text="Installation failed!")
            messagebox.showerror("Installation Error", f"Installation failed:\n{str(e)}")
    
    def create_desktop_shortcut(self, install_path):
        """Create desktop shortcut"""
        try:
            desktop_path = Path.home() / "Desktop"
            shortcut_path = desktop_path / "File Organizer Pro.url"
            
            shortcut_content = f"""[InternetShortcut]
URL=file:///{install_path / "FileOrganizerPro.exe"}
IconFile={install_path / "FileOrganizerPro.exe"}
IconIndex=0
"""
            
            with open(shortcut_path, 'w', encoding='utf-8') as f:
                f.write(shortcut_content)
                
        except Exception as e:
            print(f"Warning: Could not create desktop shortcut: {e}")
    
    def create_start_menu_shortcut(self, install_path):
        """Create start menu shortcut"""
        try:
            start_menu_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            start_menu_path.mkdir(parents=True, exist_ok=True)
            
            shortcut_path = start_menu_path / "File Organizer Pro.url"
            
            shortcut_content = f"""[InternetShortcut]
URL=file:///{install_path / "FileOrganizerPro.exe"}
IconFile={install_path / "FileOrganizerPro.exe"}
IconIndex=0
"""
            
            with open(shortcut_path, 'w', encoding='utf-8') as f:
                f.write(shortcut_content)
                
        except Exception as e:
            print(f"Warning: Could not create start menu shortcut: {e}")

def main():
    """Main function"""
    root = tk.Tk()
    app = InstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
