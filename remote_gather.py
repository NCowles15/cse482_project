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


def process_file(file_path, local_path, keywords):
    file_list = []
    count = 0
    line_count = 0
    out_str = ""
    file_char_size = 0
    char_size = 0
    start_time = time.time()

    with open(local_path, 'w+') as save_file:
        with open(file_path, 'r') as read_file:
            for i,line in enumerate(read_file):
                file_char_size+=len(line)
                if line.strip() != "":
                    try:
                        tweet = json.loads(line)
                        if 'text' in tweet.keys():
                            for keyword in keywords:
                                if keyword.lower() in tweet["text"].lower():
                                    # print(tweet["text"])
                                    file_list.append(tweet)
                                    out_str+=json.dumps(tweet, indent=2)
                                    count+=1
                                    char_size += len(json.dumps(tweet, indent=2))
                                    break
                    except:
                        print("Failed on line: {}".format(i))
                    # else:
                    #     print(tweet)
                line_count=i
        save_file.write(out_str)
    time_diff = time.time() - start_time
    time_diff_pretty = time.strftime('%H:%M:%S', time.gmtime(time_diff))
    ret_size = os.path.getsize(local_path)
    ret_size_pretty = convert_size(ret_size)
    ret_str = " Kept: {}/{} lines; Reduced size {} to {}, {:0.2f}% reduction; New size: {}; Time: {};\n".format(count, line_count, file_char_size, char_size, file_char_size/(char_size+1), ret_size_pretty, time_diff_pretty)

    return ret_str, ret_size


def main():
    listings = get_listing_file()
    keywords = ["Apple", "aapl", "AAPL"]
    twit_dir = "/user/research/ptan/data/Twitter/"
    local_dir = os.getcwd()
    local_twit = os.path.join(local_dir, "Twitter")
    save_string = ""
    total_size = 0
    log_count = 56
    log_size = 0
    if not listings:
        listings = get_listing(twit_dir)
    start_time = time.time()
    listings_new = [item[0] for item in listings]
    listings=listings_new
    try:
        for i, file in enumerate(listings):
            filename = file
            if 7269< i < len(listings):
            # if i < 10:
                print("[{}] Reading file {}/{}: {}".format(datetime.datetime.now().time(), i, len(listings), filename))
                save_string += "[{}] Reading file {}/{}: {};".format(datetime.datetime.now().time(), i, len(listings), filename)
                remote_path = os.path.join(twit_dir, filename)
                local_path = os.path.join(local_twit, filename)
                # print("Downloading {} to {}".format(remote_path, local_path))
                # sftp.get(remote_path, local_path)
                # remote_file = sftp.open(remote_path)
                ret_string, ret_size = process_file(remote_path, local_path, keywords)
                save_string += ret_string
                print(ret_string[1:-1])
                total_size+=ret_size
                log_size+=ret_size
                if log_size > 50000000:
                    save_string += "It took {} to read {} files\n".format(
                        time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), len(listings))
                    filename = "TweetParseLogTrue" + str(log_count) + ".txt"
                    local_path = os.path.join(local_dir, filename)
                    with open(local_path, 'w+') as save_file:
                        save_file.write(save_string)
                    log_size = 0
                    log_count+=1
                # if total_size>1000000000:
                #     print("[{}] Nearing memory limit at file {}/{}. Please purge these files to continue".format(datetime.datetime.now().time(),i,len(listings)))
                #     break
        save_string += "It took {} to read {} files\n".format(
            time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), len(listings))
        filename = "TweetParseLogTrue" + str(log_count) + ".txt"
        local_path = os.path.join(local_dir, filename)
        with open(local_path, 'w+') as save_file:
            save_file.write(save_string)
    except KeyboardInterrupt:
        save_string += "It took {} to read {} files\n".format(
            time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), len(listings))
        filename = "TweetTerminateLog.txt"
        local_path = os.path.join(local_dir, filename)
        with open(local_path, 'w+') as save_file:
            save_file.write(save_string)



if __name__ == "__main__":
    main()