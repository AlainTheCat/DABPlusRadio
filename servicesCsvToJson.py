import csv
import json

"""
Converts the services file in CSV format:

1 RADIO ONE 1   ,00  00  F3  6A ,01  FE  00  0B ,18,206352,73 F0 ,MONTPELLIER 9C  ,
100/100         ,00  00  F6  92 ,01  FE  00  03 ,28,220352,72 F0 ,MONTPELLIER 11C ,
ADO dab+        ,00  00  F2  1B ,01  FE  00  02 ,28,220352,72 F0 ,MONTPELLIER 11C ,
...
to a JSON format file with the various keys and data in the correct format:

{
    "service1": {
        "serviceName": "1 RADIO ONE 1   ",
        "serviceID": "0x0000F36A",
        "componentID": "0x01FE000B",
        "tuneIndex": "18",
        "tuneFrequency": "220352",
        "EID": "0x73F0",
        "componentLabel": "MONTPELLIER 9C "
    },
    "service2": {
        "serviceName": "100/100         ",
        "serviceID": "0x0000F692",
        "componentID": "0x01FE0003",
        "tuneIndex": "28",
        "tuneFrequency": "220352",
        "EID": "0x72F0",
        "componentLabel": "MONTPELLIER 11C "
    },
    "service3": {
        "serviceName": "ADO dab        ",
        "serviceID": "0x0000F21B",
        "componentID": "0x01FE0002",
        "tuneIndex": "28",
        "tuneFrequency": "220352",
        "EID": "0x72F0",
        "componentLabel": "MONTPELLIER 11C "
    },
    ...
}
"""

def modifyTxtFile(txt_file_Path):

    with (open("services.csv", "w", encoding='utf-8') as csv_file):
        # step1
        # Add header: serviceName, serviceID, componentID, tuneIndex, tuneFrequency, EID and componentLabel
        csv_file.write("serviceName,serviceID,componentID,tuneIndex,tuneFrequency,EID,componentLabel\n")
        # step2
        # Read the text file row by row and add to the new csv file
        file = open(txt_file_Path, "r", encoding="utf-8")
        for line in file:
            print(line)
            # step 4
            # modify this line
            # find the seven data
            positions = [i for i, c in enumerate(line) if c == ',']
            print(positions)  # Affiche [1, 9, 20]
            serviceName = line[0: positions[0]]
            serviceID = "0x" + line[positions[0] + 1: positions[1]].replace(" ", "")
            componentID = "0x" + line[positions[1] + 1: positions[2]].replace(" ", "")
            tuneIndex = line[positions[2] + 1: positions[3]]
            tuneFrequency = line[positions[3] + 1: positions[4]]
            EID = "0x" + line[positions[4] + 1: positions[5]].replace(" ", "")
            componentLabel = line[positions[5] + 1: positions[6]]
            new_line = serviceName + "," + serviceID + "," + componentID + "," + tuneIndex + "," + tuneFrequency + "," + EID + "," + componentLabel + "\n"
            csv_file.write(new_line)
        file.close()



def csv_to_json(csv_file_Path, json_file_Path):

    data_dict = {}

    # Step 2
    # open a csv file handler
    with open(csv_file_path, encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler, delimiter=',')

        # convert each row into a dictionary
        # and add the converted data to the data_variable
        it = 0
        for rows in csv_reader:
            # assuming a column named 'No'
            # to be the primary key
            print(rows)
            it = it + 1
            key = "service" + str(it)
            data_dict[key] = rows
        # print(data_dict)

    # Change the primary key
    nb_data = len(data_dict)
    print(nb_data)
    # for it in range(nb_data):
        # new_key = "service" + str(it + 1)
        # print(new_key)
        # data_dict[it + 1] = {new_key: data_dict[it + 1]}

    # open a json file handler and use json.dumps
    # method to dump the data
    # Step 3
    with open(json_file_path, 'w', encoding='utf-8') as json_file_handler:
        # Step 4
        json_file_handler.write(json.dumps(data_dict, indent=4))


# driver code
# be careful while providing the path of the csv file
# provide the file path relative to your machine

# Step 1
# txt_file_path = input('Enter the absolute path of the TXT file: ')
# json_file_path = input('Enter the absolute path of the JSON file: ')
# csv_file_path = input('Enter the absolute path of the CSV file: ')

txt_file_path = "services.txt"
csv_file_path = "services.csv"
json_file_path = "services.json"

modifyTxtFile(txt_file_path)

csv_to_json(csv_file_path, json_file_path)
