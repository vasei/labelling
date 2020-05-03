def read_label_file(label_file_address):
    data = {}
    with open(label_file_address) as f:
        for line in f:  # print the list items
            line_contents = line.split(",")
            try:
                data_index = line_contents[0]
                data_type = line_contents[1]
                if data_index not in data:
                    data[data_index] = {}

                try:
                    temp = [int(x) for x in line_contents[2:]]
                except:
                    temp = []

                data[data_index][data_type] = temp

            except:
                print("bad file")
    return data


def write_label_file(label_file_address, data):
    with open(label_file_address, 'w') as file:
        for image_name in data:
            image_data = data[image_name]
            for data_type in image_data:
                line_string = image_name + "," + data_type + "," + ",".join(
                    str(elem) for elem in image_data[data_type]) + "\n"
                file.write(line_string)
