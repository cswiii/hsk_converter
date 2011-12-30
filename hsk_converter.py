#!/usr/bin/python

# hsk_convert.py
#
# This script takes a [modified] xls from the Lingomi.com HSK website and
# converts it into a simple, usable semicolon-delimited format suitable
# for use with Anki.
# 
# Source/more info: <http://lingomi.com/blog/hsk-lists-2010/>
#
# It adds a bit of formatting to the characters to easy readability and 
# memorization, with the Chinese character on one side of the 'card' and
# the pinyin/english definition on the other side.
#
# This does not work with the CSVs supplied on the Lingomi website 
# (although that would be about 4-5 lines of code to implement). Rather,
# for this, I saved the XLS files, edited them to remove the first two 
# rows (credits) and the first two columns (difficulty), and /then/ saved 
# my own CSV.
#
# Currently this does not export to the file itself, though that would be
# trivial. I just pipe output to a file manually. Afterwards, it can be
# used to create a new deck in Anki, via the "Import" option.

import sys
import csv
from subprocess import Popen, PIPE, STDOUT

def replace_all(text, dic):
  for i, j in dic.iteritems():
    text = text.replace(i, j)
  return text

if len(sys.argv) == 1:
  print "This program requires a suitable CSV file."
  print "Ex: hsk_converter.py </path/to/vocab_list.csv>"
  sys.exit()

try:
   open(sys.argv[1])
except IOError as e:
   print 'Recipe file "', sys.argv[1], '" not found.  Check the location and try again.'
   sys.exit(1)

# The accent colors here are based on another list I'd been using.
# These are, I suspect, in turn based on the Dummitt color model for associating
# a color with a tone. 
# See <http://blog.ningin.com/2008/10/16/learning-chinese-through-tone-color-and-nathan-dummitt/>
accent_dic = {'1':'<font color="red">1</font>', '2':'<font color="orange">2</font>', '3':'<font color="green">3</font>','4':'<font color="blue">4</font>'}
data_records = []
chinese_character = []
pinyin = []
english_definition = []
merged_pinyin_english = ""
#rejoined_data = []
final_rawtext = ""

''' Read the csv. '''
input_file = open(sys.argv[1])
for line in input_file:
  data_records.append(line)
reader = csv.reader(data_records, delimiter=',', quotechar='"') 
# Is there any way to write/save the following attribution text,
# within the delimited format, as to provide credit where credit
# is due, within the set description? I haven't figured that out.
print "# HSK 2010 Vocabulary list for Anki"
print "# Based on The lists compiled by Lingomi [ref: http://lingomi.com/blog/hsk-lists-2010/]"
print "# Source for this list: " , input_file
print "# Original vocabulary lists licensed CC-BY-SA"

for row in reader:
  chinese_character = row[0]
  pinyin = row[1]
  english_definition = row[2]
  ''' Enlarge Chinese Character '''
  converted_chinese_character = "<p style=\"font-size:150px\">" + chinese_character + "</p>"
  ''' Italicise and colorize pinyin. '''
  converted_pinyin = "<i>" + pinyin + "</i>"
  # This is kind of hacky. It really only colorizes the tone indicator
  # itself.  Later on it would be good to search and replace the entire
  # substring.
  converted_pinyin = replace_all(converted_pinyin, accent_dic)
  ''' Convert semicolons in english to <BR>. '''
  converted_english_definition = english_definition.replace(";","<BR>")
  ''' Merge pinyin and english sections. '''
  merged_pinyin_english = converted_pinyin + "<hr width=\"20%\">" + converted_english_definition
  '''TODO: Output data to a file. '''
  #rejoined_row = []
  #rejoined_row.append(converted_chinese_character)
  #rejoined_row.append(merged_pinyin_english)
  #print rejoined_row 
  final_rawtext = converted_chinese_character + "; " + merged_pinyin_english
  print final_rawtext    
