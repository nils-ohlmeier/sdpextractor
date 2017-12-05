#!/usr/bin/env python

import re

combined_line = ""
draft_section = None
sdp_type = None
sdp_text = ''

def write_sdp(draft_section, sdp_type, sdp_content):
    file_name = "sdp-%s-%s.txt" % (draft_section, sdp_type)
    output_file = open(file_name, 'w')
    output_file.write(sdp_content)
    output_file.close()
    print 'Wrote SDP file', file_name

file_o = open('draft-ietf-rtcweb-sdp-08.txt', 'r')

for line in file_o:
    if line.startswith('5.'):
        # Flush accumulated SDP at section boundaries
        if sdp_text:
            write_sdp(draft_section, sdp_type, sdp_text)
        sdp_text = ''
        draft_section = line.split()[0].rstrip('.')
        print 'Found section', draft_section
    line = line.lstrip()
    if line.startswith('|') and line.endswith('|\n') and line.count('|') == 3:
        words = line.split('|')
        first_word = words[1].strip()
        headline_match = re.match('(.*) SDP Contents', first_word)
        if headline_match:
            # Flush accumulated SDP at new SDP heading
            if sdp_text:
                write_sdp(draft_section, sdp_type, sdp_text)
            sdp_text = ''

            if headline_match.group(1) == 'Offer':
                sdp_type = 'offer'
            elif headline_match.group(1) == 'Answer':
                sdp_type = 'answer'
            elif headline_match.group(1) == 'Updated Offer':
                sdp_type = 'updated_offer'
            elif headline_match.group(1) == 'Updated Answer':
                sdp_type = 'updated_answer'
            else:
                print 'New headline found:', headline_match.group(1)
        if not first_word or first_word.startswith('***') or "SDP Contents" in first_word:
            continue
        if first_word[1] == '=':
            if combined_line:
                sdp_text += (combined_line + "\n")
            if combined_line and first_word == "v=0":
                combined_line = first_word
        else:
            combined_line += first_word
