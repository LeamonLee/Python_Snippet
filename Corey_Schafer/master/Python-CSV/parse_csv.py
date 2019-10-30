import csv

with open('names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # If prints out in here, then the writer won't be able to write stuffs out in the new csv file.
    # for row in csv_reader:
    #     print(row)
    # print()
    
    with open('new_names.csv', 'w') as new_file:
        fieldnames = ['first_name', 'last_name']        # returns an interable object

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')

        csv_writer.writeheader()

        for line in csv_reader:
            print("csv_reader: ", csv_reader)
            del line['email']
            csv_writer.writerow(line)

with open('names.csv', 'r') as csv_file:
    # my_csv_reader = csv.reader(csv_file, quotechar='|')
    my_csv_reader = csv.reader(csv_file)                # returns an interable object

    # next(my_csv_reader)                                 # If we want to skip out the header

    # If prints out in here, then the writer won't be able to write stuffs out in the new csv file.
    # for row in my_csv_reader:                         
    #     print(row)
    
    with open('new_names_2.csv', 'w') as new_file:

        csv_writer = csv.writer(new_file, delimiter='\t')

        for line in my_csv_reader:
            # del line[2]
            csv_writer.writerow(line)


with open('names2.csv', 'r') as csv_file:
    
    my_csv_reader = csv.reader(csv_file, quotechar='"')                # returns an interable object

    # next(my_csv_reader)                                               # If we want to skip out the header

    for row in my_csv_reader:                         
        print(row)