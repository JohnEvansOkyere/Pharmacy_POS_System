#!/usr/bin/env python3
"""
Installation Script for Ghanaian Pharmacy POS System
Automates the setup and configuration process
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("    GHANA PHARMACY POS SYSTEM - INSTALLATION")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    
    try:
        # Install packages from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: requirements.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        "backups",
        "logs",
        "exports",
        "receipts"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory exists: {directory}")

def initialize_database():
    """Initialize the database with sample data"""
    print("\nInitializing database...")
    
    try:
        # Import and initialize database
        from database import DatabaseManager
        
        db = DatabaseManager()
        db.initialize_database()
        db.close()
        
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def create_shortcuts():
    """Create desktop shortcuts and start menu entries"""
    print("\nCreating shortcuts...")
    
    try:
        # Create batch file for Windows
        if os.name == 'nt':  # Windows
            batch_content = '''@echo off
cd /d "%~dp0"
python main.py
pause
'''
            with open("Start Pharmacy POS.bat", "w") as f:
                f.write(batch_content)
            print("✅ Created Windows batch file")
        
        # Create shell script for Linux
        else:  # Linux/Unix
            script_content = '''#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
'''
            with open("start_pharmacy_pos.sh", "w") as f:
                f.write(script_content)
            
            # Make executable
            os.chmod("start_pharmacy_pos.sh", 0o755)
            print("✅ Created Linux shell script")
            
    except Exception as e:
        print(f"⚠️  Warning: Could not create shortcuts: {e}")

def create_config_file():
    """Create default configuration file"""
    print("\nCreating configuration file...")
    
    config = {
        "version": "1.0.0",
        "install_date": datetime.now().isoformat(),
        "database_path": "pharmacy.db",
        "backup_directory": "backups",
        "log_directory": "logs",
        "export_directory": "exports",
        "receipt_directory": "receipts",
        "auto_backup": True,
        "backup_frequency": "daily",
        "max_backups": 10,
        "default_currency": "GHS",
        "default_tax_rate": 0.0,
        "receipt_width": 40,
        "show_logo": False,
        "show_tax": True,
        "show_cashier": True
    }
    
    try:
        import json
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration file created")
        return True
    except Exception as e:
        print(f"❌ Error creating config file: {e}")
        return False

def run_system_check():
    """Run system compatibility check"""
    print("\nRunning system check...")
    
    checks = []
    
    # Check available disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        if free_gb >= 1:
            checks.append(f"✅ Disk space: {free_gb}GB available")
        else:
            checks.append(f"⚠️  Disk space: Only {free_gb}GB available (1GB recommended)")
    except:
        checks.append("⚠️  Could not check disk space")
    
    # Check write permissions
    try:
        test_file = "test_write.tmp"
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        checks.append("✅ Write permissions: OK")
    except:
        checks.append("❌ Write permissions: Failed")
    
    # Check SQLite
    try:
        import sqlite3
        checks.append("✅ SQLite: Available")
    except:
        checks.append("❌ SQLite: Not available")
    
    # Check tkinter
    try:
        import tkinter
        checks.append("✅ Tkinter: Available")
    except:
        checks.append("❌ Tkinter: Not available")
    
    for check in checks:
        print(f"   {check}")

def create_user_manual():
    """Create a basic user manual"""
    print("\nCreating user manual...")
    
    manual_content = """# Ghanaian Pharmacy POS System - User Manual

## Quick Start Guide

### 1. Starting the System
- Double-click "Start Pharmacy POS.bat" (Windows) or "start_pharmacy_pos.sh" (Linux)
- Or run: python main.py

### 2. Default Login
- Username: admin
- Password: admin123

### 3. Making Your First Sale
1. Click "POS Sales"
2. Search for a drug or use quick-add buttons
3. Add items to cart
4. Enter customer details (optional)
5. Click "COMPLETE SALE"

### 4. Managing Inventory
1. Click "Inventory"
2. Add new drugs or update existing ones
3. Monitor stock levels and expiry dates
4. Set reorder levels for alerts

### 5. Generating Reports
1. Click "Reports"
2. Select date range
3. View sales summaries and analytics
4. Export data as needed

## Important Notes

- Always backup your data regularly
- Check inventory alerts daily
- Keep your system updated
- Contact support if you encounter issues

## Support Contact
- Email: support@ghanapharmacypos.com
- Phone: +233 XX XXX XXXX
"""
    
    try:
        with open("USER_MANUAL.md", "w", encoding="utf-8") as f:
            f.write(manual_content)
        print("✅ User manual created")
        return True
    except Exception as e:
        print(f"❌ Error creating user manual: {e}")
        return False

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation failed: Python version incompatible")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed: Could not install dependencies")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Installation failed: Could not initialize database")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Create shortcuts
    create_shortcuts()
    
    # Create config file
    if not create_config_file():
        print("\n⚠️  Warning: Could not create configuration file")
    
    # Run system check
    run_system_check()
    
    # Create user manual
    create_user_manual()
    
    # Installation complete
    print("\n" + "=" * 60)
    print("    INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("🎉 Ghanaian Pharmacy POS System is ready to use!")
    print()
    print("📋 Next Steps:")
    print("1. Run the application: python main.py")
    print("2. Login with default credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("3. Configure your pharmacy information in Settings")
    print("4. Add your drug inventory")
    print("5. Start making sales!")
    print()
    print("📚 Documentation:")
    print("- README.md - Complete system documentation")
    print("- USER_MANUAL.md - Quick start guide")
    print()
    print("🆘 Support:")
    print("- Email: support@ghanapharmacypos.com")
    print("- Phone: +233 XX XXX XXXX")
    print()
    
    # Ask if user wants to start the application
    response = input("Would you like to start the application now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("\nStarting Ghanaian Pharmacy POS System...")
        try:
            subprocess.run([sys.executable, "main.py"])
        except Exception as e:
            print(f"Error starting application: {e}")
            print("You can start it manually by running: python main.py")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 