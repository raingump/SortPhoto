import os
import exifread
import sys
import getopt
import re
import shutil
from datetime import datetime


def get_exif(file_name_with_path):
    field = "EXIF DateTimeOriginal"
    fd = open(file_name_with_path, 'rb')
    tags = exifread.process_file(fd)
    fd.close()

    file_date = ""
    if field in tags:
        print("file %s,date %s" % (file_name_with_path, str(tags[field])))
        file_date = str(tags[field])

    if len(file_date) == 0:
        timestamp = os.path.getmtime(file_name_with_path)
        file_date = datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')
        print("file_date is empty, get create time as result, ctime = %s" % file_date)
        # timestamp1 = os.path.getatime(file_name_with_path)
        # timestamp2 = os.path.getmtime(file_name_with_path)
        # print("timestamp1 = %s, timestamp2 = %s" % (datetime.fromtimestamp(timestamp1).strftime('%Y:%m:%d %H:%M:%S'), datetime.fromtimestamp(timestamp2).strftime('%Y:%m:%d %H:%M:%S')))

    return file_date


def find_all_file(imgpath):
    file_date_dict = {}
    for root, ds, fs in os.walk(imgpath):
        for f in fs:
            full_file_name = os.path.join(root, f)
            if os.path.isfile(full_file_name):
                file_date_dict[full_file_name] = get_exif(full_file_name)
            else:
                print ("nofile: full_file_name = %s" % full_file_name)
    return file_date_dict


def get_all_img(imgpath):
    file_date_dict = {}
    for file_name in os.listdir(imgpath):
        full_file_name = os.path.join(imgpath, file_name)
        if os.path.isfile(full_file_name):
            file_date_dict[full_file_name] = get_exif(full_file_name)

    return file_date_dict


def usage():
    print(sys.argv[0])
    print("-h help info")
    print("-d img_dir")
    print("-o output dir")


def copy_file_to(file_name, dir_name):
    if not os.path.exists(dir_name):
        print("mkdir %s" % dir_name)
        os.makedirs(dir_name)

    if os.path.exists(dir_name):
        print("copy %s to dir %s" % (filename, dir_name))
        shutil.copy(file_name, dir_name)


img_dir = ""
out_dir = ""
opts, args = getopt.getopt(sys.argv[1:], "hd:o:")

for op, value in opts:
    if op == "-d":
        img_dir = value
    if op == "-o":
        out_dir = value
    if op == "-h":
        usage()
        sys.exit()


all_file_dict = {}
if len(img_dir) > 0:
    # all_file_dict = get_all_img(img_dir)
    all_file_dict = find_all_file(img_dir)
else:
    print("%s -d img_dir" % (sys.argv[0]))


for filename, filedate in all_file_dict.items():
    date_re = re.compile(r'((\d+):(\d+):(\d+) \d+:\d+:\d+)')
    result = date_re.search(filedate)
    if result:
        result_group = result.groups()
        # for date_item in result_group:
        #    print date_item
        dir_name = result_group[1] + result_group[2]
        if len(out_dir) > 0:
            copy_file_to(filename, out_dir + "/" + dir_name)
    else:
        # print("%s has no date info" %(filename))
        if len(out_dir) > 0:
            copy_file_to(filename, out_dir + "/nodate")
