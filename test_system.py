#!/usr/bin/env python3
"""
Test script for the Automated Job Notification System
"""

import json
import sys
import os
from datetime import datetime

def test_config():
    """Test if configuration is properly set up"""
    print("🔧 Testing configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check email config
        email_config = config.get('email', {})
        sender = email_config.get('sender_email', '')
        password = email_config.get('app_password', '')
        receiver = email_config.get('receiver_email', '')
        
        if sender == 'your_email@gmail.com' or not sender:
            print("❌ Sender email not configured")
            return False
        
        if password == 'your_gmail_app_password' or not password:
            print("❌ Gmail App Password not configured")
            return False
        
        if not receiver:
            print("❌ Receiver email not configured")
            return False
        
        print(f"✅ Email configured: {sender} -> {receiver}")
        
        # Check job search config
        keywords = config.get('job_search', {}).get('keywords', [])
        locations = config.get('job_search', {}).get('locations', [])
        
        print(f"✅ Job keywords: {len(keywords)} configured")
        print(f"✅ Job locations: {len(locations)} configured")
        
        return True
        
    except FileNotFoundError:
        print("❌ config.json not found")
        return False
    except json.JSONDecodeError:
        print("❌ config.json is not valid JSON")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing dependencies...")

    required_packages = [
        ('schedule', 'schedule'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('lxml', 'lxml')
    ]
    missing_packages = []

    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} missing")
            missing_packages.append(package_name)

    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False

    return True

def test_job_mailer():
    """Test the JobMailer class"""
    print("\n🤖 Testing JobMailer...")
    
    try:
        from job_mailer import JobMailer
        
        job_mailer = JobMailer()
        print("✅ JobMailer initialized successfully")
        
        # Test job search
        jobs = job_mailer.get_mock_jobs()
        print(f"✅ Mock job search returned {len(jobs)} jobs")
        
        # Test email formatting
        email_body = job_mailer.format_email_body(jobs)
        print("✅ Email formatting works")
        
        return True
        
    except Exception as e:
        print(f"❌ JobMailer test failed: {e}")
        return False

def test_email_sending():
    """Test email sending (optional)"""
    print("\n📧 Email sending test...")
    
    choice = input("Do you want to send a test email? (y/n): ").lower().strip()
    
    if choice != 'y':
        print("⏭️ Skipping email test")
        return True
    
    try:
        from job_mailer import JobMailer
        
        job_mailer = JobMailer()
        
        # Create a test job
        test_jobs = [{
            "title": "Test Job - System Verification",
            "company": "Test Company",
            "location": "Remote",
            "url": "https://example.com/test",
            "description": "This is a test email to verify the system is working",
            "posted_date": datetime.now().strftime('%Y-%m-%d'),
            "source": "System Test"
        }]
        
        job_mailer.send_email(test_jobs)
        print("✅ Test email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("Check your email configuration and internet connection")
        return False

def main():
    """Run all tests"""
    print("🧪 Automated Job Notification System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies),
        ("JobMailer Class", test_job_mailer),
        ("Email Sending", test_email_sending)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your system is ready to run.")
        print("\nTo start the job notifier:")
        print("python job_mailer.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before running the system.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
