# webscrape-mask-donation

Collects the COVID-19 mask donation information aggregated on [this](https://findthemasks.com/give.html) site. 
The data is organized into a csv file with columns: 
'State', 'City', 'Location', 'Address', 'Instructions', 'Accepting', 'Open packages?'. 
The webpage is updated frequently (often more than once per hour), 
so users are encouraged to run this script often in order to keep their data up to date. 

The webpage uses JavaScript, so a Selenium webdriver is used to load the page in its entirety. 
Please do not close the FireFox window until the program completes. 
