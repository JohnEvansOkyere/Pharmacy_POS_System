#!/usr/bin/env python3
"""
Test Script for Ghanaian Pharmacy POS System
Verifies all components are working correctly
"""

import sys
import os
import sqlite3
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    
    modules = [
        'tkinter',
        'sqlite3',
        'datetime',
        'reportlab',
        'PIL',
        'tkcalendar'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        print("Please install missing packages: pip install -r requirements.txt")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    print("\nTesting database...")
    
    try:
        from database import DatabaseManager
        
        # Test database connection
        db = DatabaseManager()
        print("✅ Database connection")
        
        # Test database initialization
        db.initialize_database()
        print("✅ Database initialization")
        
        # Test basic operations
        settings = db.get_settings()
        if settings:
            print("✅ Settings retrieval")
        
        drugs = db.get_all_drugs()
        if drugs:
            print(f"✅ Drug data: {len(drugs)} drugs found")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\nTesting utility functions...")
    
    try:
        from utils import format_currency, format_date, validate_email, validate_phone
        
        # Test currency formatting
        result = format_currency(123.45, "GHS")
        if result == "GHS 123.45":
            print("✅ Currency formatting")
        else:
            print(f"❌ Currency formatting: expected 'GHS 123.45', got '{result}'")
            return False
        
        # Test date formatting
        result = format_date("2024-12-01")
        if result == "2024-12-01":
            print("✅ Date formatting")
        else:
            print(f"❌ Date formatting: expected '2024-12-01', got '{result}'")
            return False
        
        # Test email validation
        if validate_email("test@example.com"):
            print("✅ Email validation")
        else:
            print("❌ Email validation")
            return False
        
        # Test phone validation
        if validate_phone("+233123456789"):
            print("✅ Phone validation")
        else:
            print("❌ Phone validation")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'database.py',
        'pos_screen.py',
        'inventory_screen.py',
        'sales_history_screen.py',
        'reports_screen.py',
        'settings_screen.py',
        'utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist or can be created"""
    print("\nTesting directories...")
    
    directories = [
        'backups',
        'logs',
        'exports',
        'receipts'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✅ Created {directory}")
            except Exception as e:
                print(f"❌ Could not create {directory}: {e}")
                return False
        else:
            print(f"✅ {directory} exists")
    
    return True

def test_database_integrity():
    """Test database integrity"""
    print("\nTesting database integrity...")
    
    try:
        from utils import validate_database
        
        result = validate_database()
        
        if result.get('valid', False):
            print("✅ Database integrity check passed")
            return True
        else:
            print(f"❌ Database integrity check failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Database integrity test failed: {e}")
        return False

def test_sample_data():
    """Test if sample data is properly loaded"""
    print("\nTesting sample data...")
    
    try:
        from database import DatabaseManager
        
        db = DatabaseManager()
        
        # Check drugs
        drugs = db.get_all_drugs()
        if len(drugs) >= 10:
            print(f"✅ Sample drugs: {len(drugs)} drugs loaded")
        else:
            print(f"⚠️  Sample drugs: Only {len(drugs)} drugs found (expected 10+)")
        
        # Check settings
        settings = db.get_settings()
        if settings:
            print("✅ Default settings loaded")
        else:
            print("⚠️  No default settings found")
        
        # Check users
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            print(f"✅ Users: {user_count} users found")
        else:
            print("⚠️  No users found")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def run_performance_test():
    """Run basic performance tests"""
    print("\nRunning performance tests...")
    
    try:
        from database import DatabaseManager
        import time
        
        db = DatabaseManager()
        
        # Test search performance
        start_time = time.time()
        drugs = db.search_drugs("para")
        search_time = time.time() - start_time
        
        if search_time < 1.0:
            print(f"✅ Search performance: {search_time:.3f}s")
        else:
            print(f"⚠️  Search performance: {search_time:.3f}s (slow)")
        
        # Test database size
        db_size = os.path.getsize("pharmacy.db") / (1024 * 1024)  # MB
        print(f"✅ Database size: {db_size:.2f} MB")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("    GHANA PHARMACY POS SYSTEM - SYSTEM TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Directories", test_directories),
        ("Database", test_database),
        ("Database Integrity", test_database_integrity),
        ("Sample Data", test_sample_data),
        ("Utility Functions", test_utils),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"    TEST RESULTS: {passed}/{total} TESTS PASSED")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nTo start the application, run:")
        print("   python main.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run installation script: python install.py")
        print("3. Check file permissions and disk space")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main() 