import requests  # library for making HTTP requests in Python. It allows you to send HTTP requests using Python and receive HTTP responses.
from bs4 import BeautifulSoup  # library for parsing and navigating HTML and XML documents. It allows you to easily search and extract data from HTML or XML documents.
import csv  # built-in library that provides functions to read and write CSV files.
import pandas as pd  # library for data manipulation and analysis in Python. It provides data structures for efficiently storing large datasets and tools for working with them.
import os  # built-in library that provides functions for interacting with the operating system.
from plotly.subplots import make_subplots  #  is a function from the plotly.subplots module of the plotly library. It is used to create subplots in a Plotly figure.


class UserSelection:

    def __init__(self):
        # The __init__ method is called when a new instance of the class is created.
        # It's used to initialize the attributes of the instance.
        # In this case, the UserSelection class doesn't have any attributes to initialize,
        # so the method just has the pass statement, which does nothing.
        self.city = None
        self.contract = None

    def get_input(self):
        # This method asks the user for input and stores it in the city and contract attributes
        # of the UserSelection instance.
        self.city = self.city_input()
        self.contract = self.contract_input()

    def city_input(self):
        # This method presents the user with a list of cities to choose from and returns the city
        # chosen by the user.
        cities = {
            1: 'budapest',
            2: 'debrecen',
            3: 'pécs',
            4: 'miskolc',
            5: 'szeged'
        }
        # The user is asked to input a number between 1 and 5 to choose a city.
        user_input_city = int(input('''Which city do you want to look for? 
                Select the number:
                    (1) Budapest 
                    (2) Debrecen  
                    (3) Pécs 
                    (4) Miskolc 
                    (5) Szeged 
                '''))
        # If the user's input is invalid (not a number between 1 and 5),
        # a message is printed and the method is called again.
        if not 1 <= user_input_city <= 5:
            print('Invalid input, please type a number between 1 and 5')
            return self.city_input()  # while loop
        # If the user's input is valid, the chosen city is returned.
        try:
            city = cities[user_input_city]
        except KeyError:
            city = None
        return city

    def contract_input(self):
        # This method presents the user with a choice between properties available to rent
        # or properties available for sale, and returns the choice made by the user.
        types = {
            1: 'kiado',
            2: 'elado',
        }
        # The user is asked to input 1 or 2 to choose a contract type.
        user_input_contract = int(input('''What type of contract are you looking for? 
               Select the number:
                   (1) Properties available to RENT 
                   (2) Properties available for SALE  
               '''))
        # If the user's input is invalid (not 1 or 2), a message is printed and the method is called again.
        if not 1 <= user_input_contract <= 2:
            print('Invalid input, please choose 1 or 2')
            return self.contract_input()
        # If the user's input is valid, the chosen contract type is returned.
        try:
            contract = types[user_input_contract]
        except KeyError:
            contract = None
        return contract


