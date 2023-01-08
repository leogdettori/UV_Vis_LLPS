#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created by Leo Dettori and Mohamed Mohamed on 2021.07.14.
"""

def plot_temp_program(experiment, file_name, output, temperature_program = "Both", samples = "All"):

    import matplotlib.pyplot as plt
    import os

    #If plotting all samples:
    if samples == "All":
        #Prints initial message
        print("Plotting "+str(temperature_program)+" plots for All samples...")
        
    #If plotting select samples:
    if samples != "All":
        #Prints initila message
        print("Plotting "+str(temperature_program)+" plots for " + str(len(samples))+ " samples...")
        
    
    #Creates a master folder to store the results in an orderly fashion
    #Checks all folders in the slected ouput directory
    folders = next(os.walk(output))[1]   #Compiles a list of all folder within this folder
    #print(folders)
    #Updates output destination with the name of the mother file
    output = output + "/" + str(file_name)
    #Checks if master folder was already created, if not it will be created now
    if file_name not in folders:
        os.mkdir(output)
        print("\n"+"Master folder to store results was successfully created in the output location!")
    
    
    #Begins steps to create a folder to store plots
    #Updates output directory
    #If plotting all samples:
    if samples == "All":
        output = output +"/"+ str(temperature_program)+"_All_Samples"
    #If plotting select samples:
    if samples != "All":
        #Prepares the name of the folder to be created
        folder_name = str(temperature_program)+"_" + str(len(samples)) +"_Samples"
        #Checks if that folder was created before
        folders_2 = next(os.walk(output))[1]   #Compiles a list of all folder within this folder
        if folder_name not in folders_2:  #if the folder was not created yet
            output = output +"/"+ folder_name
        else: #if this folder was already created
            ind = 1  #creates a useful counter for the folder name index 
            
            #Starts a loop to find an index that was not used yet 
            while folder_name + '_' + str(ind) in folders_2:        
                #folder_name = folder_name + '_' + str(ind)  #updates folder name with the current index
                ind = ind + 1  #updates folder name index to next index number
            
            #When an index that was not used yet is found, the output path gets updated with the new folder name
            output = output +"/"+ folder_name + '_' + str(ind)                
    
    #Creates the folder to store plots
    os.mkdir(output)
    #Updates output
    output = output +"/"
    
    
    #Starts to loop trhough the wavelengths
    for i1 in experiment:
        
        #Creates the text file to export the data for the current wavelength
        f1 = open(str(output) + str(i1).strip('"[]"') + "nm.txt", "a")
        f1.write(str(i1).strip('"[]"')+ "nm" +"\n"+"\n")
        f1.close()

        #creates figure that will be used to store the plot and legend
        plt.gcf().clear()
        fig = plt.figure(figsize =(15, 10))
        ax = fig.add_subplot(111)

        #starts to loop through the samples for each wavelength
        for i2 in experiment[str(i1)]:  

            #When plotting all samples (all samples are toggled on:
            if samples == "All":
            
            
                #starts to loop through the temeperature programs for each sample for each wavelength
                for i3 in experiment[str(i1)][str(i2)]:
                    #print(i3)

                    #Selects the desired temperature program (e.g.: heating or cooling)
                    if i3 == temperature_program:
                        #Defines the axis from the data
                        x_axis = experiment[str(i1)][str(i2)][str(i3)]["Temp"]
                        y_axis = experiment[str(i1)][str(i2)][str(i3)]["Abs"]
                        #Defines label from the data
                        run_label = str(i2)
                        run_label = run_label.strip("[]''")

                        #Plotting the data of current run
                        ax.plot(x_axis, y_axis, label=run_label)
                        
                        #Updating the text file to export the data with information from the current run
                        f1 = open(str(output) + str(i1).strip('"[]"') + "nm.txt", "a")
                        f1.write(str(run_label).strip('"[]"') +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+"\n")
                        f1.close()

                    elif temperature_program == "Both" or temperature_program == "Heating_and_Cooling":
                        #Updates temperature_program for the labels and title
                        temperature_program = "Heating_and_Cooling"
                        #Defines the axis from the data
                        x_axis = experiment[str(i1)][str(i2)][str(i3)]["Temp"]
                        y_axis = experiment[str(i1)][str(i2)][str(i3)]["Abs"]
                        #Defines label from the data
                        run_label = str(i2).strip("[]''") +"_"+ str(i3).strip("[]''")

                        #Plotting the data of current run
                        ax.plot(x_axis, y_axis, label=run_label)
                        
                        #Updating the text file to export the data with information from the current run
                        f1 = open(str(output) + str(i1).strip('"[]"') + "nm.txt", "a")
                        f1.write(str(run_label).strip('"[]"') +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+"\n")
                        f1.close()
                        
                        
            #When plotting a select set of samples (not all samples are toggled on):
            if samples != "All":
                
                #Only goes ahead for the samples that are toggled on
                if i2 in samples:                

                    #starts to loop through the temeperature programs for each sample for each wavelength
                    for i3 in experiment[str(i1)][str(i2)]:

                        #Selects the desired temperature program (e.g.: heating or cooling)
                        if i3 == temperature_program:
                            #Defines the axis from the data
                            x_axis = experiment[str(i1)][str(i2)][str(i3)]["Temp"]
                            y_axis = experiment[str(i1)][str(i2)][str(i3)]["Abs"]
                            #Defines label from the data
                            run_label = str(i2)
                            run_label = run_label.strip("[]''")

                            #Plotting the data of current run
                            ax.plot(x_axis, y_axis, label=run_label)
                            
                            #Updating the text file to export the data with information from the current run
                            f1 = open(str(output) + str(i1).strip('"[]"') + "nm.txt", "a")
                            f1.write(str(run_label).strip('"[]"') +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+"\n")
                            f1.close()
                            
                            

                        elif temperature_program == "Both" or temperature_program == "Heating_and_Cooling":
                            #Updates temperature_program for the labels and title
                            temperature_program = "Heating_and_Cooling"
                            #Defines the axis from the data
                            x_axis = experiment[str(i1)][str(i2)][str(i3)]["Temp"]
                            y_axis = experiment[str(i1)][str(i2)][str(i3)]["Abs"]
                            #Defines label from the data
                            run_label = str(i2).strip("[]''") +"_"+ str(i3).strip("[]''")

                            #Plotting the data of current run
                            ax.plot(x_axis, y_axis, label=run_label)
                            
                            
                            #Updating the text file to export the data with information from the current run
                            f1 = open(str(output) + str(i1).strip('"[]"') + "nm.txt", "a")
                            f1.write(str(run_label).strip('"[]"') +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+"\n")
                            f1.close()



        #Adjusts the "looks" of the plot
        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), fontsize=15)
        text = ax.text(-0.2,1.05, '', transform=ax.transAxes)
        ax.set_xlabel('Temperature', fontsize=15)
        ax.set_ylabel('Scattering', fontsize=15)
        ax.grid('on')
        
        #Sets the title of the plot and subseqeuntly saves figure into a png file
        #If plotting all samples
        if samples == "All":
            #sets title of the plot
            ax.set_title(str(i1).strip("[]''") + str(' nm - ') +str(temperature_program) + " - " +str(samples)+ " Samples", fontsize=20) 
            #Saves figure into a png file
            fig.savefig((output+"/"+str(temperature_program)+"_"+str(i1)).strip("[]''")+"nm"+"_All_Samples"+".png", bbox_extra_artists=(lgd,text), bbox_inches='tight')
            
        #If plotting select samples
        if samples != "All":
            #sets title of the plot
            ax.set_title(str(i1).strip("[]''") + str(' nm - ') +str(temperature_program) + " - "  +str(len(samples))+" Samples", fontsize=20) 
            #Saves figure into a png file
            fig.savefig((output+"/"+str(temperature_program)+"_"+str(i1)).strip("[]''")+"nm_"+ str(len(samples))+"_Samples"+".png", bbox_extra_artists=(lgd,text), bbox_inches='tight')
        
        
        plt.close('all')
        #plt.gcf().clear()
    print("\n")
    print("Done!")
    print("\n")
    print("# ===================================================== #")
    print("\n")

