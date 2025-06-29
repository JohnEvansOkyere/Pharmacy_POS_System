"""
Database Manager for Ghanaian Pharmacy POS System
Handles all database operations with SQLite
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path="pharmacy.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    def initialize_database(self):
        """Create all necessary tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Drugs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS drugs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generic_name TEXT NOT NULL,
                    brand_name TEXT NOT NULL,
                    dosage TEXT NOT NULL,
                    form TEXT NOT NULL,
                    batch_number TEXT NOT NULL,
                    expiry_date DATE NOT NULL,
                    unit_price REAL NOT NULL,
                    quantity_in_stock INTEGER NOT NULL,
                    reorder_level INTEGER DEFAULT 10,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sales table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receipt_number TEXT UNIQUE NOT NULL,
                    total_amount REAL NOT NULL,
                    payment_method TEXT DEFAULT 'Cash',
                    customer_name TEXT,
                    customer_phone TEXT,
                    cashier_name TEXT NOT NULL,
                    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sale items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    drug_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_price REAL NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id),
                    FOREIGN KEY (drug_id) REFERENCES drugs (id)
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pharmacy_name TEXT DEFAULT 'Ghana Pharmacy',
                    pharmacy_address TEXT DEFAULT '',
                    pharmacy_phone TEXT DEFAULT '',
                    pharmacy_email TEXT DEFAULT '',
                    tax_rate REAL DEFAULT 0.0,
                    currency TEXT DEFAULT 'GHS',
                    receipt_footer TEXT DEFAULT 'Thank you for your purchase!',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.connection.commit()
            
            # Insert default settings if not exists
            cursor.execute("SELECT COUNT(*) FROM settings")
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO settings (pharmacy_name, pharmacy_address, pharmacy_phone, tax_rate)
                    VALUES (?, ?, ?, ?)
                ''', ('Ghana Pharmacy', 'Accra, Ghana', '+233 XX XXX XXXX', 0.0))
            
            # Insert default admin user if not exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO users (username, password, role, full_name)
                    VALUES (?, ?, ?, ?)
                ''', ('admin', 'admin123', 'admin', 'System Administrator'))
            
            # Insert sample drugs if not exists
            cursor.execute("SELECT COUNT(*) FROM drugs")
            if cursor.fetchone()[0] == 0:
                self.insert_sample_drugs()
            
            self.connection.commit()
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            raise
    
    def insert_sample_drugs(self):
        """Insert sample Ghanaian pharmacy drugs"""
        sample_drugs = [
            ('Paracetamol', 'Panadol', '500mg', 'Tablet', 'BATCH001', '2025-12-31', 2.50, 100),
            ('Amoxicillin', 'Amoxil', '250mg', 'Capsule', 'BATCH002', '2025-06-30', 15.00, 50),
            ('Ibuprofen', 'Brufen', '400mg', 'Tablet', 'BATCH003', '2025-08-15', 3.00, 75),
            ('Metronidazole', 'Flagyl', '400mg', 'Tablet', 'BATCH004', '2025-05-20', 8.00, 60),
            ('Artemether/Lumefantrine', 'Coartem', '20/120mg', 'Tablet', 'BATCH005', '2025-10-10', 25.00, 40),
            ('Ciprofloxacin', 'Ciprotab', '500mg', 'Tablet', 'BATCH006', '2025-07-25', 12.00, 30),
            ('Omeprazole', 'Losec', '20mg', 'Capsule', 'BATCH007', '2025-09-30', 18.00, 25),
            ('Cetirizine', 'Zyrtec', '10mg', 'Tablet', 'BATCH008', '2025-11-15', 5.00, 80),
            ('Vitamin C', 'Ascorbic Acid', '1000mg', 'Tablet', 'BATCH009', '2025-12-31', 1.50, 150),
            ('Iron Supplement', 'Ferrous Sulfate', '325mg', 'Tablet', 'BATCH010', '2025-08-20', 4.00, 90)
        ]
        
        cursor = self.connection.cursor()
        for drug in sample_drugs:
            cursor.execute('''
                INSERT INTO drugs (generic_name, brand_name, dosage, form, batch_number, 
                                 expiry_date, unit_price, quantity_in_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', drug)
        
        self.connection.commit()
    
    # Drug Management Methods
    def add_drug(self, drug_data: Dict) -> bool:
        """Add a new drug to inventory"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO drugs (generic_name, brand_name, dosage, form, batch_number,
                                 expiry_date, unit_price, quantity_in_stock, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                drug_data['generic_name'], drug_data['brand_name'], drug_data['dosage'],
                drug_data['form'], drug_data['batch_number'], drug_data['expiry_date'],
                drug_data['unit_price'], drug_data['quantity_in_stock'], drug_data.get('reorder_level', 10)
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding drug: {e}")
            return False
    
    def update_drug(self, drug_id: int, drug_data: Dict) -> bool:
        """Update existing drug information"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE drugs SET generic_name=?, brand_name=?, dosage=?, form=?, 
                               batch_number=?, expiry_date=?, unit_price=?, 
                               quantity_in_stock=?, reorder_level=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (
                drug_data['generic_name'], drug_data['brand_name'], drug_data['dosage'],
                drug_data['form'], drug_data['batch_number'], drug_data['expiry_date'],
                drug_data['unit_price'], drug_data['quantity_in_stock'], 
                drug_data.get('reorder_level', 10), drug_id
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating drug: {e}")
            return False
    
    def get_drug(self, drug_id: int) -> Optional[Dict]:
        """Get drug by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM drugs WHERE id = ?", (drug_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting drug: {e}")
            return None
    
    def get_drug_by_id(self, drug_id: int) -> Optional[Dict]:
        """Get drug by ID (alias for get_drug)"""
        return self.get_drug(drug_id)
    
    def search_drugs(self, search_term: str) -> List[Dict]:
        """Search drugs by name"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM drugs 
                WHERE generic_name LIKE ? OR brand_name LIKE ?
                ORDER BY generic_name
            ''', (f'%{search_term}%', f'%{search_term}%'))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error searching drugs: {e}")
            return []
    
    def get_all_drugs(self) -> List[Dict]:
        """Get all drugs"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM drugs ORDER BY generic_name")
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting all drugs: {e}")
            return []
    
    def update_stock(self, drug_id: int, quantity: int) -> bool:
        """Update drug stock quantity"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE drugs SET quantity_in_stock = quantity_in_stock + ?, 
                               updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (quantity, drug_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def get_low_stock_drugs(self) -> List[Dict]:
        """Get drugs with low stock"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM drugs 
                WHERE quantity_in_stock <= reorder_level
                ORDER BY quantity_in_stock
            ''')
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting low stock drugs: {e}")
            return []
    
    def get_expiring_drugs(self, days: int = 30) -> List[Dict]:
        """Get drugs expiring within specified days"""
        try:
            cursor = self.connection.cursor()
            expiry_date = datetime.now() + timedelta(days=days)
            cursor.execute('''
                SELECT * FROM drugs 
                WHERE expiry_date <= ?
                ORDER BY expiry_date
            ''', (expiry_date.date(),))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting expiring drugs: {e}")
            return []
    
    # Sales Management Methods
    def create_sale(self, sale_data: Dict) -> Optional[int]:
        """Create a new sale transaction"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO sales (receipt_number, total_amount, payment_method, 
                                 customer_name, customer_phone, cashier_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sale_data['receipt_number'], sale_data['total_amount'],
                sale_data.get('payment_method', 'Cash'), sale_data.get('customer_name', ''),
                sale_data.get('customer_phone', ''), sale_data['cashier_name']
            ))
            sale_id = cursor.lastrowid
            self.connection.commit()
            return sale_id
        except Exception as e:
            print(f"Error creating sale: {e}")
            return None
    
    def add_sale_item(self, sale_id: int, item_data: Dict) -> bool:
        """Add item to sale"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO sale_items (sale_id, drug_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                sale_id, item_data['drug_id'], item_data['quantity'],
                item_data['unit_price'], item_data['total_price']
            ))
            
            # Update stock
            cursor.execute('''
                UPDATE drugs SET quantity_in_stock = quantity_in_stock - ?
                WHERE id = ?
            ''', (item_data['quantity'], item_data['drug_id']))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding sale item: {e}")
            return False
    
    def get_sale(self, sale_id: int) -> Optional[Dict]:
        """Get sale by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
            sale = cursor.fetchone()
            if sale:
                sale_dict = dict(sale)
                # Get sale items
                cursor.execute('''
                    SELECT si.*, d.generic_name, d.brand_name, d.dosage, d.form
                    FROM sale_items si
                    JOIN drugs d ON si.drug_id = d.id
                    WHERE si.sale_id = ?
                ''', (sale_id,))
                sale_dict['items'] = [dict(row) for row in cursor.fetchall()]
                return sale_dict
            return None
        except Exception as e:
            print(f"Error getting sale: {e}")
            return None
    
    def get_sales_by_date(self, start_date: str, end_date: str) -> List[Dict]:
        """Get sales within date range"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM sales 
                WHERE DATE(sale_date) BETWEEN ? AND ?
                ORDER BY sale_date DESC
            ''', (start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting sales by date: {e}")
            return []
    
    def get_daily_sales(self, date: str) -> Dict:
        """Get daily sales summary"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT COUNT(*) as total_transactions,
                       SUM(total_amount) as total_amount
                FROM sales 
                WHERE DATE(sale_date) = ?
            ''', (date,))
            result = cursor.fetchone()
            return dict(result) if result else {'total_transactions': 0, 'total_amount': 0}
        except Exception as e:
            print(f"Error getting daily sales: {e}")
            return {'total_transactions': 0, 'total_amount': 0}
    
    # Settings Methods
    def get_settings(self) -> Dict:
        """Get system settings"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM settings ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else {}
        except Exception as e:
            print(f"Error getting settings: {e}")
            return {}
    
    def update_settings(self, settings_data: Dict) -> bool:
        """Update system settings"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE settings SET pharmacy_name=?, pharmacy_address=?, pharmacy_phone=?,
                                 pharmacy_email=?, tax_rate=?, currency=?, receipt_footer=?,
                                 updated_at=CURRENT_TIMESTAMP
                WHERE id = (SELECT id FROM settings ORDER BY id DESC LIMIT 1)
            ''', (
                settings_data.get('pharmacy_name', ''),
                settings_data.get('pharmacy_address', ''),
                settings_data.get('pharmacy_phone', ''),
                settings_data.get('pharmacy_email', ''),
                settings_data.get('tax_rate', 0.0),
                settings_data.get('currency', 'GHS'),
                settings_data.get('receipt_footer', '')
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def generate_receipt_number(self) -> str:
        """Generate unique receipt number"""
        try:
            cursor = self.connection.cursor()
            today = datetime.now().strftime("%Y%m%d")
            cursor.execute('''
                SELECT COUNT(*) FROM sales 
                WHERE receipt_number LIKE ?
            ''', (f'{today}%',))
            count = cursor.fetchone()[0]
            return f"{today}{count+1:04d}"
        except Exception as e:
            print(f"Error generating receipt number: {e}")
            return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close() 