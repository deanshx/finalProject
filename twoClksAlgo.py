import csv
import re
import matplotlib.pyplot as plt

spc_to_name = 29
spc_to_sent = 17
script_name = "8MM.txt"
subs_name = "subshrek.txt"


# Script clean receives a path to a script.txt file
# The function cleans the script of all words that are not - who spoke them or what they said
# e.g: background sounds or behavioral expressions
def script_clean(path, spc_to_speaker, spc_to_sent):
    clean_txt = open("clean_script.txt", "w")
    with open(path, "r") as txt_file:
        line = txt_file.readline()
        ws_count = 0
        while line:
            # print ("Leading spaces", len(line) - len(line.lstrip(' ')))
            ws_count = len(line) - len(line.lstrip(' '))  # This calculated the number of preceeding whitespaces in each line
            if ws_count == spc_to_sent or ws_count == spc_to_speaker:  # Checking if the number of whitespaces is
                clean_txt.write(line)                                 # either spc_to_speaker or spc_to_sent which represent the name and sentance said
            line = txt_file.readline()

    with open("clean_script.txt", "r") as f:  # Cleaning the script from any instances of parentheses
        input = f.read()                     #  using REGEX that goes through the entire file
        output = re.sub("[\(\[].[\s\S]*?[\)\]]", "", input)
        clean_txt1 = open("clean_script.txt", "w")
        clean_txt1.write(output)


# csv_twoClk receives the clean_script.txt it then creates a new CSV file
# that contains two columns - Name of speaker and how many words they said in a sentence
# i.e: Shrek, 8
def csv_two_clks(path, ws_speaker, ws_sentence):
    csv_file = open('mycsv.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'Num of words'])
    tmp_name = ""

    with open(path, "r") as txt_file:
        line = txt_file.readline()
        ws_count = 0
        num_of_words = 0
        while line:
            if not line.strip():  # Checking if line is not empty
                line = txt_file.readline()
                continue
            ws_count = len(line) - len(line.lstrip(' '))
            if  ws_count == ws_speaker:  # If line has spc_to_speaker spaces then it represents a speaker name
                tmp_name = line.strip()  # saving the last speakers name so that we can insert it to the CSV file
                num_of_words = 0
            if ws_count == ws_sentence:
                num_of_words = len((line.strip()).split()) # If line has spc_to_sent spaces then it represents the sentence said
                csv_writer.writerow([tmp_name, num_of_words])
            line = txt_file.readline()


# extract_clks: receives a regular csv file and creates a new csv file
# which its columns represent our 2 un-normalised clocks = clks.csv
def extract_clks(path):
    clks_csv = open('clks.csv', 'w', newline='')
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(clks_csv)

    csv_writer.writerow(['Clock 1', 'Clock 2'])

    name_tmp = ""
    name_count = -1
    words_count = 0

    next(csv_reader)  # This is used to skip the column titles

    for line in csv_reader:
        if name_count == -1:      # first 2 ifs are used to initialise the counters
            name_tmp = line[0]
            name_count += 1
        if words_count == 0:
            words_count = int(line[1])
            continue
        if line[0] == name_tmp:   # This means the speaker hasn't changed then we continue summing the words said
            words_count += int(line[1])
        else:
            csv_writer.writerow([name_count, words_count])  # Writing the data to the new CSV
            name_tmp = line[0]     # This is the next speakers name
            words_count += int(line[1])
            name_count += 1


# This function receives a path to the CSV file that contains the two clocks C1 & C2
# and creates a new CSV file that contains the normalized clocks: N(C1) & N(C2)
# and their difference in column 3 (Clock1 - Clock2) that will be needed later
def normal_clks(path):
    n_clks_csv = open('n_clks.csv', 'w', newline='' )
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(n_clks_csv)

    csv_writer.writerow(['Normal Clock 1', 'Normal Clock 2', 'Clk_1 - Clk_2'])

    for line in csv_reader:
        pass

    clk_1_size = int(line[0])
    clk_2_size = int(line[1])

    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)

    next(csv_reader)
    flag = 0
    for line in csv_reader:  # In this loop we normalize the clocks using the formula to make sure the clocks are now in
        if flag == 0:          # the interval of [0,1]
            first_clk_2 = int(line[1])
            flag = 1
        csv_writer.writerow([int(line[0])/clk_1_size, (int(line[1]) - first_clk_2)/(clk_2_size - first_clk_2),
                             (int(line[0])/clk_1_size) - ((int(line[1]) - first_clk_2)/(clk_2_size - first_clk_2))])


# Graph plot for N(Clk1) and N(Clk1-Clk2)
def graph_plot (path):
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    x = []
    y = []
    next(csv_reader)

    for line in csv_reader:
        x.append(float(line[0]))
        y.append(float(line[2]))

    y_max = max(y)
    y_min = min(y)

    plt.plot(x, y, color='blue', linestyle='-', linewidth=3,
             markerfacecolor='blue', markersize=12)
    plt.ylim(y_min-0.01, y_max+0.01)
    plt.xlim(0, 1)
    plt.xlabel('Speaker Change')
    plt.ylabel('Difference between Clk1 and Clk2 ')
    plt.title('Graph')
    plt.show()


# Here we clean the subtitles of the movie from all parentheses using a REGEX
def clean_subtitles(path):
    with open(path, "r") as f:  # Cleaning the subtitles from any instances of parentheses
        input = f.read()       # using REGEX that goes through the entire file
        output = re.sub("[\(\[</].[\s\S]*?[\>\)\]]", "", input)
        clean_txt1 = open("clean_subtitles.txt", "w")
        clean_txt1.write(output)


script_clean(script_name, spc_to_name, spc_to_sent)  # We need to automate the process of receiving these
csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)  # We need to automate the process of receiving these
extract_clks("mycsv.csv")
normal_clks("clks.csv")
graph_plot("n_clks.csv")
#clean_subtitles(subs_name)

