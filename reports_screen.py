"""
Reports Screen for Ghanaian Pharmacy POS System
Sales analytics and business insights
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class ReportsScreen:
    def __init__(self, parent, db, status_callback):
        self.parent = parent
        self.db = db
        self.status_callback = status_callback
        
        self.setup_ui()
        self.load_daily_summary()
        
    def setup_ui(self):
        """Setup the reports interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Date selection and quick reports
        top_frame = tk.Frame(main_frame, bg='white')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Date selection section
        date_frame = tk.LabelFrame(top_frame, text="Report Period", font=('Arial', 14, 'bold'), 
                                 bg='white', fg='#2c3e50')
        date_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        date_content = tk.Frame(date_frame, bg='white')
        date_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Date range selection
        date_label = tk.Label(date_content, text="Date Range:", font=('Arial', 12), bg='white')
        date_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Start date
        start_date_label = tk.Label(date_content, text="From:", font=('Arial', 11), bg='white')
        start_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_date_var = tk.StringVar()
        self.start_date_entry = DateEntry(date_content, textvariable=self.start_date_var, 
                                        font=('Arial', 11), width=15, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # End date
        end_date_label = tk.Label(date_content, text="To:", font=('Arial', 11), bg='white')
        end_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.end_date_var = tk.StringVar()
        self.end_date_entry = DateEntry(date_content, textvariable=self.end_date_var, 
                                      font=('Arial', 11), width=15, date_pattern='yyyy-mm-dd')
        self.end_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Set default dates (current month)
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        self.start_date_var.set(start_of_month.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))
        
        # Generate report button
        generate_button = tk.Button(date_content, text="Generate Report", command=self.generate_report,
                                  font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                                  relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Quick reports section
        quick_frame = tk.LabelFrame(top_frame, text="Quick Reports", font=('Arial', 14, 'bold'), 
                                  bg='white', fg='#2c3e50')
        quick_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        quick_content = tk.Frame(quick_frame, bg='white')
        quick_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Quick report buttons
        today_button = tk.Button(quick_content, text="Today's Report", command=self.today_report,
                               font=('Arial', 11), bg='#27ae60', fg='white',
                               relief=tk.FLAT, padx=15, pady=8, cursor='hand2', width=15)
        today_button.pack(pady=5)
        
        week_button = tk.Button(quick_content, text="This Week", command=self.week_report,
                              font=('Arial', 11), bg='#f39c12', fg='white',
                              relief=tk.FLAT, padx=15, pady=8, cursor='hand2', width=15)
        week_button.pack(pady=5)
        
        month_button = tk.Button(quick_content, text="This Month", command=self.month_report,
                               font=('Arial', 11), bg='#9b59b6', fg='white',
                               relief=tk.FLAT, padx=15, pady=8, cursor='hand2', width=15)
        month_button.pack(pady=5)
        
        # Middle section - Summary cards
        middle_frame = tk.Frame(main_frame, bg='white')
        middle_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary cards
        self.summary_cards = {}
        summary_data = [
            ('total_sales', 'Total Sales', 'GHS 0.00', '#27ae60'),
            ('total_transactions', 'Transactions', '0', '#3498db'),
            ('average_sale', 'Average Sale', 'GHS 0.00', '#f39c12'),
            ('best_day', 'Best Day', 'N/A', '#9b59b6')
        ]
        
        for i, (key, title, value, color) in enumerate(summary_data):
            card_frame = tk.Frame(middle_frame, bg=color, relief=tk.RAISED, bd=2)
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            title_label = tk.Label(card_frame, text=title, font=('Arial', 12, 'bold'), 
                                 bg=color, fg='white')
            title_label.pack(pady=(10, 5))
            
            value_label = tk.Label(card_frame, text=value, font=('Arial', 16, 'bold'), 
                                 bg=color, fg='white')
            value_label.pack(pady=(0, 10))
            
            self.summary_cards[key] = value_label
        
        # Bottom section - Detailed reports
        bottom_frame = tk.Frame(main_frame, bg='white')
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for different report types
        notebook = ttk.Notebook(bottom_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Sales summary tab
        sales_frame = tk.Frame(notebook, bg='white')
        notebook.add(sales_frame, text="Sales Summary")
        
        # Sales summary content
        sales_content = tk.Frame(sales_frame, bg='white')
        sales_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sales by day
        daily_frame = tk.LabelFrame(sales_content, text="Daily Sales", font=('Arial', 12, 'bold'), 
                                  bg='white', fg='#2c3e50')
        daily_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Daily sales treeview
        daily_columns = ('Date', 'Sales', 'Transactions', 'Average')
        self.daily_tree = ttk.Treeview(daily_frame, columns=daily_columns, show='headings', height=10)
        
        for col in daily_columns:
            self.daily_tree.heading(col, text=col)
            self.daily_tree.column(col, width=150, anchor=tk.CENTER)
        
        self.daily_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top selling drugs tab
        drugs_frame = tk.Frame(notebook, bg='white')
        notebook.add(drugs_frame, text="Top Selling Drugs")
        
        # Top drugs content
        drugs_content = tk.Frame(drugs_frame, bg='white')
        drugs_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top drugs treeview
        drugs_columns = ('Rank', 'Drug', 'Quantity Sold', 'Revenue', 'Percentage')
        self.drugs_tree = ttk.Treeview(drugs_content, columns=drugs_columns, show='headings', height=10)
        
        for col in drugs_columns:
            self.drugs_tree.heading(col, text=col)
            self.drugs_tree.column(col, width=120, anchor=tk.CENTER)
        
        self.drugs_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inventory status tab
        inventory_frame = tk.Frame(notebook, bg='white')
        notebook.add(inventory_frame, text="Inventory Status")
        
        # Inventory content
        inventory_content = tk.Frame(inventory_frame, bg='white')
        inventory_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inventory alerts
        alerts_frame = tk.LabelFrame(inventory_content, text="Inventory Alerts", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        alerts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.alerts_text = tk.Text(alerts_frame, height=8, font=('Arial', 10), 
                                 bg='#f8f9fa', fg='#2c3e50', wrap=tk.WORD)
        self.alerts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Export section
        export_frame = tk.LabelFrame(inventory_content, text="Export Reports", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        export_content = tk.Frame(export_frame, bg='white')
        export_content.pack(fill=tk.X, padx=10, pady=10)
        
        export_sales_button = tk.Button(export_content, text="Export Sales Report", 
                                      command=self.export_sales_report,
                                      font=('Arial', 11), bg='#27ae60', fg='white',
                                      relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        export_sales_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_inventory_button = tk.Button(export_content, text="Export Inventory Report", 
                                          command=self.export_inventory_report,
                                          font=('Arial', 11), bg='#3498db', fg='white',
                                          relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        export_inventory_button.pack(side=tk.LEFT, padx=(0, 10))
        
        print_report_button = tk.Button(export_content, text="Print Report", 
                                      command=self.print_report,
                                      font=('Arial', 11), bg='#f39c12', fg='white',
                                      relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        print_report_button.pack(side=tk.LEFT)
        
    def load_daily_summary(self):
        """Load daily summary for current period"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        self.generate_report_data(start_date, end_date)
    
    def generate_report(self):
        """Generate report for selected date range"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        if not start_date or not end_date:
            messagebox.showwarning("Warning", "Please select both start and end dates!")
            return
        
        self.generate_report_data(start_date, end_date)
    
    def generate_report_data(self, start_date, end_date):
        """Generate report data for the specified period"""
        # Get sales data
        sales = self.db.get_sales_by_date(start_date, end_date)
        
        # Update summary cards
        total_amount = sum(sale['total_amount'] for sale in sales)
        total_transactions = len(sales)
        average_sale = total_amount / total_transactions if total_transactions > 0 else 0
        
        self.summary_cards['total_sales'].config(text=f"GHS {total_amount:.2f}")
        self.summary_cards['total_transactions'].config(text=str(total_transactions))
        self.summary_cards['average_sale'].config(text=f"GHS {average_sale:.2f}")
        
        # Find best day
        if sales:
            daily_sales = {}
            for sale in sales:
                sale_date = datetime.strptime(sale['sale_date'], '%Y-%m-%d %H:%M:%S').date()
                date_str = sale_date.strftime('%Y-%m-%d')
                if date_str not in daily_sales:
                    daily_sales[date_str] = 0
                daily_sales[date_str] += sale['total_amount']
            
            best_day = max(daily_sales.items(), key=lambda x: x[1])
            self.summary_cards['best_day'].config(text=f"{best_day[0]}\nGHS {best_day[1]:.2f}")
        else:
            self.summary_cards['best_day'].config(text="N/A")
        
        # Update daily sales
        self.update_daily_sales(sales)
        
        # Update top selling drugs
        self.update_top_drugs(sales)
        
        # Update inventory alerts
        self.update_inventory_alerts()
        
        self.status_callback(f"Generated report for {start_date} to {end_date}")
    
    def update_daily_sales(self, sales):
        """Update daily sales treeview"""
        # Clear existing items
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)
        
        if not sales:
            return
        
        # Group sales by date
        daily_sales = {}
        for sale in sales:
            sale_date = datetime.strptime(sale['sale_date'], '%Y-%m-%d %H:%M:%S').date()
            date_str = sale_date.strftime('%Y-%m-%d')
            if date_str not in daily_sales:
                daily_sales[date_str] = {'amount': 0, 'transactions': 0}
            daily_sales[date_str]['amount'] += sale['total_amount']
            daily_sales[date_str]['transactions'] += 1
        
        # Add to treeview
        for date_str, data in sorted(daily_sales.items()):
            average = data['amount'] / data['transactions'] if data['transactions'] > 0 else 0
            self.daily_tree.insert('', 'end', values=(
                date_str,
                f"GHS {data['amount']:.2f}",
                data['transactions'],
                f"GHS {average:.2f}"
            ))
    
    def update_top_drugs(self, sales):
        """Update top selling drugs treeview"""
        # Clear existing items
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)
        
        if not sales:
            return
        
        # Get drug sales data (simplified - in real app you'd query sale_items)
        # For now, we'll show a placeholder
        self.drugs_tree.insert('', 'end', values=(
            "1", "Paracetamol (Panadol)", "45", "GHS 112.50", "15%"
        ))
        self.drugs_tree.insert('', 'end', values=(
            "2", "Amoxicillin (Amoxil)", "32", "GHS 480.00", "12%"
        ))
        self.drugs_tree.insert('', 'end', values=(
            "3", "Ibuprofen (Brufen)", "28", "GHS 84.00", "10%"
        ))
        self.drugs_tree.insert('', 'end', values=(
            "4", "Vitamin C", "25", "GHS 37.50", "8%"
        ))
        self.drugs_tree.insert('', 'end', values=(
            "5", "Cetirizine (Zyrtec)", "22", "GHS 110.00", "7%"
        ))
    
    def update_inventory_alerts(self):
        """Update inventory alerts"""
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
    
    def today_report(self):
        """Generate today's report"""
        today = datetime.now().date()
        self.start_date_var.set(today.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))
        self.generate_report()
    
    def week_report(self):
        """Generate this week's report"""
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        self.start_date_var.set(start_of_week.strftime('%Y-%m-%d'))
        self.end_date_var.set(end_of_week.strftime('%Y-%m-%d'))
        self.generate_report()
    
    def month_report(self):
        """Generate this month's report"""
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        
        # Get end of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        self.start_date_var.set(start_of_month.strftime('%Y-%m-%d'))
        self.end_date_var.set(end_of_month.strftime('%Y-%m-%d'))
        self.generate_report()
    
    def export_sales_report(self):
        """Export sales report"""
        # TODO: Implement export functionality
        messagebox.showinfo("Export", "Sales report export functionality will be implemented here.\n\nThis will export sales data to CSV/Excel format.")
        self.status_callback("Sales report export requested")
    
    def export_inventory_report(self):
        """Export inventory report"""
        # TODO: Implement export functionality
        messagebox.showinfo("Export", "Inventory report export functionality will be implemented here.\n\nThis will export inventory data to CSV/Excel format.")
        self.status_callback("Inventory report export requested")
    
    def print_report(self):
        """Print current report"""
        # TODO: Implement print functionality
        messagebox.showinfo("Print", "Print functionality will be implemented here.\n\nThis will print the current report to a printer.")
        self.status_callback("Print report requested") 