# DataEngineer_Miniproject
Design a job to download files daily from SGX website.


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements-to-run">Requirements to run</a></li>
    <li>
      <a href="#discription-and-usage">Discription and Usage</a>
      <ul>
        <li><a href="#get_filepy">get_file.py</a></li>
        <li><a href="#nc_file_downloadpy">NC_file_download.py</a></li>
        <li><a href="#download_filecsv">download_file.csv</a></li>
      </ul>
    </li>
    <li><a href="#answer-questions-in-requirements-of-project">Answer questions in Requirements of project</a></li>
  </ol>
</details>



## Requirements to run
   - Python installed on the system.
   - Chrome Browser installed on the system.
   - Required python modules installed: ```logging```, ```os.path```, ```time```, ```sys```, ```datetime```, ```csv```,```platform```, ```webdriver_manager```,```pandas```,```selenium``` 

  

## Discription and Usage
### get_file.py
#### Description : This is a Python script that downloads files from SGX website

   - The script uses the Selenium library to automate Chrome browser and navigate to SGX website where files can be downloaded.
   - Users are required to input the numbers (corresponding to the name of files) and the date of files they wish to download. (1 corresponds to 'WEBPXTICK_DT.zip', 2 corresponds to 'TickData_structure.dat', 3 corresponds to 'TC.txt', 4 corresponds to 'TC_structure.dat')
   - Multiple numbers can be entered at once, separated by commas (e.g. 1,2,3,4).
   - The program will exit if the date (users input) is a weekend or not valid (e.g. 30 Feb 2023).  
   - Otherwise, it creates a folder (if not exist) with the date based on files (date that user provide) and sets it as the default download directory for Chrome.
   - The script logs the progress of the download by writing to a CSV file named **download_file.csv**. (At first, the 'status' is 'Not Completed')
   - Then, the download process starts by accessing the download link.
   - Once the download process has completed (or it may not happen), verify the existence of the file by its name. If the file is found, the 'status' field in the **download_file.csv** will be updated to 'Completed' to indicate that the download was successful. If the file is not found, the 'status' field remain unchanged.
   - The downloaded files are stored in a 'Downloads' folder, organized by the date of the files.
#### Usage

   - Execute the program based on your operating system: ```py get_file.py``` (if you are using Window terminal) or ```python3 get_file.py``` (if you are using Linux terminal).
   - After the program is launched, users will be prompted to input interger numbers. (1 corresponds to 'WEBPXTICK_DT.zip', 2 corresponds to 'TickData_structure.dat', 3 corresponds to 'TC.txt', 4 corresponds to 'TC_structure.dat'). Multiple numbers can be entered at once, separated by commas (e.g. 1,2,3,4). 
   - Users also will be prompted to input date (require in format "DD MON YYYY", e.g. "13 Mar 2023"). Only one date input can be provided at a time. If users input date is weekend or not valid (e.g. 30 Feb 2023), the program will exit in 10s. 
   - Or execute the program: ```py get_file.py -n '1,4' -d '16 Mar 2023'```(if you are using Window terminal) or ```python3 get_file.py -n '1,4' -d '16 Mar 2023'``` if you are using Linux terminal). The above commands will immediately initiate the download process without requiring any input.
   - After that, the download process starts. When it is completed, the browser quits.
   
   
   
### NC_file_download.py
#### Description : This is a Python script that downloads files which are 'Not Completed' (Redownload)
  
   - The script reads a CSV file named **download_file.csv** that contains information about the files had been downloaded from **get_file.py**.
   - It prints out the rows that have a status of 'Not Completed', which indicates that the file has not been downloaded yet.
   - Users are prompted to enter the ID of the files (only 'Not Complete' files) they want to download.
   - The script then extracts the type of data and the date from the selected row, creates a directory with the name of the date if it doesn't already exist, and sets up the browser to download the file to that directory.
   - If the download is successful, the status of the row in the CSV file is updated to 'Completed'. If there is an error during the download, the status of the row is updated to 'Not Completed' and an error message is logged.
   - The downloaded files are stored in a 'Downloads' folder, organized by the date of the files.

