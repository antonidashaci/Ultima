#!/usr/bin/env python3
"""
Python Calculator with GUI
Created by ULTIMA AI Agent
"""

import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ULTIMA Calculator")
        self.root.geometry("300x400")
        
        # Variable to store calculation
        self.equation = tk.StringVar()
        self.equation.set("0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Display
        display = tk.Entry(self.root, textvariable=self.equation, 
                          font=('Arial', 20), justify='right', state='readonly')
        display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='ew')
        
        # Buttons
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for (text, row, col) in buttons:
            if text == '0':
                btn = tk.Button(self.root, text=text, font=('Arial', 16),
                              command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky='ew')
            else:
                btn = tk.Button(self.root, text=text, font=('Arial', 16),
                              command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
        
        # Configure grid weights
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
    
    def button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.equation.get().replace('×', '*').replace('÷', '/')))
                self.equation.set(result)
            except:
                self.equation.set("Error")
        elif char == 'C':
            self.equation.set("0")
        elif char == '±':
            try:
                current = float(self.equation.get())
                self.equation.set(str(-current))
            except:
                pass
        elif char == '%':
            try:
                current = float(self.equation.get())
                self.equation.set(str(current / 100))
            except:
                pass
        else:
            current = self.equation.get()
            if current == "0" or current == "Error":
                self.equation.set(char)
            else:
                self.equation.set(current + char)

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
