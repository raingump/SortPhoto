# SortPhoto
A python script to make it way more easier to sort the pictures by date.


# How to use

```shell
python sort_photos.py -d /YOUR/SOURCEDIR -o /YOUR/RESULTDIR
```
It is to take the pictures in the `/YOUR/SOURCEDIR` directory, organize them by month, and export them to the `/YOUR/RESULTDIR` directory.


# Require
You may need to install [ExifRead](https://pypi.org/project/ExifRead/) if you encounter an error like  `ModuleNotFoundError: No module named 'exifread'`.
Installation of ExifRead:

```shell
$ pip install exifread
```


# Features

1. Iterate through the subfolders in the given `/YOUR/SOURCEDIR` directory to get all the files.
2. Use a more accurate modification time when EXIF information is missing.



# Thanks to

Thanks to [码客](https://zhuanlan.zhihu.com/p/55266474). Most of the codes come from this site. And I added 2 features to make it a lot more convenient to use.
