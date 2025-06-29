# Ghanaian Pharmacy POS System

A comprehensive, offline Point of Sale (POS) system specifically designed for Ghanaian pharmacy operations. This system provides complete drug inventory management, sales processing, reporting, and business analytics in a user-friendly desktop application.

## 🏥 Features

### Core POS Functionality
- **Intuitive Sales Interface**: Fast drug search, quick-add buttons, and real-time cart management
- **Payment Processing**: Cash payments with automatic change calculation
- **Professional Receipts**: Customizable receipt printing with pharmacy branding
- **Customer Management**: Track customer information and purchase history

### Inventory Management
- **Complete Drug Database**: Store generic names, brand names, dosages, forms, batch numbers, and expiry dates
- **Stock Management**: Real-time inventory tracking with automatic stock updates
- **Alerts & Notifications**: Low stock warnings and expiry date alerts
- **Batch Tracking**: Monitor batch numbers and expiry dates for compliance

### Sales & Analytics
- **Sales History**: Complete transaction records with search and filtering
- **Daily Reports**: Real-time sales dashboard with daily summaries
- **Business Analytics**: Sales trends, best-selling products, and performance metrics
- **Export Capabilities**: Export reports to CSV/Excel format

### System Features
- **100% Offline**: No internet dependency - works completely offline
- **Data Backup**: Automatic and manual backup/restore functionality
- **User Management**: Role-based access control (Admin/Cashier)
- **Customizable Settings**: Pharmacy information, tax rates, receipt format
- **Ghanaian Context**: Local currency (GHS), common drug names, and local workflow patterns

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 or Ubuntu Desktop
- Minimum 4GB RAM
- 500MB free disk space

### Quick Installation

1. **Clone or Download the Repository**
   ```bash
   git clone <repository-url>
   cd pharmacy_gysbin
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### First-Time Setup

1. **Launch the Application**
   - The system will automatically create the database and sample data
   - Default admin credentials: Username: `admin`, Password: `admin123`

2. **Configure Pharmacy Information**
   - Go to Settings → Pharmacy Information
   - Enter your pharmacy details, contact information, and license number

3. **Customize System Settings**
   - Set your preferred currency (default: GHS)
   - Configure tax rates if applicable
   - Set up receipt format and branding

4. **Add Your Drug Inventory**
   - Use the Inventory screen to add your drugs
   - Sample data is included to get you started
   - Import existing inventory using the bulk import feature

## 📋 System Requirements

### Hardware Requirements
- **Processor**: Intel Core i3 or equivalent
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Display**: 1024x768 minimum resolution, 1920x1080 recommended

### Software Requirements
- **Operating System**: Windows 10/11 or Ubuntu 20.04+
- **Python**: 3.8 or higher
- **Database**: SQLite (included)
- **Printer**: Any Windows/Linux compatible printer for receipts

## 🎯 Quick Start Guide

### Making Your First Sale

1. **Open the POS Screen**
   - Click "POS Sales" in the main navigation

2. **Search for a Drug**
   - Type the drug name in the search bar
   - Or click on quick-add buttons for common drugs

3. **Add to Cart**
   - Select the drug and enter quantity
   - Click "Add to Cart"

4. **Complete the Sale**
   - Enter customer information (optional)
   - Select payment method
   - Click "COMPLETE SALE"

### Managing Inventory

1. **Add New Drugs**
   - Go to Inventory → Add New Drug
   - Fill in all required information
   - Set reorder levels for automatic alerts

2. **Update Stock**
   - Select a drug and click "Update Stock"
   - Enter the quantity adjustment (+ or -)

3. **Monitor Alerts**
   - Check the alerts section for low stock and expiring drugs
   - Take action to reorder or dispose of expired items

### Generating Reports

1. **Daily Summary**
   - Go to Reports → Today's Report
   - View sales summary and key metrics

2. **Custom Reports**
   - Select date range for detailed analysis
   - Export data to CSV for further analysis

3. **Inventory Reports**
   - Check inventory status and alerts
   - Generate stock reports for ordering

## 🔧 Configuration

### Pharmacy Settings
- **Pharmacy Information**: Name, address, phone, email, license number
- **System Settings**: Currency, tax rates, language, date format
- **Receipt Settings**: Header, footer, logo, receipt width
- **Backup Settings**: Auto backup frequency and location

### User Management
- **Admin Role**: Full system access, settings, reports
- **Cashier Role**: POS sales, basic inventory view
- **Password Management**: Secure password policies

### Receipt Customization
- **Header Text**: Pharmacy name and branding
- **Footer Text**: Thank you message, contact information
- **Logo**: Add pharmacy logo to receipts
- **Format**: Customize receipt width and layout

## 📊 Database Schema

### Core Tables
- **drugs**: Drug inventory with all details
- **sales**: Transaction records
- **sale_items**: Individual items in each sale
- **settings**: System configuration
- **users**: User accounts and permissions

### Sample Data
The system includes sample Ghanaian pharmacy drugs:
- Paracetamol (Panadol)
- Amoxicillin (Amoxil)
- Ibuprofen (Brufen)
- Metronidazole (Flagyl)
- Artemether/Lumefantrine (Coartem)
- And more...

## 🔒 Security Features

- **Data Integrity**: SQLite transactions prevent data corruption
- **Backup Protection**: Automatic and manual backup systems
- **User Authentication**: Role-based access control
- **Offline Security**: No internet vulnerabilities

## 📈 Performance

- **Fast Response**: All operations under 2 seconds
- **Memory Efficient**: Optimized for basic hardware
- **Scalable**: Handles 100+ transactions per day
- **Reliable**: No crashes during critical operations

## 🛠️ Troubleshooting

### Common Issues

1. **Application Won't Start**
   - Check Python version (3.8+ required)
   - Verify all dependencies are installed
   - Check file permissions

2. **Database Errors**
   - Run database validation: `python -c "from utils import validate_database; print(validate_database())"`
   - Restore from backup if needed

3. **Printer Issues**
   - Check printer drivers
   - Verify printer is set as default
   - Test with Windows/Linux print dialog

4. **Performance Issues**
   - Close other applications
   - Check available RAM
   - Clean up old backup files

### Support

For technical support:
- **Email**: support@ghanapharmacypos.com
- **Phone**: +233 XX XXX XXXX
- **Documentation**: See the user manual in the docs folder

## 🔄 Updates & Maintenance

### Regular Maintenance
- **Daily**: Check inventory alerts
- **Weekly**: Review sales reports
- **Monthly**: Create full system backup
- **Quarterly**: Clean up old data and optimize database

### Backup Strategy
- **Automatic**: Daily backups to local folder
- **Manual**: Create backups before major changes
- **Offsite**: Copy backups to external storage
- **Testing**: Regularly test backup restoration

## 📝 License

This software is licensed under the MIT License. See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## 📞 Contact

- **Developer**: Ghana Pharmacy POS Team
- **Email**: info@ghanapharmacypos.com
- **Website**: www.ghanapharmacypos.com
- **Support**: support@ghanapharmacypos.com

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Compatibility**: Windows 10/11, Ubuntu 20.04+  
**Database**: SQLite 3.x 