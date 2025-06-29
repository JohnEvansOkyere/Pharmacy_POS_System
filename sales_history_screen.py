"""
Sales History Screen for Ghanaian Pharmacy POS System
View and search past sales transactions
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class SalesHistoryScreen:
    def __init__(self, parent, db, status_callback):
        self.parent = parent
        self.db = db
        self.status_callback = status_callback
        
        self.setup_ui()
        self.load_recent_sales()
        
    def setup_ui(self):
        """Setup the sales history interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Search and filters
        top_frame = tk.Frame(main_frame, bg='white')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search section
        search_frame = tk.LabelFrame(top_frame, text="Search & Filter", font=('Arial', 14, 'bold'), 
                                   bg='white', fg='#2c3e50')
        search_frame.pack(fill=tk.X)
        
        search_content = tk.Frame(search_frame, bg='white')
        search_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Date range selection
        date_label = tk.Label(search_content, text="Date Range:", font=('Arial', 12), bg='white')
        date_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Start date
        start_date_label = tk.Label(search_content, text="From:", font=('Arial', 11), bg='white')
        start_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_date_var = tk.StringVar()
        self.start_date_entry = DateEntry(search_content, textvariable=self.start_date_var, 
                                        font=('Arial', 11), width=15, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # End date
        end_date_label = tk.Label(search_content, text="To:", font=('Arial', 11), bg='white')
        end_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.end_date_var = tk.StringVar()
        self.end_date_entry = DateEntry(search_content, textvariable=self.end_date_var, 
                                      font=('Arial', 11), width=15, date_pattern='yyyy-mm-dd')
        self.end_date_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Set default dates (last 30 days)
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        self.start_date_var.set(thirty_days_ago.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))
        
        # Search button
        search_button = tk.Button(search_content, text="Search", command=self.search_sales,
                                font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                                relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        search_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Quick date buttons
        quick_frame = tk.Frame(search_content, bg='white')
        quick_frame.pack(side=tk.LEFT)
        
        today_button = tk.Button(quick_frame, text="Today", command=self.set_today,
                               font=('Arial', 10), bg='#27ae60', fg='white',
                               relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        today_button.pack(side=tk.LEFT, padx=(0, 5))
        
        week_button = tk.Button(quick_frame, text="This Week", command=self.set_this_week,
                              font=('Arial', 10), bg='#f39c12', fg='white',
                              relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        week_button.pack(side=tk.LEFT, padx=(0, 5))
        
        month_button = tk.Button(quick_frame, text="This Month", command=self.set_this_month,
                               font=('Arial', 10), bg='#9b59b6', fg='white',
                               relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        month_button.pack(side=tk.LEFT)
        
        # Middle section - Sales summary
        middle_frame = tk.Frame(main_frame, bg='white')
        middle_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary section
        summary_frame = tk.LabelFrame(middle_frame, text="Sales Summary", font=('Arial', 14, 'bold'), 
                                    bg='white', fg='#2c3e50')
        summary_frame.pack(fill=tk.X)
        
        summary_content = tk.Frame(summary_frame, bg='white')
        summary_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Summary labels
        self.summary_labels = {}
        summary_fields = [
            ('total_sales', 'Total Sales:'),
            ('total_transactions', 'Total Transactions:'),
            ('average_sale', 'Average Sale:'),
            ('best_selling', 'Best Selling:')
        ]
        
        for i, (field, label) in enumerate(summary_fields):
            row = i // 2
            col = i % 2
            
            label_widget = tk.Label(summary_content, text=label, font=('Arial', 12, 'bold'), 
                                  bg='white', fg='#2c3e50')
            label_widget.grid(row=row, column=col*2, sticky=tk.W, padx=(0, 10), pady=5)
            
            value_widget = tk.Label(summary_content, text="", font=('Arial', 12), 
                                  bg='white', fg='#e74c3c')
            value_widget.grid(row=row, column=col*2+1, sticky=tk.W, padx=(0, 30), pady=5)
            
            self.summary_labels[field] = value_widget
        
        # Bottom section - Sales list
        bottom_frame = tk.Frame(main_frame, bg='white')
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sales list section
        sales_frame = tk.LabelFrame(bottom_frame, text="Sales Transactions", font=('Arial', 14, 'bold'), 
                                  bg='white', fg='#2c3e50')
        sales_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sales treeview
        columns = ('Receipt #', 'Date', 'Customer', 'Items', 'Total', 'Payment', 'Cashier')
        self.sales_tree = ttk.Treeview(sales_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = [120, 120, 150, 80, 100, 100, 100]
        for i, col in enumerate(columns):
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=column_widths[i], anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(sales_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Bind double-click to view details
        self.sales_tree.bind('<Double-1>', self.view_sale_details)
        
        # Action buttons
        actions_frame = tk.Frame(sales_frame, bg='white')
        actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        view_button = tk.Button(actions_frame, text="View Details", command=self.view_selected_sale,
                              font=('Arial', 11), bg='#3498db', fg='white',
                              relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        view_button.pack(side=tk.LEFT, padx=(0, 10))
        
        reprint_button = tk.Button(actions_frame, text="Reprint Receipt", command=self.reprint_receipt,
                                 font=('Arial', 11), bg='#f39c12', fg='white',
                                 relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        reprint_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_button = tk.Button(actions_frame, text="Export", command=self.export_sales,
                                font=('Arial', 11), bg='#27ae60', fg='white',
                                relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        export_button.pack(side=tk.LEFT)
        
    def load_recent_sales(self):
        """Load recent sales (last 30 days by default)"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        self.search_sales_by_date(start_date, end_date)
    
    def search_sales(self):
        """Search sales by date range"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        if not start_date or not end_date:
            messagebox.showwarning("Warning", "Please select both start and end dates!")
            return
        
        self.search_sales_by_date(start_date, end_date)
    
    def search_sales_by_date(self, start_date, end_date):
        """Search sales within date range"""
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Get sales from database
        sales = self.db.get_sales_by_date(start_date, end_date)
        
        # Add sales to treeview
        for sale in sales:
            # Format date
            sale_date = datetime.strptime(sale['sale_date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            
            # Get item count (simplified - in real app you'd query sale_items)
            item_count = "N/A"  # TODO: Get actual item count
            
            self.sales_tree.insert('', 'end', values=(
                sale['receipt_number'],
                sale_date,
                sale['customer_name'] or "Walk-in Customer",
                item_count,
                f"GHS {sale['total_amount']:.2f}",
                sale['payment_method'],
                sale['cashier_name']
            ))
        
        # Update summary
        self.update_summary(sales)
        
        self.status_callback(f"Found {len(sales)} sales from {start_date} to {end_date}")
    
    def update_summary(self, sales):
        """Update sales summary"""
        if not sales:
            self.summary_labels['total_sales'].config(text="GHS 0.00")
            self.summary_labels['total_transactions'].config(text="0")
            self.summary_labels['average_sale'].config(text="GHS 0.00")
            self.summary_labels['best_selling'].config(text="N/A")
            return
        
        total_amount = sum(sale['total_amount'] for sale in sales)
        total_transactions = len(sales)
        average_sale = total_amount / total_transactions if total_transactions > 0 else 0
        
        self.summary_labels['total_sales'].config(text=f"GHS {total_amount:.2f}")
        self.summary_labels['total_transactions'].config(text=str(total_transactions))
        self.summary_labels['average_sale'].config(text=f"GHS {average_sale:.2f}")
        self.summary_labels['best_selling'].config(text="See Reports")  # TODO: Implement best selling calculation
    
    def set_today(self):
        """Set date range to today"""
        today = datetime.now().date()
        self.start_date_var.set(today.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))
        self.search_sales()
    
    def set_this_week(self):
        """Set date range to this week"""
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        self.start_date_var.set(start_of_week.strftime('%Y-%m-%d'))
        self.end_date_var.set(end_of_week.strftime('%Y-%m-%d'))
        self.search_sales()
    
    def set_this_month(self):
        """Set date range to this month"""
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        
        # Get end of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        self.start_date_var.set(start_of_month.strftime('%Y-%m-%d'))
        self.end_date_var.set(end_of_month.strftime('%Y-%m-%d'))
        self.search_sales()
    
    def get_selected_sale(self):
        """Get the currently selected sale"""
        selected = self.sales_tree.selection()
        if not selected:
            return None
        
        # Get receipt number from selected item
        receipt_number = self.sales_tree.item(selected[0])['values'][0]
        
        # Find sale in database
        sales = self.db.get_sales_by_date(self.start_date_var.get(), self.end_date_var.get())
        for sale in sales:
            if sale['receipt_number'] == receipt_number:
                return sale
        
        return None
    
    def view_selected_sale(self):
        """View details of selected sale"""
        sale = self.get_selected_sale()
        if not sale:
            messagebox.showwarning("Warning", "Please select a sale to view!")
            return
        
        self.view_sale_details(sale)
    
    def view_sale_details(self, event=None):
        """View sale details"""
        if event:
            # Called from double-click
            sale = self.get_selected_sale()
        else:
            # Called from button
            sale = self.get_selected_sale()
        
        if not sale:
            return
        
        # Get full sale details with items
        sale_details = self.db.get_sale(sale['id'])
        if not sale_details:
            messagebox.showerror("Error", "Could not load sale details!")
            return
        
        self.show_sale_details_dialog(sale_details)
    
    def show_sale_details_dialog(self, sale):
        """Show sale details dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Sale Details - Receipt #{sale['receipt_number']}")
        dialog.geometry("600x500")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Content
        content_frame = tk.Frame(dialog, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sale info
        info_frame = tk.LabelFrame(content_frame, text="Sale Information", font=('Arial', 12, 'bold'), 
                                 bg='white', fg='#2c3e50')
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_content = tk.Frame(info_frame, bg='white')
        info_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Sale details
        sale_date = datetime.strptime(sale['sale_date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        details = [
            ("Receipt Number:", sale['receipt_number']),
            ("Date:", sale_date),
            ("Customer:", sale['customer_name'] or "Walk-in Customer"),
            ("Phone:", sale['customer_phone'] or "N/A"),
            ("Payment Method:", sale['payment_method']),
            ("Cashier:", sale['cashier_name']),
            ("Total Amount:", f"GHS {sale['total_amount']:.2f}")
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2
            
            label_widget = tk.Label(info_content, text=label, font=('Arial', 11, 'bold'), 
                                  bg='white', fg='#2c3e50')
            label_widget.grid(row=row, column=col*2, sticky=tk.W, padx=(0, 10), pady=2)
            
            value_widget = tk.Label(info_content, text=value, font=('Arial', 11), 
                                  bg='white', fg='#34495e')
            value_widget.grid(row=row, column=col*2+1, sticky=tk.W, padx=(0, 20), pady=2)
        
        # Items list
        items_frame = tk.LabelFrame(content_frame, text="Items", font=('Arial', 12, 'bold'), 
                                  bg='white', fg='#2c3e50')
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Items treeview
        item_columns = ('Item', 'Dosage', 'Form', 'Qty', 'Unit Price', 'Total')
        items_tree = ttk.Treeview(items_frame, columns=item_columns, show='headings', height=8)
        
        for col in item_columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=100, anchor=tk.CENTER)
        
        items_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add items to treeview
        for item in sale.get('items', []):
            items_tree.insert('', 'end', values=(
                f"{item['generic_name']}\n({item['brand_name']})",
                item['dosage'],
                item['form'],
                item['quantity'],
                f"GHS {item['unit_price']:.2f}",
                f"GHS {item['total_price']:.2f}"
            ))
        
        # Buttons
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=10)
        
        reprint_button = tk.Button(buttons_frame, text="Reprint Receipt", 
                                 command=lambda: self.reprint_receipt(sale),
                                 font=('Arial', 11, 'bold'), bg='#f39c12', fg='white',
                                 relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        reprint_button.pack(side=tk.LEFT, padx=(0, 10))
        
        close_button = tk.Button(buttons_frame, text="Close", command=dialog.destroy,
                               font=('Arial', 11), bg='#95a5a6', fg='white',
                               relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        close_button.pack(side=tk.LEFT)
    
    def reprint_receipt(self, sale=None):
        """Reprint receipt for selected sale"""
        if not sale:
            sale = self.get_selected_sale()
        
        if not sale:
            messagebox.showwarning("Warning", "Please select a sale to reprint!")
            return
        
        # Get full sale details
        sale_details = self.db.get_sale(sale['id'])
        if not sale_details:
            messagebox.showerror("Error", "Could not load sale details!")
            return
        
        # TODO: Implement receipt printing
        messagebox.showinfo("Receipt", f"Receipt #{sale['receipt_number']} would be printed here.\n\nThis feature requires printer setup.")
        self.status_callback(f"Reprinted receipt #{sale['receipt_number']}")
    
    def export_sales(self):
        """Export sales data"""
        # TODO: Implement export functionality
        messagebox.showinfo("Export", "Export functionality will be implemented here.\n\nThis will export sales data to CSV/Excel format.")
        self.status_callback("Export requested") 