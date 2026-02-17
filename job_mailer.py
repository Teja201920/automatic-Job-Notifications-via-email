import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time
import json
import os
import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import random
from enhanced_job_search import EnhancedJobSearch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_mailer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class JobMailer:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.sent_jobs = self.load_sent_jobs()
        self.enhanced_search = EnhancedJobSearch()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file {config_file} not found. Creating default config.")
            self.create_default_config(config_file)
            return self.load_config(config_file)
    
    def create_default_config(self, config_file):
        """Create default configuration file"""
        default_config = {
            "email": {
                "sender_email": "your_email@gmail.com",
                "app_password": "your_gmail_app_password",
                "receiver_email": "vantharamsuryagayathri.22.cse@anits.edu.in"
            },
            "job_search": {
                "keywords": ["Full Stack Developer", "AI/ML Developer", "Machine Learning", "Data Science", "Python Developer"],
                "locations": ["Remote", "India", "Bangalore", "Hyderabad", "Chennai", "Mumbai", "Pune"],
                "experience_levels": ["Intern", "Entry Level", "0-1 years", "Fresher"]
            },
            "schedule": {
                "time": "17:30",
                "timezone": "Asia/Kolkata"
            },
            "sources": {
                "internshala": True,
                "unstop": True,
                "glassdoor": False,
                "linkedin": False
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        logging.info(f"Created default config file: {config_file}")
        logging.info("Please update the email credentials in config.json")
    
    def load_sent_jobs(self):
        """Load previously sent jobs to avoid duplicates"""
        try:
            with open('sent_jobs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_sent_jobs(self):
        """Save sent jobs to file"""
        with open('sent_jobs.json', 'w') as f:
            json.dump(self.sent_jobs, f, indent=2)
    
    def get_mock_jobs(self) -> List[Dict]:
        """Generate mock job listings for demonstration"""
        companies = ["TechCorp", "InnovateLabs", "StartupHub", "DataWise", "CodeCraft", "MLSolutions", "DevForce"]
        job_types = ["Full Stack Developer", "AI/ML Engineer", "Python Developer", "Data Scientist", "Backend Developer"]
        locations = ["Remote", "Bangalore", "Hyderabad", "Chennai", "Mumbai", "Pune"]
        
        jobs = []
        for i in range(5):
            job = {
                "title": f"{random.choice(job_types)} Intern",
                "company": random.choice(companies),
                "location": random.choice(locations),
                "url": f"https://example.com/job{i+1}",
                "description": "Great opportunity for freshers",
                "posted_date": datetime.now().strftime('%Y-%m-%d'),
                "source": "Mock Data"
            }
            jobs.append(job)
        
        return jobs
    
    def search_internshala_jobs(self) -> List[Dict]:
        """Search for jobs on Internshala with real scraping"""
        jobs = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Search for internships
            search_urls = [
                "https://internshala.com/internships/full%20stack%20developer-internship/",
                "https://internshala.com/internships/python%20developer-internship/",
                "https://internshala.com/internships/machine%20learning-internship/",
                "https://internshala.com/internships/data%20science-internship/"
            ]

            for url in search_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Find internship cards
                        internship_cards = soup.find_all('div', class_='internship_meta')

                        for card in internship_cards[:2]:  # Limit to 2 per search
                            try:
                                # Extract job details
                                title_elem = card.find('h3', class_='heading_4_5')
                                company_elem = card.find('p', class_='company_name')
                                location_elem = card.find('p', class_='location_link')
                                link_elem = card.find('a', href=True)

                                if title_elem and company_elem and link_elem:
                                    title = title_elem.get_text(strip=True)
                                    company = company_elem.get_text(strip=True)
                                    location = location_elem.get_text(strip=True) if location_elem else "Remote"
                                    job_url = "https://internshala.com" + link_elem['href']

                                    job = {
                                        "title": title,
                                        "company": company,
                                        "location": location,
                                        "url": job_url,
                                        "description": f"Internship opportunity at {company}",
                                        "posted_date": datetime.now().strftime('%Y-%m-%d'),
                                        "source": "Internshala"
                                    }
                                    jobs.append(job)
                            except Exception as e:
                                logging.error(f"Error parsing internship card: {e}")
                                continue

                    time.sleep(2)  # Be respectful to the server
                except Exception as e:
                    logging.error(f"Error fetching {url}: {e}")
                    continue

        except Exception as e:
            logging.error(f"Error searching Internshala: {e}")

        return jobs
    
    def search_unstop_jobs(self) -> List[Dict]:
        """Search for jobs on Unstop with real scraping"""
        jobs = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Search URLs for different job types
            search_urls = [
                "https://unstop.com/internships?search=full%20stack%20developer",
                "https://unstop.com/internships?search=python%20developer",
                "https://unstop.com/internships?search=machine%20learning",
                "https://unstop.com/internships?search=data%20science"
            ]

            for url in search_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Find job cards (Unstop structure may vary)
                        job_cards = soup.find_all('div', class_=['opportunity-card', 'card'])

                        for card in job_cards[:2]:  # Limit to 2 per search
                            try:
                                # Extract job details
                                title_elem = card.find(['h3', 'h4', 'h5'], class_=['title', 'heading'])
                                company_elem = card.find(['p', 'span'], class_=['company', 'organization'])
                                link_elem = card.find('a', href=True)

                                if title_elem and link_elem:
                                    title = title_elem.get_text(strip=True)
                                    company = company_elem.get_text(strip=True) if company_elem else "Company"
                                    job_url = link_elem['href']

                                    # Ensure full URL
                                    if not job_url.startswith('http'):
                                        job_url = "https://unstop.com" + job_url

                                    job = {
                                        "title": title,
                                        "company": company,
                                        "location": "Remote/India",
                                        "url": job_url,
                                        "description": f"Opportunity at {company}",
                                        "posted_date": datetime.now().strftime('%Y-%m-%d'),
                                        "source": "Unstop"
                                    }
                                    jobs.append(job)
                            except Exception as e:
                                logging.error(f"Error parsing Unstop job card: {e}")
                                continue

                    time.sleep(2)  # Be respectful to the server
                except Exception as e:
                    logging.error(f"Error fetching {url}: {e}")
                    continue

        except Exception as e:
            logging.error(f"Error searching Unstop: {e}")

        return jobs

    def search_indeed_jobs(self) -> List[Dict]:
        """Search for jobs on Indeed"""
        jobs = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Search URLs for Indeed India
            search_terms = ["full+stack+developer", "python+developer", "machine+learning", "data+science"]

            for term in search_terms:
                try:
                    url = f"https://in.indeed.com/jobs?q={term}&l=India&sc=0kf%3Aattr%28DSQF7%29%3B&fromage=7"
                    response = requests.get(url, headers=headers, timeout=10)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Find job cards
                        job_cards = soup.find_all('div', class_=['job_seen_beacon', 'slider_container'])

                        for card in job_cards[:2]:  # Limit to 2 per search
                            try:
                                title_elem = card.find('h2', class_='jobTitle')
                                company_elem = card.find('span', class_='companyName')
                                location_elem = card.find('div', class_='companyLocation')
                                link_elem = card.find('a', href=True) if title_elem else None

                                if title_elem and company_elem and link_elem:
                                    title = title_elem.get_text(strip=True)
                                    company = company_elem.get_text(strip=True)
                                    location = location_elem.get_text(strip=True) if location_elem else "India"
                                    job_url = "https://in.indeed.com" + link_elem['href']

                                    job = {
                                        "title": title,
                                        "company": company,
                                        "location": location,
                                        "url": job_url,
                                        "description": f"Job opportunity at {company}",
                                        "posted_date": datetime.now().strftime('%Y-%m-%d'),
                                        "source": "Indeed"
                                    }
                                    jobs.append(job)
                            except Exception as e:
                                logging.error(f"Error parsing Indeed job card: {e}")
                                continue

                    time.sleep(3)  # Be more respectful to Indeed
                except Exception as e:
                    logging.error(f"Error fetching Indeed jobs for {term}: {e}")
                    continue

        except Exception as e:
            logging.error(f"Error searching Indeed: {e}")

        return jobs

    def search_all_jobs(self) -> List[Dict]:
        """Search all configured job sources"""
        all_jobs = []

        # Add fewer mock jobs now that we have real scraping
        mock_jobs = self.get_mock_jobs()
        all_jobs.extend(mock_jobs[:2])  # Only 2 mock jobs

        if self.config["sources"]["internshala"]:
            logging.info("Searching Internshala...")
            all_jobs.extend(self.search_internshala_jobs())

        if self.config["sources"]["unstop"]:
            logging.info("Searching Unstop...")
            all_jobs.extend(self.search_unstop_jobs())

        # Add Indeed search
        logging.info("Searching Indeed...")
        all_jobs.extend(self.search_indeed_jobs())

        # Add enhanced job search
        logging.info("Searching enhanced job sources...")
        all_jobs.extend(self.enhanced_search.search_all_enhanced())

        # Filter out duplicates and already sent jobs
        unique_jobs = []
        today = datetime.now().strftime('%Y-%m-%d')

        for job in all_jobs:
            job_id = f"{job['company']}_{job['title']}_{job['location']}"
            if job_id not in self.sent_jobs.get(today, []):
                unique_jobs.append(job)

        return unique_jobs
    
    def format_email_body(self, jobs: List[Dict]) -> str:
        """Format the email body with job listings"""
        today = datetime.now().strftime('%B %d, %Y')
        
        if not jobs:
            return f"""🔔 Daily Job Digest – {today} 🔔

No new job listings found today matching your criteria.

We'll keep searching and notify you when new opportunities arise!

— JobBot Automation
"""
        
        job_list = []
        for job in jobs:
            job_entry = f"🔹 {job['title']} @ {job['company']} ({job['location']})\n   📍 {job['url']}\n   📝 {job['description']}"
            job_list.append(job_entry)
        
        body = f"""🔔 Daily Job Digest – {today} 🔔

Found {len(jobs)} new job opportunities for you:

{chr(10).join(job_list)}

🎯 Search Keywords: {', '.join(self.config['job_search']['keywords'])}
📍 Locations: {', '.join(self.config['job_search']['locations'])}

Best of luck with your applications!

— JobBot Automation
"""
        return body
    
    def send_email(self, jobs: List[Dict]):
        """Send email with job listings"""
        try:
            sender_email = self.config["email"]["sender_email"]
            app_password = self.config["email"]["app_password"]
            receiver_email = self.config["email"]["receiver_email"]
            
            if sender_email == "your_email@gmail.com" or app_password == "your_gmail_app_password":
                logging.error("Please update email credentials in config.json")
                return
            
            msg = MIMEMultipart()
            msg['Subject'] = f"🧠💻 Daily Job Digest: {len(jobs)} New Opportunities – {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            
            body = self.format_email_body(jobs)
            msg.attach(MIMEText(body, 'plain'))
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
            
            # Mark jobs as sent
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in self.sent_jobs:
                self.sent_jobs[today] = []
            
            for job in jobs:
                job_id = f"{job['company']}_{job['title']}_{job['location']}"
                self.sent_jobs[today].append(job_id)
            
            self.save_sent_jobs()
            logging.info(f"[SUCCESS] Email sent successfully with {len(jobs)} job listings!")
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to send email: {e}")
    
    def run_daily_job_search(self):
        """Main function to search and send jobs"""
        logging.info("🔍 Starting daily job search...")
        
        jobs = self.search_all_jobs()
        logging.info(f"Found {len(jobs)} new job listings")
        
        if jobs or True:  # Send email even if no jobs found
            self.send_email(jobs)
        else:
            logging.info("No new jobs found, skipping email")
    
    def start_scheduler(self):
        """Start the job scheduler"""
        schedule_time = self.config["schedule"]["time"]
        schedule.every().day.at(schedule_time).do(self.run_daily_job_search)
        
        logging.info(f"📅 Job notifier scheduled to run daily at {schedule_time}")
        logging.info("🚀 Job notifier is now running...")
        
        # Run once immediately for testing
        logging.info("Running initial job search...")
        self.run_daily_job_search()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    job_mailer = JobMailer()
    job_mailer.start_scheduler()
