#!/usr/bin/env python3
"""
Test script to see what real jobs are being found
"""

from job_mailer import JobMailer
import json

def test_real_job_search():
    """Test the real job search functionality"""
    print("🔍 Testing Real Job Search...")
    print("=" * 50)
    
    job_mailer = JobMailer()
    
    # Test individual sources
    print("\n📍 Testing Internshala...")
    internshala_jobs = job_mailer.search_internshala_jobs()
    print(f"Found {len(internshala_jobs)} jobs from Internshala")
    for job in internshala_jobs[:2]:
        print(f"  • {job['title']} at {job['company']} - {job['url']}")
    
    print("\n📍 Testing Unstop...")
    unstop_jobs = job_mailer.search_unstop_jobs()
    print(f"Found {len(unstop_jobs)} jobs from Unstop")
    for job in unstop_jobs[:2]:
        print(f"  • {job['title']} at {job['company']} - {job['url']}")
    
    print("\n📍 Testing Indeed...")
    indeed_jobs = job_mailer.search_indeed_jobs()
    print(f"Found {len(indeed_jobs)} jobs from Indeed")
    for job in indeed_jobs[:2]:
        print(f"  • {job['title']} at {job['company']} - {job['url']}")
    
    # Test combined search
    print("\n🔍 Testing Combined Search...")
    all_jobs = job_mailer.search_all_jobs()
    print(f"Total unique jobs found: {len(all_jobs)}")
    
    print("\n📋 Sample Job Listings:")
    print("=" * 50)
    for i, job in enumerate(all_jobs[:5], 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}")
        print()

if __name__ == "__main__":
    test_real_job_search()
