#!/usr/bin/env python3
"""
Setup script for the Automated Job Notification System
"""

import json
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def setup_email_config():
    """Guide user through email configuration"""
    print("\n🔧 Setting up email configuration...")
    print("You'll need to set up Gmail App Password for this to work.")
    print("Follow these steps:")
    print("1. Go to https://myaccount.google.com/apppasswords")
    print("2. Generate an App Password for 'Mail'")
    print("3. Use that 16-character password below")
    
    sender_email = input("\nEnter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    # Load and update config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    config['email']['sender_email'] = sender_email
    config['email']['app_password'] = app_password
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("✅ Email configuration saved!")
    return True

def test_email():
    """Test email configuration"""
    print("\n📧 Testing email configuration...")
    try:
        from job_mailer import JobMailer
        job_mailer = JobMailer()
        
        # Send a test email with mock jobs
        test_jobs = [{
            "title": "Test Job",
            "company": "Test Company", 
            "location": "Remote",
            "url": "https://example.com",
            "description": "This is a test email",
            "posted_date": "2024-01-01",
            "source": "Setup Test"
        }]
        
        job_mailer.send_email(test_jobs)
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Test email failed: {e}")
        return False

def create_startup_script():
    """Create a startup script for Windows"""
    script_content = f"""@echo off
cd /d "{os.getcwd()}"
python job_mailer.py
pause
"""
    
    with open('start_job_mailer.bat', 'w') as f:
        f.write(script_content)
    
    print("✅ Created start_job_mailer.bat for easy startup")

def main():
    print("🚀 Automated Job Notification System Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup email config
    if not setup_email_config():
        return
    
    # Test email
    test_choice = input("\nWould you like to send a test email? (y/n): ").lower()
    if test_choice == 'y':
        test_email()
    
    # Create startup script
    create_startup_script()
    
    print("\n🎉 Setup complete!")
    print("\nTo start the job notifier:")
    print("1. Double-click 'start_job_mailer.bat', or")
    print("2. Run 'python job_mailer.py' in terminal")
    print("\nThe system will:")
    print("- Search for jobs daily at 5:30 PM IST")
    print("- Send results to vantharamsuryagayathri.22.cse@anits.edu.in")
    print("- Log all activities to job_mailer.log")

if __name__ == "__main__":
    main()