#### Usage
   - Execute the program based on your operating system: ```py NC_file_download.py``` (if you are using Window terminal) or ```python3 NC_file_download.py``` (if you are using Linux terminal).
   - After the program is launched, it returns rows that have a status of 'Not Completed' from **download_file.csv**.
   - Users are prompted to enter the ID of the files (only 'Not Complete' files) they want to download. Multiple IDs can be entered at once, separated by commas (e.g. 8,13,25).
   - Or execute the program: ```py NC_file_download.py -id '2,11'```(if you are using Window terminal) or ```python3 NC_file_download.py -id '2,11'``` if you are using Linux terminal). The above commands will immediately initiate the redownload process without requiring any input.
   - After that, the redownload process starts. When it is completed, the browser quits.

### download_file.csv
#### Description: A CSV file stores the download information for files from both **get_file.py** and **NC_download_file.py**

   - This CSV has 5 columns: id, type_of_data ,date, time_init, last_update, status.
   - The 'id' column is automatically incremented whenever a new row is created.
   - The 'type_of_data' column contains 4 types: WEBPXTICK_DT.zip, TickData_structure.dat, TC.txt, TC_structure.dat.
   - The 'date' column indicates the date of the downloaded files.
   - The 'time_init' column indicates the time when the row was initially created.
   - The 'last_update' column indicates the lattest time when the row was updated.
   - The 'status' has only 2 possible values: 'Completed' and 'Not Completed'

#### Usage: If users want to view this file, they should make a copy.

## Answer questions in Requirements of project
3. Logging must be implemented.
    > A: In both **get_file.py** and **NC_download_file.py**, I have implemented logging functionality to record program information. This is achieved by creating a directory named 'logging_file' if it does not already exist, and storing the log files in this directory. The log file name is set to "logging_<current_date>.log", where <current_date> is the current date when the program is executed, in the format 'YYYY-MM-DD'. For instance, if the script is executed on **17th March 2023**, the log file will be saved as _logging_file/logging_2023-03-17.log_. The logging setup includes a specified logging format that consists of the date and time of the log message, the severity level of the message, and the actual message content. The logging levels are set to DEBUG for the log file and INFO for the console.
4. The recovery plan should be considered. For example, you may ask yourself the following questions:
 - a. If the downloading failed on one day or on some days how do you redownload the missed file(s)?
    > A: There is a CSV file named **download_file.csv** that contains information about the files that were not successfully downloaded, as indicated by the "Not Completed" status. I can use the **NC_download_file.py** to redownload these files.
 - b. Is the redownloading automatic or does it require manual intervention?
    > A: The redownloading is automatic by using **NC_download_file.py**. When running it, the script will generate a table that lists all the rows from the CSV file where the "status" column value is set to "Not Completed". I will input the IDs of the rows that need to be redownloaded, which can be inputed many IDs at the same time. Once the IDs have been entered, the script will commence the redownloading process, downloading the files one by one.
 - c. The website only lists the recent files. Is it possible to download older files?
    > A: The website only list files (if any) for the past 5 market days. However, I have discovered that the download links for the files follow a specific pattern. For instance, the download link of **WEBPXTICK_DT.zip** on **17 Mar 2023** is _https://links.sgx.com/1.0.0/derivatives-historical/5378/WEBPXTICK_DT.zip_. The number **5378** in the URL corresponds to the date **17 Mar 2023**. Therefore, if I wish to download files for other days, I can modify the download link by changing the date-specific number and the name of the file (There are 4 types of file: WEBPXTICK_DT.zip, TickData_structure.dat, TC.txt, TC_structure.dat). For example, to download file **TC_structure.dat** on **13 Jan 2023**, the download link would be _https://links.sgx.com/1.0.0/derivatives-historical/5333/TC_structure.dat_
5. Address any of your concerns in your design.
    > - **get_file.py** and **NC_download_file.py** are designed to accurately download files starting from 19 Dec 2020. I cannot guarantee that input dates before **19 Dec 2020** will return the correct download link.
    > - Both **get_file.py** and **NC_download_file.py** are compatible with the Linux and Windows operating systems. However, their compatibility with other operating systems is uncertain.
