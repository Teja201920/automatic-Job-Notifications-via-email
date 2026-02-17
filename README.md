# 🤖 Automated Job Notification System

An intelligent job search and notification system that automatically finds relevant job opportunities and emails them to you daily.

## ✨ Features

- 🔍 **Smart Job Search**: Searches multiple job platforms for relevant opportunities
- 📧 **Daily Email Notifications**: Sends curated job listings at 5:30 PM IST
- 🎯 **Customizable Filters**: Filter by keywords, locations, and experience levels
- 📝 **Duplicate Prevention**: Tracks sent jobs to avoid spam
- 📊 **Detailed Logging**: Comprehensive logs for monitoring and debugging
- ⚙️ **Easy Configuration**: JSON-based configuration for easy customization

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings

1. **Enable Gmail App Passwords**:
   - Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
   - Generate an App Password for "Mail"
   - Copy the 16-character password

2. **Update config.json**:
   ```json
   {
     "email": {
       "sender_email": "your_actual_email@gmail.com",
       "app_password": "your_16_char_app_password",
       "receiver_email": "vantharamsuryagayathri.22.cse@anits.edu.in"
     }
   }
   ```

### 3. Run the System

```bash
python job_mailer.py
```

Or double-click `start_job_mailer.bat` (Windows)

## 📋 Configuration Options

### Job Search Criteria

Edit `config.json` to customize your job search:

```json
{
  "job_search": {
    "keywords": [
      "Full Stack Developer",
      "AI/ML Developer",
      "Python Developer",
      "React Developer"
    ],
    "locations": [
      "Remote",
      "Bangalore",
      "Hyderabad",
      "Chennai"
    ],
    "experience_levels": [
      "Intern",
      "Entry Level",
      "Fresher"
    ]
  }
}
```

### Schedule Settings

```json
{
  "schedule": {
    "time": "17:30",
    "timezone": "Asia/Kolkata"
  }
}
```

### Job Sources

```json
{
  "sources": {
    "internshala": true,
    "unstop": true,
    "glassdoor": false,
    "linkedin": false
  }
}
```

## 📁 File Structure

```
automatic job/
├── job_mailer.py          # Main application
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── README.md             # This file
├── start_job_mailer.bat  # Windows startup script
├── job_mailer.log        # Application logs
└── sent_jobs.json        # Tracking sent jobs
```

## 🔧 Advanced Setup

### Running as a Service (Windows)

1. Install `pywin32`:
   ```bash
   pip install pywin32
   ```

2. Create a Windows service to run automatically

### Cloud Deployment

Deploy on platforms like:
- **PythonAnywhere** (Free tier available)
- **Heroku** (With scheduler add-on)
- **AWS Lambda** (With CloudWatch Events)
- **Google Cloud Functions** (With Cloud Scheduler)

### Real Web Scraping

To enable actual job scraping, extend the methods in `job_mailer.py`:

```python
def search_internshala_jobs(self):
    """Real implementation with web scraping"""
    headers = {'User-Agent': 'Mozilla/5.0...'}
    response = requests.get('https://internshala.com/internships', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Parse job listings...
```

## 📊 Monitoring

### Logs

Check `job_mailer.log` for:
- Job search results
- Email sending status
- Error messages
- System activity

### Sent Jobs Tracking

`sent_jobs.json` tracks all sent jobs by date to prevent duplicates.

## 🛠️ Troubleshooting

### Common Issues

1. **Email not sending**:
   - Verify Gmail App Password is correct
   - Check if 2FA is enabled on Gmail
   - Ensure "Less secure app access" is not blocking

2. **No jobs found**:
   - Check internet connection
   - Verify job search keywords
   - Review logs for errors

3. **Script stops running**:
   - Check for Python errors in logs
   - Ensure system doesn't go to sleep
   - Consider running as a service

### Testing

Run a test email:
```python
from job_mailer import JobMailer
job_mailer = JobMailer()
job_mailer.run_daily_job_search()
```

## 🔮 Future Enhancements

- [ ] Real-time job scraping from multiple sources
- [ ] Machine learning for job relevance scoring
- [ ] Web dashboard for managing preferences
- [ ] Mobile app notifications
- [ ] Integration with job application tracking
- [ ] Salary range filtering
- [ ] Company blacklist/whitelist
- [ ] Resume matching score

## 📞 Support

For issues or questions:
1. Check the logs in `job_mailer.log`
2. Review this README
3. Verify configuration settings
4. Test email connectivity

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Job Hunting! 🎯**
