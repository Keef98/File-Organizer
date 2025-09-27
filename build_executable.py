#!/usr/bin/env python3
"""
Build script for File Organizer Pro
Creates standalone executable and distribution package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("[OK] PyInstaller is already installed")
        return True
    except ImportError:
        print("[INFO] Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[OK] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install PyInstaller: {e}")
            return False

def create_icon():
    """Create a simple icon file"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a folder icon
        draw.rectangle([8, 16, 56, 56], fill=(33, 150, 243, 255), outline=(25, 118, 210, 255), width=2)
        draw.rectangle([12, 12, 52, 20], fill=(33, 150, 243, 255), outline=(25, 118, 210, 255), width=2)
        
        # Draw a document
        draw.rectangle([20, 24, 44, 48], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=1)
        draw.line([(24, 28), (40, 28)], fill=(100, 100, 100, 255), width=1)
        draw.line([(24, 32), (36, 32)], fill=(100, 100, 100, 255), width=1)
        draw.line([(24, 36), (38, 36)], fill=(100, 100, 100, 255), width=1)
        
        img.save('icon.ico', format='ICO')
        print("[OK] Created icon.ico")
        return True
    except ImportError:
        print("[WARNING] PIL not available, creating simple icon file")
        # Create a simple text file as placeholder
        with open('icon.ico', 'w') as f:
            f.write('placeholder')
        return True
    except Exception as e:
        print(f"[WARNING] Could not create icon: {e}")
        return False

def build_executable():
    """Build the standalone executable"""
    print("[INFO] Building standalone executable...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=FileOrganizerPro",
        "--add-data=organizer.py;.",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=os",
        "--hidden-import=shutil",
        "--hidden-import=pathlib",
        "organizer_gui.py"
    ]
    
    # Add icon if available
    if os.path.exists('icon.ico'):
        cmd.extend(["--icon=icon.ico"])
    
    try:
        subprocess.check_call(cmd)
        print("[OK] Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build executable: {e}")
        return False

def create_distribution():
    """Create distribution package"""
    print("[INFO] Creating distribution package...")
    
    dist_dir = Path("FileOrganizerPro_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy executable
    exe_path = Path("dist/FileOrganizerPro.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "FileOrganizerPro.exe")
        print("[OK] Copied executable")
    else:
        print("[ERROR] Executable not found")
        return False
    
    # Copy icon
    if os.path.exists('icon.ico'):
        shutil.copy2('icon.ico', dist_dir / "icon.ico")
    
    # Create README
    readme_content = """# File Organizer Pro

A modern, professional file organization tool with a beautiful GUI.

## Features
- 🗂️ Smart file categorization
- 🎯 Custom category creation
- 👀 Preview mode (dry run)
- ⌨️ Keyboard shortcuts
- 🖱️ Drag & drop support
- 📊 Real-time statistics
- 📝 Activity logging
- 🎨 Modern dark theme

## Usage
1. Run `FileOrganizerPro.exe`
2. Select a folder to organize
3. Click 'Scan' to preview categories
4. Enable 'Dry Run' to test changes
5. Click 'Organize Files' to start

## Keyboard Shortcuts
- Ctrl+O: Browse for folder
- Ctrl+S: Scan folder
- Ctrl+R: Start organization
- Escape: Stop organization
- F1: Show help

## Requirements
- Windows 7 or later
- No additional software required

## Support
For issues or questions, please check the documentation or contact support.

© 2024 File Organizer Pro
"""
    
    with open(dist_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create batch launcher
    launcher_content = """@echo off
title File Organizer Pro
echo Starting File Organizer Pro...
FileOrganizerPro.exe
pause
"""
    
    with open(dist_dir / "Launch.bat", 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Create installation script
    install_script = """@echo off
title File Organizer Pro - Installer
echo.
echo ========================================
echo    File Organizer Pro - Installer
echo ========================================
echo.
echo This will install File Organizer Pro to your system.
echo.
set /p install_path="Enter installation path (default: C:\\Program Files\\FileOrganizerPro): "
if "%install_path%"=="" set install_path=C:\\Program Files\\FileOrganizerPro
echo.
echo Installing to: %install_path%
echo.
mkdir "%install_path%" 2>nul
copy "FileOrganizerPro.exe" "%install_path%\\" >nul
copy "README.txt" "%install_path%\\" >nul
if exist "icon.ico" copy "icon.ico" "%install_path%\\" >nul
echo.
echo Installation complete!
echo.
echo You can now run File Organizer Pro from:
echo %install_path%\\FileOrganizerPro.exe
echo.
echo Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\File Organizer Pro.url"
echo URL=file:///%install_path%\\FileOrganizerPro.exe >> "%USERPROFILE%\\Desktop\\File Organizer Pro.url"
echo IconFile=%install_path%\\FileOrganizerPro.exe >> "%USERPROFILE%\\Desktop\\File Organizer Pro.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\File Organizer Pro.url"
echo.
echo Desktop shortcut created!
echo.
pause
"""
    
    with open(dist_dir / "Install.bat", 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    print("[OK] Distribution package created")
    return True

def main():
    """Main build process"""
    print("=" * 50)
    print("File Organizer Pro - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("organizer_gui.py"):
        print("[ERROR] organizer_gui.py not found. Please run this script from the project directory.")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Create icon
    create_icon()
    
    # Build executable
    if not build_executable():
        return False
    
    # Create distribution
    if not create_distribution():
        return False
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print(f"Distribution package: FileOrganizerPro_Distribution/")
    print(f"Executable: FileOrganizerPro_Distribution/FileOrganizerPro.exe")
    print("\nTo test the installation:")
    print("1. Navigate to FileOrganizerPro_Distribution/")
    print("2. Run Install.bat to install the application")
    print("3. Or run FileOrganizerPro.exe directly")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
