import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser  # To open the folder containing the .exe file

# Global output directory for the EXE file
output_dir = os.path.expanduser("~/output")  # Output directory is now user agnostic and works across platforms

# Check if PyInstaller is available (assumed to be pre-installed)
def check_pyinstaller_installed():
    try:
        __import__("PyInstaller")
    except ImportError:
        messagebox.showerror("Error", "PyInstaller is not installed. Please install it manually: pip install pyinstaller.")
        sys.exit(1)

# Ensure PyInstaller is installed
check_pyinstaller_installed()

# Function to run PyInstaller to create the .exe
def convert_to_exe(script_path, icon_path, app_name):
    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"The script file '{script_path}' does not exist.")
        return
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define PyInstaller command
    if not icon_path or not os.path.exists(icon_path):
        # No icon provided: Use default icon, and avoid --icon flag
        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",     # Bundle everything into one .exe file
            "--windowed",    # Prevent console window from opening (for GUI apps)
            "--optimize=1",  # Apply optimization
            "--strip",       # Strip the executable to reduce size
            f"--name={app_name if app_name else 'App'}",  # Set app name, default to 'App'
            f"--distpath={output_dir}",  # Set output directory
            script_path      # Path to the script being packaged
        ]
    else:
        # Icon provided, use the --icon flag
        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--windowed",
            "--optimize=1",
            "--strip",
            f"--icon={icon_path}",
            f"--name={app_name if app_name else 'App'}",
            f"--distpath={output_dir}",
            script_path
        ]
    
    # Enable logging for debugging if needed
    command.extend(["--log-level=DEBUG"])

    # Run the PyInstaller command and capture any errors
    try:
        print("Running PyInstaller...")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.showinfo("Success", "Executable created successfully!")
        print("PyInstaller output:\n", result.stdout.decode())
        open_location_button.config(state=tk.NORMAL)  # Enable the "Open File Location" button
    except subprocess.CalledProcessError as e:
        error_message = f"Error occurred during PyInstaller execution: {e.stderr.decode()}"
        print(error_message)
        messagebox.showerror("Error", error_message)

# Function to open the folder containing the generated executable
def open_file_location():
    if os.path.exists(output_dir):
        webbrowser.open(output_dir)  # Open the folder in the file explorer
    else:
        messagebox.showerror("Error", "Output folder does not exist.")

# Function to select a Python script
def select_script():
    script_path = filedialog.askopenfilename(title="Select Python Script", filetypes=[("Python Files", "*.py")])
    if script_path:
        script_entry.delete(0, tk.END)
        script_entry.insert(0, script_path)

# Function to select an icon file
def select_icon():
    icon_path = filedialog.askopenfilename(title="Select Icon File", filetypes=[("Icon Files", "*.ico")])
    if icon_path:
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, icon_path)

# Function to trigger the conversion when "Convert" button is clicked
def on_convert():
    script_path = script_entry.get().strip()
    icon_path = icon_entry.get().strip() if icon_entry.get().strip() else None  # Use None for default icon
    app_name = app_name_entry.get().strip()

    convert_to_exe(script_path, icon_path, app_name)

# Create the main Tkinter window
root = tk.Tk()
root.title("CounTrol - Python to EXE Converter")
root.geometry("500x400")
root.configure(bg="white")

# Custom styling
label_style = {'bg': 'white', 'fg': 'black', 'font': ('Arial', 12)}
entry_style = {'bg': '#f0f0f0', 'fg': 'black', 'insertbackground': 'black', 'highlightbackground': '#888888', 'bd': 2}
button_style = {'bg': 'black', 'fg': 'white', 'activebackground': '#333333', 'font': ('Arial', 10, 'bold')}

# Script selection
tk.Label(root, text="Select Python Script:", **label_style).pack(pady=10)
script_frame = tk.Frame(root, bg="white")
script_frame.pack(pady=5)
script_entry = tk.Entry(script_frame, width=40, **entry_style)
script_entry.pack(side=tk.LEFT, padx=5)
script_button = tk.Button(script_frame, text="Browse", command=select_script, **button_style)
script_button.pack(side=tk.LEFT)

# Icon selection
tk.Label(root, text="Select Icon (.ico) File (Optional):", **label_style).pack(pady=10)
icon_frame = tk.Frame(root, bg="white")
icon_frame.pack(pady=5)
icon_entry = tk.Entry(icon_frame, width=40, **entry_style)
icon_entry.pack(side=tk.LEFT, padx=5)
icon_button = tk.Button(icon_frame, text="Browse", command=select_icon, **button_style)
icon_button.pack(side=tk.LEFT)

# App name input
tk.Label(root, text="Enter App Name (Optional):", **label_style).pack(pady=10)
app_name_entry = tk.Entry(root, width=45, **entry_style)
app_name_entry.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert to EXE", command=on_convert, **button_style)
convert_button.pack(pady=20)

# Open File Location button (disabled by default)
open_location_button = tk.Button(root, text="Open File Location", command=open_file_location, **button_style)
open_location_button.pack(pady=10)
open_location_button.config(state=tk.DISABLED)  # Disabled by default, will be enabled after successful EXE creation

# Start the Tkinter main loop
root.mainloop()
