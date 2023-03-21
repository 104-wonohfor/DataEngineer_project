# DE_mini_project
Design a job to download files daily from SGX website.


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirement-of-project">Requirement of project</a></li>
    <li><a href="#library">Library</a></li>
    <li>
      <a href="#discription-and-usage">Discription and Usage</a>
      <ul>
        <li><a href="#get_file">get_file</a></li>
        <li><a href="#nc_download_file">NC_download_file</a></li>
        <li><a href="#download_file_csv">download_file_csv</a></li>
      </ul>
    </li>
    <li><a href="#answer-questions-in-requirement">Answer questions in Requirement</a></li>
  </ol>
</details>


## Requirement of project
1. It should be written in python and run like usual Linux commands, i.e. accepting command line options or even config file.
2. It should be able to download both historical files (files not on today) and today's file based on user's instructions.
3. Logging must be implemented.
  - a. Use logging module provided by python, which can provide flexible logging configurations, e.g. some messages are logged to both stdout and file, and some to file only.
  - b. Make decisions on what messages/levels to log by yourself. The logs should help to debug/resolve issues.
4. The recovery plan should be considered. For example, you may ask yourself the following questions:
  - a. If the downloading failed on one day or on some days how do you redownload the missed file(s)?
  - b. Is the redownloading automatic or does it require manual intervention?
  - c. The website only lists the recent files. Is it possible to download older files?
5. Address any of your concerns in your design.

## Library

## Discription and Usage
### get_file
#### - Discription : This is a Python script that downloads files from SGX website

   - The script uses the Selenium library to automate Chrome browser and navigate to SGX website where files can be downloaded.
   - Users are required to input the numbers (corresponding to the name of files) and the date of files they wish to download. (1 corresponds to 'WEBPXTICK_DT.zip', 2 corresponds to 'TickData_structure.dat', 3 corresponds to 'TC.txt', 4 corresponds to 'TC_structure.dat')
   - Multiple numbers can be entered at once, separated by commas (e.g. 1,2,3,4).
   - The program will exit if the date (users input) is a weekend or not valid (e.g. 30 Feb 2023).  
   - Otherwise, it creates a folder (if not exist) with the date based on files (date that user provide) and sets it as the default download directory for Chrome.
   - The script logs the progress of the download by writing to a CSV file named **download_file.csv**. (At first, the 'status' is 'Not Completed')
   - Then, the download process starts by accessing the download link.
   - Once the download process has completed (or it may not happen), verify the existence of the file by its name. If the file is found, the 'status' field in the **download_file.csv** will be updated to 'Completed' to indicate that the download was successful. If the file is not found, the 'status' field remain unchanged.
#### - Usage

   - After the program is launched, users will be prompted to input interger numbers. (1 corresponds to 'WEBPXTICK_DT.zip', 2 corresponds to 'TickData_structure.dat', 3 corresponds to 'TC.txt', 4 corresponds to 'TC_structure.dat'). Multiple numbers can be entered at once, separated by commas (e.g. 1,2,3,4). Any extra space may lead to error.
   - Users also will be prompted to input date (require in format "DD MON YYYY", e.g. "13 Mar 2023"). Only one date input can be provided at a time. If users input date is weekend or not valid (e.g. 30 Feb 2023), the program will exit in 10s. 
   - After that, the download process will start until the browser quits.
   
   
   
### NC_download_file
#### - Discription : This is a Python script that downloads files which are 'Not Completed' (Redownload)

   - The script reads a CSV file named 'download_file.csv' that contains information about the files had been downloaded from **get_file.py**
   - 

### download_file_csv

## Answer questions in Requirement
3. Logging must be implemented.
    > A: In both **get_file.py** and **NC_download_file.py**, I have implemented logging functionality to record program information. This is achieved by creating a directory named 'logging_file' if it does not already exist, and storing the log files in this directory. The log file name is set to "logging_<current_date>.log", where <current_date> is the current date when the program is executed, in the format 'YYYY-MM-DD'. For instance, if the script is executed on **17th March 2023**, the log file will be saved as _logging_file/logging_2023-03-17.log_. The logging setup includes a specified logging format that consists of the date and time of the log message, the severity level of the message, and the actual message content. The logging levels are set to DEBUG for the log file and INFO for the console.
4. The recovery plan should be considered. For example, you may ask yourself the following questions:
 - a. If the downloading failed on one day or on some days how do you redownload the missed file(s)?
    > A: There is a CSV file named **download_file.csv** that contains information about the files that were not successfully downloaded, as indicated by the "Not Completed" status. I can use the **NC_download_file.py** script to redownload these files.
 - b. Is the redownloading automatic or does it require manual intervention?
    > A: The redownloading is automatic by using **NC_download_file.py**. When running it, the script will generate a table that lists all the rows from the CSV file where the "status" column value is set to "Not Completed". I will input the IDs of the rows that need to be redownloaded, which can be inputed many IDs at the same time. Once the IDs have been entered, the script will commence the redownloading process, downloading the files one by one.
 - c. The website only lists the recent files. Is it possible to download older files?
    > A: The website only list files (if any) for the past 5 market days. However, I have discovered that the download links for the files follow a specific pattern. For instance, the download link of **WEBPXTICK_DT.zip** on **17 Mar 2023** is _https://links.sgx.com/1.0.0/derivatives-historical/5378/WEBPXTICK_DT.zip_. The number **5378** in the URL corresponds to the date **17 Mar 2023**. Therefore, if I wish to download files for other days, I can modify the download link by changing the date-specific number and the name of the file (There are 4 types of file: WEBPXTICK_DT.zip, TickData_structure.dat, TC.txt, TC_structure.dat). For example, to download file **TC_structure.dat** on **13 Jan 2023**, the download link would be _https://links.sgx.com/1.0.0/derivatives-historical/5333/TC_structure.dat_
5. Address any of your concerns in your design.
    > - **get_file.py** and **NC_download_file.py** are designed to accurately download files starting from 19 Dec 2020. I cannot guarantee that input dates before **19 Dec 2020** will return the correct download link.
    
