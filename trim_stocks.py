import sys
import os
import ast
import time
import json
import operator
import datetime
import math

def clean_date(date_str):
    date=datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    # print(date)
    return date

def main():
    with open("TweetDates.json",'r') as dates:
        dates_list = json.load(dates)
       
    # Date,Open,High,Low,Close,Volume,OpenInt
    # YYYY-MM-DD
    out_string = ""
    with open("aapl.us.txt",'r') as stock:
        out_string+=stock.readline()
        for i, line in enumerate(stock):
            line_list = line.split(',')
            year = int(line_list[0][:4])
            print(year)
            if year>2014:
                cleaned_date = clean_date(line_list[0])
                print("{}->{}".format(line_list[0], cleaned_date))
                if cleaned_date in dates_list:
                    out_string+=line
            
    with open("aaplStock.csv",'w+') as trim:
        trim.write(out_string)


if __name__ == "__main__":
    main()