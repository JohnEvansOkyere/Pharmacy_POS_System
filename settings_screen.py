"""
Settings Screen for Ghanaian Pharmacy POS System
System configuration and pharmacy settings
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

class SettingsScreen:
    def __init__(self, parent, db, status_callback):
        self.parent = parent
        self.db = db
        self.status_callback = status_callback
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook for different settings categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pharmacy Information tab
        pharmacy_frame = tk.Frame(notebook, bg='white')
        notebook.add(pharmacy_frame, text="Pharmacy Information")
        
        self.setup_pharmacy_tab(pharmacy_frame)
        
        # System Settings tab
        system_frame = tk.Frame(notebook, bg='white')
        notebook.add(system_frame, text="System Settings")
        
        self.setup_system_tab(system_frame)
        
        # Receipt Settings tab
        receipt_frame = tk.Frame(notebook, bg='white')
        notebook.add(receipt_frame, text="Receipt Settings")
        
        self.setup_receipt_tab(receipt_frame)
        
        # Backup & Restore tab
        backup_frame = tk.Frame(notebook, bg='white')
        notebook.add(backup_frame, text="Backup & Restore")
        
        self.setup_backup_tab(backup_frame)
        
        # About tab
        about_frame = tk.Frame(notebook, bg='white')
        notebook.add(about_frame, text="About")
        
        self.setup_about_tab(about_frame)
        
    def setup_pharmacy_tab(self, parent):
        """Setup pharmacy information tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Pharmacy Information", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Form fields
        form_frame = tk.Frame(content_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pharmacy name
        name_label = tk.Label(form_frame, text="Pharmacy Name:", font=('Arial', 12, 'bold'), 
                            bg='white', fg='#2c3e50')
        name_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.pharmacy_name_var = tk.StringVar()
        name_entry = tk.Entry(form_frame, textvariable=self.pharmacy_name_var, 
                            font=('Arial', 12), width=50)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pharmacy address
        address_label = tk.Label(form_frame, text="Address:", font=('Arial', 12, 'bold'), 
                               bg='white', fg='#2c3e50')
        address_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.pharmacy_address_var = tk.StringVar()
        address_entry = tk.Entry(form_frame, textvariable=self.pharmacy_address_var, 
                               font=('Arial', 12), width=50)
        address_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pharmacy phone
        phone_label = tk.Label(form_frame, text="Phone Number:", font=('Arial', 12, 'bold'), 
                             bg='white', fg='#2c3e50')
        phone_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.pharmacy_phone_var = tk.StringVar()
        phone_entry = tk.Entry(form_frame, textvariable=self.pharmacy_phone_var, 
                             font=('Arial', 12), width=30)
        phone_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pharmacy email
        email_label = tk.Label(form_frame, text="Email Address:", font=('Arial', 12, 'bold'), 
                             bg='white', fg='#2c3e50')
        email_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.pharmacy_email_var = tk.StringVar()
        email_entry = tk.Entry(form_frame, textvariable=self.pharmacy_email_var, 
                             font=('Arial', 12), width=40)
        email_entry.pack(fill=tk.X, pady=(0, 15))
        
        # License information
        license_label = tk.Label(form_frame, text="Pharmacy License Number:", font=('Arial', 12, 'bold'), 
                               bg='white', fg='#2c3e50')
        license_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.license_var = tk.StringVar()
        license_entry = tk.Entry(form_frame, textvariable=self.license_var, 
                               font=('Arial', 12), width=30)
        license_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pharmacist information
        pharmacist_label = tk.Label(form_frame, text="Pharmacist Name:", font=('Arial', 12, 'bold'), 
                                  bg='white', fg='#2c3e50')
        pharmacist_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.pharmacist_var = tk.StringVar()
        pharmacist_entry = tk.Entry(form_frame, textvariable=self.pharmacist_var, 
                                  font=('Arial', 12), width=40)
        pharmacist_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Save button
        save_button = tk.Button(form_frame, text="Save Pharmacy Information", 
                              command=self.save_pharmacy_info,
                              font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                              relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        save_button.pack()
        
    def setup_system_tab(self, parent):
        """Setup system settings tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="System Configuration", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Form fields
        form_frame = tk.Frame(content_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Currency
        currency_label = tk.Label(form_frame, text="Currency:", font=('Arial', 12, 'bold'), 
                                bg='white', fg='#2c3e50')
        currency_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.currency_var = tk.StringVar(value="GHS")
        currency_combo = ttk.Combobox(form_frame, textvariable=self.currency_var, 
                                    values=["GHS", "USD", "EUR", "GBP"], 
                                    font=('Arial', 12), state="readonly", width=20)
        currency_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Tax rate
        tax_label = tk.Label(form_frame, text="Tax Rate (%):", font=('Arial', 12, 'bold'), 
                           bg='white', fg='#2c3e50')
        tax_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.tax_rate_var = tk.StringVar(value="0.0")
        tax_entry = tk.Entry(form_frame, textvariable=self.tax_rate_var, 
                           font=('Arial', 12), width=20)
        tax_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Language
        language_label = tk.Label(form_frame, text="Language:", font=('Arial', 12, 'bold'), 
                                bg='white', fg='#2c3e50')
        language_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.language_var = tk.StringVar(value="English")
        language_combo = ttk.Combobox(form_frame, textvariable=self.language_var, 
                                    values=["English", "French", "Arabic"], 
                                    font=('Arial', 12), state="readonly", width=20)
        language_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Date format
        date_format_label = tk.Label(form_frame, text="Date Format:", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        date_format_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.date_format_var = tk.StringVar(value="YYYY-MM-DD")
        date_format_combo = ttk.Combobox(form_frame, textvariable=self.date_format_var, 
                                       values=["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"], 
                                       font=('Arial', 12), state="readonly", width=20)
        date_format_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Auto backup
        self.auto_backup_var = tk.BooleanVar(value=True)
        auto_backup_check = tk.Checkbutton(form_frame, text="Enable Auto Backup", 
                                         variable=self.auto_backup_var,
                                         font=('Arial', 12), bg='white', fg='#2c3e50')
        auto_backup_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Low stock alerts
        self.low_stock_alerts_var = tk.BooleanVar(value=True)
        low_stock_check = tk.Checkbutton(form_frame, text="Enable Low Stock Alerts", 
                                       variable=self.low_stock_alerts_var,
                                       font=('Arial', 12), bg='white', fg='#2c3e50')
        low_stock_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Expiry alerts
        self.expiry_alerts_var = tk.BooleanVar(value=True)
        expiry_check = tk.Checkbutton(form_frame, text="Enable Expiry Alerts", 
                                    variable=self.expiry_alerts_var,
                                    font=('Arial', 12), bg='white', fg='#2c3e50')
        expiry_check.pack(anchor=tk.W, pady=(10, 20))
        
        # Save button
        save_button = tk.Button(form_frame, text="Save System Settings", 
                              command=self.save_system_settings,
                              font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                              relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        save_button.pack()
        
    def setup_receipt_tab(self, parent):
        """Setup receipt settings tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Receipt Configuration", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Form fields
        form_frame = tk.Frame(content_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Receipt header
        header_label = tk.Label(form_frame, text="Receipt Header:", font=('Arial', 12, 'bold'), 
                              bg='white', fg='#2c3e50')
        header_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.receipt_header_var = tk.StringVar()
        header_entry = tk.Entry(form_frame, textvariable=self.receipt_header_var, 
                              font=('Arial', 12), width=50)
        header_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Receipt footer
        footer_label = tk.Label(form_frame, text="Receipt Footer:", font=('Arial', 12, 'bold'), 
                              bg='white', fg='#2c3e50')
        footer_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.receipt_footer_var = tk.StringVar()
        footer_text = tk.Text(form_frame, height=4, font=('Arial', 12), wrap=tk.WORD)
        footer_text.pack(fill=tk.X, pady=(0, 15))
        self.footer_text_widget = footer_text
        
        # Receipt width
        width_label = tk.Label(form_frame, text="Receipt Width (characters):", font=('Arial', 12, 'bold'), 
                             bg='white', fg='#2c3e50')
        width_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.receipt_width_var = tk.StringVar(value="40")
        width_entry = tk.Entry(form_frame, textvariable=self.receipt_width_var, 
                             font=('Arial', 12), width=20)
        width_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Show logo
        self.show_logo_var = tk.BooleanVar(value=False)
        show_logo_check = tk.Checkbutton(form_frame, text="Show Pharmacy Logo on Receipt", 
                                       variable=self.show_logo_var,
                                       font=('Arial', 12), bg='white', fg='#2c3e50')
        show_logo_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Show tax
        self.show_tax_var = tk.BooleanVar(value=True)
        show_tax_check = tk.Checkbutton(form_frame, text="Show Tax on Receipt", 
                                      variable=self.show_tax_var,
                                      font=('Arial', 12), bg='white', fg='#2c3e50')
        show_tax_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Show cashier
        self.show_cashier_var = tk.BooleanVar(value=True)
        show_cashier_check = tk.Checkbutton(form_frame, text="Show Cashier Name on Receipt", 
                                          variable=self.show_cashier_var,
                                          font=('Arial', 12), bg='white', fg='#2c3e50')
        show_cashier_check.pack(anchor=tk.W, pady=(10, 20))
        
        # Preview button
        preview_button = tk.Button(form_frame, text="Preview Receipt", 
                                 command=self.preview_receipt,
                                 font=('Arial', 11), bg='#f39c12', fg='white',
                                 relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_button = tk.Button(form_frame, text="Save Receipt Settings", 
                              command=self.save_receipt_settings,
                              font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white',
                              relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        save_button.pack(side=tk.LEFT)
        
    def setup_backup_tab(self, parent):
        """Setup backup and restore tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Backup & Restore", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Backup section
        backup_frame = tk.LabelFrame(content_frame, text="Create Backup", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        backup_frame.pack(fill=tk.X, pady=(0, 20))
        
        backup_content = tk.Frame(backup_frame, bg='white')
        backup_content.pack(fill=tk.X, padx=10, pady=10)
        
        backup_info = tk.Label(backup_content, 
                             text="Create a backup of your pharmacy data including all sales, inventory, and settings.",
                             font=('Arial', 11), bg='white', fg='#34495e', wraplength=500)
        backup_info.pack(anchor=tk.W, pady=(0, 10))
        
        backup_button = tk.Button(backup_content, text="Create Backup Now", 
                                command=self.create_backup,
                                font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        backup_button.pack()
        
        # Restore section
        restore_frame = tk.LabelFrame(content_frame, text="Restore Backup", font=('Arial', 12, 'bold'), 
                                    bg='white', fg='#2c3e50')
        restore_frame.pack(fill=tk.X, pady=(0, 20))
        
        restore_content = tk.Frame(restore_frame, bg='white')
        restore_content.pack(fill=tk.X, padx=10, pady=10)
        
        restore_info = tk.Label(restore_content, 
                              text="Restore your pharmacy data from a previous backup. This will replace all current data.",
                              font=('Arial', 11), bg='white', fg='#34495e', wraplength=500)
        restore_info.pack(anchor=tk.W, pady=(0, 10))
        
        restore_button = tk.Button(restore_content, text="Restore from Backup", 
                                 command=self.restore_backup,
                                 font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                 relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        restore_button.pack()
        
        # Auto backup settings
        auto_frame = tk.LabelFrame(content_frame, text="Automatic Backup Settings", font=('Arial', 12, 'bold'), 
                                 bg='white', fg='#2c3e50')
        auto_frame.pack(fill=tk.X)
        
        auto_content = tk.Frame(auto_frame, bg='white')
        auto_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Backup frequency
        frequency_label = tk.Label(auto_content, text="Backup Frequency:", font=('Arial', 11, 'bold'), 
                                 bg='white', fg='#2c3e50')
        frequency_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.backup_frequency_var = tk.StringVar(value="Daily")
        frequency_combo = ttk.Combobox(auto_content, textvariable=self.backup_frequency_var, 
                                     values=["Daily", "Weekly", "Monthly"], 
                                     font=('Arial', 11), state="readonly", width=20)
        frequency_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Backup location
        location_label = tk.Label(auto_content, text="Backup Location:", font=('Arial', 11, 'bold'), 
                                bg='white', fg='#2c3e50')
        location_label.pack(anchor=tk.W, pady=(0, 5))
        
        location_frame = tk.Frame(auto_content, bg='white')
        location_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.backup_location_var = tk.StringVar(value="./backups")
        location_entry = tk.Entry(location_frame, textvariable=self.backup_location_var, 
                                font=('Arial', 11), width=40)
        location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(location_frame, text="Browse", command=self.browse_backup_location,
                                font=('Arial', 10), bg='#95a5a6', fg='white',
                                relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        browse_button.pack(side=tk.RIGHT)
        
    def setup_about_tab(self, parent):
        """Setup about tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="About Ghanaian Pharmacy POS System", 
                             font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Version info
        version_frame = tk.Frame(content_frame, bg='white')
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        version_info = [
            ("Version:", "1.0.0"),
            ("Build Date:", datetime.now().strftime("%Y-%m-%d")),
            ("Database Version:", "1.0"),
            ("Python Version:", "3.8+")
        ]
        
        for label, value in version_info:
            info_frame = tk.Frame(version_frame, bg='white')
            info_frame.pack(fill=tk.X, pady=5)
            
            label_widget = tk.Label(info_frame, text=label, font=('Arial', 12, 'bold'), 
                                  bg='white', fg='#2c3e50', width=15, anchor=tk.W)
            label_widget.pack(side=tk.LEFT)
            
            value_widget = tk.Label(info_frame, text=value, font=('Arial', 12), 
                                  bg='white', fg='#34495e')
            value_widget.pack(side=tk.LEFT)
        
        # Description
        desc_frame = tk.LabelFrame(content_frame, text="System Description", font=('Arial', 12, 'bold'), 
                                 bg='white', fg='#2c3e50')
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        desc_text = tk.Text(desc_frame, height=8, font=('Arial', 11), 
                          bg='#f8f9fa', fg='#2c3e50', wrap=tk.WORD)
        desc_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        description = """Ghanaian Pharmacy POS System is a comprehensive point-of-sale solution designed specifically for pharmacy operations in Ghana.

Key Features:
• Complete drug inventory management
• Fast and intuitive sales interface
• Comprehensive reporting and analytics
• Stock alerts and expiry tracking
• Professional receipt generation
• Data backup and restore functionality
• 100% offline operation

This system is designed to help pharmacy staff manage their operations efficiently while maintaining accurate records of all transactions and inventory."""
        
        desc_text.insert(1.0, description)
        desc_text.config(state=tk.DISABLED)
        
        # Contact information
        contact_frame = tk.LabelFrame(content_frame, text="Support Information", font=('Arial', 12, 'bold'), 
                                    bg='white', fg='#2c3e50')
        contact_frame.pack(fill=tk.X)
        
        contact_content = tk.Frame(contact_frame, bg='white')
        contact_content.pack(fill=tk.X, padx=10, pady=10)
        
        contact_info = [
            ("Email:", "support@ghanapharmacypos.com"),
            ("Phone:", "+233 XX XXX XXXX"),
            ("Website:", "www.ghanapharmacypos.com")
        ]
        
        for label, value in contact_info:
            info_frame = tk.Frame(contact_content, bg='white')
            info_frame.pack(fill=tk.X, pady=2)
            
            label_widget = tk.Label(info_frame, text=label, font=('Arial', 11, 'bold'), 
                                  bg='white', fg='#2c3e50', width=10, anchor=tk.W)
            label_widget.pack(side=tk.LEFT)
            
            value_widget = tk.Label(info_frame, text=value, font=('Arial', 11), 
                                  bg='white', fg='#3498db')
            value_widget.pack(side=tk.LEFT)
    
    def load_settings(self):
        """Load current settings from database"""
        settings = self.db.get_settings()
        
        if settings:
            self.pharmacy_name_var.set(settings.get('pharmacy_name', ''))
            self.pharmacy_address_var.set(settings.get('pharmacy_address', ''))
            self.pharmacy_phone_var.set(settings.get('pharmacy_phone', ''))
            self.pharmacy_email_var.set(settings.get('pharmacy_email', ''))
            self.tax_rate_var.set(str(settings.get('tax_rate', 0.0)))
            self.currency_var.set(settings.get('currency', 'GHS'))
            self.receipt_footer_var.set(settings.get('receipt_footer', ''))
            
            # Set footer text
            if hasattr(self, 'footer_text_widget'):
                self.footer_text_widget.delete(1.0, tk.END)
                self.footer_text_widget.insert(1.0, settings.get('receipt_footer', ''))
    
    def save_pharmacy_info(self):
        """Save pharmacy information"""
        try:
            settings_data = {
                'pharmacy_name': self.pharmacy_name_var.get().strip(),
                'pharmacy_address': self.pharmacy_address_var.get().strip(),
                'pharmacy_phone': self.pharmacy_phone_var.get().strip(),
                'pharmacy_email': self.pharmacy_email_var.get().strip()
            }
            
            if self.db.update_settings(settings_data):
                messagebox.showinfo("Success", "Pharmacy information saved successfully!")
                self.status_callback("Pharmacy information updated")
            else:
                messagebox.showerror("Error", "Failed to save pharmacy information!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving pharmacy information: {str(e)}")
    
    def save_system_settings(self):
        """Save system settings"""
        try:
            settings_data = {
                'currency': self.currency_var.get(),
                'tax_rate': float(self.tax_rate_var.get())
            }
            
            if self.db.update_settings(settings_data):
                messagebox.showinfo("Success", "System settings saved successfully!")
                self.status_callback("System settings updated")
            else:
                messagebox.showerror("Error", "Failed to save system settings!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid tax rate!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving system settings: {str(e)}")
    
    def save_receipt_settings(self):
        """Save receipt settings"""
        try:
            footer_text = self.footer_text_widget.get(1.0, tk.END).strip()
            
            settings_data = {
                'receipt_footer': footer_text
            }
            
            if self.db.update_settings(settings_data):
                messagebox.showinfo("Success", "Receipt settings saved successfully!")
                self.status_callback("Receipt settings updated")
            else:
                messagebox.showerror("Error", "Failed to save receipt settings!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving receipt settings: {str(e)}")
    
    def preview_receipt(self):
        """Preview receipt format"""
        # TODO: Implement receipt preview
        messagebox.showinfo("Preview", "Receipt preview functionality will be implemented here.")
        self.status_callback("Receipt preview requested")
    
    def create_backup(self):
        """Create a backup of the database"""
        try:
            from utils import create_backup
            backup_path = create_backup()
            messagebox.showinfo("Backup", f"Backup created successfully!\nLocation: {backup_path}")
            self.status_callback("Backup created successfully")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
            self.status_callback("Backup failed")
    
    def restore_backup(self):
        """Restore from backup"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Backup File",
                filetypes=[("Backup files", "*.backup"), ("All files", "*.*")]
            )
            
            if file_path:
                if messagebox.askyesno("Confirm Restore", 
                                     "This will replace all current data. Are you sure you want to continue?"):
                    from utils import restore_backup
                    if restore_backup(file_path):
                        messagebox.showinfo("Restore", "Backup restored successfully!")
                        self.status_callback("Backup restored successfully")
                    else:
                        messagebox.showerror("Restore Error", "Failed to restore backup!")
                        self.status_callback("Backup restore failed")
                        
        except Exception as e:
            messagebox.showerror("Restore Error", f"Error during restore: {str(e)}")
            self.status_callback("Backup restore failed")
    
    def browse_backup_location(self):
        """Browse for backup location"""
        folder_path = filedialog.askdirectory(title="Select Backup Location")
        if folder_path:
            self.backup_location_var.set(folder_path) 