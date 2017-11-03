# -*- coding:utf-8 -*-
import string

# character we want to count
letters = string.ascii_letters
# init variable
letter_percentage = {}
letter_count = {}
total_count = 0.0
#  open the file
input_file = open('./PlainTextMessage.txt')
# read line by line
for line in input_file.readlines():
    # read char by char
    for char in line:
        # just care a..zA..Z
        if char in letters:
            # total number add one
            total_count += 1.0
            # if already set in dict, just add one, if not, init
            char = char.lower()
            if char in letter_count:
                letter_count[char] += 1.0
            else:
                letter_count[char] = 1.0

input_file.close()

# calc percentage
for char in letter_count.keys():
    letter_percentage[char] = float(letter_count[char] / total_count) * 100

# print and write to Report.txt
report_fd = open('./Report.txt', mode='w+')
print 'total count:', total_count
report_fd.write('total count: %d\n' % total_count)
report_fd.write('\n')

for k, v in letter_count.items():
    print k, ": ", v
    report_fd.write("%s: %d\n" % (k, v))

report_fd.write('\n')

for k, v in letter_percentage.items():
    print k, ": ", v
    report_fd.write("%s: %f\n" % (k, v))

report_fd.close()
