#!/usr/bin/env python3

import os
import re
import sys
import time
import shutil
import getopt
import pdf2image
from PIL import Image


def main(argv):
    dpi = 60
    outfile = ""
    pdffile = ""

    try:
        opts, args = getopt.getopt(argv,"h:p:d:",["pdf=","dpi="])
    except getopt.GetoptError:
        print("pdf2md -p <pdf file> -d <pdf dpi>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("pdf2md -p <pdf file> -d <pdf dpi>")
            sys.exit()
        elif opt in ("-p", "--pdf"):
            pdffile = arg
            outfile = pdffile[:-4]
        elif opt in ("-d", "--dpi"):
            dpi = arg

    if outfile != '' and pdffile != '':
        parentdir = os.path.abspath(os.getcwd())
        outfileformatted = re.sub(r'[^\w]', '', outfile.replace('-', '_'))
        path = os.path.join(parentdir, outfileformatted)
        pdfpath = os.path.join(path, 'pdf')
        if os.path.isdir(path):
            inp = int(input('Folder already exists, would you like to delete it?\n0 = no, 1 = yes: '))
            if inp == 1:
                shutil.rmtree(path)
            else:
                print('Exiting')
                sys.exit()

        os.mkdir(path)
        os.mkdir(pdfpath)

        images = pdftopil(pdffile, dpi)
        image_counter = 0

        for image in images:
            image_counter += 1
            image.save('%s/%s.png' % (pdfpath, image_counter), 'PNG')

            with open('%s/%s.md' % (path, outfileformatted), 'a') as f:
                f.write('### %s\n![%s](%s)\n- %s\n\n--- \n\n' % (image_counter, image_counter, 'pdf/%s.png' % (image_counter), image_counter))

        print('Done!')

    else:
        print("pdf2md -f <file name> -p <pdf file> -d <pdf dpi>")


def pdftopil(PDF_PATH, dpi):
    start_time = time.time()
    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=dpi, output_folder=None, first_page=None, last_page=None, fmt='png', thread_count=100, userpw=None, use_cropbox=False, strict=False)
    print ("Time taken : " + str(time.time() - start_time))
    return pil_images


if __name__ == "__main__":
    main(sys.argv[1:])
