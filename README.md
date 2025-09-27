
# File-Organizer
A Python tool with **CLI + GUI modes** to automatically organize messy folders into neat categories.   Perfect for **Downloads** or **Desktop** cleanup.
=======

# File Organizer Pro

<p align="center">
	<img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-blue" alt="Platform">
	<img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python Version">
	<img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

> **A robust, professional, and modern file organization tool with a beautiful GUI and advanced settings.**

---

## � Introduction

**File Organizer Pro** is designed to help you keep your files and folders organized with minimal effort. Whether you have a cluttered Downloads folder, a massive collection of images, or just want to automate your file management, this tool provides a user-friendly, powerful, and customizable solution.

---

## 🖼️ Visual Overview

<details>
<summary>Click to expand: Screenshots & Workflow</summary>

![Main Window](https://user-images.githubusercontent.com/yourusername/file-organizer-main.png)
![Settings Dialog](https://user-images.githubusercontent.com/yourusername/file-organizer-settings.png)

1. **Select a folder** to organize (default is Desktop)
2. **Scan** to preview how files will be categorized
3. **Organize** to move files into folders by type or custom rules
4. **Review logs and statistics** for transparency and control

</details>

---

## �🚀 Features

- 🗂️ **Smart file categorization**: Automatically sorts files by type (images, videos, documents, etc.)
- 🎯 **Custom category creation**: Define your own rules for file organization
- 👀 **Preview mode (dry run)**: See what will happen before making changes
- ⌨️ **Keyboard shortcuts**: For power users and efficiency
- 🖱️ **Drag & drop support**: Quickly add folders to organize
- 📊 **Real-time statistics**: See counts and categories instantly
- 📝 **Activity logging**: Track every action for peace of mind
- 🎨 **Modern dark & light themes**: Choose your preferred look
- ⚙️ **Settings**: Control default folder, file type filters, theme, and log file location

---

## ⚙️ Settings Explained

Open the **Settings** dialog (⚙️) to customize your experience:

- **Default Folder**: The folder shown by default when the app starts. Set to your Desktop or any frequently used directory.
- **File Type Filters**: Only organize files matching these patterns (e.g. `*.jpg;*.png;*.mp4`). Separate multiple types with semicolons.
- **Theme**: Switch between dark and light modes for comfort.
- **Log File Location**: Choose where activity logs are saved for review or troubleshooting.

Example `settings.json`:

```json
{
	"default_folder": "C:/Users/YourName/Desktop",
	"file_type_filters": "*.jpg;*.png;*.mp4",
	"theme": "dark",
	"log_file_location": "file_organizer.log"
}
```

---

## 📦 Installation

### Option 1: Standalone Executable (Recommended)

```bash
python build_executable.py
# Then navigate to FileOrganizerPro_Distribution/
python install_gui.py
# Or run Install.bat for command-line installation
```

### Option 2: Python Installation

```bash
pip install -r requirements.txt
python organizer_gui.py
```

---

## 🖥️ Usage Guide

1. **Run the application**
2. **Select a folder to organize** (default is Desktop, can be changed in Settings)
3. **Click 'Scan'** to preview categories and see what will be organized
4. **Enable 'Dry Run'** to test changes without moving files
5. **Click 'Organize Files'** to start organizing
6. **Review the log and statistics** for details on what was moved and where
7. **Customize via ⚙️ Settings** for a tailored experience

---

## ⌨️ Keyboard Shortcuts

| Shortcut   | Action                |
|------------|-----------------------|
| Ctrl+O     | Browse for folder     |
| Ctrl+S     | Scan folder           |
| Ctrl+R     | Start organization    |
| Escape     | Stop organization     |
| F1         | Show help             |

---

## 📝 Best Practices & Tips

- **Always use Dry Run first** to preview changes, especially on important folders.
- **Backup important data** before organizing large or critical directories.
- **Use custom categories** to fine-tune how your files are sorted.
- **Check the log file** for a record of all actions and for troubleshooting.
- **Update your file type filters** to focus on specific file types as needed.

---

## 🛠️ Troubleshooting & FAQ

**Q: The app doesn't start or crashes.**
A: Make sure you have Python 3.7+ installed and all dependencies from `requirements.txt`.

**Q: Files aren't being moved.**
A: Ensure 'Dry Run' is disabled. Check your file type filters and permissions.

**Q: How do I reset my settings?**
A: Delete or edit `settings.json` in the app directory.

**Q: Can I undo an organization?**
A: Use the log file to see what was moved and manually restore if needed. Undo functionality is planned for future releases.

**Q: How do I add new file types or categories?**
A: Use the custom categories feature in the app or edit your settings.

---

## 🛠️ Requirements

- Windows 7 or later (for executable)
- Python 3.7+ (for Python version)
- No additional software required for executable

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📖 Support & Documentation

For issues or questions, please check the documentation or [open an issue](https://github.com/yourusername/File-Organizer-Pro/issues).

---

<p align="center">
	<sub>© 2025 File Organizer Pro. All rights reserved.</sub>
</p>

