#!/usr/bin/env python3
"""
Ghanaian Pharmacy POS System
Main Application Entry Point
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
import sys

# Import our modules
from database import DatabaseManager
from pos_screen import POSScreen
from inventory_screen import InventoryScreen
from sales_history_screen import SalesHistoryScreen
from reports_screen import ReportsScreen
from settings_screen import SettingsScreen
from utils import create_backup, restore_backup

class PharmacyPOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ghanaian Pharmacy POS System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Set window icon and make it resizable
        self.root.resizable(True, True)
        self.root.minsize(1200, 800)
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_database()
        
        # Current user (default to admin)
        self.current_user = "Admin"
        
        # Setup UI
        self.setup_ui()
        
        # Show main POS screen by default
        self.show_pos_screen()
        
    def setup_ui(self):
        """Setup the main application UI with navigation"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Pharmacy name and title
        title_label = tk.Label(header_frame, text="GHANA PHARMACY POS SYSTEM", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Current time
        self.time_label = tk.Label(header_frame, text="", font=('Arial', 12), 
                                  fg='white', bg='#2c3e50')
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=20)
        self.update_time()
        
        # Navigation frame
        nav_frame = tk.Frame(main_frame, bg='#34495e', height=60)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("POS Sales", self.show_pos_screen, '#27ae60'),
            ("Inventory", self.show_inventory_screen, '#3498db'),
            ("Sales History", self.show_sales_history_screen, '#f39c12'),
            ("Reports", self.show_reports_screen, '#9b59b6'),
            ("Settings", self.show_settings_screen, '#e74c3c'),
            ("Backup", self.backup_data, '#95a5a6'),
            ("Exit", self.exit_application, '#c0392b')
        ]
        
        for text, command, color in nav_buttons:
            btn = tk.Button(nav_frame, text=text, command=command, 
                           font=('Arial', 12, 'bold'), bg=color, fg='white',
                           relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.lighten_color(color)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Main content area
        self.content_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg='#34495e', height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", font=('Arial', 10), 
                                    fg='white', bg='#34495e')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # User info
        user_label = tk.Label(status_frame, text=f"User: {self.current_user}", 
                             font=('Arial', 10), fg='white', bg='#34495e')
        user_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening - in production you'd want a proper color library
        return color
    
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def clear_content(self):
        """Clear the main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_pos_screen(self):
        """Show the POS sales screen"""
        self.clear_content()
        self.status_label.config(text="POS Sales Screen")
        POSScreen(self.content_frame, self.db, self.update_status)
    
    def show_inventory_screen(self):
        """Show the inventory management screen"""
        self.clear_content()
        self.status_label.config(text="Inventory Management")
        InventoryScreen(self.content_frame, self.db, self.update_status)
    
    def show_sales_history_screen(self):
        """Show the sales history screen"""
        self.clear_content()
        self.status_label.config(text="Sales History")
        SalesHistoryScreen(self.content_frame, self.db, self.update_status)
    
    def show_reports_screen(self):
        """Show the reports screen"""
        self.clear_content()
        self.status_label.config(text="Reports Dashboard")
        ReportsScreen(self.content_frame, self.db, self.update_status)
    
    def show_settings_screen(self):
        """Show the settings screen"""
        self.clear_content()
        self.status_label.config(text="System Settings")
        SettingsScreen(self.content_frame, self.db, self.update_status)
    
    def backup_data(self):
        """Create a backup of the database"""
        try:
            backup_path = create_backup()
            messagebox.showinfo("Backup", f"Database backup created successfully!\nLocation: {backup_path}")
            self.update_status("Backup completed successfully")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
            self.update_status("Backup failed")
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
    
    def exit_application(self):
        """Exit the application with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.db.close()
            self.root.quit()
            sys.exit()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PharmacyPOS()
    app.run() 