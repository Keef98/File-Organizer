#!/usr/bin/env python3
"""
GUI Installer for File Organizer Pro
Provides a user-friendly graphical interface for installation
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import sys
from pathlib import Path

class FileOrganizerInstaller:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """Configure the installer window"""
        self.root.title("File Organizer Pro - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2d2d2d")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
    def setup_ui(self):
        """Create the installer interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2d2d2d", height=100)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🗂️ File Organizer Pro", 
                              font=("Segoe UI", 24, "bold"), 
                              fg="#0078d4", bg="#2d2d2d")
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(header_frame, text="Professional File Organization Tool", 
                                font=("Segoe UI", 12), 
                                fg="#ffffff", bg="#2d2d2d")
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg="#2d2d2d")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Installation path
        path_frame = tk.Frame(content_frame, bg="#2d2d2d")
        path_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(path_frame, text="Installation Path:", 
                font=("Segoe UI", 12, "bold"), 
                fg="#ffffff", bg="#2d2d2d").pack(anchor="w")
        
        path_input_frame = tk.Frame(path_frame, bg="#2d2d2d")
        path_input_frame.pack(fill="x", pady=(5, 0))
        
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "FileOrganizerPro"))
        self.path_entry = tk.Entry(path_input_frame, textvariable=self.path_var, 
                                 font=("Consolas", 10), width=50,
                                 bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(path_input_frame, text="Browse", 
                             command=self.browse_path,
                             font=("Segoe UI", 9, "bold"),
                             bg="#0078d4", fg="#ffffff",
                             relief="flat", padx=15, pady=5)
        browse_btn.pack(side="right")
        
        # Installation options
        options_frame = tk.LabelFrame(content_frame, text="Installation Options", 
                                    font=("Segoe UI", 12, "bold"),
                                    fg="#ffffff", bg="#2d2d2d", relief="flat", bd=1)
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.create_desktop_var = tk.BooleanVar(value=True)
        self.create_startmenu_var = tk.BooleanVar(value=True)
        self.launch_after_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(options_frame, text="Create Desktop Shortcut", 
                      variable=self.create_desktop_var,
                      font=("Segoe UI", 10), fg="#ffffff", bg="#2d2d2d",
                      selectcolor="#0078d4", activebackground="#2d2d2d").pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(options_frame, text="Create Start Menu Shortcut", 
                      variable=self.create_startmenu_var,
                      font=("Segoe UI", 10), fg="#ffffff", bg="#2d2d2d",
                      selectcolor="#0078d4", activebackground="#2d2d2d").pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(options_frame, text="Launch after installation", 
                      variable=self.launch_after_var,
                      font=("Segoe UI", 10), fg="#ffffff", bg="#2d2d2d",
                      selectcolor="#0078d4", activebackground="#2d2d2d").pack(anchor="w", padx=10, pady=5)
        
        # Features list
        features_frame = tk.LabelFrame(content_frame, text="Features", 
                                     font=("Segoe UI", 12, "bold"),
                                     fg="#ffffff", bg="#2d2d2d", relief="flat", bd=1)
        features_frame.pack(fill="x", pady=(0, 20))
        
        features_text = """• Modern dark theme interface
• Automatic file organization by type
• Custom category creation
• Preview mode (test before organizing)
• Real-time progress tracking
• Settings export/import
• Keyboard shortcuts
• Cross-platform compatibility"""
        
        tk.Label(features_frame, text=features_text, 
                font=("Segoe UI", 9), fg="#cccccc", bg="#2d2d2d",
                justify="left").pack(anchor="w", padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg="#2d2d2d")
        button_frame.pack(fill="x", pady=20)
        
        install_btn = tk.Button(button_frame, text="Install File Organizer Pro", 
                              command=self.install,
                              font=("Segoe UI", 12, "bold"),
                              bg="#107c10", fg="#ffffff",
                              relief="flat", padx=20, pady=10)
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                             command=self.cancel,
                             font=("Segoe UI", 12, "bold"),
                             bg="#d13438", fg="#ffffff",
                             relief="flat", padx=20, pady=10)
        # Use grid for centering
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        install_btn.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        cancel_btn.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        
        # Progress bar (hidden initially)
        self.progress = ttk.Progressbar(content_frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.pack_forget()
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to install")
        self.status_label = tk.Label(content_frame, textvariable=self.status_var,
                                   font=("Segoe UI", 10), fg="#cccccc", bg="#2d2d2d")
        self.status_label.pack()
        
    def browse_path(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Select installation directory")
        if folder:
            self.path_var.set(folder)
    
    def install(self):
        """Perform the installation"""
        install_path = self.path_var.get().strip()
        
        if not install_path:
            messagebox.showerror("Error", "Please select an installation path")
            return
        
        try:
            # Show progress
            self.progress.pack(fill="x", pady=(0, 10))
            self.progress.start()
            self.status_var.set("Installing...")
            self.root.update()
            
            # Create installation directory
            install_dir = Path(install_path)
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            files_to_copy = [
                "FileOrganizerPro.exe",
                "config.json", 
                "README.md",
                "MODERN_FEATURES.md",
                "Run_FileOrganizer.bat"
            ]
            
            for file in files_to_copy:
                if os.path.exists(file):
                    shutil.copy2(file, install_dir / file)
            
            # Create shortcuts
            if self.create_desktop_var.get():
                self.create_shortcut(install_dir, "desktop")
            
            if self.create_startmenu_var.get():
                self.create_shortcut(install_dir, "startmenu")
            
            # Stop progress
            self.progress.stop()
            self.progress.pack_forget()
            
            # Success message
            self.status_var.set("Installation completed successfully!")
            
            result = messagebox.askyesno("Installation Complete", 
                                       f"File Organizer Pro has been installed to:\n{install_path}\n\n"
                                       f"Would you like to launch it now?")
            
            if result and self.launch_after_var.get():
                exe_path = install_dir / "FileOrganizerPro.exe"
                if exe_path.exists():
                    os.startfile(str(exe_path))
            
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            self.progress.pack_forget()
            self.status_var.set("Installation failed")
            messagebox.showerror("Installation Error", f"Failed to install: {str(e)}")
    
    def create_shortcut(self, install_dir, shortcut_type):
        """Create desktop or start menu shortcut"""
        try:
            if shortcut_type == "desktop":
                shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "File Organizer Pro.lnk")
            else:  # startmenu
                start_menu = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
                os.makedirs(start_menu, exist_ok=True)
                shortcut_path = os.path.join(start_menu, "File Organizer Pro.lnk")
            
            # Create VBS script for shortcut
            vbs_script = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{install_dir}\\FileOrganizerPro.exe"
oLink.WorkingDirectory = "{install_dir}"
oLink.Description = "File Organizer Pro - Professional File Organization Tool"
oLink.IconLocation = "{install_dir}\\FileOrganizerPro.exe,0"
oLink.Save'''
            
            with open("create_shortcut.vbs", "w") as f:
                f.write(vbs_script)
            
            os.system("cscript create_shortcut.vbs >nul 2>&1")
            os.remove("create_shortcut.vbs")
            
        except Exception as e:
            print(f"Warning: Could not create {shortcut_type} shortcut: {e}")
    
    def cancel(self):
        """Cancel installation"""
        self.root.quit()

def main():
    """Launch the installer"""
    root = tk.Tk()
    app = FileOrganizerInstaller(root)
    root.mainloop()

if __name__ == "__main__":
    main()
