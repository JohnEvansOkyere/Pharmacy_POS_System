"""
Utilities for Ghanaian Pharmacy POS System
Backup, restore, and other utility functions
"""

import os
import shutil
import sqlite3
from datetime import datetime
import zipfile
import json

def create_backup():
    """
    Create a backup of the pharmacy database and settings
    
    Returns:
        str: Path to the created backup file
    """
    try:
        # Create backups directory if it doesn't exist
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"pharmacy_backup_{timestamp}.backup"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Create backup archive
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # Add database file
            if os.path.exists("pharmacy.db"):
                backup_zip.write("pharmacy.db", "pharmacy.db")
            
            # Add settings file if exists
            if os.path.exists("settings.json"):
                backup_zip.write("settings.json", "settings.json")
            
            # Add backup metadata
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "version": "1.0.0",
                "description": "Ghanaian Pharmacy POS System Backup"
            }
            
            backup_zip.writestr("metadata.json", json.dumps(metadata, indent=2))
        
        return backup_path
        
    except Exception as e:
        raise Exception(f"Failed to create backup: {str(e)}")

def restore_backup(backup_path):
    """
    Restore pharmacy data from a backup file
    
    Args:
        backup_path (str): Path to the backup file
        
    Returns:
        bool: True if restore was successful, False otherwise
    """
    try:
        # Verify backup file exists
        if not os.path.exists(backup_path):
            raise Exception("Backup file not found")
        
        # Create temporary directory for extraction
        temp_dir = "temp_restore"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Extract backup
        with zipfile.ZipFile(backup_path, 'r') as backup_zip:
            backup_zip.extractall(temp_dir)
        
        # Verify backup contents
        if not os.path.exists(os.path.join(temp_dir, "pharmacy.db")):
            raise Exception("Invalid backup: database file not found")
        
        # Create backup of current database before restore
        if os.path.exists("pharmacy.db"):
            current_backup = f"pharmacy.db.before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2("pharmacy.db", current_backup)
        
        # Restore database
        shutil.copy2(os.path.join(temp_dir, "pharmacy.db"), "pharmacy.db")
        
        # Restore settings if exists
        if os.path.exists(os.path.join(temp_dir, "settings.json")):
            shutil.copy2(os.path.join(temp_dir, "settings.json"), "settings.json")
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise Exception(f"Failed to restore backup: {str(e)}")

def validate_database():
    """
    Validate the pharmacy database integrity
    
    Returns:
        dict: Validation results
    """
    try:
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        
        # Check if required tables exist
        required_tables = ['drugs', 'sales', 'sale_items', 'settings', 'users']
        existing_tables = []
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for row in cursor.fetchall():
            existing_tables.append(row[0])
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        # Check database integrity
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "valid": len(missing_tables) == 0 and integrity_result == "ok",
            "missing_tables": missing_tables,
            "integrity_check": integrity_result
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }

def format_currency(amount, currency="GHS"):
    """
    Format amount as currency
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    try:
        if currency == "GHS":
            return f"GHS {amount:.2f}"
        elif currency == "USD":
            return f"${amount:.2f}"
        elif currency == "EUR":
            return f"€{amount:.2f}"
        elif currency == "GBP":
            return f"£{amount:.2f}"
        else:
            return f"{amount:.2f}"
    except:
        return str(amount)

def format_date(date_string, format_type="YYYY-MM-DD"):
    """
    Format date string
    
    Args:
        date_string (str): Date string to format
        format_type (str): Desired format
        
    Returns:
        str: Formatted date string
    """
    try:
        if not date_string:
            return ""
        
        # Parse the date
        if "T" in date_string:
            # ISO format
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        else:
            # Try different formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    dt = datetime.strptime(date_string, fmt)
                    break
                except ValueError:
                    continue
            else:
                return date_string
        
        # Format according to preference
        if format_type == "YYYY-MM-DD":
            return dt.strftime("%Y-%m-%d")
        elif format_type == "DD/MM/YYYY":
            return dt.strftime("%d/%m/%Y")
        elif format_type == "MM/DD/YYYY":
            return dt.strftime("%m/%d/%Y")
        else:
            return dt.strftime("%Y-%m-%d")
            
    except Exception:
        return date_string

def calculate_tax(amount, tax_rate):
    """
    Calculate tax amount
    
    Args:
        amount (float): Base amount
        tax_rate (float): Tax rate as percentage
        
    Returns:
        float: Tax amount
    """
    try:
        return amount * (tax_rate / 100)
    except:
        return 0.0

def calculate_total_with_tax(amount, tax_rate):
    """
    Calculate total amount including tax
    
    Args:
        amount (float): Base amount
        tax_rate (float): Tax rate as percentage
        
    Returns:
        float: Total amount including tax
    """
    try:
        tax = calculate_tax(amount, tax_rate)
        return amount + tax
    except:
        return amount

def validate_email(email):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Validate phone number format (Ghanaian format)
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    # Remove spaces, dashes, and parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for Ghanaian phone number patterns
    patterns = [
        r'^\+233[0-9]{9}$',  # +233XXXXXXXXX
        r'^233[0-9]{9}$',    # 233XXXXXXXXX
        r'^0[0-9]{9}$',      # 0XXXXXXXXX
        r'^[0-9]{10}$'       # XXXXXXXXXX
    ]
    
    return any(re.match(pattern, phone) for pattern in patterns)

def format_phone(phone):
    """
    Format phone number to standard Ghanaian format
    
    Args:
        phone (str): Phone number to format
        
    Returns:
        str: Formatted phone number
    """
    import re
    
    # Remove spaces, dashes, and parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Convert to standard format
    if phone.startswith('+233'):
        return phone
    elif phone.startswith('233'):
        return '+' + phone
    elif phone.startswith('0'):
        return '+233' + phone[1:]
    elif len(phone) == 10:
        return '+233' + phone
    else:
        return phone

def get_file_size_mb(file_path):
    """
    Get file size in megabytes
    
    Args:
        file_path (str): Path to file
        
    Returns:
        float: File size in MB
    """
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        return 0.0
    except:
        return 0.0

def get_database_size():
    """
    Get pharmacy database size
    
    Returns:
        float: Database size in MB
    """
    return get_file_size_mb("pharmacy.db")

def cleanup_old_backups(max_backups=10):
    """
    Clean up old backup files, keeping only the most recent ones
    
    Args:
        max_backups (int): Maximum number of backups to keep
    """
    try:
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            return
        
        # Get all backup files
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.endswith('.backup'):
                file_path = os.path.join(backup_dir, file)
                backup_files.append((file_path, os.path.getmtime(file_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        for file_path, _ in backup_files[max_backups:]:
            try:
                os.remove(file_path)
            except:
                pass
                
    except Exception as e:
        print(f"Error cleaning up old backups: {e}")

def export_to_csv(data, filename, headers=None):
    """
    Export data to CSV file
    
    Args:
        data (list): List of data rows
        filename (str): Output filename
        headers (list): Column headers
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if headers:
                writer.writerow(headers)
            
            for row in data:
                writer.writerow(row)
        
        return True
        
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def log_activity(activity, user="System"):
    """
    Log system activity
    
    Args:
        activity (str): Activity description
        user (str): User performing the activity
    """
    try:
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"activity_{datetime.now().strftime('%Y%m')}.log")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {user}: {activity}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
    except Exception as e:
        print(f"Error logging activity: {e}")

def get_system_info():
    """
    Get system information
    
    Returns:
        dict: System information
    """
    import platform
    
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "hostname": platform.node()
    } 