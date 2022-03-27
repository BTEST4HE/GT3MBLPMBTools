# GT3MBLPMBTools
This script can convert MBL and PMB files used in GT3 for playback in the production version and "Store Demo Vol. 2 (PCPX-96609)", as well as input and output to text format.
Since there are at least four different MBL formats and as many as five different PMB formats, we created this script to be able to play them.
Although some MBLs and PMBs are incomplete, most of them can now be converted, so we are releasing them to the public.

# Downloads
[Latest release](https://github.com/BTEST4HE/GT3MBLPMBTools/releases/latest)

# mbltools
Scripts to convert MBL files for playback in the production version of GT3, export and import in text format, etc.
When converting from MBL to MBL, if the file before conversion and the file after conversion are the same, there is a specification that the converted file is not output.
## Usage
`mbltools [options] input [output_dir]`

### Positional arguments
`input`:input file path or directory  
`output_dir`:output directory(optional)  

### Optional arguments(options)
`-h, --help`:show this help message and exit  
`-s, --storedemo`:output MBL files that can be played back in GT3 Store Demo Vol.2  
`-p, --product`:output MBL files that can be played back in the production version of GT3  
`-r, --recursive`:reads "input" as a directory and recursively retrieves files in the directory  
`-e, --textexport`:export MBL files to text format  
`-i, --textimport`:import from text format MBL to binary format MBL  

# pmbtools
Scripts to convert PMB files for playback in the production version of GT3,
export and import in text and PMB.BIN (image data) formats, etc.
When converting from PMB to PMB, if the file before conversion and the file after conversion are the same, there is a specification that the converted file is not output.
## Usage
`pmbtools [options] input [output_dir]`

### Positional arguments
`input`:input file path or directory  
`output_dir`:output directory(optional)  

### Optional arguments(options)
`-h, --help`:show this help message and exit  
`-s, --storedemo`:output PMB files that can be played back in GT3 Store Demo Vol.2  
`-p, --product`:output PMB files that can be played back in the production version of GT3  
`-r, --recursive`:reads "input" as a directory and recursively retrieves files in the directory  
`-e, --textexport`:export from PMB file to text format and PMBBIN(image data) files  
`-i, --textimport`:import from text format PMB and PMBBIN(image data) files to binary format PNB  (if you do not use the -r option, specify only the text file path in "input")