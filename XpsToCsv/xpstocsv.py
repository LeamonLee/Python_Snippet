import re

#Reading Files:
with open("ex7_DBFormat.csv", "r", encoding='utf-8') as read_f:
    with open('newFile.csv', 'a', encoding='utf-8') as write_f:
        ##Iterating through the file:
        for line in read_f:

            # Method 1
            new_line = re.sub(r"\s+", ",", line.strip())
            # Method 2
            # line.strip()
            # line = " ".join(line.split())
            # Doesn't work
            # line.replace(" ", ",")

            print(new_line)
            # print(line, end = '')

            write_f.write(new_line + '\n')
        
    