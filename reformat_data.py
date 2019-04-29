import sys
import os
import ast
import time
import json
import operator
import datetime
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def get_listing(dir):
    name_listings = os.listdir(dir)
    fpw = open("twitDirFiles.txt", "w")
    listings = []
    for item in name_listings:
        item_path = os.path.join(dir, item)
        stats = os.stat(item_path)
        listings.append((item, stats))
    listings.sort(key=operator.itemgetter(1))
    for item in listings:
        print("{} {}".format(item[0], item[1]), file=fpw)
    return listings


def get_listing_file():
    try:
        fp = open("twitDirFiles.txt")
        listings = [line.strip().split(' ') for line in fp]
        fp.close()
        return listings
    except:
        return []

def make_array(file_path, out_path):
    save_string="["
    with open(file_path, 'r') as read_file:
        for i, line in enumerate(read_file):
            if line[:2] == "}{":
                save_string+="},{\n"
            else:
                save_string+=line
        save_string += "]"

    with open(out_path, 'w+') as save_file:
        # print("saving {}...{} to {}".format(save_string[:20], save_string[len(save_string)-20:], file_path+".json"))
        save_file.write(save_string)

def array_to_data(file_path):
    with open(file_path, 'r') as read_file:
        data = json.load(read_file)

    # print("data from {}: {}".format(file_path,data))
    return data

def main():
    listings = get_listing_file()
    keywords = ["Apple", "aapl", "AAPL"]
    twit_dir = "/user/research/ptan/data/Twitter/"
    local_dir = os.getcwd()
    local_twit = os.path.join(local_dir, "Twitter")
    local_twit_json = os.path.join(local_dir, "../TwitterJSON")
    if not listings:
        listings = get_listing(local_twit)

    listings_new = [item[0] for item in listings]
    listings = listings_new
    total_data = []
    start_time = time.time()
    inner_time = time.time()
    j=1
    for i, file in enumerate(listings):
        filename = file
        print("[{}] Reading file {}/{}: {}".format(datetime.datetime.now().time(), i, len(listings), filename))
        if i < (len(listings)/10)*j and j<8:
            remote_path = os.path.join(twit_dir, filename)
            local_path = os.path.join(local_twit, filename)
            save_path = os.path.join(local_twit_json, filename+".json")
            make_array(local_path, save_path)
            new_data = array_to_data(save_path)
            total_data += new_data
        else:
            print( "It took {} to read {} files".format(
                time.strftime('%H:%M:%S', time.gmtime(time.time() - inner_time)), len(listings)/10))
            print( "It took {} to read {} files".format(
                time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), i))
            filename = "TweetPackage.json"
            local_path = os.path.join(local_dir, filename)
            save_type = "w+"
            with open(local_path, save_type) as save_file:
                json.dump(total_data, save_file)
            j+=1
            inner_time = time.time()

    print( "It took {} to read {} files".format(
        time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), len(listings)))

if __name__ == "__main__":
    main()