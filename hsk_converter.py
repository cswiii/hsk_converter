#!/usr/bin/python

# hsk_converter.py
#
# This script takes a CSV from the Lingomi.com HSK website and
# converts it into a friendly, usable semicolon-delimited format suitable
# for use with Anki.
# 
# Source/more info: <http://lingomi.com/blog/hsk-lists-2010/>
#
# It adds a bit of formatting to the characters to easy readability and 
# memorization, with the Chinese character on one side of the 'card' and
# the pinyin/english definition on the other side.
#
# Updates:
# - Now converts native Lingomi CSVs correctly (without having to manually
#   remove rows and columns)
# - Correctly colorizes entire word and part of phrase, rather than just
#   the individual tone marker
# - Cleaned up some crufty logic (there still surely remains some!)
#
# Currently this does not export to the file itself, though that would be
# trivial. I just pipe output to a file manually. Afterwards, it can be
# used to create a new deck in Anki, via the "Import" option.
#
# Note: When importing, you'll need to choose an appropriate deck and/or
# probably not use the 'Default' one.  This seems to throw an error in Anki.

import sys
import re
import csv
from subprocess import Popen, PIPE, STDOUT

reload(sys)
sys.setdefaultencoding('utf-8')

def get_tone(s):
   m = re.search(r'\d+$', s)
   return int(m.group()) if m else "" 

def colorize_phrase(p):
  """ Italicise and colorize pinyin. """

  wordsplit = []
  colored_word= ""
  wordsplit = p.split(' ')
  for word in wordsplit:
    tone = get_tone(word)
    colored_segment="<font color=\"" + accent_dic[tone] + "\">" + word + "</font> "
    colored_word += colored_segment
    converted_pinyin = "<i>" + colored_word + "</i>"
  return converted_pinyin

if len(sys.argv) == 1:
  print "This program requires a suitable CSV file."
  print "Ex: hsk_converter.py </path/to/vocab_list.csv>"
  sys.exit()

try:
   open(sys.argv[1])
except IOError as e:
   print 'Vocabulary file "', sys.argv[1], '" not found.  Check the location and try again.'
   sys.exit(1)

# The accent colors here are based on another list I'd been using.
# These are, I suspect, in turn based on the Dummitt color model for associating
# a color with a tone. 
# See <http://blog.ningin.com/2008/10/16/learning-chinese-through-tone-color-and-nathan-dummitt/>
accent_dic = {1:'red', 2:'orange', 3:'green', 4:'blue', 5:'black', "":'black'}
data_records = []
chinese_character = []
pinyin = []
english_definition = []
merged_pinyin_english = ""
final_rawtext = ""

""" Read the CSV """
input_file = open(sys.argv[1])
for line in input_file:
  data_records.append(line)
""" delete CSV header stuff """
del data_records[0:3]
reader = csv.reader(data_records, delimiter=',', quotechar='"') 
# Is there any way to write/save the following attribution text,
# within the delimited format, as to provide credit where credit
# is due, within the set description? I haven't figured that out.
print "# HSK 2010 Vocabulary list for Anki"
print "# Based on The lists compiled by Lingomi [ref: http://lingomi.com/blog/hsk-lists-2010/]"
print "# Source for this list: " ,sys.argv[1] , ""
print "# Original vocabulary lists licensed CC-BY-SA"
for row in reader:
  difficulty_unused = row[0]
  chinese_character = row[1].decode('utf8')
  pinyin = row[2].decode('utf8')
  english_definition = row[3].decode('utf8')
  """ Enlarge Chinese Character """
  converted_chinese_character = "<p style=\"font-size:100px\">" + chinese_character + "</p>"
  converted_chinese_character.encode('utf8')
  """ Italicise and colorize pinyin. """
  converted_pinyin =  colorize_phrase(pinyin)
  """ As to not confuse the parser, we will convert semicolons that
  separate english definitions to newlines>.
  """
  converted_english_definition = english_definition.replace(";","<BR> ")
  """ Merge pinyin and english sections. """
  merged_pinyin_english = converted_pinyin + "<br>" + converted_english_definition

  """ TODO: Output data to a file. """
  final_rawtext = converted_chinese_character + "; " + merged_pinyin_english
  final_rawtext.encode('utf8')
  print final_rawtext
