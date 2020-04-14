import csv 
import sys 
import itertools

def getKeyPosition(header_row, key_value):
    counter = 0
    for header in header_row:
        if (header == key_value):
            return counter
        counter += 1 

# This will create a dictonary of your rows by their key. (key is the column location)
def getKeyDict(csv_reader, key_position):
    key_dict = {}

    row_counter = 0
    unique_records = 0
    for row in csv_reader:
        row_counter += 1
        if row[key_position] not in key_dict:
            key_dict.update({row[key_position]: row})
        unique_records += 1

    # My use case requires a lot of checking for duplicates 
    if unique_records != row_counter:
        print ("Duplicate Keys in File")

    return key_dict

def main():
    f1 = open(sys.argv[1]) 
    f2 = open(sys.argv[2])
    f1_csv = csv.reader(f1)
    f2_csv = csv.reader(f2)

    f1_header = next(f1_csv)
    f2_header = next(f2_csv)
    f1_header_key_position = getKeyPosition(f1_header, "Alert ID")
    f2_header_key_position = getKeyPosition(f2_header, "Alert ID")

    f1_row_dict = getKeyDict(f1_csv, f1_header_key_position)
    f2_row_dict = getKeyDict(f2_csv, f2_header_key_position)

    outputFile = open("KeyDifferenceFile.csv" , 'w')
    writer = csv.writer(outputFile)
    writer.writerow(f1_header)


    #Heres the logic for comparing rows
    for key, row_1 in f1_row_dict.items():
        #Do whatever comparisions you need here. 
        if key not in f2_row_dict:
            print ("Oh no, this key doesn't exist in the file 2")

        if key in f2_row_dict:
            row_2 = f2_row_dict.get(key)

            if row_1 != row_2:
                print ("oh no, the two rows don't match!")

            # You can get more header keys to compare by if you want.
            data_position = getKeyPosition(f2_header, "DATA")
            row_1_data = row_1[data_position]
            row_2_data = row_2[data_position]
            if row_1_data != row_2_data:
                print ("oh no, the data doesn't match!")

            # Heres how you'd right the rows 
                row_to_write = []

                #Differences between
                for row_1_column, row_2_column in zip(row_1_data, row_2_data):
                    row_to_write.append(row_1_column - row_2_column)

                writer.writerow(row_to_write)


    # Make sure to close those files! 
    f1.close()
    f2.close()
    outputFile.close()
    
main()
