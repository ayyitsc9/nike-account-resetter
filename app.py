# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
import subprocess, platform, json, time, ctypes, sys, random, os, threading, queue, asyncio
import datetime
from datetime import datetime
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

try:
    from colorama import init, Fore, Style
    from imap_tools import MailBox
    from bs4 import BeautifulSoup
    from pyppeteer import launch
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'imap_tools'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyppeteer'])

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
# Initializing Colorama || Utils
init(convert=True) if platform.system() == "Windows" else init()
print(f"{Fore.CYAN} {Style.BRIGHT} --- Script Created by @ayyitsc9 ---\n")
ctypes.windll.kernel32.SetConsoleTitleW("Nike Account Resetter ~ By @ayyitsc9")
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
# Initializing Settings
def init():
    # For variables from settings.json file
    global mail_domain, use_proxies, headless_setting, email_folder, email_limit, username, password, new_account_password, max_threads, timeout
    with open("./settings.json", "r") as settings:
        data = json.load(settings)
        # Mail domain value (for gmail : 'gmail', for yahoo : 'mail.yahoo')
        mail_domain = data['mail_domain']
        # Boolean value for whether or not to use proxies
        use_proxies = data['use_proxies']
        # Boolean value for whether or not to run headless
        headless_setting = data['headless']
        # Email Login credentials
        username = data['login']['username']
        password = data['login']['password']
        # By default, in most cases this should be inbox
        email_folder = data['email_folder_to_search'].upper()
        # Number of emails to check
        email_limit = data['amount_of_emails_to_check']
        # Password to set when resetting accounts
        new_account_password = data['new_account_password']
        # Number of threads we can run
        max_threads = data['max_browser_threads']
        # Sets browser timeout | Need MS, we take in seconds on our settings.json for simplicity
        timeout = data['timeout'] * 1000

    # For proxies
    if use_proxies:
        global proxy_file, proxy_list
        proxy_file = open("./proxies.txt", "r")
        proxy_list = proxy_file.read().split("\n")
        proxy_file.close()

    # Other variables
    global detected, success, failed, new_account_credentials, failed_to_reset, emails_success, emails_failed
    # Detected : Counter for how many Nike reset emails are found
    # Success : Counter for how many have been reset successfully
    # Failed : Counter for how many didn't reset due to error
    # New Account Credentials : List containing lists of account credentials Ex : [["nikeaccount1@gmail.com", "Newpassword!123"], ["nikeaccount2@gmail.com", "Newpassword!123"]
    # Failed to Reset : List containing lists of accounts that failed to reset Ex : [["nikeaccount1@gmail.com", "https://nike.com/fakeresetlink1"], "nikeaccount2@gmail.com", "https://nike.com/fakeresetlink2"]
    detected, success, failed, new_account_credentials, failed_to_reset, emails_success, emails_failed = 0, 0, 0, [], [], [], []

    # Queue Handling | Initialize Queue
    global queue_
    queue_ = queue.Queue(maxsize=max_threads)


# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

def save_to_txt(type_):
    # Type_ will = Reset if user decided to run AccountReset()
    if type_ == "Reset":
        # Saves resetted accounts to reset_accounts.txt
        with open("./resetter/reset_accounts.txt", "a") as success_file:
            # Loops through all the resetted accounts
            for account in new_account_credentials:
                # Writes each account to reset_accounts.txt in email:password format for easy copying
                success_file.write(f"{account[0]}:{account[1]}\n")
            success_file.close()

        # Saves failed to reset accounts to reset_failed.txt
        with open("./resetter/reset_failed.txt", "a") as failed_file:
            # Loops through all the accounts that failed to reset due to any errors
            for account in failed_to_reset:
                # Writes each account and its reset link to reset_failed.txt
                failed_file.write(f"{account[0]} | {account[1]}\n")
            failed_file.close()

    # Type_ will = Email if user decided to run SendResetEmail()
    elif type_ == "Email":
        # Saves accounts that were sent reset emails to email_success.txt
        with open("./email_sender/email_success.txt", "a") as success_file:
            # Loops through all the accounts that were sent reset email
            for account in emails_success:
                # Writes each account to emails_succcess.txt
                success_file.write(f"{account}\n")
            success_file.close()

        # Saves failed to send reset emails to email_failed.txt
        with open("./email_sender/email_failed.txt", "a") as failed_file:
            # Loops through all the accounts that failed to send reset email due to any errors
            for account in emails_failed:
                # Writes each account and its reset link to email_failed.txt
                failed_file.write(f"{account}\n")
            failed_file.close()

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

