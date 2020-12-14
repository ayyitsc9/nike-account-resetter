Nike Account Resetter by @ayyitsc9
==========

- Main Function : Reset nike accounts by scraping your email for reset emails (Fully automated)
- Secondary Function :  Send nike reset email to emails in emails_to_send_to.txt
- Tertiary Function : Delete read nike reset emails


Installation and Set Up
------------
Click Code > Download ZIP > Create a folder on your PC > Extract All Files to that folder

- Setup settings.json. For the majority of you will only need edit the following settings : username, password, new_account_password, use_proxies
- I added extra settings for those that are familiar with them (headless, timeout, max_browser_threads)
- If you do not code, I would recommend just deleting the app.py file and running the app.exe file


Warnings/ Disclaimers
------------
- Do not move around input files. Make sure the location of files remain the same (app.py or app.exe, proxies.txt, settings.json, resetter folder, email_sender folder in main directory) (send_reset_emails_to.txt in email_sender folder) The rest of the files can be deleted or moved as it will auto generate if not found
- Using imap and enabling less secure apps access may put your email at risk. I do not take responsibility for anything that may happen. Make sure to do your research on "IMAP". If you decide to run the script, make sure to disable IMAP and less secure apps access after running it!
- I do not claim this to bypass nike detection. Does it get the reset job done? Yes. Do I know if it can get reset again? I don't know what factors are into play there.
- I would not use residential proxies as they may timeout too often
- If you run residential proxies, I would restart pc after running script just to be sure to close any processes that may be left. Although exiting through script should close them, it's better to be safe


JSON Values
------------

- mail_domain(str) : Domain of the email you will be scraping (For gmail set to "gmail", For yahoo set to "mail.yahoo"
- use_proxies(bool) : Set to true if you want to use proxies (Make sure to add proxies in proxies.txt, one line per proxy) Set to false if you want to use localhost
- headless(bool) : Set to true if you don't want to see the browsers that are opening (May save resources but may also be unstable), Set to false to see browsers executing
- email_folder_to_search(str) : Only tested for "inbox", you can try changing it to the folder name you'd like to search
- amount_of_emails_to_check(int) : Amount of emails you want to scrape, it will start from latest emails
- login(dict) : Contains two keys, username and password. This is required for account resetting [1] and deleting read nike reset emails [3]
- username(str) : Your email username Ex : test@gmail.com
- password(str) : Your email password Ex : Mypassword123!
- new_account_password(str): The password you want to set when resetting nike accounts (Requirements : 8 - 36 characters/ 1 uppercase letter/ 1 lowercase letter/ 1 number)
- max_browser_threads(int) : Max amount of browsers you want running at a time. We have tested 2 - 10 threads and it worked. It may differ based on your device specs. Recommend 2 - 4 threads
- timeout(int): Amount of seconds browser should wait for a response (5 seems to be ideal to maintain speed, but the higher the lesser chance for failure by loading error)


Guide
-----

__[1] Nike Account Resetter__

- Set up settings.json (Uses all values in settings.json, make sure it's correct value and value type!)
- Search how to enable IMAP access for your specific email provider
- For gmail users : https://myaccount.google.com/lesssecureapps Enable this and https://mail.google.com/mail/u/0/#settings/fwdandpop Enable IMAP here 
- You can now run [1] Nike Account Resetter

__[2] Reset Email Sender__

- Set up settings.json (Does not use mail_domain, email_folder_to_search, username, password, new_account_password)
- Load emails you want to send reset emails to on email_sender folder > send_reset_emails_to.txt (One email per line)
- This does not access your email in any way so it can be ran without toggle IMAP/ Less secure app access
- You can now run [2] Reset Email Sender

__[3] Seen Reset Email Deleter__

- Set up settings.json  (Does not use mail_domain, email_folder_to_search, username, password, new_account_password)
- Search how to enable IMAP access for your specific email provider
- For gmail users : https://myaccount.google.com/lesssecureapps Enable this and https://mail.google.com/mail/u/0/#settings/fwdandpop Enable IMAP here 
- You can now run [3] Seen Reset Email Deleter

- For ease of use I would leave all settings.json fields filled out regardless of which command you plan to use! You would just need to turn on IMAP/ Less secure apps access when running [1] and [3]


Other
-----

- Bot will create success and failed output files when running [1] and [2] if they are not already present
- [3] does not create a text file with logs. It will only log to console
- If you have TSB, it is better to run their account checker with Reset toggled in the bottom right corner
- If you have other bots that do not have that same feature, then you would need to create a list of the emails you want to send reset emails to and load them in send_reset_emails_to.txt (One email per line) and run [2]
- Have any questions? DM me on twitter! I will try to get back to everyone


A Note from Me
-------
You are not required to support me in any while but if you would like to do so I will list ways to below! Thank you everyone for giving my script a try and I hope you found it useful ♥ I'm just about to start diving into javascript and bot protection, if you would like to help/ mentor me feel free to dm! 👀😅

 If you would like to support me, you can do so by :
- Following me on twitter https://twitter.com/ayyitsc9
- Comment on my legit check https://twitter.com/ayyitsc9/status/996240726286479360
- Spread the word to your friends and groups
- Cashapp $BloomCord

I appreciate you if you do any of these! Shout out to @dc_han, he brought this up to me since he was struggling with all the resetting 😂
