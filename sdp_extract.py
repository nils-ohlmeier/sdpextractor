#!/usr/bin/env python

combined_line = ""
sdp_counter = 0
output_file = None

def create_new_file():
    global sdp_counter, output_file
    if output_file:
        output_file.close()
        sdp_counter += 1
    file_name = "sdp%02d.txt" % (sdp_counter)
    output_file = open(file_name, 'w')

file_o = open('draft-ietf-rtcweb-sdp-08.txt', 'r')

create_new_file()

for line in file_o:
    line = line.lstrip()
    if line.startswith('|') and line.endswith('|\n') and line.count('|') == 3:
        words = line.split('|')
        first_word = words[1].strip()
        if not first_word or first_word.startswith('***') or "SDP Contents" in first_word:
            continue
        if first_word[1] == '=':
            if combined_line:
                output_file.write(combined_line + "\n")
            if combined_line and first_word == "v=0":
                print "wrote sdp file %d" % (sdp_counter)
                create_new_file()
            combined_line = first_word
        else:
            combined_line += first_word