# For Nike Account Resetter
def login():
    global email
    Logger.normal("Logging in...")
    try:
        # Connect/ Initialize
        email = MailBox(f'imap.{mail_domain}.com')
        # Log into email
        email.login(username, password, email_folder)
    except Exception as e:
        Logger.error(f"Failed to log in! Error : {e}")

def logout():
    Logger.normal("Logging out...")
    email.logout()

# - - - -  - - - - - - - - - - 

# For Reset Email Sender
def load_emails():
    global emails_list
    # Load the emails we want to send a reset email to (One email per line)
    input_file = open("./email_sender/send_reset_emails_to.txt", "r")
    emails_list = input_file.read().split("\n")
    
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
lightblue = "\033[94m"
orange = "\033[33m"

class Logger:
    @staticmethod
    def timestamp():
        return str(datetime.now())[:-7]
    @staticmethod
    def normal(message):
        print(f"{lightblue}[{Logger.timestamp()}] {message}")
    @staticmethod
    def other(message):
        print(f"{orange}[{Logger.timestamp()}] {message}")
    @staticmethod
    def error(message):
        print(f"{Fore.RED}[{Logger.timestamp()}] {message}")
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[{Logger.timestamp()}] {message}")

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

class Proxy:
    @staticmethod
    def get_proxy(proxy_list):
        proxy_list = proxy_list
        full_proxy = random.choice(proxy_list)
        if len(full_proxy.split(":")) == 2:
            proxy_type = "IP"
        elif len(full_proxy.split(":")) == 4:
            proxy_type = "UP"
        else:
            Logger.error("Invalid proxy format detected! Using localhost...")
            proxy_type = "LH"
        return full_proxy, proxy_type
    
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

