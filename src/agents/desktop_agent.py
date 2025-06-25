#!/usr/bin/env python3
"""
DesktopAgent – generates simple standalone desktop app scaffolds.
Current MVP: writes a minimal Tkinter "Hello" window or CLI script and marks task complete.
Future: integrate PyInstaller to build executables.
"""

import asyncio
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional

from .base_agent import BaseAgent, Task, TaskStatus


HELLO_APP_TEMPLATE = """
import tkinter as tk

root = tk.Tk()
root.title("{title}")
root.geometry("300x120")

tk.Label(root, text="{message}", font=("Arial", 14)).pack(expand=True)

root.mainloop()
"""

CLI_APP_TEMPLATE = """
#! /usr/bin/env python3
print("{message}")
"""

CALCULATOR_APP_TEMPLATE = """
import tkinter as tk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("{title}")
        self.geometry("320x420")

        self.expression = ""

        self.entry_text = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.entry_text, font=("Arial", 20), bd=8, relief=tk.RIDGE, justify='right')
        entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=15, padx=10, pady=10)

        buttons = [
            ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
            ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
            ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
            ('0',4,0), ('.',4,1), ('=',4,2), ('+',4,3),
            ('C',5,0)
        ]

        for (text,row,col) in buttons:
            btn = tk.Button(self, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text:self.on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error"
        else:
            self.expression += str(char)
        self.entry_text.set(self.expression)


if __name__ == "__main__":
    Calculator().mainloop()
"""

class DesktopAgent(BaseAgent):
    """Simple agent that scaffolds desktop applications."""

    def get_capabilities(self):
        return ["desktop_application"]

    async def execute_task(self, task: Task) -> Optional[Dict]:
        """Create simple desktop app scaffold based on task description/metadata"""
        # Extract info from metadata or fallback
        app_name = task.metadata.get("app_name") if task.metadata else None
        if not app_name:
            # derive from description
            app_name = task.description.replace(" ", "_")[:30] or "desktop_app"
        app_dir = self.workspace_path / "workspace" / app_name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Decide template type
        template_type = (task.metadata.get("template") if task.metadata else None) or "auto"

        description_lower = task.description.lower()

        if template_type == "cli":
            file_path = app_dir / "main.py"
            file_path.write_text(CLI_APP_TEMPLATE.format(message="Hello from ULTIMA!"))

        elif template_type == "calculator" or "calculator" in description_lower:
            file_path = app_dir / "calculator.py"
            title = task.metadata.get("title", "Calculator") if task.metadata else "Calculator"
            file_path.write_text(CALCULATOR_APP_TEMPLATE.format(title=title))

        else:  # default GUI hello template
            file_path = app_dir / "app.py"
            title = task.metadata.get("title", app_name) if task.metadata else app_name
            file_path.write_text(HELLO_APP_TEMPLATE.format(title=title, message="Hello from ULTIMA!"))

        # Build standalone executable if possible (requires pyinstaller)
        executable_path = None
        if template_type != "cli":  # only package GUI apps for now
            pyinstaller = shutil.which("pyinstaller")
            if not pyinstaller:
                self.logger.info("PyInstaller not found, attempting installation via pip...")
                try:
                    # Retry with --break-system-packages flag for PEP 668 systems
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "--quiet", "pyinstaller"])
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"PyInstaller installation failed: {e}")
                pyinstaller = shutil.which("pyinstaller")

            if pyinstaller:
                try:
                    # Use --onefile and place dist inside app_dir/dist
                    cmd = [pyinstaller, "--onefile", "--noconsole", "--distpath", str(app_dir / "dist"), "--workpath", str(app_dir / "build"), "--specpath", str(app_dir), str(file_path.name)]
                    subprocess.run(cmd, cwd=app_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    candidate = app_dir / "dist" / file_path.stem
                    if candidate.exists():
                        executable_path = candidate
                except subprocess.CalledProcessError:
                    self.logger.error("PyInstaller packaging failed")
            else:
                self.logger.error("PyInstaller could not be installed; skipping executable packaging")

        # async sleep to simulate processing time
        await asyncio.sleep(0.5)

        result = {
            "app_path": str(app_dir),
            "entry_file": str(file_path)
        }
        if executable_path:
            result["executable"] = str(executable_path)

        return result 