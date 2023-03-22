import argparse
import pandas as pd
import logging
import os.path
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import platform

# Create a parser object
parser = argparse.ArgumentParser(description="A program that takes numbers and date as input (e.g. py NC_file_download.py -id '3,9')")

# Add arguments for numbers and date
parser.add_argument("-id", "--id", help="Input Id of rows that wish to redownload", type=str)

# Parse arguments from command line
args = parser.parse_args()

# Set up logging
log_dir = 'logging_file'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = f"{log_dir}/logging_{datetime.now().strftime('%Y-%m-%d')}.log"
log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=log_file, format=log_format, level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Function 
def find_file_by_partial_name(partial_name, path):
    """Find file by name to check the download is completed or not.
    
    Args:
        partial_name (str): The substring to search for in file names.
        path (str): The file path contains the file.
    
    Returns:
        str or None: The absolute path to the first file found or None if no file
            with the given partial name is found.
    """
    
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if partial_name in name: 
                return os.path.join(dirpath, name)
    return None

def get_download_link(input_num, input_date):
    """Get the download link based on name of file (WEBPXTICK_DT.zip, TickData_structure.dat,...) and date (date will be converted to corresponding number).
       Accurately download files starting from 19 Dec 2020, not guarantee input dates before 19 Dec 2020.

    Args:
        input_num (int): the input number (1-4) corresponding to the file to download
        input_date (str): the input date in the format "DD MON YYYY", convert to corresponding numbers

    Returns:
        str: a download link for the specified file and date
    """
    
    start_date = dt.date(2020, 12, 29)
    start_number = 4800
    
    # Convert 'input_date' to corresponding numbers
    date_num = dt.datetime.strptime(input_date, "%d %b %Y").date()
    delta = date_num - start_date
    num_weekend_days = sum(1 for i in range(delta.days + 1) if (start_date + dt.timedelta(i)).weekday() >= 5)
    num = start_number + delta.days - num_weekend_days
    
    # Check if date is weekend or not
    if date_num.weekday() >= 5:
        logging.info("Error: date is a weekend.")
        return None
    else:
        name_file_dict = {1: 'WEBPXTICK_DT.zip', 
                          2: 'TickData_structure.dat', 
                          3: 'TC.txt', 
                          4: 'TC_structure.dat'}
        name_file = name_file_dict.get(input_num, '')
        
        get_link = f"https://links.sgx.com/1.0.0/derivatives-historical/{num}/{name_file}"
        return get_link


# Read csv file
df = pd.read_csv('download_file.csv')

# Print row which status is 'Not Completed'
not_completed_df = df[df['status'] == 'Not Completed']
num_rows = not_completed_df.shape[0]
print('Number of rows in not_completed_df:', num_rows)
print(not_completed_df.to_string(index=False))


# Use default values if arguments are not given
if args.id is None:
    args.id = input("Input ID: ")

id_input = args.id.split(',')

for id in id_input:
    id = int(id)
    
# Extract tod,y,i from the selected row
    tod = df.loc[df['id'] == id, 'type_of_data'].iloc[0]
    y = df.loc[df['id'] == id, 'date'].iloc[0]

    if 'WEBPXTICK_DT' in tod:
        i = 1
    elif 'TickData_structure' in tod:
        i = 2
    elif 'TC_20' in tod:
        i = 3
    elif 'TC_structure' in tod:
        i = 4


# Create file base on date
    path_down = r"{0}\Downloads\{1}".format(os.getcwd(),y)
    try:
        system_name = platform.system()
    except:
        pass

    if system_name == 'Linux':
        path_down = path_down.replace("\\", "/")

    if not os.path.exists(path_down):
        os.makedirs(path_down)

# Run Chrome
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": path_down})
    s=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s,options=options)
    browser.get("https://www.sgx.com/research-education/derivatives")
    sleep(5)

# Log download info
    logging.info("Downloading {0} ({1})".format(tod,y))

# Update last_update of row
    row_index = df.index[df['id'] == id].tolist()[0]
    df.at[row_index, 'last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.to_csv('download_file.csv', index=False)
    logging.info('Update last_update of row in csv successfully')
    
# Download process    
    try:
        # Download
        link_download = get_download_link(i,y)
        browser.get(link_download)
        sleep(10)

        # Check if file exist -> Download completed or not
        filepath = find_file_by_partial_name('{}'.format(tod), path_down)
        if filepath:
            logging.info("Completed: Download file '{0} ({1})'".format(tod,y))
            status = 'Completed'
        else:
            logging.info("Not completed: Download file '{0} ({1})'".format(tod,y))
            status = 'Not Completed'
        
        # Update the status of row 
        row_index = df.index[df['id'] == id].tolist()[0]
        df.at[row_index, 'last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df.at[row_index, 'status'] = status
        df.to_csv('download_file.csv', index=False)
        logging.info('Update status of row in csv successfully')
    
    except Exception as e:
            logging.error("Error downloading {0} ({1}): {2}".format(tod,y,e))

# Quit the browser
sleep(10)
browser.quit()
logging.info('Quit the browser')



