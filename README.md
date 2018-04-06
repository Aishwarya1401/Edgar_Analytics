# Edgar_Analytics
Insight data challenge

The code is written in Python

I read the log.csv file using csv.DictReader

I created an Ordered dictionary with ip as the key and value as a dictionary of each field in log record , and an ordered dictionary maintains the order in which the records were processed.

As I'm processing the records I'm checking if the time elapsed for each ip is greater than inactivity period, if it is I'm writing that particular ip to the outputfile and removing it from the dictionary.

I'm directly incrementing the count of web page requests for each ip because in the FAQ it is given that every time a user accesses an EDGAR document, that request should be counted even if the user is requesting the same document multiple times, so it doesn't matter what the document id.


For calculating the difference between two time I'm using datetime module of Python

At the end of file I'm writing all the records which are left in the dictionary
