# -*- coding: utf-8 -*-
"""Main module."""

__author__ = "Yarving Liu"
__author_email__ = "yarving@qq.com"


import os
import tempfile
from datetime import datetime

import requests
from PyPDF2 import PdfFileReader, PdfFileWriter


def merge(files, filename):
    """ Merge PDF files

    """
    writer = PdfFileWriter()

    for f in files:
        pdf = PdfFileReader(open(f, "rb"), strict=False)

        # 分别将page添加到输出output中
        for page in range(pdf.getNumPages()):
            writer.addPage(pdf.getPage(page))

    with open(filename, "wb") as stream:
        writer.write(stream)


def download(date, force=False):
    """

    """
    fmt_path = '%Y-%m/%d'
    file_path = datetime.strftime(date, fmt_path)
    fmt_name = '%Y%m%d'
    file_prefix = datetime.strftime(date, fmt_name)

    outfile = f"rmrb{file_prefix}.pdf"
    if os.path.exists(outfile) and not force:
        print(f"{outfile} already exist, skip to download")
        return outfile

    base = "http://paper.people.com.cn/rmrb/images"
    print("downloading with requests")

    # create a temp dir to download segment files
    temp_dir = tempfile.mkdtemp()
    files = []
    for i in range(1, 31):
        filename = f"rmrb{file_prefix}{i:02d}.pdf"
        url = f"{base}/{file_path}/{i:02d}/{filename}"

        r = requests.get(url)
        if r.ok:
            print(url)
            output = os.path.join(temp_dir, filename)
            files.append(output)
            with open(output, "wb") as f:
                f.write(r.content)
        else:
            print('download complete!!')
            break

    merge(files, outfile)

    return outfile