class AccountReset:
    def __init__(self, mail, a_tags):
        self.mail, self.a_tags = mail, a_tags
        self.get_details()
        # Add item to our queue
        # This helps us limit threads!
        queue_.put(self)
        # Initialize and start thread/ reset_account method
        Logger.normal("Starting reset account thread...")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    # - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
    # Email Login/ Parsing
    
    def get_details(self):
        global max_threads, queue_
        # Parse nike account email

        # Checks if the email was forwarded to mail, otherwise it will just assign the To: value of the email to self.nike_account_email
        if 'Forwarded' not in self.mail.text:
            self.nike_account_email = self.mail.to[0]
        else:
            self.nike_account_email = self.a_tags[1].text

        # Parse reset link

        # Loop through all <a> tags within the email
        for a_tag in self.a_tags:
            # Find <a> tag with the text value "here"
            if a_tag.text ==  "here":
                # Get href (link) of the <a> tag
                self.reset_redirect_link = a_tag['href']
                # First split is to get the left part of the reset key cut out
                # Second split is to remove the right part of the resey key
                # Result is just the reset key
                self.reset_key = self.reset_redirect_link.split("%3FresetKey=")[1].split("%")[0]

    # - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
    # Nike Account Resetting

    def run(self):
        asyncio.run(self.reset_account())

    async def reset_account(self):
        # Checks if use_proxies is True // Using seleniumwire options
        if use_proxies:
            proxy_details = Proxy.get_proxy(proxy_list)
            if proxy_details[1] == "IP":
                # Start browser with IP auth proxy
                browser = await launch({'args': [f'--proxy-server={proxy_details[0]}'], 'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
            elif proxy_details[1] == "UP":
                # Start browser and apply ip:port of proxy
                browser = await launch({'args': [f'--proxy-server={proxy_details[0].split(":")[0]}:{proxy_details[0].split(":")[1]}'], 'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
            else:
                # Open browser, no proxy
                browser = await launch({'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)  
        else:
            browser = await launch({'headless': headless_setting}, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        # Get pages and set page variable to the first page
        page = await browser.pages()
        page = page[0]
        # If use_proxies is True and it's a User pass proxy, authenticate it with user and password
        if use_proxies and proxy_details[1] == "UP":
            await page.authenticate({'username': proxy_details[0].split(":")[2], 'password': proxy_details[0].split(":")[3]})
        try:
            global detected, success, failed, queue
            # Creates browser instance
            self.reset_link = f"https://unite.nike.com/s3/unite/updatePassword.html?resetKey={self.reset_key}&locale=en_US&redirectUrl=http://www.nike.com&backendEnvironment=identity"
            # Go to reset link and wait until there are no more than 2 connections for at least 500 ms
            await page.goto(self.reset_link, {'waitUntil':'networkidle2'})
            # Wait for text field to load
            page.waitForXPath("//*[@data-componentname='passwordCreate']", timeout=timeout)
            # Get text field element
            password_field = await page.Jx("//*[@data-componentname='passwordCreate']")
            # Enter in new password
            await password_field[0].type(new_account_password)
            # Wait for reset button to load
            page.waitForXPath("//*[@value='UPDATE PASSWORD']", timeout=timeout)
            # Get reset button element
            reset_button = await page.Jx("//*[@value='UPDATE PASSWORD']")
            # Click reset button
            await reset_button[0].click()
            try:
                # Wait for page to redirect
                await page.waitForNavigation({'timeout':timeout})
                # Increment global success variable
                success += 1
                Logger.normal(f"[{self.nike_account_email}] Successfully reset account!")
                # Add accounts' new login credentials to our new_account_credentials list
                new_account_credentials.append([self.nike_account_email, new_account_password])
            except Exception as e:
                # Password requirements : Minimum 8 characters/ 1 uppercase letter/ 1 lowercase letter/ 1 number (Max 36 characters)
                Logger.error(f"Failed to reset account! Common errors : Expired reset link, Invalid new password | Other Errors : Banned, Detected, Network Issue | Error : {e}")
                # Increment global failed variable
                failed += 1
                # Add account email and reset url to list (So user can track if only certain accounts failed to reset)
                failed_to_reset.append([self.nike_account_email, self.reset_link])
        except Exception as e:
            # Common errors : Timeout when trying to get element
            Logger.error(f"Failed to reset account! Error : {e}")
            # Increment global failed variable
            failed += 1
            # Add account email and reset url to list (So user can track if only certain accounts failed to reset)
            failed_to_reset.append([self.nike_account_email, self.reset_link])
        # Runs regardless of which of the try or except block execute
        finally:
            await asyncio.sleep(1.5)
            # Closes page
            await page.close()
            # Closes browser
            await browser.close()
            # Removes item from our queue
            queue_.get()
            # Indicate that this task is finished executing, without this our queue_.join() call below will wait forever as we have not signified that process is finished
            queue_.task_done()
            # Update values in our command prompt title
            ctypes.windll.kernel32.SetConsoleTitleW(f"Nike Account Resetter ~ By @ayyitsc9 | Detected : {str(detected)} | Success : {str(success)} | Failed : {str(failed)}")
    
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

class SendResetEmail:
    def __init__(self, email):
        self.email = email
        # Add item to our queue
        # This helps us limit threads!
        queue_.put(self)
        # Initialize and start thread/ send reset email
        Logger.normal("Starting send reset email thread...")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        asyncio.run(self.send())

    async def send(self):
        # Checks if use_proxies is True // Using seleniumwire options
        if use_proxies:
            proxy_details = Proxy.get_proxy(proxy_list)
            if proxy_details[1] == "IP":
                # Start browser with IP auth proxy
                browser = await launch({'args': [f'--proxy-server={proxy_details[0]}'], 'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
            elif proxy_details[1] == "UP":
                # Start browser and apply ip:port of proxy
                browser = await launch({'args': [f'--proxy-server={proxy_details[0].split(":")[0]}:{proxy_details[0].split(":")[1]}'], 'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
            else:
                # Open browser, no proxy
                browser = await launch({'headless': headless_setting }, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)  
        else:
            browser = await launch({'headless': headless_setting}, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        # Get pages and set page variable to the first page
        page = await browser.pages()
        page = page[0]
        # If use_proxies is True and it's a User pass proxy, authenticate it with user and password
        if use_proxies and proxy_details[1] == "UP":
            await page.authenticate({'username': proxy_details[0].split(":")[2], 'password': proxy_details[0].split(":")[3]})
        try:
            global detected, success, failed, queue
            # Go to reset link and wait until there are no more than 2 connections for at least 500 ms
            await page.goto("https://www.nike.com/login", {'waitUntil':'networkidle2'})
            # Wait for forgot password to load
            page.waitForXPath('//*[@class="nike-unite-login-options"]/div/a', timeout=timeout)
            # Get forgot password element
            forgot_password = await page.Jx('//*[@class="nike-unite-login-options"]/div/a')
            # Click forgot password element
            await forgot_password[0].click()
            # Wait for text field to load
            page.waitForXPath('//*[@data-componentname="emailAddress"]', timeout=timeout)
            # Get text field element
            email_field = await page.Jx('//*[@data-componentname="emailAddress"]')
            # Enter in email
            await email_field[0].type(self.email)
            # Wait for reset button to load
            page.waitForXPath("//*[@value='RESET']", timeout=timeout)
            # Get reset button element
            reset_button = await page.Jx("//*[@value='RESET']")
            # Click reset button
            await reset_button[0].click()
            await asyncio.sleep(1.5)
            # Get header value, this is our tell if the reset email was sent since link does not change
            header = await page.Jx("//*[@class='view-header']")
            head_value = await page.evaluate('(element) => element.textContent', header[0])
            if head_value == "PASSWORD RESET":
                # Increment global success variable
                success += 1
                Logger.normal(f"[{self.email}] Successfully sent reset email!")
                # Add accounts' new login credentials to our new_account_credentials list
                emails_success.append(self.email)
            else:
                # Password requirements : Minimum 8 characters/ 1 uppercase letter/ 1 lowercase letter/ 1 number (Max 36 characters)
                Logger.error(f"Failed to send reset email! Common error : Invalid Email | Other Errors : Banned, Detected, Network Issue")
                # Increment global failed variable
                failed += 1
                # Add account email and reset url to list (So user can track if only certain accounts failed to reset)
                emails_failed.append(self.email)
        except Exception as e:
            # Common errors : Timeout when trying to get element
            Logger.error(f"Failed to send reset email! Error : {e}")
            # Increment global failed variable
            failed += 1
            # Add account email and reset url to list (So user can track if only certain accounts failed to reset)
            emails_failed.append(self.email)
        # Runs regardless of which of the try or except block execute
        finally:
            await asyncio.sleep(1.5)
            # Closes page
            # await page.close()
            # Closes browser
            await browser.close()
            # Removes item from our queue
            queue_.get()
            # Indicate that this task is finished executing, without this our queue_.join() call below will wait forever as we have not signified that process is finished
            queue_.task_done()
            # Update values in our command prompt title
            ctypes.windll.kernel32.SetConsoleTitleW(f"Nike Account Resetter ~ By @ayyitsc9 | Detected : {str(detected)} | Success : {str(success)} | Failed : {str(failed)}")

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -




# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

while True:
    print(Style.RESET_ALL)
    print("What would you like to do?\n")
    print("######################################\n")
    print("Run [1] if you have reset emails already\nRun [2] if not (Note: If you have TSB, it is better to run the account checker with reset toggled at the bottom right)\n")
    print("[1]Run Nike Account Resetter\t\t[2]Run Reset Email Sender\n")
    print("[3]Delete Seen Reset Emails\t\t[4]Exit\n")
    print("######################################\n")
    task = input("Enter Option : ")
    print("\n")
    if task == "1":
        init()
        login()
        # Fetch 1 email at a time to lower memory consumption instead of fetching bulk
        for mail in email.fetch(reverse=True, limit=email_limit):
            # Finding nike reset email
            if "Password Reset Request" in mail.subject:
                if 'nike' in mail.from_ or 'nike' in mail.text:
                    global detected, success, failed
                    # Increment detected value
                    detected += 1
                    Logger.other("Detected Nike reset email!")
                    # Update command prompt title
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Nike Account Resetter ~ By @ayyitsc9 | Detected : {str(detected)} | Success : {str(success)} | Failed : {str(failed)}")
                    # Parse HTML
                    soup = BeautifulSoup(mail.html, 'html.parser')
                    # Get all <a> tags from email html
                    a_tags = soup.find_all('a')
                    AccountReset(mail, a_tags)
        logout()
        # Make sure all tasks in queue have finished executing
        queue_.join()
        # Save failed to reset and successfully reset accounts to txt files
        save_to_txt("Reset")
        Logger.success("Finished Account Resetter Execution!")
    elif task == "2":
        init()
        load_emails()
        for email in emails_list:
            SendResetEmail(email)
        # Make sure all tasks in queue have finished executing
        queue_.join()
        # Save failed to send and successfully sent reset emails to txt files
        save_to_txt("Email")
        Logger.success("Finished Reset Email Sender Execution!")
    elif task == "3":
        init()
        login()
        # Fetch 1 email at a time to lower memory consumption instead of fetching bulk
        for mail in email.fetch(reverse=True, limit=email_limit, mark_seen=True):
            # Finding nike reset email that has been read already
            if "Password Reset Request" in mail.subject and 'SEEN' in mail.flags:
                if 'nike' in mail.from_ or 'nike' in mail.text:
                    # Delete email
                    email.delete(mail.uid)
                    Logger.success("Successfully deleted read reset email!")
                    # Increment success value
                    success += 1
                    # Update command prompt title
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Nike Account Resetter ~ By @ayyitsc9 | Detected : {str(detected)} | Success : {str(success)} | Failed : {str(failed)}")
        logout()
        Logger.success("Finished Delete Seen Reset Emails Execution!")
    elif task == "4":
        Logger.other("Comment on my legit check @ https://twitter.com/ayyitsc9")
        Logger.other("Star the repository @ https://github.com/ayyitsc9/nike-account-resetter")
        Logger.error("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit()
    else:
        print("Invalid input. Try again!")

