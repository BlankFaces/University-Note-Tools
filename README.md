# University-Note-Tools
Tools which I made to make note taking efficiently and less stressful

## cap
This tool converts a PDF file into separate images stored in memory and added to a cherrytree sqlite file to be able to annotate under each slide during a lecture.


It can also append at the end of adding all the slides, or just on its own, subtitles which are taken from panopto (a service which stores the recording) as json and parses into a readable format.


Requires Poppler, and PIL

## pdf2md
This tool converts a PDF file into separate images and stores it on storage, and generates a formatted markdown file which references the different images, for annotating under each slide.


Also requires Poppler, and PIL

## parse-panopto-captions
Parses panopto captions into a file to make it easy to read