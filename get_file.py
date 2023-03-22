import argparse
import logging
import os.path
import sys
from datetime import datetime as datetimer
import datetime as dt
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import platform

    
# Create a parser object
parser = argparse.ArgumentParser(description="A program that takes numbers and date as input (e.g. py get_file.py -n '1,3' -d '20 Mar 2023')")

# Add arguments for numbers and date
parser.add_argument("-n", "--numbers", help="Input numbers.(1 corresponds to 'WEBPXTICK_DT.zip', 2 corresponds to 'TickData_structure.dat', 3 corresponds to 'TC.txt', 4 corresponds to 'TC_structure.dat'). Multiple numbers can be entered at once, separated by commas (e.g. 1,2,3,4)", type=str)
parser.add_argument("-d", "--date", help="Input date in dd mmm yyyy format (e.g. '13 Mar 2023')", type=str)

# Parse arguments from command line
args = parser.parse_args()

# Set up logging
log_dir = 'logging_file'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = f"{log_dir}/logging_{datetimer.now().strftime('%Y-%m-%d')}.log"
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


def add_log_entry(tod, y):
    """Append a new row to the 'download_file.csv' file.

    Args:
        tod (str): type of data
        y (str): date of file
    """
    # Open CSV file in read mode and get the last ID value
    with open('download_file.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        id = 0
        for row in reader:
            if len(row) > 0:
                id = int(row[0])

    # Append new row to CSV file
    with open('download_file.csv', 'a', newline='') as csvfile:
        csvfile.seek(0, 2)
        writer = csv.writer(csvfile)
        id += 1
        time_init = datetimer.now().strftime('%Y-%m-%d %H:%M:%S')
        last_update = datetimer.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Not Completed'
        writer.writerow([id, tod, y, time_init, last_update, status])
        logging.info('Add new row to csv successfully!')


def update_log_entry(status):
    """Update the recent rows from add_log_entry() to change the status.

    Args:
        status (str): status of file ('Completed' or 'Not Completed')
    """
    # Open CSV file in read mode and find the last row
    with open('download_file.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        last_row = rows[-1]

    # Update last row's last_update and status fields
    last_row[-2] = datetimer.now().strftime('%Y-%m-%d %H:%M:%S')
    last_row[-1] = status

    # Write updated rows back to CSV file
    with open('download_file.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    logging.info('Update status of row in csv successfully!')

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






# Input values if arguments are not given
if args.numbers is None:
    args.numbers = input("Input numbers: ")
if args.date is None:
    args.date = input("Input date in dd mmm yyyy format: ")

# Replace commas with spaces in numbers argument
args.numbers = args.numbers.replace(",","")

# Check if date is valid or not
try:
    y_check = dt.datetime.strptime(args.date, "%d %b %Y").date()
except ValueError:
    logging.info("Error: date {} is not valid.".format(args.date))
    logging.info('The program will exit in 10s')
    sleep(10)
    sys.exit()


# Check if date is weekend or not
if y_check.weekday() < 5:
    pass
else:
    logging.info("Error: date {} is a weekend.".format(args.date))
    logging.info('The program will exit in 10s')
    sleep(10)
    sys.exit()



# Create file base on date
path_down= r"{0}\Downloads\{1}".format(os.getcwd(),args.date)

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


# Download process
for i in args.numbers:
    y_date = datetimer.strptime(args.date, '%d %b %Y').strftime('%Y%m%d') #Take the input date to detect file name
    i = int(i)
    tod_dict = {1: 'WEBPXTICK_DT-{}'.format(y_date), 
                2: 'TickData_structure', 
                3: 'TC_{}'.format(y_date), 
                4: 'TC_structure'}
    tod = tod_dict.get(i, '')
    
    # Log download info
    logging.info("Downloading {0} ({1})".format(tod,args.date))
    
    # Add row to download_file.csv
    add_log_entry(tod,args.date)

    try:
        # Download based on link
        link_download = get_download_link(i,args.date)
        browser.get(link_download)
        sleep(10)

        # Check if file exist -> Download completed or not
        filepath = find_file_by_partial_name('{}'.format(tod), path_down)
        if filepath:
            logging.info("Completed: Download file '{0} ({1})'".format(tod,args.date))
            status = 'Completed'
        else:
            logging.info("Not completed: Download file '{0} ({1})'".format(tod,args.date))
            status = 'Not completed'
        
        # Update the status of recent row 
        update_log_entry(status)

    except Exception as e:
        logging.error("Error downloading {0} ({1}): {2}".format(tod,args.date,e))

# Quit the browser
sleep(10)
browser.quit()
logging.info('Quit the browser')
