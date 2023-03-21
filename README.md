# DE_mini_project
DE_mini_project


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
### NC_download_file
### download_file_csv

## Answer questions in Requirement
4. The recovery plan should be considered. For example, you may ask yourself the following questions:
 - a. If the downloading failed on one day or on some days how do you redownload the missed file(s)?
    > A: The infromation of missed files were saved in download_file.csv which have 'status' are 'Not Completed'. It can be redownload by using NC_download_file.py.
 - b. Is the redownloading automatic or does it require manual intervention?
    > A: The redownloading is automatic by using NC_download_file.py. When running it, it will provide a table contains all row which have 'status' is 'Not Completed'. Then, input ID of rows which need to be redownload. 
