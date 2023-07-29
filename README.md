# EasyApply-LinkedIn-Automation
"EasyApply LinkedIn Automation" project is an automated Python script that simplifies the job search process on LinkedIn.

EasyApply LinkedIn Automation

Description
EasyApply LinkedIn Automation is a Python script that automates the process of searching for jobs on LinkedIn and applying to them with a single click. The script uses the Selenium library to interact with the LinkedIn website and perform the job search and application tasks.

Features
Login to LinkedIn: The script logs into your personal LinkedIn account using your email and password provided in the config.json file.

Job Search: The script navigates to the LinkedIn Jobs section and searches for jobs matching the specified keywords and location in the config.json file.

Easy Apply: The script finds job listings with the "Easy apply" option and applies to them automatically.

Pagination: The script handles pagination to search for jobs on multiple pages.

Scrolling: The script uses scrolling to load more job listings dynamically.

Proxy Support (Optional): The script supports using proxies, such as ScrapeOps, for web scraping. However, it's important to note that using proxies is not necessary, and the script can work without them as well.

Getting Started
Prerequisites
Python 3.x installed on your system.
Google Chrome browser installed (or Firefox with some minor changes in the script).
Installation
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/Looky225/EasyApply-LinkedIn-Automation.git
Change into the project directory:

bash
Copy code
cd EasyApply-LinkedIn-Automation
Create a virtual environment (optional but recommended):

Copy code
python -m venv myenv
Activate the virtual environment:

On Windows:

Copy code
myenv\Scripts\activate
On macOS or Linux:

bash
Copy code
source myenv/bin/activate
Install the required Python packages:

Copy code
pip install -r requirements.txt
Usage
Update the config.json file with your LinkedIn email, password, keywords, and location preferences.

Run the app.py script:

Copy code
python app.py
The script will open a Chrome browser window (or Firefox, if configured). It will log in to your LinkedIn account and start the job search and application process.

Sit back and relax while the script automatically applies to jobs with the "Easy apply" option.

Important Notes
Proxy Usage (Optional): The script supports using proxies, but they are not mandatory. If you don't have access to ScrapeOps or any other proxy service, you can still use the script without any issues.

Captcha and Account Restrictions: Please use this script responsibly and avoid making too many requests to LinkedIn. Excessive automation may lead to encountering captchas or other security measures from LinkedIn to protect its platform. Additionally, LinkedIn may reprimand or restrict accounts that violate their terms of service. Be cautious and moderate in your usage to avoid any issues with your LinkedIn account.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Disclaimer
This script is provided for educational purposes only. The developer is not responsible for any misuse or violations of LinkedIn's terms of service. Use this script at your own risk.
