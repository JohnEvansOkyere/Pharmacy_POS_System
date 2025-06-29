"""
Inventory Management Screen for Ghanaian Pharmacy POS System
Handles drug inventory management, stock updates, and alerts
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class InventoryScreen:
    def __init__(self, parent, db, status_callback):
        self.parent = parent
        self.db = db
        self.status_callback = status_callback
        self.current_drug = None
        
        self.setup_ui()
        self.load_drugs()
        self.load_alerts()
        
    def setup_ui(self):
        """Setup the inventory management interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Alerts and quick actions
        top_frame = tk.Frame(main_frame, bg='white')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Alerts section
        alerts_frame = tk.LabelFrame(top_frame, text="Inventory Alerts", font=('Arial', 14, 'bold'), 
                                   bg='white', fg='#2c3e50')
        alerts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Alerts content
        self.alerts_text = tk.Text(alerts_frame, height=6, font=('Arial', 10), 
                                 bg='#f8f9fa', fg='#2c3e50', wrap=tk.WORD)
        self.alerts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Quick actions section
        actions_frame = tk.LabelFrame(top_frame, text="Quick Actions", font=('Arial', 14, 'bold'), 
                                    bg='white', fg='#2c3e50')
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Action buttons
        add_button = tk.Button(actions_frame, text="Add New Drug", command=self.show_add_drug_dialog,
                             font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                             relief=tk.FLAT, padx=20, pady=10, cursor='hand2', width=15)
        add_button.pack(pady=5)
        
        edit_button = tk.Button(actions_frame, text="Edit Drug", command=self.edit_selected_drug,
                              font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                              relief=tk.FLAT, padx=20, pady=10, cursor='hand2', width=15)
        edit_button.pack(pady=5)
        
        stock_button = tk.Button(actions_frame, text="Update Stock", command=self.show_stock_update_dialog,
                               font=('Arial', 12, 'bold'), bg='#f39c12', fg='white',
                               relief=tk.FLAT, padx=20, pady=10, cursor='hand2', width=15)
        stock_button.pack(pady=5)
        
        refresh_button = tk.Button(actions_frame, text="Refresh", command=self.refresh_data,
                                 font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white',
                                 relief=tk.FLAT, padx=20, pady=10, cursor='hand2', width=15)
        refresh_button.pack(pady=5)
        
        # Middle section - Search and filters
        middle_frame = tk.Frame(main_frame, bg='white')
        middle_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search section
        search_frame = tk.LabelFrame(middle_frame, text="Search & Filter", font=('Arial', 14, 'bold'), 
                                   bg='white', fg='#2c3e50')
        search_frame.pack(fill=tk.X)
        
        search_content = tk.Frame(search_frame, bg='white')
        search_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Search entry
        search_label = tk.Label(search_content, text="Search:", font=('Arial', 12), bg='white')
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_content, textvariable=self.search_var, 
                              font=('Arial', 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Filter options
        filter_label = tk.Label(search_content, text="Filter:", font=('Arial', 12), bg='white')
        filter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_content, textvariable=self.filter_var, 
                                  values=["All", "Low Stock", "Expiring Soon", "Out of Stock"], 
                                  font=('Arial', 12), state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        # Bottom section - Drug list
        bottom_frame = tk.Frame(main_frame, bg='white')
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Drugs list section
        drugs_frame = tk.LabelFrame(bottom_frame, text="Drug Inventory", font=('Arial', 14, 'bold'), 
                                  bg='white', fg='#2c3e50')
        drugs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Drugs treeview
        columns = ('ID', 'Generic Name', 'Brand Name', 'Dosage', 'Form', 'Stock', 'Price', 'Expiry', 'Status')
        self.drugs_tree = ttk.Treeview(drugs_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = [50, 150, 150, 80, 80, 60, 80, 100, 100]
        for i, col in enumerate(columns):
            self.drugs_tree.heading(col, text=col)
            self.drugs_tree.column(col, width=column_widths[i], anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(drugs_frame, orient=tk.VERTICAL, command=self.drugs_tree.yview)
        self.drugs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.drugs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Bind double-click to edit
        self.drugs_tree.bind('<Double-1>', self.on_drug_double_click)
        
    def load_drugs(self):
        """Load all drugs into the treeview"""
        # Clear existing items
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)
        
        # Get drugs from database
        drugs = self.db.get_all_drugs()
        
        # Add drugs to treeview
        for drug in drugs:
            # Determine status
            status = "OK"
            if drug['quantity_in_stock'] <= 0:
                status = "OUT OF STOCK"
            elif drug['quantity_in_stock'] <= drug['reorder_level']:
                status = "LOW STOCK"
            
            # Check expiry
            expiry_date = datetime.strptime(drug['expiry_date'], '%Y-%m-%d').date()
            days_to_expiry = (expiry_date - datetime.now().date()).days
            if days_to_expiry <= 30:
                status = "EXPIRING SOON"
            
            self.drugs_tree.insert('', 'end', values=(
                drug['id'],
                drug['generic_name'],
                drug['brand_name'],
                drug['dosage'],
                drug['form'],
                drug['quantity_in_stock'],
                f"GHS {drug['unit_price']:.2f}",
                drug['expiry_date'],
                status
            ))
        
        self.status_callback(f"Loaded {len(drugs)} drugs")
    
    def load_alerts(self):
        """Load and display inventory alerts"""
        alerts = []
        
        # Low stock alerts
        low_stock_drugs = self.db.get_low_stock_drugs()
        if low_stock_drugs:
            alerts.append("⚠️ LOW STOCK ALERTS:")
            for drug in low_stock_drugs:
                alerts.append(f"  • {drug['generic_name']} ({drug['brand_name']}) - {drug['quantity_in_stock']} left")
            alerts.append("")
        
        # Expiring drugs alerts
        expiring_drugs = self.db.get_expiring_drugs(30)
        if expiring_drugs:
            alerts.append("⚠️ EXPIRING SOON ALERTS:")
            for drug in expiring_drugs:
                expiry_date = datetime.strptime(drug['expiry_date'], '%Y-%m-%d').date()
                days_left = (expiry_date - datetime.now().date()).days
                alerts.append(f"  • {drug['generic_name']} ({drug['brand_name']}) - Expires in {days_left} days")
            alerts.append("")
        
        # Out of stock alerts
        out_of_stock = [drug for drug in self.db.get_all_drugs() if drug['quantity_in_stock'] <= 0]
        if out_of_stock:
            alerts.append("🚫 OUT OF STOCK ALERTS:")
            for drug in out_of_stock:
                alerts.append(f"  • {drug['generic_name']} ({drug['brand_name']})")
            alerts.append("")
        
        if not alerts:
            alerts.append("✅ All inventory items are in good condition!")
        
        # Update alerts text
        self.alerts_text.delete(1.0, tk.END)
        self.alerts_text.insert(1.0, '\n'.join(alerts))
        
        # Color code the alerts
        self.alerts_text.tag_configure("warning", foreground="#e74c3c")
        self.alerts_text.tag_configure("ok", foreground="#27ae60")
        
        # Apply tags
        content = self.alerts_text.get(1.0, tk.END)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('⚠️') or line.startswith('🚫'):
                self.alerts_text.tag_add("warning", f"{i+1}.0", f"{i+1}.end")
            elif line.startswith('✅'):
                self.alerts_text.tag_add("ok", f"{i+1}.0", f"{i+1}.end")
    
    def on_search(self, event=None):
        """Handle drug search"""
        search_term = self.search_var.get().strip()
        if search_term:
            drugs = self.db.search_drugs(search_term)
            self.display_filtered_drugs(drugs)
        else:
            self.load_drugs()
    
    def on_filter(self, event=None):
        """Handle filter selection"""
        filter_type = self.filter_var.get()
        drugs = self.db.get_all_drugs()
        
        if filter_type == "Low Stock":
            filtered_drugs = [drug for drug in drugs if drug['quantity_in_stock'] <= drug['reorder_level'] and drug['quantity_in_stock'] > 0]
        elif filter_type == "Expiring Soon":
            filtered_drugs = self.db.get_expiring_drugs(30)
        elif filter_type == "Out of Stock":
            filtered_drugs = [drug for drug in drugs if drug['quantity_in_stock'] <= 0]
        else:
            filtered_drugs = drugs
        
        self.display_filtered_drugs(filtered_drugs)
    
    def display_filtered_drugs(self, drugs):
        """Display filtered drugs in treeview"""
        # Clear existing items
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)
        
        # Add filtered drugs
        for drug in drugs:
            status = "OK"
            if drug['quantity_in_stock'] <= 0:
                status = "OUT OF STOCK"
            elif drug['quantity_in_stock'] <= drug['reorder_level']:
                status = "LOW STOCK"
            
            expiry_date = datetime.strptime(drug['expiry_date'], '%Y-%m-%d').date()
            days_to_expiry = (expiry_date - datetime.now().date()).days
            if days_to_expiry <= 30:
                status = "EXPIRING SOON"
            
            self.drugs_tree.insert('', 'end', values=(
                drug['id'],
                drug['generic_name'],
                drug['brand_name'],
                drug['dosage'],
                drug['form'],
                drug['quantity_in_stock'],
                f"GHS {drug['unit_price']:.2f}",
                drug['expiry_date'],
                status
            ))
    
    def on_drug_double_click(self, event):
        """Handle double-click on drug item"""
        self.edit_selected_drug()
    
    def get_selected_drug(self):
        """Get the currently selected drug"""
        selected = self.drugs_tree.selection()
        if not selected:
            return None
        
        # Get drug ID from selected item
        drug_id = self.drugs_tree.item(selected[0])['values'][0]
        return self.db.get_drug(drug_id)
    
    def show_add_drug_dialog(self):
        """Show dialog to add new drug"""
        self.show_drug_dialog(None)
    
    def edit_selected_drug(self):
        """Edit the selected drug"""
        drug = self.get_selected_drug()
        if not drug:
            messagebox.showwarning("Warning", "Please select a drug to edit!")
            return
        
        self.show_drug_dialog(drug)
    
    def show_drug_dialog(self, drug=None):
        """Show drug add/edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Drug" if drug is None else "Edit Drug")
        dialog.geometry("500x600")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Form fields
        fields_frame = tk.Frame(dialog, bg='white')
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form variables
        generic_name_var = tk.StringVar(value=drug['generic_name'] if drug else "")
        brand_name_var = tk.StringVar(value=drug['brand_name'] if drug else "")
        dosage_var = tk.StringVar(value=drug['dosage'] if drug else "")
        form_var = tk.StringVar(value=drug['form'] if drug else "")
        batch_number_var = tk.StringVar(value=drug['batch_number'] if drug else "")
        unit_price_var = tk.StringVar(value=str(drug['unit_price']) if drug else "")
        quantity_var = tk.StringVar(value=str(drug['quantity_in_stock']) if drug else "")
        reorder_level_var = tk.StringVar(value=str(drug['reorder_level']) if drug else "10")
        
        # Form labels and entries
        labels_entries = [
            ("Generic Name:", generic_name_var),
            ("Brand Name:", brand_name_var),
            ("Dosage:", dosage_var),
            ("Form:", form_var),
            ("Batch Number:", batch_number_var),
            ("Unit Price (GHS):", unit_price_var),
            ("Quantity in Stock:", quantity_var),
            ("Reorder Level:", reorder_level_var)
        ]
        
        for i, (label_text, var) in enumerate(labels_entries):
            label = tk.Label(fields_frame, text=label_text, font=('Arial', 11, 'bold'), 
                           bg='white', fg='#2c3e50')
            label.pack(anchor=tk.W, pady=(10, 5))
            
            if label_text == "Form:":
                # Dropdown for form
                form_combo = ttk.Combobox(fields_frame, textvariable=var, 
                                        values=["Tablet", "Capsule", "Syrup", "Injection", "Cream", "Drops"], 
                                        font=('Arial', 11), state="readonly", width=30)
                form_combo.pack(fill=tk.X, pady=(0, 10))
            else:
                entry = tk.Entry(fields_frame, textvariable=var, font=('Arial', 11), width=30)
                entry.pack(fill=tk.X, pady=(0, 10))
        
        # Expiry date
        expiry_label = tk.Label(fields_frame, text="Expiry Date:", font=('Arial', 11, 'bold'), 
                              bg='white', fg='#2c3e50')
        expiry_label.pack(anchor=tk.W, pady=(10, 5))
        
        expiry_date_var = tk.StringVar(value=drug['expiry_date'] if drug else "")
        expiry_entry = DateEntry(fields_frame, textvariable=expiry_date_var, 
                               font=('Arial', 11), width=30, date_pattern='yyyy-mm-dd')
        expiry_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        buttons_frame = tk.Frame(fields_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=20)
        
        save_button = tk.Button(buttons_frame, text="Save", command=lambda: self.save_drug(
            dialog, drug, generic_name_var, brand_name_var, dosage_var, form_var, 
            batch_number_var, expiry_date_var, unit_price_var, quantity_var, reorder_level_var
        ), font=('Arial', 12, 'bold'), bg='#27ae60', fg='white', 
        relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=dialog.destroy,
                                font=('Arial', 12), bg='#95a5a6', fg='white',
                                relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        cancel_button.pack(side=tk.LEFT)
    
    def save_drug(self, dialog, drug, generic_name_var, brand_name_var, dosage_var, form_var, 
                 batch_number_var, expiry_date_var, unit_price_var, quantity_var, reorder_level_var):
        """Save drug data"""
        try:
            drug_data = {
                'generic_name': generic_name_var.get().strip(),
                'brand_name': brand_name_var.get().strip(),
                'dosage': dosage_var.get().strip(),
                'form': form_var.get().strip(),
                'batch_number': batch_number_var.get().strip(),
                'expiry_date': expiry_date_var.get(),
                'unit_price': float(unit_price_var.get()),
                'quantity_in_stock': int(quantity_var.get()),
                'reorder_level': int(reorder_level_var.get())
            }
            
            # Validate required fields
            for field, value in drug_data.items():
                if not value and field != 'reorder_level':
                    messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                    return
            
            # Save to database
            if drug is None:
                # Add new drug
                if self.db.add_drug(drug_data):
                    messagebox.showinfo("Success", "Drug added successfully!")
                    dialog.destroy()
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "Failed to add drug!")
            else:
                # Update existing drug
                if self.db.update_drug(drug['id'], drug_data):
                    messagebox.showinfo("Success", "Drug updated successfully!")
                    dialog.destroy()
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "Failed to update drug!")
                    
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for price, quantity, and reorder level!")
    
    def show_stock_update_dialog(self):
        """Show dialog to update stock"""
        drug = self.get_selected_drug()
        if not drug:
            messagebox.showwarning("Warning", "Please select a drug to update stock!")
            return
        
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Stock")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Content
        content_frame = tk.Frame(dialog, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Drug info
        info_label = tk.Label(content_frame, text=f"Drug: {drug['generic_name']} ({drug['brand_name']})", 
                            font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50')
        info_label.pack(pady=(0, 20))
        
        current_stock_label = tk.Label(content_frame, text=f"Current Stock: {drug['quantity_in_stock']}", 
                                     font=('Arial', 11), bg='white', fg='#34495e')
        current_stock_label.pack(pady=(0, 20))
        
        # Stock adjustment
        adjustment_label = tk.Label(content_frame, text="Stock Adjustment (+/-):", 
                                  font=('Arial', 11, 'bold'), bg='white', fg='#2c3e50')
        adjustment_label.pack(anchor=tk.W, pady=(0, 5))
        
        adjustment_var = tk.StringVar()
        adjustment_entry = tk.Entry(content_frame, textvariable=adjustment_var, 
                                  font=('Arial', 12), width=20)
        adjustment_entry.pack(fill=tk.X, pady=(0, 20))
        adjustment_entry.focus()
        
        # Buttons
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=20)
        
        update_button = tk.Button(buttons_frame, text="Update Stock", command=lambda: self.update_stock(
            dialog, drug['id'], adjustment_var
        ), font=('Arial', 12, 'bold'), bg='#27ae60', fg='white', 
        relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        update_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=dialog.destroy,
                                font=('Arial', 12), bg='#95a5a6', fg='white',
                                relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        cancel_button.pack(side=tk.LEFT)
    
    def update_stock(self, dialog, drug_id, adjustment_var):
        """Update drug stock"""
        try:
            adjustment = int(adjustment_var.get())
            
            if self.db.update_stock(drug_id, adjustment):
                messagebox.showinfo("Success", "Stock updated successfully!")
                dialog.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to update stock!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for stock adjustment!")
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_drugs()
        self.load_alerts()
        self.status_callback("Inventory data refreshed") 