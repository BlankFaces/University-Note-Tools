#!/usr/bin/env python3
import sys
import getopt
import sqlite3
import pdf2image
from PIL import Image
import time
from io import BytesIO
import json
from html import escape


def main(argv):
    dpi = 60
    cherryfile = ""
    nodename = ""
    pdffile = ""
    jsonfile = ""

    try:
        opts, args = getopt.getopt(argv,"h:n:c:p:j:d:",["name=", "cherry=","pdf=","json=","dpi="])
    except getopt.GetoptError:
        print("cap -n <name of node> -c <cherrytree file> -p <pdf file> -j <json transcript> -d <pdf dpi>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("cap -n <name of node> -c <cherrytree file> -p <pdf file> -j <json transcript> -d <pdf dpi>")
            sys.exit()
        elif opt in ("-c", "--cherry"):
            cherryfile = arg
        elif opt in ("-n", "--name"):
            nodename = arg
        elif opt in ("-p", "--pdf"):
            pdffile = arg
        elif opt in ("-j", "--json"):
            jsonfile = arg
        elif opt in ("-d", "--dpi"):
            dpi = arg

    if nodename != '' and cherryfile != '':
        conn = sqlite3.connect(cherryfile)
        cursor = conn.cursor()

        cursor.execute('SELECT *, max(node_id) FROM node')
        latest_node = cursor.fetchone()
        
        cursor.execute("""SELECT *, max(sequence) FROM children""")
        sequence_max_id = cursor.fetchone()

        cursor.execute("""INSERT INTO children(node_id, father_id, sequence)
        VALUES (?, 0, ?)""", (latest_node[0] + 1, sequence_max_id[2] + 1))

        if pdffile != '' and jsonfile != '':
            pdf_cherry(conn, cursor, nodename, latest_node, pdffile, dpi, True, jsonfile)
        elif pdffile != '':
            pdf_cherry(conn, cursor, nodename, latest_node, pdffile, dpi, False, jsonfile)
        elif jsonfile != '':
            json_cherry(conn, cursor, nodename, latest_node, jsonfile)
        else:
            print("cap -n <name of node> -c <cherrytree file> -p <pdf file> -j <json transcript> -d <pdf dpi>")
    else:
        print("cap -n <name of node> -c <cherrytree file> -p <pdf file> -j <json transcript> -d <pdf dpi>")


def pdf_cherry(conn, cursor, nodename, latest_node, pdffile, dpi, json_mode, jsonfile):
    images = pdftopil(pdffile, dpi)
    image_counter = 0
    offset = 0

    for image in images:
        stream = BytesIO()
        image.save(stream, 'PNG')
        image_content = stream.getvalue()
        cursor.execute("""INSERT INTO image(node_id ,offset ,justification ,anchor ,png ,filename ,link ,time )
            VALUES (?, ?, 'left', '', ?, '', '', 0)""", (latest_node[0] + 1, offset, image_content))
        offset += 5
        image_counter += 1

    text = '<?xml version="1.0" encoding="UTF-8"?>\n<node><rich_text justification="left">\n'
    for i in range(image_counter):
        text += '-\n\n\n'
    text += '</rich_text>'
    if json_mode:
        text += json_transscript(jsonfile)
    text += '</node>'
    
    cursor.execute("""INSERT INTO node(node_id, name, txt, syntax, tags, is_ro, is_richtxt, has_codebox, has_table, has_image, level, ts_creation, ts_lastsave)   
        VALUES (?, ?, ?, 'custom-colors', '', 0, 1, 0, 0, 1, 0, ?, ?)""", (latest_node[0] + 1, nodename, text, latest_node[12], latest_node[13] + 1))
    conn.commit()

def json_cherry(conn, cursor, nodename, latest_node, jsonfile):
    text = '<?xml version="1.0" encoding="UTF-8"?>\n<node>%s</node>' % json_transscript(jsonfile)
    cursor.execute("""INSERT INTO node(node_id, name, txt, syntax, tags, is_ro, is_richtxt, has_codebox, has_table, has_image, level, ts_creation, ts_lastsave)   
        VALUES (?, ?, ?, 'custom-colors', '', 0, 1, 0, 0, 1, 0, ?, ?)""", (latest_node[0] + 1, nodename, text, latest_node[12], latest_node[13] + 1))
    conn.commit()


def json_transscript(jsonfile):
    with open(jsonfile, 'r') as my_file:
        data=my_file.read()

    obj = json.loads(data)
    captions = [line['Caption'] for line in obj]
    time_stamps = [line['Time'] for line in obj]

    text = '<rich_text>Transcript:\n\n'
    
    for i in range(len(captions)):
        ty_res = time.gmtime(time_stamps[i])
        text += "%s: %s\n" % (time.strftime("%H:%M:%S",ty_res), escape(captions[i]))

    text += '</rich_text>\n'

    return text


def pdftopil(PDF_PATH, dpi):
    start_time = time.time()
    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=dpi, output_folder=None, first_page=None, last_page=None, fmt='png', thread_count=100, userpw=None, use_cropbox=False, strict=False)
    print ("Time taken : " + str(time.time() - start_time))
    return pil_images


if __name__ == "__main__":
    main(sys.argv[1:])
