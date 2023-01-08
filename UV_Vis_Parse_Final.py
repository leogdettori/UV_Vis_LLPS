#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created by Leo Dettori and Mohamed Mohamed on 2021.07.12.
"""

# ====================================================== #

def Parse_UV_Vis(file_path_UV_Vis):

    #This is important for the program to know when to stop
    c = open(file_path_UV_Vis)
    lines1 = c.readlines()
    total_lines = len(lines1)
    #print("\n"+"UV-Vis Results:"+"\n")
    print("Loading data...")
    c.close()

    # Read the data
    f = open(file_path_UV_Vis)

    #Creates dictionary for this experiment
    experiment = {}

    #creates handy counters
    i = 0
    i2 = 0
    i3 = 0
    counter_1 = 0
    counter_2 = 0
    bypass_line = 0

    #creates handy variables/lists
    wavelength_list = []
    wavelength_list_2 = []
    sample_name_list = []
    sample_name_list_2 = []
    temp_program_list = []
    temp_program_list_2 = []
    temp_abs_list_2 = []
    name = ''
    current_sample_name = ''
    previous_sample_name = ''
    
    #Extracts file name for output purposes within the next functions
    file_name_split = file_path_UV_Vis.split("/")
    file_name = file_name_split[-1].split(".")[0]
    #print(file_name)


    #Starts the loop trhough the file. Line by line.
    while i <= total_lines:
        this_line = f.readline()
        i = i + 1

        #Identifies how many wavelengths were used using the key word wavelength
        if this_line.startswith('Wavelengths'):
            #Splits line
            split_line = this_line.split(",")
            #counts how many wavelengths
            wavelengths_number = len(split_line) - 1

            #saves wavelengths into a list called wavelength and creates dictionary entries for each wavelength
            while i2 < wavelengths_number:
                i2 = i2 + 1

                wavelength_list.append(split_line[i2].strip("\n"))

                #Creates a sub-dictionary for the current wavelength
                this_wavelength = str(wavelength_list[i2-1])
                experiment[str(this_wavelength)] = {}

            #print(wavelength_list)
            #print(experiment)


        #Identifies how many cells and runs (e.g. increase, decresase temperature) were used for each wavelength
        if this_line.startswith('Name'):
            #print(this_line)
            #Splits line
            split_line = this_line.split(",")
            #print(split_line)

            #Starts extracting information from each run
            for i3 in split_line:

                #Extracts Names of each run and temperature program (e.g.: heating or cooling)
                if i3 != 'Name' and i3 !='\n' and i3 != '':
                    #print(i3)
                    #Extracts current name
                    name = i3
                    split_name = name.split("_")

                    #Extract current wavelength
                    current_wavelength = split_name[-2].strip("nm")
                    #Adds into the instruction 'wavelength_list_2' to aid with adding the data to the dictionary later
                    wavelength_list_2.append(current_wavelength)


                    #Extract current temperature program (e.g.: heating or cooling)
                    current_temp_program = split_name[-1].split('-')
                    #print(current_temp_program[0])

                    #checks if heating or cooling:
                    if current_temp_program[0] > current_temp_program[1]:
                        current_program = "Cooling"

                        #Adds into the instruction 'temp_program_list_2' to aid with adding the data to the dictionary later
                        temp_program_list_2.append(current_program)

                    else:
                        current_program = "Heating"

                        #Adds into the instruction 'temp_program_list_2' to aid with adding the data to the dictionary later
                        temp_program_list_2.append(current_program)

                    #Creates a list to neatly organize all temperature program options without repetitions
                    if current_program not in temp_program_list:
                        temp_program_list.append(current_program)    

                    #Extracts Sample Name for comparizon purposes and creation of dictionary for sample
                    current_sample_name = name.split("_")
                    current_sample_name.pop(-1)   # Removes temperature information from name
                    current_sample_name.pop(-1)   # Removes wavelength information from name
                    current_sample_name = "_".join(current_sample_name)  # Puts the name back together again
                    #print("yes")
                    #print(current_sample_name)
                    #Adds into the instruction 'sample_name_list_2' to aid with adding the data to the dictionary later
                    sample_name_list_2.append(current_sample_name)


                    #Creates a sub-dictionary for the current sample inside the current wavelength sub-dictionary
                    #Only creates a sub-dictionary if we're going through this sample for the first time in the current wavelength 
                    #There is a bug in the UV-Vis software where it creates a sample called 'Reference' with blank data that comes out after all the data. This 'Reference' sample does not respect the loop of sampels per wavelength, so we need this 'or' exception to handle it
                    if current_sample_name != previous_sample_name or current_sample_name == 'Reference':  
                        experiment[str(current_wavelength)][current_sample_name] = {}

                    #Creates a list to neatly organize all samples names without repetitions
                    if current_sample_name not in sample_name_list:
                        sample_name_list.append(current_sample_name)


                    #Creates a sub-dictionary for the current temperature program inside the current sample sub-dictionary
                    #and prepares the final subdictionaries where the data will be stored
                    experiment[str(current_wavelength)][current_sample_name][current_program] = {'Temp':[], 'Abs':[], 'run_name':[]}
                    #Stores run name information:
                    experiment[str(current_wavelength)][current_sample_name][current_program]['run_name'].append(name)

                    #Tranfers current sample_name to previous_sample_name, so it can be used for comparizon purposes in the next iterations
                    previous_sample_name = current_sample_name         
                    #print(split_name)
                    #print(current_wavelength)


        #Uses the header line to create the instruction 'temp_abs_list_2' to aid with adding the data to the dictionary later
        if this_line.startswith(',Temperature') and bypass_line == 0:
            bypass_line = 1

            #Splits the line into the individual labels of the header and removes the initial '' element
            split_line = this_line.split(",")
            split_line.pop(0)



            #Goes through each element of the split line toe create the instruction 'temp_abs_list_2'
            for i5 in split_line:
                if ' (Â°C)' in i5:     #Updates temperature label to "Temp"
                    i5 = 'Temp'                
                i5 = i5.strip('\n')     #removes '\n' from the label
                temp_abs_list_2.append(i5)

            #print(split_line)
            #print(temp_abs_list_2)
            continue


        #Starts to read and add into the dictionary temperature and absorbance values
        if this_line.startswith(',') and bypass_line == 1:
            split_line = this_line.split(",")
            split_line.pop(0)     #removes the initial element ''
            #print(len(split_line))
            #print(split_line)

            #Resetting counters for next iteration
            counter_1 = 0
            counter_2 = 0


            #Starts to loop throuhg each data point
            while counter_2 < len(split_line):
                #print(counter_1)
                #print(counter_2)
                current_data_point = split_line[counter_2]
                current_data_point = current_data_point.strip('\n')     #removes '\n' from the data point
                #print(current_data_point)

                #When dealing with temperature, adds the data to the temperature dictionary entry
                if temp_abs_list_2[counter_2] == 'Temp':
                    try:
                        experiment[str(wavelength_list_2[counter_1])][sample_name_list_2[counter_1]][temp_program_list_2[counter_1]][temp_abs_list_2[counter_2]].append(float(current_data_point))
                    except:
                        pass

                #When dealing with absorbance, adds the data to the absorbance dictionary entry
                if temp_abs_list_2[counter_2] == 'Abs':
                    try:
                        experiment[str(wavelength_list_2[counter_1])][sample_name_list_2[counter_1]][temp_program_list_2[counter_1]][temp_abs_list_2[counter_2]].append(float(current_data_point))
                    except:
                        pass
                    
                    counter_1 = counter_1 + 1     #Updates counter for 'wavelength_list_2' 'sample_name_list_2' and 'temp_program_list_2' intruction lists

                #Updates counter for 'temp_abs_list_2' instruction list
                counter_2 = counter_2 + 1   




            #print(this_line)


    #print(temp_program_list_2)
    #print(len(temp_program_list_2))
    #print(len(wavelength_list_2))
    #print(len(sample_name_list_2))
    #print(len(temp_abs_list_2))

    #print(experiment)

    f.close()

    print("\n")
    print("Wavelengths:")
    print(wavelength_list)
    print("\n")
    print("Samples:")
    print(sample_name_list)
    print("\n")
    print("Temeperature Programs:")
    print(temp_program_list)
    print("\n")

    print("Done!")
    print("\n")
    print("# ===================================================== #")
    print("\n")
    
    return experiment, file_name

