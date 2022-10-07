# Web-Scraping Booking Alert Project

The code provided was made specific to the use-case of my own and would be helpful as an example of a functional API that scrapes a website and alert its user about the latest information through the usage of APIs from other communication platforms.

While it was functional, it was hosted on a server at DigitalOcean to constantly query and send updates on a booking situation in a particular website to my mobile phone via Discord for a prompt alert to secure my bookings.

This use-case can be helpful in school projects that require the concepts of web-scraiping, building of APIs, and integration with other existing APIs. 

## How does it function?

1. **discordExtension.py**
    * Authenticates itself into the targetted website
    * Queries website for information
    * Sends the information to the user via discord

2. **findPracticals.py**
    * Contains the main functions needed to
        * Authenticate the API script into the targetted website
        * Query the website for information
        * Attempts a re-login whenever a session is expired
3. **html_js_extract.py**
    * Utilises Selenium's automated testing to receive a DOM body with a valid Google Captcha key for authentication
4. **pass_from_config.py**
    * Functions that parse authentication information from a config file to the main code

<br>

## Train of thoughts

The objective of this project was to scrape a booking website of a driving school I was enrolled in to retrieve data on the latest booking slots for driving lessons.

**My problem statement:**
> It was a hassle to constantly login to the school portal and check on the latest booking slots. Normally, slots would have been taken up by other students by the time I login to see the slots.

**The solution:**
>Automate a script that authenticates me into the portal and query for the latest booking slots before updating me via Discord.

Breaking down the problem, I came to conclusion on the resources I needed:

All scripts will be written in Python for flexibility and convenience. As for the modules used, I ended up using the following,

* **Python Requests**
    * Perform both POST and GET requests programmatically to our target website and store cookies and user data into session objects

* **BeautifulSoup**
    * Scraping of HTML body from HTTP requests to extract important information such as the request verification token from the HTML body

* **Selenium** 
    * Automatically flashing our webpage and retrieving a recaptcha token for authentication (it was impossible to retrieve the token from the HTML body via web-scraping or launching the browser in headless mode)

* **Chromedriver.py** 
    * Ensure that the Chrome drivers used for Selenium was up-to-date

* **Configparser** 
    * Conveniently set necessary config information, such as that needed to authenticate ourselves into the target website

* **Discord.py** 
    * A Discord API will be used so that the information retrieved from the website can be sent conveniently to my phone via a channel message

I ended up hosting my script on a Linux Debian server via DigitalOcean. After creating a server instance, I configured a GUI and accessed it via a remote desktop. Although SSH would have been a more practical and secured option, at the time of testing, I needed a GUI to flash my browser and "trick" the recaptcha into giving me an authentication key.

### Authentication

Observing the login form in the webpage's HTML, aside from the login ID and password, two other pieces of information were needed:

The first was a Request Verification token, which randomly generates in a hidden input field in the login form upon page load. Using the BeautifulSoup library in python, I was able to retrieve the token value to be used in the request payload in order to establish a user session for the program. 

The second information needed was a google Captcha key. This however was very difficult to achieve through the same means as the web-scraping technique used previously. 

Google Captcha key is issued via an external script on the webpage. Thus, using the python get request, it is not possible to retrieve the key value in the DOM body as the script has not been executed. Even rendering the page will not allow the script to retrieve the key since the render function might not support the execution of external scripts or API scripts. Using selenium, the browser driver will be able to load the HTML content after the javascripts have been fully executed, utilizing the capabilities of automated testing.

However, using headless testing (meaning that the chrome driver of selenium runs in the background), Google Captcha keys appear to be invalid. It may be due to the lack of a "normal" browser for Google to assign cookies or verify the client.

Thus the final solution is to utilize automated testing from selenium to retrieve the HTML elements after script execution, before passing the retrieved key over to the bot for form validation. The compromise is that the chrome driver window will appear for a second before minimizing and closing after the key has been retrieved.

### Querying of data

After solving the login segment, I had to figure out how the webpage was queried in order to retrieve information on the latest lesson slots. After a lot of research and inspection, it turns out that a POST request is made via Ajax upon a button-click event to be displayed on the webpage. Thus I replicated the request on my script to retrieve the same information.

The Ajax request submitted the entire HTML form body in its serialized state in order to get the booking information. By process of elimination, I figured out which form data was needed and which one was not in order to get the target information. Eventually, I was able to receive a response with the booking information I needed to be sent to me automatically.

### Sending updates to the user

After the information has been retrieved from the website, I created a script that uses the Python Discord API which allows me to create my own Discord bot and set commands and send messages to my server. Thus, when information is received from the website, the bot will update me on the latest booking slots via a text channel. I also created it in a way that the script can be paused or resumed via commands sent by me to the bot.