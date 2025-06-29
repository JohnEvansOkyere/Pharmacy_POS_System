"""
POS Sales Screen for Ghanaian Pharmacy POS System
Main sales interface with product search and cart management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import os

class POSScreen:
    # Color palette
    PRIMARY_BG = '#F4F6F8'
    CARD_BG = '#FFFFFF'
    PRIMARY_TEXT = '#2C3E50'
    SECONDARY_TEXT = '#7F8C8D'
    PRIMARY_GREEN = '#27AE60'
    ACCENT_ORANGE = '#F39C12'
    ACCENT_PURPLE = '#9B59B6'
    ACCENT_RED = '#E74C3C'
    ACCENT_BLUE = '#3498DB'
    BORDER_COLOR = '#E0E4E8'

    def __init__(self, parent, db, status_callback):
        self.parent = parent
        self.db = db
        self.status_callback = status_callback
        self.cart_items = []
        self.current_drug = None
        
        self.setup_ui()
        self.load_quick_drugs()
        
    def setup_ui(self):
        """Setup the POS interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg=self.PRIMARY_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Product search and selection
        left_frame = tk.Frame(main_frame, bg=self.PRIMARY_BG, width=600)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Product search section
        search_frame = tk.LabelFrame(left_frame, text="Product Search", font=('Arial', 14, 'bold'), 
                                   bg=self.CARD_BG, fg=self.PRIMARY_TEXT, bd=2, relief=tk.GROOVE, labelanchor='n')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        search_label = tk.Label(search_frame, text="Search Drugs:", font=('Arial', 12), bg=self.CARD_BG, fg=self.PRIMARY_TEXT)
        search_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                   font=('Arial', 14), width=40, bg='#F8FAFB', fg=self.PRIMARY_TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        self.search_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        self.search_entry.focus()
        
        # Autocomplete Listbox
        self.suggestion_box = tk.Listbox(search_frame, font=('Arial', 12), height=5, bg='#F8FAFB', fg=self.PRIMARY_TEXT, activestyle='dotbox', relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        self.suggestion_box.pack_forget()
        self.suggestion_box.bind('<<ListboxSelect>>', self.on_suggestion_select)
        self.suggestion_box.bind('<Return>', self.on_suggestion_enter)
        
        # Quick drugs section
        quick_frame = tk.LabelFrame(left_frame, text="Quick Add Drugs", font=('Arial', 14, 'bold'), 
                                   bg=self.CARD_BG, fg=self.PRIMARY_TEXT, bd=2, relief=tk.GROOVE, labelanchor='n')
        quick_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        quick_frame.pack_propagate(False)
        
        # Quick drugs buttons frame
        self.quick_buttons_frame = tk.Frame(quick_frame, bg=self.CARD_BG)
        self.quick_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Product details section
        details_frame = tk.LabelFrame(left_frame, text="Product Details", font=('Arial', 14, 'bold'), 
                                    bg='white', fg='#2c3e50')
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product details content
        details_content = tk.Frame(details_frame, bg='white')
        details_content.pack(fill=tk.X, padx=10, pady=10)
        
        # Product info labels
        self.product_labels = {}
        product_fields = [
            ('generic_name', 'Generic Name:'),
            ('brand_name', 'Brand Name:'),
            ('dosage', 'Dosage:'),
            ('form', 'Form:'),
            ('unit_price', 'Unit Price:'),
            ('quantity_in_stock', 'Stock:'),
            ('expiry_date', 'Expiry:')
        ]
        
        for i, (field, label) in enumerate(product_fields):
            row = i // 2
            col = i % 2
            
            label_widget = tk.Label(details_content, text=label, font=('Arial', 11, 'bold'), 
                                  bg='white', fg='#2c3e50')
            label_widget.grid(row=row, column=col*2, sticky=tk.W, padx=(0, 5), pady=2)
            
            value_widget = tk.Label(details_content, text="", font=('Arial', 11), 
                                  bg='white', fg='#34495e')
            value_widget.grid(row=row, column=col*2+1, sticky=tk.W, padx=(0, 20), pady=2)
            
            self.product_labels[field] = value_widget
        
        # Add to cart section
        cart_add_frame = tk.Frame(details_frame, bg='white')
        cart_add_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        quantity_label = tk.Label(cart_add_frame, text="Quantity:", font=('Arial', 12, 'bold'), 
                                bg='white', fg='#2c3e50')
        quantity_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(cart_add_frame, textvariable=self.quantity_var, 
                                     font=('Arial', 12), width=10)
        self.quantity_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        add_button = tk.Button(cart_add_frame, text="Add to Cart", command=self.add_to_cart,
                             font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                             relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        add_button.pack(side=tk.LEFT)
        
        # Right panel - Cart and checkout
        right_frame = tk.Frame(main_frame, bg=self.PRIMARY_BG, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)
        
        # Cart section
        cart_frame = tk.LabelFrame(right_frame, text="Shopping Cart", font=('Arial', 14, 'bold'), 
                                 bg=self.CARD_BG, fg=self.PRIMARY_TEXT, bd=2, relief=tk.GROOVE, labelanchor='n')
        cart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Cart treeview
        cart_columns = ('Item', 'Qty', 'Price', 'Total')
        style = ttk.Style()
        style.configure('Treeview', font=('Arial', 11), rowheight=28, background=self.CARD_BG, fieldbackground=self.CARD_BG, foreground=self.PRIMARY_TEXT)
        style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background=self.PRIMARY_BG, foreground=self.PRIMARY_TEXT)
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_columns, show='headings', height=15)
        
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor=tk.CENTER)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cart total
        total_frame = tk.Frame(cart_frame, bg=self.CARD_BG)
        total_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        total_label = tk.Label(total_frame, text="Total:", font=('Arial', 16, 'bold'), 
                             bg=self.CARD_BG, fg=self.PRIMARY_TEXT)
        total_label.pack(side=tk.LEFT)
        
        self.total_var = tk.StringVar(value="GHS 0.00")
        total_value = tk.Label(total_frame, textvariable=self.total_var, 
                             font=('Arial', 16, 'bold'), bg=self.CARD_BG, fg=self.ACCENT_RED)
        total_value.pack(side=tk.RIGHT)
        
        # Cart actions
        cart_actions_frame = tk.Frame(cart_frame, bg=self.CARD_BG)
        cart_actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        remove_button = tk.Button(cart_actions_frame, text="Remove Item", command=self.remove_item,
                                font=('Arial', 11), bg=self.ACCENT_RED, fg='white',
                                relief=tk.FLAT, padx=15, pady=5, cursor='hand2', activebackground='#C0392B')
        remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        modify_button = tk.Button(cart_actions_frame, text="Modify Qty", command=self.modify_quantity,
                                font=('Arial', 11), bg=self.ACCENT_PURPLE, fg='white',
                                relief=tk.FLAT, padx=15, pady=5, cursor='hand2', activebackground='#7D3C98')
        modify_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(cart_actions_frame, text="Clear Cart", command=self.clear_cart,
                               font=('Arial', 11), bg=self.ACCENT_ORANGE, fg='white',
                               relief=tk.FLAT, padx=15, pady=5, cursor='hand2', activebackground='#B9770E')
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        print_button = tk.Button(cart_actions_frame, text="Print Receipt", command=self.print_receipt,
                               font=('Arial', 11), bg=self.ACCENT_BLUE, fg='white',
                               relief=tk.FLAT, padx=15, pady=5, cursor='hand2', activebackground='#2471A3')
        print_button.pack(side=tk.LEFT)
        
        # Checkout section
        checkout_frame = tk.LabelFrame(right_frame, text="Checkout", font=('Arial', 14, 'bold'), 
                                     bg=self.CARD_BG, fg=self.PRIMARY_TEXT, bd=2, relief=tk.GROOVE, labelanchor='n')
        checkout_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Customer info
        customer_frame = tk.Frame(checkout_frame, bg=self.CARD_BG)
        customer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        customer_name_label = tk.Label(customer_frame, text="Customer Name:", font=('Arial', 11), 
                                     bg=self.CARD_BG, fg=self.PRIMARY_TEXT)
        customer_name_label.pack(anchor=tk.W)
        
        self.customer_name_var = tk.StringVar()
        customer_name_entry = tk.Entry(customer_frame, textvariable=self.customer_name_var, 
                                     font=('Arial', 11), width=30, bg='#F8FAFB', fg=self.PRIMARY_TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        customer_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        customer_phone_label = tk.Label(customer_frame, text="Customer Phone:", font=('Arial', 11), 
                                      bg=self.CARD_BG, fg=self.PRIMARY_TEXT)
        customer_phone_label.pack(anchor=tk.W)
        
        self.customer_phone_var = tk.StringVar()
        customer_phone_entry = tk.Entry(customer_frame, textvariable=self.customer_phone_var, 
                                      font=('Arial', 11), width=30, bg='#F8FAFB', fg=self.PRIMARY_TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        customer_phone_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Payment method
        payment_frame = tk.Frame(checkout_frame, bg=self.CARD_BG)
        payment_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        payment_label = tk.Label(payment_frame, text="Payment Method:", font=('Arial', 11), 
                               bg=self.CARD_BG, fg=self.PRIMARY_TEXT)
        payment_label.pack(anchor=tk.W)
        
        self.payment_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(payment_frame, textvariable=self.payment_var, 
                                   values=["Cash", "Mobile Money", "Card"], 
                                   font=('Arial', 11), state="readonly", width=20)
        payment_combo.pack(anchor=tk.W, pady=(0, 10))
        
        # Checkout button
        checkout_button = tk.Button(checkout_frame, text="COMPLETE SALE", command=self.complete_sale,
                                  font=('Arial', 16, 'bold'), bg=self.PRIMARY_GREEN, fg='white',
                                  relief=tk.FLAT, padx=30, pady=10, cursor='hand2', activebackground='#229954')
        checkout_button.pack(pady=10)
        
    def load_quick_drugs(self, filtered_drugs=None):
        """Load drugs in a linear list format"""
        for widget in self.quick_buttons_frame.winfo_children():
            widget.destroy()
        list_frame = tk.Frame(self.quick_buttons_frame, bg=self.CARD_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        canvas = tk.Canvas(list_frame, bg=self.CARD_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.CARD_BG)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        drugs = filtered_drugs if filtered_drugs is not None else self.db.get_all_drugs()
        for i, drug in enumerate(drugs):
            drug_frame = tk.Frame(scrollable_frame, bg=self.CARD_BG, relief=tk.RAISED, bd=1, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
            drug_frame.pack(fill=tk.X, padx=5, pady=6, ipadx=4, ipady=4)
            info_frame = tk.Frame(drug_frame, bg=self.CARD_BG)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
            name_label = tk.Label(info_frame, text=f"{drug['generic_name']} ({drug['brand_name']})", font=('Arial', 12, 'bold'), bg=self.CARD_BG, fg=self.PRIMARY_TEXT, anchor=tk.W)
            name_label.pack(anchor=tk.W)
            details_label = tk.Label(info_frame, text=f"{drug['dosage']} {drug['form']} - Stock: {drug['quantity_in_stock']}", font=('Arial', 10), bg=self.CARD_BG, fg=self.SECONDARY_TEXT, anchor=tk.W)
            details_label.pack(anchor=tk.W)
            action_frame = tk.Frame(drug_frame, bg=self.CARD_BG)
            action_frame.pack(side=tk.RIGHT, padx=10, pady=5)
            price_label = tk.Label(action_frame, text=f"GHS {drug['unit_price']:.2f}", font=('Arial', 12, 'bold'), bg=self.CARD_BG, fg=self.ACCENT_RED)
            price_label.pack(side=tk.TOP, pady=(0, 5))
            # Quantity entry
            qty_var = tk.StringVar(value="1")
            qty_entry = tk.Entry(action_frame, textvariable=qty_var, width=4, font=('Arial', 10), justify='center', bg='#F8FAFB', fg=self.PRIMARY_TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
            qty_entry.pack(side=tk.LEFT, padx=(0, 5))
            # Add to cart button
            add_button = tk.Button(action_frame, text="Add to Cart", command=lambda d=drug, qv=qty_var: self.add_drug_to_cart(d, qv), font=('Arial', 10, 'bold'), bg=self.PRIMARY_GREEN, fg='white', relief=tk.FLAT, padx=14, pady=4, cursor='hand2', activebackground='#229954')
            add_button.pack(side=tk.LEFT)
            def on_enter(e, frame=drug_frame):
                frame.configure(bg='#EAF2F8')
                for child in frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg='#EAF2F8')
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.configure(bg='#EAF2F8')
            def on_leave(e, frame=drug_frame):
                frame.configure(bg=self.CARD_BG)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=self.CARD_BG)
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.configure(bg=self.CARD_BG)
            drug_frame.bind('<Enter>', on_enter)
            drug_frame.bind('<Leave>', on_leave)
            info_frame.bind('<Enter>', on_enter)
            info_frame.bind('<Leave>', on_leave)
            drug_frame.bind('<Button-1>', lambda e, d=drug: self.select_drug(d))
            info_frame.bind('<Button-1>', lambda e, d=drug: self.select_drug(d))
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def add_drug_to_cart(self, drug, qty_var=None):
        """Add drug directly to cart with default quantity of 1"""
        try:
            quantity = 1
            if qty_var is not None:
                try:
                    quantity = int(qty_var.get())
                except Exception:
                    quantity = 1
            
            if quantity > drug['quantity_in_stock']:
                messagebox.showwarning("Warning", f"Only {drug['quantity_in_stock']} items in stock!")
                return
            
            # Check if item already in cart
            for item in self.cart_items:
                if item['drug_id'] == drug['id']:
                    new_quantity = item['quantity'] + quantity
                    if new_quantity > drug['quantity_in_stock']:
                        messagebox.showwarning("Warning", f"Only {drug['quantity_in_stock']} items in stock!")
                        return
                    item['quantity'] = new_quantity
                    item['total_price'] = new_quantity * item['unit_price']
                    self.update_cart_display()
                    self.status_callback(f"Updated quantity for {drug['generic_name']}")
                    # Reset Quick Add Drugs to show all drugs
                    self.load_quick_drugs()
                    return
            
            # Add new item to cart
            cart_item = {
                'drug_id': drug['id'],
                'generic_name': drug['generic_name'],
                'brand_name': drug['brand_name'],
                'quantity': quantity,
                'unit_price': drug['unit_price'],
                'total_price': quantity * drug['unit_price']
            }
            
            self.cart_items.append(cart_item)
            self.update_cart_display()
            self.status_callback(f"Added {quantity}x {drug['generic_name']} to cart")
            # Reset Quick Add Drugs to show all drugs
            self.load_quick_drugs()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {str(e)}")
    
    def update_cart_display(self):
        """Update the cart display with improved functionality"""
        # Clear existing items
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items to treeview
        for i, item in enumerate(self.cart_items):
            tree_item = self.cart_tree.insert('', 'end', values=(
                f"{item['generic_name']}\n({item['brand_name']})",
                item['quantity'],
                f"GHS {item['unit_price']:.2f}",
                f"GHS {item['total_price']:.2f}"
            ))
        
        # Update total
        total = sum(item['total_price'] for item in self.cart_items)
        self.total_var.set(f"GHS {total:.2f}")
    
    def get_selected_cart_index(self):
        selected = self.cart_tree.selection()
        if not selected:
            return None
        item_id = selected[0]
        # Get index by matching displayed values
        values = self.cart_tree.item(item_id)['values']
        for idx, item in enumerate(self.cart_items):
            if f"{item['generic_name']}\n({item['brand_name']})" == values[0]:
                return idx
        return None

    def remove_item(self):
        selected_index = self.get_selected_cart_index()
        if selected_index is None:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return
        removed_item = self.cart_items.pop(selected_index)
        self.update_cart_display()
        self.status_callback(f"Removed {removed_item['generic_name']} from cart")
    
    def clear_cart(self):
        """Clear all items from cart"""
        if not self.cart_items:
            return
        
        if messagebox.askyesno("Clear Cart", "Are you sure you want to clear the cart?"):
            self.cart_items.clear()
            self.update_cart_display()
            self.status_callback("Cart cleared")
    
    def complete_sale(self):
        """Complete the sale transaction"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        # Generate receipt number
        receipt_number = self.db.generate_receipt_number()
        
        # Calculate total
        total_amount = sum(item['total_price'] for item in self.cart_items)
        
        # Create sale data
        sale_data = {
            'receipt_number': receipt_number,
            'total_amount': total_amount,
            'payment_method': self.payment_var.get(),
            'customer_name': self.customer_name_var.get(),
            'customer_phone': self.customer_phone_var.get(),
            'cashier_name': 'Admin'  # TODO: Get from user session
        }
        
        # Create sale in database
        sale_id = self.db.create_sale(sale_data)
        if not sale_id:
            messagebox.showerror("Error", "Failed to create sale!")
            return
        
        # Add sale items
        for item in self.cart_items:
            item_data = {
                'drug_id': item['drug_id'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total_price': item['total_price']
            }
            
            if not self.db.add_sale_item(sale_id, item_data):
                messagebox.showerror("Error", f"Failed to add {item['generic_name']} to sale!")
                return
        
        # Show success message
        messagebox.showinfo("Success", f"Sale completed successfully!\nReceipt #: {receipt_number}\nTotal: GHS {total_amount:.2f}")
        
        # Clear cart and form
        self.cart_items.clear()
        self.update_cart_display()
        self.customer_name_var.set("")
        self.customer_phone_var.set("")
        self.payment_var.set("Cash")
        self.clear_product_details()
        
        self.status_callback(f"Sale completed - Receipt #{receipt_number}")
    
    def on_search(self, event=None):
        search_term = self.search_var.get().strip()
        if len(search_term) >= 1:
            drugs = self.db.search_drugs(search_term)
            if drugs:
                # Show suggestions
                self.suggestion_box.delete(0, tk.END)
                for drug in drugs:
                    self.suggestion_box.insert(tk.END, f"{drug['generic_name']} ({drug['brand_name']})")
                self.suggestion_box.place(x=self.search_entry.winfo_x(), y=self.search_entry.winfo_y() + self.search_entry.winfo_height() + 5, width=self.search_entry.winfo_width())
                self.suggestion_box.lift()
                self.suggestion_box.pack()
                self.suggestion_box.selection_clear(0, tk.END)
            else:
                self.suggestion_box.pack_forget()
                self.clear_product_details()
        else:
            self.suggestion_box.pack_forget()
            self.clear_product_details()
    
    def on_suggestion_select(self, event):
        if not self.suggestion_box.curselection():
            return
        index = self.suggestion_box.curselection()[0]
        search_term = self.search_var.get().strip()
        drugs = self.db.search_drugs(search_term)
        if drugs and index < len(drugs):
            drug = drugs[index]
            self.select_drug(drug)
            self.search_var.set(f"{drug['generic_name']} ({drug['brand_name']})")
            self.suggestion_box.pack_forget()
            # Filter Quick Add Drugs to show only this drug
            self.load_quick_drugs(filtered_drugs=[drug])
    
    def on_suggestion_enter(self, event):
        self.on_suggestion_select(event)
        self.suggestion_box.pack_forget()
    
    def select_drug(self, drug):
        """Select a drug and display its details"""
        self.current_drug = drug
        
        # Update product details
        self.product_labels['generic_name'].config(text=drug['generic_name'])
        self.product_labels['brand_name'].config(text=drug['brand_name'])
        self.product_labels['dosage'].config(text=drug['dosage'])
        self.product_labels['form'].config(text=drug['form'])
        self.product_labels['unit_price'].config(text=f"GHS {drug['unit_price']:.2f}")
        self.product_labels['quantity_in_stock'].config(text=str(drug['quantity_in_stock']))
        self.product_labels['expiry_date'].config(text=drug['expiry_date'])
        
        # Reset quantity
        self.quantity_var.set("1")
        
        self.status_callback(f"Selected: {drug['generic_name']} ({drug['brand_name']})")
    
    def clear_product_details(self):
        """Clear product details display"""
        self.current_drug = None
        for label in self.product_labels.values():
            label.config(text="")
    
    def print_receipt(self):
        """Print current cart as receipt"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        try:
            # Generate receipt content
            receipt_content = self.generate_receipt_content()
            
            # Show receipt preview
            self.show_receipt_preview(receipt_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating receipt: {str(e)}")
    
    def generate_receipt_content(self):
        """Generate receipt content"""
        settings = self.db.get_settings()
        
        receipt_lines = []
        receipt_lines.append("=" * 40)
        receipt_lines.append(f"{settings.get('pharmacy_name', 'Ghana Pharmacy')}")
        receipt_lines.append(f"{settings.get('pharmacy_address', '')}")
        receipt_lines.append(f"Phone: {settings.get('pharmacy_phone', '')}")
        receipt_lines.append("=" * 40)
        receipt_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append(f"Receipt: {self.db.generate_receipt_number()}")
        receipt_lines.append("-" * 40)
        receipt_lines.append("ITEM                    QTY    PRICE    TOTAL")
        receipt_lines.append("-" * 40)
        
        for item in self.cart_items:
            name = f"{item['generic_name']} ({item['brand_name']})"
            if len(name) > 20:
                name = name[:17] + "..."
            receipt_lines.append(f"{name:<20} {item['quantity']:>3} {item['unit_price']:>8.2f} {item['total_price']:>8.2f}")
        
        receipt_lines.append("-" * 40)
        total = sum(item['total_price'] for item in self.cart_items)
        receipt_lines.append(f"TOTAL: {'':>25} GHS {total:>8.2f}")
        receipt_lines.append("=" * 40)
        receipt_lines.append(settings.get('receipt_footer', 'Thank you for your purchase!'))
        receipt_lines.append("=" * 40)
        
        return receipt_lines
    
    def show_receipt_preview(self, receipt_lines):
        """Show receipt preview dialog"""
        preview_window = tk.Toplevel(self.parent)
        preview_window.title("Receipt Preview")
        preview_window.geometry("500x600")
        preview_window.configure(bg='white')
        preview_window.transient(self.parent)
        preview_window.grab_set()
        
        # Center the window
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (preview_window.winfo_screenheight() // 2) - (600 // 2)
        preview_window.geometry(f"500x600+{x}+{y}")
        
        # Receipt content
        content_frame = tk.Frame(preview_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Receipt Preview", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Receipt text
        receipt_text = tk.Text(content_frame, font=('Courier', 10), bg='white', 
                             fg='black', wrap=tk.NONE, height=20)
        receipt_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Insert receipt content
        for line in receipt_lines:
            receipt_text.insert(tk.END, line + '\n')
        
        receipt_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=10)
        
        print_button = tk.Button(button_frame, text="Print Receipt", 
                               command=lambda: self.actual_print_receipt(receipt_lines, preview_window),
                               font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                               relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        print_button.pack(side=tk.LEFT, padx=(0, 10))
        
        close_button = tk.Button(button_frame, text="Close", 
                               command=preview_window.destroy,
                               font=('Arial', 12), bg='#95a5a6', fg='white',
                               relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        close_button.pack(side=tk.LEFT)
    
    def actual_print_receipt(self, receipt_lines, preview_window):
        """Actually print the receipt"""
        try:
            # For now, we'll save to a file and show a message
            # In a real implementation, you would send to printer
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipts/receipt_{timestamp}.txt"
            
            # Ensure receipts directory exists
            os.makedirs("receipts", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in receipt_lines:
                    f.write(line + '\n')
            
            messagebox.showinfo("Print", f"Receipt saved to {filename}\n\nIn a real implementation, this would be sent to the printer.")
            preview_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Print Error", f"Error printing receipt: {str(e)}")

    def modify_quantity(self):
        selected_index = self.get_selected_cart_index()
        if selected_index is None:
            messagebox.showwarning("Warning", "Please select an item to modify!")
            return
        cart_item = self.cart_items[selected_index]
        
        # Create quantity modification dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Modify Quantity")
        dialog.geometry("300x200")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"300x200+{x}+{y}")
        
        # Content
        content_frame = tk.Frame(dialog, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Item info
        item_label = tk.Label(content_frame, 
                            text=f"Item: {cart_item['generic_name']}\n({cart_item['brand_name']})", 
                            font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50',
                            wraplength=250)
        item_label.pack(pady=(0, 20))
        
        # Current quantity
        current_label = tk.Label(content_frame, 
                               text=f"Current Quantity: {cart_item['quantity']}", 
                               font=('Arial', 11), bg='white', fg='#7f8c8d')
        current_label.pack(pady=(0, 10))
        
        # New quantity input
        quantity_frame = tk.Frame(content_frame, bg='white')
        quantity_frame.pack(pady=(0, 20))
        
        quantity_label = tk.Label(quantity_frame, text="New Quantity:", 
                                font=('Arial', 11), bg='white', fg='#2c3e50')
        quantity_label.pack(side=tk.LEFT, padx=(0, 10))
        
        quantity_var = tk.StringVar(value=str(cart_item['quantity']))
        quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, 
                                font=('Arial', 11), width=10)
        quantity_entry.pack(side=tk.LEFT)
        quantity_entry.focus()
        quantity_entry.select_range(0, tk.END)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=10)
        
        def update_quantity():
            try:
                new_quantity = int(quantity_var.get())
                if new_quantity <= 0:
                    messagebox.showwarning("Warning", "Quantity must be greater than 0!")
                    return
                
                # Get current stock from database
                drug = self.db.get_drug_by_id(cart_item['drug_id'])
                if not drug:
                    messagebox.showerror("Error", "Drug not found in database!")
                    return
                
                if new_quantity > drug['quantity_in_stock']:
                    messagebox.showwarning("Warning", f"Only {drug['quantity_in_stock']} items in stock!")
                    return
                
                # Update cart item
                cart_item['quantity'] = new_quantity
                cart_item['total_price'] = new_quantity * cart_item['unit_price']
                
                self.update_cart_display()
                self.status_callback(f"Updated quantity for {cart_item['generic_name']}")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity!")
        
        update_button = tk.Button(button_frame, text="Update", command=update_quantity,
                                font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                                relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        update_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                                font=('Arial', 11), bg='#95a5a6', fg='white',
                                relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        cancel_button.pack(side=tk.LEFT)
        
        # Bind Enter key to update
        quantity_entry.bind('<Return>', lambda e: update_quantity())
        quantity_entry.bind('<Escape>', lambda e: dialog.destroy())

    def add_to_cart(self):
        """Add drug directly to cart with manual quantity entry"""
        try:
            quantity = int(self.quantity_var.get())
            
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be greater than 0!")
                return
            
            drug = self.current_drug
            if not drug:
                messagebox.showwarning("Warning", "Please select a drug first!")
                return
            
            if quantity > drug['quantity_in_stock']:
                messagebox.showwarning("Warning", f"Only {drug['quantity_in_stock']} items in stock!")
                return
            
            # Check if item already in cart
            for item in self.cart_items:
                if item['drug_id'] == drug['id']:
                    new_quantity = item['quantity'] + quantity
                    if new_quantity > drug['quantity_in_stock']:
                        messagebox.showwarning("Warning", f"Only {drug['quantity_in_stock']} items in stock!")
                        return
                    item['quantity'] = new_quantity
                    item['total_price'] = new_quantity * item['unit_price']
                    self.update_cart_display()
                    self.status_callback(f"Updated quantity for {drug['generic_name']}")
                    return
            
            # Add new item to cart
            cart_item = {
                'drug_id': drug['id'],
                'generic_name': drug['generic_name'],
                'brand_name': drug['brand_name'],
                'quantity': quantity,
                'unit_price': drug['unit_price'],
                'total_price': quantity * drug['unit_price']
            }
            
            self.cart_items.append(cart_item)
            self.update_cart_display()
            self.status_callback(f"Added {quantity}x {drug['generic_name']} to cart")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!") 