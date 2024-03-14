"# budapest-real-estate-scraper" 

Budapest Real Estate Scraper

Web crawler is an algorithm used to analyze the code of a website in search of information, and then use it to generate insights or classify the data found. In this case, the web crawler will be used to collect information about the proprieties available to buy or rent in Hungary. The website to be scrapped is https://realestatehungary.hu/.

Please note that this scraper was developed in 2022, and as of the current date, the website may have implemented measures to prevent scraping of its data.

The data collected will be the following:
• City
• Street
• Street type
• District (only for Budapest)
• Buying Price (Million HUF) or Rental Price (Thousand HUF/Month)
• Area
• Balcony Area
• Number of rooms
• Value of HUF/m²

The data will be written and saved locally in two formats (.csv and .xlsx) and a dashboard containing a basic analysis of the data will be displayed in a webpage. Afterall, the user will be able to understand better the real estate market within the chosen city.

The Web Crawler for Hungary Real Estate will work as following:

The user will first select the city in which the crawler will collect the data. The available cities are Budapest, Debrecen, Pécs, Miskolc and Szeged.
Second, the user will select either it will be searched for proprieties available for rental or for sale.

After that, the script will collect all the data and save the files into a local folder. It is important to tell that the data will be cleaned in order to exclude those rows in which there is information missing or misleading information.

In the next step the user will be asked if he/she wants to run the program again or end it. When the user ends the scraper, the program will output a link to a local webpage where the files created will be used to display an interactive dashboard. For this project, the webpage will work only locally but it can be later be deployed with cloud services (i.e., AWS) to be accessed by anyone in any part of the world.

In order to be able to do the tasks, the program will be written in Python programming language version 3.11.0.
Also, the following external libraries are necessary to complete de task:

• requests
• bs4
• csv
• pandas
• dash

The program will have a console interface (no graphical interface is planned). When the program is started, a menu will be displayed, and the user can choose from the options explained above. The user will need a web browser in order to access the local webpage outputted by the program and see the available dashboards created with the collected data.# budapest-real-estate-scraper