class WebScraper:
    # Initialize the attributes of the WebScraper
    def __init__(self, url, csv_file, city, contract):
        self.url = url  # URL to scrape
        self.csv_file = csv_file  # CSV file to write to
        self.city = city  # City to scrape data for
        self.contract = contract  # Type of contract (rent or sale)
        self.data = []  # List to store the scraped data

    def scrape(self):

        # List of street types in Hungarian.
        # This list is used when collecting the address of the apartment in order to split the string in the correct place.
        street_types = ['utca', 'út', 'útja', 'körút', 'krt', 'tér', 'tere', 'köz', 'körönd', 'rakpart', 'liget',
                        'sziget', 'híd', 'sor', 'part', 'pályaudvar', 'állomás', 'fasor']

        # Headers to send with the request.
        # Some websites block requests from web scraping tools or other automated clients by checking the User-Agent header,
        # so specifying a User-Agent that identifies your client as a web browser can help to avoid being blocked.
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

        # Send a request to the URL and parse the response with BeautifulSoup
        # The requests.get() function sends an HTTP GET request to the specified URL and returns a Response object.
        # The Response object has a text attribute, which contains the content of the response in Unicode.
        # The BeautifulSoup function takes in two arguments: the HTML content and the parser to use.
        # In this case, I am is using the html.parser built-in Python library to parse the HTML.
        # This creates a BeautifulSoup object,that allows you to easily navigate and search the HTML to find the data you want.
        response = requests.get(self.url, headers=headers)
        print(self.url)
        page = BeautifulSoup(response.text, 'html.parser')

        # Find the number of pages to scrape
        # Here it is used the BeautifulSoup find() method to search for the 'div' element with the 'class' "pagination__page-number".
        # The find() method returns the first element it finds that matches the specified criteria.
        # In this case, the element containing the last page number is found and using the 'get_text()' and 'split()'
        # the last page number is collected. It is also transformed into an integer to be used in a for loop after.
        #try:
            #last_page = int(page.find('div', class_='pagination__page-number').get_text().split()[2])
        #except:

        last_page = 5

        # Scrape each page using the variable 'last_page'.
        # By doing this, the for loop will go over all the pages of the URL.
        for i in range(1, last_page):

            # Send a request to the URL and parse the response with BeautifulSoup.
            # This is the same step made above to send the request, but this time
            # it is made in order to get the necessary information in ALL the pages of the website.
            response = requests.get(self.url + '?page=' + str(i), headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the data you want to scrape on the page.
            # find_all() method to search for all the 'a' elements with the class "listing__link js-listing-active-area" in the HTML.
            # The find_all() method returns a list of all elements that match the specified criteria.
            # In this case it is found the cards which contains all the necessary information about the apartment in a page.
            items = soup.find_all('a', class_='listing__link js-listing-active-area')

            # Scrape the data for each item.
            # This loop is running over the list created above and will collect the specific information needed.
            for item in items:

                item_data = {}
                item_data['full_address'] = item.find('span', class_='d-block fw-500 fs-7 text-onyx font-family-secondary').get_text().strip()
                item_data['City'] = self.city
                item_data['Price'] = item.find(class_='price').get_text().strip()
                if self.contract == 'kiado':
                    item_data['Price(HUF)'] = float(item_data['Price'].split(' ')[0]) * 1000
                else:
                    item_data['Price(HUF)'] = float(item_data['Price'].split(' ')[0]) * 1000000
                item_data['Area'] = item.find('div',
                                              class_='listing__parameter listing__data--area-size').get_text().strip()
                item_data['Area(m²)'] = float(item_data['Area'].split(' ')[0])

                balcony = item.find('div', class_='listing__parameter listing__data--balcony-size')
                if balcony is None:
                    item_data['Balcony'] = ''
                else:
                    item_data['Balcony'] = item.find('div',
                                                     class_='listing__parameter listing__data--balcony-size').get_text().strip()
                    item_data['Balcony(m²)'] = float(item_data['Balcony'].split(' ')[0])

                rooms = item.find('div', class_='listing__parameter listing__data--room-count')
                if rooms is None:
                    item_data['Rooms'] = 0
                else:
                    item_data['Rooms'] = item.find('div',
                                                   class_='listing__parameter listing__data--room-count').get_text().strip()

                if item_data['City'] == 'budapest':
                    item_data['District'] = item_data['full_address'].split(',')[-1].split('.')[0]
                else:
                    item_data['District'] = ''

                street = item_data['full_address'].split(',')[0]
                street_list = street.split(' ')

                for p in range(len(street_list)):

                    if street_list[p] in street_types:
                        item_data['Street type'] = street_list[p]
                        street_name_list = street_list[0:p]
                        item_data['Street'] = ' '.join(street_name_list)
                        break
                    else:
                        street_type = 0
                        street_name = 0

                self.data.append(item_data)

    def write_to_csv(self):
        # Method to write the scraped data to a CSV file
        # Open the CSV file in write mode
        with open(f'{self.city}{self.contract}.csv', 'w', encoding='utf8', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.DictWriter(csvfile, fieldnames=['City', 'Street', 'Street type', 'District',
                                                         'Price(HUF)', 'Area(m²)', 'Balcony(m²)', 'Rooms', ],
                                    extrasaction='ignore')
            # Write the field names to the CSV file
            writer.writeheader()
            # Write the data to the CSV file
            for row in self.data:
                writer.writerow(row)

    def csv_to_excel(self):
        file = f'C:/Users/gabri/OneDrive/Área de Trabalho/BME/1st semester/Programming/HM/{self.city}{self.contract}.csv'
        read_file = pd.read_csv(file)
        # read_file.drop(read_file.loc[read_file['Price']==0].index, inplace=True)
        # read_file.drop(read_file.loc[read_file['Rooms']==0].index, inplace=True)
        file_excel = f'C:/Users/gabri/OneDrive/Área de Trabalho/BME/1st semester/Programming/HM/{self.city}{self.contract}excel.xlsx'
        read_file.to_excel(file_excel, index=None, header=True)


def run_again():

    # Ask the user to run the code again
    run = input("Do you want to run the code again (y/n)? ")

    # If the user wants to run the code again, call the main function and return True
    if run == 'y':
        # Call the main function
        try:
            main()
        # If an exception is raised, print the error message
        except Exception as e:
            print(f'An error occurred: {e}')
        return True

    # If the user wants to exit, print goodbye and return False
    elif run == 'n':
        print('Goodbye!!!')
        return False
    # If the input is invalid, print an error message and call the function again
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return run_again()


def dashboard():
    # Set the directory where the Excel files are located
    directory = 'C:/Users/gabri/OneDrive/Área de Trabalho/BME/Programming/HM/'

    # Initialize a list to store the names of the Excel files
    excel_filenames = []

    # Iterate through all the files in the directory
    for filename in os.listdir(directory):
        # Check if the file is an Excel file
        if filename.endswith('.xlsx'):
            # Add the file to the list of Excel filenames
            excel_filenames.append(filename)

    # Create a dictionary to map the labels to the names of the Excel files
    label_dict = {'Debrecen Sale': 'debreceneladoexcel.xlsx',
                  'Budapest Sale': 'budapesteladoexcel.xlsx',
                  'Miskolc Sale': 'miskolceladoexcel.xlsx',
                  'Pécs Sale': 'pécseladoexcel.xlsx',
                  'Szeged Sale': 'szegedeladoexcel.xlsx',

                  'Debrecen Rent': 'debrecenkiadoexcel.xlsx',
                  'Budapest Rent': 'budapestkiadoexcel.xlsx',
                  'Miskolc Rent': 'miskolckiadoexcel.xlsx',
                  'Pécs Rent': 'pécskiadoexcel.xlsx',
                  'Szeged Rent': 'szegedkiadoexcel.xlsx'}

    # Initialize lists to store the data for sales and rent
    dfs_sales = []
    dfs_rent = []
    dfs_budapest_districts_sales = []
    dfs_budapest_districts_rent = []

    # Iterate through the list of Excel filenames
    for filename in excel_filenames:
        # Load the data from the Excel file into a dataframe
        df = pd.read_excel(directory + filename)

        # Calculate the average of the 'Price' and 'Area' column
        avg_price = df['Price(HUF)'].mean()
        avg_area = df['Area(m²)'].mean()

        # Get the label for the current Excel file
        # Uses a list comprehension to iterate over the key-value pairs in label_dict, and it includes only the key in the list if the value is equal to filename.
        # The resulting list will contain only the keys from label_dict that have a value equal to filename.
        label = [key for key, value in label_dict.items() if value == filename]
        # Set the label to 'Unknown' if it was not found in the dictionary
        if not label:
            label = 'Unknown'
        else:
            label = label[0]

        # Check if the current file contains 'budapest' in its name
        if 'budapest' and 'elado' in filename:
            # Create a new dataframe that contains only the rows where the 'District' column is not null
            df_budapest_districts = df[df['District'].notnull()]
            # Group the data by the 'District' column and calculate the average of the 'Price' column for each group
            avg_price_per_district = df_budapest_districts.groupby('District')['Price(HUF)'].mean()
            # Append the resulting data to the list for the third bar chart
            dfs_budapest_districts_sales.append({'filename': filename, 'avg_price_per_district': avg_price_per_district})

        if 'budapest' and 'kiado' in filename:
            # Create a new dataframe that contains only the rows where the 'District' column is not null
            df_budapest_districts = df[df['District'].notnull()]
            # Group the data by the 'District' column and calculate the average of the 'Price' column for each group
            avg_price_per_district = df_budapest_districts.groupby('District')['Price(HUF)'].mean()
            # Append the resulting data to the list for the third bar chart
            dfs_budapest_districts_rent.append({'filename': filename, 'avg_price_per_district': avg_price_per_district})

        # Separate the data based on the type of data (sales or rent)
        # Appending a dictionary to a lists (dfs_sales and dfs_rent). The dictionary contains four key-value pairs: 'filename', 'label', 'avg_price', and 'avg_area'.
        # The values for these keys are being set to the variables filename, label, avg_price, and avg_area, respectively.
        if 'elado' in filename:
            dfs_sales.append({'filename': filename, 'label': label, 'avg_price': avg_price, 'avg_area': avg_area})
        elif 'kiado' in filename:
            dfs_rent.append({'filename': filename, 'label': label, 'avg_price': avg_price, 'avg_area': avg_area})

    # Create a subplot for the charts
    # The make_subplots() function returns a Figure object, which represents a Plotly figure.
    fig = make_subplots(rows=3, cols=1)

    # Add the bar charts to the subplot

    # x and y arguments are being set to lists created using list comprehensions.
    # The x list contains the 'label' column of each dataframe in a list called dfs_sales,
    # The y list contains the 'avg_price' column of each dataframe in dfs_sales.
    fig.add_bar(x=[df['label'] for df in dfs_sales], y=[df['avg_price'] for df in dfs_sales], name='Sales', row=1, col=1)
    fig.add_bar(x=[df['label'] for df in dfs_rent], y=[df['avg_price'] for df in dfs_rent], name='Rent', row=1, col=1)
    # Set the labels for the x-axis and y-axis of the second chart
    fig.update_xaxes(title_text=' ', row=1, col=1)
    fig.update_yaxes(title_text='Average Price (HUF)', row=1, col=1)

    fig.add_bar(x=[df['label'] for df in dfs_sales], y=[df['avg_area'] for df in dfs_sales], name='Sales', row=2, col=1)
    fig.add_bar(x=[df['label'] for df in dfs_rent], y=[df['avg_area'] for df in dfs_rent], name='Rent', row=2, col=1)
    # Set the labels for the x-axis and y-axis of the second chart
    fig.update_xaxes(title_text=' ', row=2, col=1)
    fig.update_yaxes(title_text='Average Area (m²)', row=2, col=1)

    # Add the bar chart for the average price per district of Budapest
    fig.add_bar(x=dfs_budapest_districts_sales[0]['avg_price_per_district'].index,
                y=dfs_budapest_districts_sales[0]['avg_price_per_district'].values, name='Budapest Districts', row=3, col=1)
    fig.add_bar(x=dfs_budapest_districts_rent[0]['avg_price_per_district'].index,
                y=dfs_budapest_districts_rent[0]['avg_price_per_district'].values, name='Budapest Districts', row=3, col=1)

    # Set the labels for the x-axis and y-axis of the third chart
    fig.update_xaxes(title_text='District', row=3, col=1)
    fig.update_yaxes(title_text='Average Price (HUF)', row=3, col=1)

    # Set the title and labels of the bar chart
    fig.update_layout(title_text='Average Price by City')
    fig.update_layout(title_text='Average Area by City')

    # Create a dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                buttons=list([
                    dict(
                        args=[{'visible': [True, False]},
                              {'title': 'Average (Sales)'}],
                        label='Sales',
                        method='update'
                    ),
                    dict(
                        args=[{'visible': [False, True]},
                              {'title': 'Average (Rent)'}],
                        label='Rent',
                        method='update'
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Show the plot
    fig.show()


def main():
    p = UserSelection()
    city = p.city_input()
    contract = p.contract_input()
    scraper = WebScraper(f'https://realestatehungary.hu/szukites/{contract}+lakas+{city}', f'{city}.csv', city,
                         contract)
    scraper.scrape()
    scraper.write_to_csv()
    scraper.csv_to_excel()
    run_again()
    #dashboard()


main()
