#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created by Leo Dettori on 2021.07.22.
"""

def find_parameters_cubic_spline(experiment, file_name, output):
    #Fits data to a cubic spline model
    
    #Initial message
    print("Calculating parameters...")
    print("\n")
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import interpolate
    import math
    import os
    
    
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
        
    
    #Creates a Parameters folder to store the results in an orderly fashion
    #Checks all folders in the slected ouput directory
    folders_2 = next(os.walk(output))[1]   #Compiles a list of all folder within this folder
    #print(folders_2)
    #Updates output destination with the name of the mother file
    output = output + "/" + "Parameters_Cubic_Spline"
        
    #Checks if Parameters folder was already created, if yes, the program already ran once and it will end
    if "Parameters_Cubic_Spline" in folders_2:
        print("\n" + "Parameters_Cubic_Spline folder was already created! ")
        print("\n" + "Finding_Parameters program will not recalculate the parameters.")  
                
    #If Parameters folder was not created yet, it will be created now and the program will proceed    
    else:
        os.mkdir(output)
        print("\n"+"Parameters_Cubic_Spline folder to store results was successfully created in the output location!")


        #Starts to loop through the wavelengths
        for i1 in experiment:
            
            #Creates the text file to export the data for the current wavelength
            f1 = open(str(output) + "/" + "Parameters_Cubic_Spline_" + str(i1).strip('"[]"') + "nm.txt", "a")
            f1.write(str(i1).strip('"[]"')+ "nm" +"\n"+"\n")
            f1.close()

            #Creates a folder to store results of current wavelength
            os.mkdir(output + "/" + str(i1) + "nm")

            #starts to loop through the samples in each wavelength
            for i2 in experiment[str(i1)]:

                    #starts to loop through the temeperature programs for each sample for each wavelength
                    for i3 in experiment[str(i1)][str(i2)]:


                        #Interpolating with cubic spline and find derivatives

                        #Prepares/resets the variables for this run:
                        cloud_point_x = ''
                        cloud_point_y = []
                        counter_y = 0   #helps when plotting cloud points
                        critical_points = ''
                        delta_T = ''
                        delta_Abs = ''


                        #Defining x and y   #if we're doing cooling, we need to re-arrange data from lowest to highest temp
                        if i3 == 'Cooling':
                            x = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Temp"]))
                            y = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Abs"]))

                        #Defining x and y when heating
                        if i3 == 'Heating':
                            x = experiment[str(i1)][str(i2)]['Heating']["Temp"]
                            y = experiment[str(i1)][str(i2)]['Heating']["Abs"]

                        #print("x = " + str(x))
                        #print("y = " + str(y))

                        #Finding recommend smoothness for the cubic spline interpolation
                        m = len(y)
                        rec_s=m-math.sqrt(2*m)
                        
                        try:


                            #Interpolating with the cubic spline
                            tck = interpolate.splrep(x, y, s= rec_s)  #Initially it was s = 0
                            #Updates x and y with the interpolation results
                            xnew = np.arange(x[0], x[-1], abs(x[0]-x[1])/100)   #np.arrange creates an array eg.: np.arange([start, ]stop, [step, ], dtype=None)
                            ynew = interpolate.splev(xnew, tck, der=0)


                            #print("\n")


                            #Plotting results
                            fig, axs = plt.subplots(2, 2, figsize =(30, 23));
                            axs[0, 0].plot(x, y, 'o' , markersize=10);
                            axs[0, 0].plot(xnew, ynew, 'b', linewidth=3);
                            axs[0, 0].grid('on');
                            axs[0, 0].legend(['Data', 'Cubic Spline'], fontsize=22);
                            axs[0, 0].set_xlabel('Temperature', fontsize=24);
                            axs[0, 0].set_ylabel('Scattering', fontsize=24);
                            axs[0, 0].set_title('Cubic Spline Interpolation', fontsize=35);


                            #print("\n")


                            #First Derivative of Interpoalted (Spline) data
                            yder = interpolate.splev(xnew, tck, der=1)

                            axs[1, 0].plot(xnew, yder, color='orange', linewidth=3);
                            axs[1, 0].grid('on');
                            axs[1, 0].legend(['1st Derivative'], fontsize=22);
                            axs[1, 0].set_xlabel('Temperature', fontsize=24);
                            axs[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 0].set_title('1st Derivative Estimation', fontsize=35);



                            #Reporting the Critical points:
                            #For this, we interpolate the first derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            m_1 = len(yder)
                            rec_s_1 = m_1-math.sqrt(2*m_1)
                            #Finds the Critical points
                            critical_points = interpolate.sproot(interpolate.splrep(xnew, yder, s= rec_s_1))
                            #Reports the Critical Point(s)
                            #print("The " + str(len(critical_points)) +" Critical points are: " + str(critical_points).strip('[]'))
                            #print(yder)



                            #print("\n")

                            #Second Derivative of Interpolated (Spline) data
                            yder_2 = interpolate.splev(xnew, tck, der=2)
                            axs[1, 1].plot(xnew, yder_2, color='green', linewidth=3);
                            axs[1, 1].grid('on');
                            axs[1, 1].legend(['2nd Derivative'], fontsize=22);
                            axs[1, 1].set_xlabel('Temperature', fontsize=24);
                            axs[1, 1].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 1].set_title('2nd Derivative Estimation', fontsize=35);


                            #Calculating the Inflection/Cloud point:
                            #For this, we interpolate the second derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            m_2 = len(yder_2)
                            rec_s_2 = m_2-math.sqrt(2*m_2)
                            #Finds the Cloud Point
                            cloud_point_x = interpolate.sproot(interpolate.splrep(xnew, yder_2, s= rec_s_2))
                            #Reports the Cloud Point(s)
                            #print("Temperature at the Inflection/Cloud point is: " + str(cloud_point_x).strip('[]'))


                            #print("\n")


                            #Give temperature and get absorbance (Finding absorbance for each cloud_point)
                            #Choose your x:
                            for j in cloud_point_x:
                                x_give = j
                                y_given = interpolate.splev(x_give, tck, der=0, ext=0)   # if ext=0, return the extrapolated value.

                                #print("For the Cloud Point Temperature (" + str(x_give).strip('[]') + "), the Scattering is " + str(y_given).strip('[]'))

                                #print("\n")

                                #Updates cloud_point_y with cloud_point_x's absrobance
                                cloud_point_y.append(y_given)


                            #Calculating delta Temperature (Tfinal - Tinitial) and delta Scattering (Absfinal - Absinitial)
                            if len(critical_points) > 1:                         
                                delta_T = critical_points[-1] - critical_points[0]
                                delta_Abs = interpolate.splev(critical_points[-1], tck, der=0, ext=0) - interpolate.splev(critical_points[0], tck, der=0, ext=0)

                                #print("Delta Temperature is "+str(delta_T))
                                #print("Delta Scattering is "+str(delta_Abs))
                                #print("\n")


                            #Calculating LLPS_Capacity
                            if len(critical_points) > 1: 
                                LLPS_Cap = interpolate.splint(critical_points[0], critical_points[-1], tck)

                                #print("LLPS Capacity is: " +str(LLPS_Cap))
                                #print("\n")


                            #Plotting Summary Plot
                            axs[0, 1].plot(xnew, ynew, 'b', linewidth=3);
                            axs[0, 1].grid('on');


                            #if cloud_point_x != '':
                            if len(cloud_point_x) > 0:
                                for j1 in cloud_point_x:                        
                                    axs[0, 1].plot(j1, cloud_point_y[counter_y] , '.', color='green', markersize=35);

                                    counter_y = counter_y + 1   #Updates handy counter to help plot cloud point


                            #Plotting lines on initial and final temperatures
                            if len(critical_points) > 0:
                                for j2 in critical_points:
                                    axs[0, 1].axvline(x=j2, color='orange', linestyle='--', linewidth=4);



                            axs[0, 1].set_xlabel('Temperature', fontsize=24);
                            axs[0, 1].set_ylabel('Scattering', fontsize=24);
                            axs[0, 1].set_title('Summary ', fontsize=38);


                            axs[0, 1].legend(['Cubic Spline','Cloud Point', 'Transtion Temperatures'], fontsize=22);
                            plt.rc('xtick', labelsize=18) ;
                            plt.rc('ytick', labelsize=18) ;

                            #Adding title and saving plot
                            fig.suptitle(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']"), fontsize=40)
                            fig.savefig(output + "/" + str(i1) + "nm" + "/" + str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']") +".png")
                            plt.close('all')

                            #Updating the text file to export the data with information from the current run
                            f1 = open(str(output) + "/" + "Parameters_Cubic_Spline_" + str(i1).strip('"[]"') + "nm.txt", "a")
                            f1.write(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip(''"[]") + ", " + str(i3).strip(''"[]") +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+ "Critical_Points/Transition_Temperatures" +", "+ str(critical_points).strip('"[]"') +"\n"+ "Inflection_Points/Cloud_Points" +", "+ str(cloud_point_x).strip('"[]"') +"\n"+ "Delta_Temperature" +", "+ str(delta_T).strip('"[]"') +"\n"+ "Delta_Scattering" +", "+ str(delta_Abs).strip('"[]"') +"\n"+"\n")
                            f1.close()
                            
                        except:
                            pass
        
        #When calculating the parameters
        print("\n" + "Parameters were successfully calculated! ")
              
    print("\n")
    print("Done!")
    print("\n")
    print("# ===================================================== #")
    print("\n")
    
    
### =========================================================================================================================== ###


"""
Created by Leo Dettori on 2021.07.22.
"""

#Defines the function of the 4PL_regression model
def func(x, a, b, c, d):
    return d + ((a-d)/(1+(x/c)**b))


#Applies the model
def find_parameters_4PL_regression(experiment, file_name, output):
    #Fits data to a Four Parameter Logistic Regression model
    
    #Initial message
    print("Calculating parameters...")
    print("\n")
    
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.optimize as opt
    import math
    import os
    from sympy import diff, solveset, lambdify, symbols, Eq, Reals, evalf
    
    
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
        
    
    #Creates a Parameters folder to store the results in an orderly fashion
    #Checks all folders in the slected ouput directory
    folders_2 = next(os.walk(output))[1]   #Compiles a list of all folder within this folder
    #print(folders_2)
    #Updates output destination with the name of the mother file
    output = output + "/" + "Parameters_4PL"
        
    #Checks if Parameters folder was already created, if yes, the program already ran once and it will end
    if "Parameters_4PL" in folders_2:
        print("\n" + "Parameters_4PL folder was already created! ")
        print("\n" + "Finding_Parameters program will not recalculate the parameters.")  
                
    #If Parameters folder was not created yet, it will be created now and the program will proceed    
    else:
        os.mkdir(output)
        print("\n"+"Parameters_4PL folder to store results was successfully created in the output location!")


        #Starts to loop through the wavelengths
        for i1 in experiment:
            
            #Creates the text file to export the data for the current wavelength
            f1 = open(str(output) + "/" + "Parameters_4PL_" + str(i1).strip('"[]"') + "nm.txt", "a")
            f1.write(str(i1).strip('"[]"')+ "nm" +"\n"+"\n")
            f1.close()

            #Creates a folder to store results of current wavelength
            os.mkdir(output + "/" + str(i1) + "nm")

            #starts to loop through the samples in each wavelength
            for i2 in experiment[str(i1)]:

                    #starts to loop through the temeperature programs for each sample for each wavelength
                    for i3 in experiment[str(i1)][str(i2)]:


                        #Performing Four Parameter Logistic Regression model

                        #Prepares/resets the variables for this run:
                        cloud_point_x = ''
                        cloud_point_y = []
                        counter_y = 0   #helps when plotting cloud points
                        critical_points = ''
                        delta_T = ''
                        delta_Abs = ''
                        
                        a_ = ''
                        b_ = ''
                        c_ = ''
                        d_ = ''
                        y_fit = []
                        c_y = ''
                        xx = []
                        y1 = []
                        y2 = []
                        



                        #Defining x and y   #if we're doing cooling, we need to re-arrange data from lowest to highest temp
                        if i3 == 'Cooling':
                            x = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Temp"]))
                            y = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Abs"]))

                        #Defining x and y when heating
                        if i3 == 'Heating':
                            x = experiment[str(i1)][str(i2)]['Heating']["Temp"]
                            y = experiment[str(i1)][str(i2)]['Heating']["Abs"]

                        #print("x = " + str(x))
                        #print("y = " + str(y))
                        
                        print(str(i1)+"_"+str(i2)+"_"+str(i3))
                        
                        try:


                            #Finding parameters using regression model
                            (a_, b_, c_, d_), _ = opt.curve_fit(func, x, y);

                            #Applying parameters to fit the data
                            y_fit = func(x, a_, b_, c_, d_)  #c_ is the cloudpoint in a 4PL regression model

                            print(c_)


                            #Plotting results
                            fig, axs = plt.subplots(2, 2, figsize =(30, 23));
                            axs[0, 0].plot(x, y, 'o' , markersize=10);
                            axs[0, 0].plot(x, y_fit, 'b', linewidth=3);
                            axs[0, 0].grid('on');
                            axs[0, 0].legend(['Data', '4PL Regression'], fontsize=22);
                            axs[0, 0].set_xlabel('Temperature', fontsize=24);
                            axs[0, 0].set_ylabel('Scattering', fontsize=24);
                            axs[0, 0].set_title('Four Parameters Logistic Regression', fontsize=35);


                            #print("\n")


                            #Calculating Estimation of First and Second Derivatives                       
                            #Defining x_ as a variable for sympy
                            x_ = symbols('x_')
                            #Applying parameters and x_ to define equation
                            equation = d_ + ((a_-d_)/(1+(x_/c_)**b_))
                            
                            
                            #From calculating the derivatives beforehand without applying the parameters a_, b_, c_, d_
                            deriv_1 = -b_*(x_/c_)**b_*(a_ - d_)/(x_*((x_/c_)**b_ + 1)**2)
                            deriv_2 = b_*(x_/c_)**b_*(a_ - d_)*(2*b_*(x_/c_)**b_/((x_/c_)**b_ + 1) - b_ + 1)/(x_**2*((x_/c_)**b_ + 1)**2)
                            
                            
                            #Finding y(absorbance) for the cloiud point (c_)
                            c_y = equation.evalf(subs={x_:c_})
                            
                            #Finding first derivative
                            #firstDeriv = equation.diff(x_)
                            #print(firstDeriv)
                            #Finding second derivative
                            #secondDeriv = equation.diff(x_, 2)
                            #print(secondDeriv)
                            #print(deriv_2)
                            #critical_Points = solveset(Eq(firstDeriv, 0), x_)
                            #print(critical_Points)
                            #critical_PointsY = [equation.subs(x_, a) for a in critical_Points]
                            #Defining a vector according to data so we can plot the derivatives
                            xx = np.linspace(x[0], x[-1], 1000)
                            #Evaluating the vector for each derivative so they can be used for plotting
                            for w in xx:
                                y1.append(deriv_1.evalf(subs={x_:w}))
                                y2.append(deriv_2.evalf(subs={x_:w}))
   
                            #print(y1)
                            
                            #Plotting First Derivative Estimation data
                            axs[1, 0].plot(xx, y1, color='orange', linewidth=3);
                            axs[1, 0].grid('on');
                            axs[1, 0].legend(['1st Derivative'], fontsize=22);
                            axs[1, 0].set_xlabel('Temperature', fontsize=24);
                            axs[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 0].set_title('1st Derivative Estimation', fontsize=35);
                            
                            #Plotting Second Derivative Estimation data
                            axs[1, 1].plot(xx, y2, color='green', linewidth=3);
                            axs[1, 1].grid('on');
                            axs[1, 1].legend(['2nd Derivative'], fontsize=22);
                            axs[1, 1].set_xlabel('Temperature', fontsize=24);
                            axs[1, 1].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 1].set_title('2nd Derivative Estimation', fontsize=35);



                            #Reporting the Critical points:
                            #For this, we interpolate the first derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            #m_1 = len(yder)
                            #rec_s_1 = m_1-math.sqrt(2*m_1)
                            #Finds the Critical points
                            #critical_points = interpolate.sproot(interpolate.splrep(xnew, yder, s= rec_s_1))
                            #Reports the Critical Point(s)
                            #print("The " + str(len(critical_points)) +" Critical points are: " + str(critical_points).strip('[]'))
                            #print(yder)



                            #print("\n")




                            #Calculating the Inflection/Cloud point:
                            #For this, we interpolate the second derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            #m_2 = len(yder_2)
                            #rec_s_2 = m_2-math.sqrt(2*m_2)
                            #Finds the Cloud Point
                            #cloud_point_x = interpolate.sproot(interpolate.splrep(xnew, yder_2, s= rec_s_2))
                            #Reports the Cloud Point(s)
                            #print("Temperature at the Inflection/Cloud point is: " + str(cloud_point_x).strip('[]'))


                            #print("\n")


                            #Give temperature and get absorbance (Finding absorbance for each cloud_point)
                            #Choose your x:
                            #for j in cloud_point_x:
                                #x_give = j
                                #y_given = interpolate.splev(x_give, tck, der=0, ext=0)   # if ext=0, return the extrapolated value.

                                #print("For the Cloud Point Temperature (" + str(x_give).strip('[]') + "), the Scattering is " + str(y_given).strip('[]'))

                                #print("\n")

                                #Updates cloud_point_y with cloud_point_x's absrobance
                                #cloud_point_y.append(y_given)


                            #Calculating delta Temperature (Tfinal - Tinitial) and delta Scattering (Absfinal - Absinitial)
                            #if len(critical_points) > 1:                         
                                #delta_T = critical_points[-1] - critical_points[0]
                                #delta_Abs = interpolate.splev(critical_points[-1], tck, der=0, ext=0) - interpolate.splev(critical_points[0], tck, der=0, ext=0)

                                #print("Delta Temperature is "+str(delta_T))
                                #print("Delta Scattering is "+str(delta_Abs))
                                #print("\n")


                            #Calculating LLPS_Capacity
                            #if len(critical_points) > 1: 
                                #LLPS_Cap = interpolate.splint(critical_points[0], critical_points[-1], tck)

                                #print("LLPS Capacity is: " +str(LLPS_Cap))
                                #print("\n")


                            #Plotting Summary Plot
                            axs[0, 1].plot(x, y_fit, 'b', linewidth=3);
                            axs[0, 1].grid('on');
                            
                            #Plotting Cloud Point on Summary Plot
                            axs[0, 1].plot(c_, c_y , '.', color='green', markersize=35);


                            #if cloud_point_x != '':
                            #if len(cloud_point_x) > 0:
                                #for j1 in cloud_point_x:                        
                                    #axs[0, 1].plot(j1, cloud_point_y[counter_y] , '.', color='green', markersize=35);

                                    #counter_y = counter_y + 1   #Updates handy counter to help plot cloud point


                            #Plotting lines on initial and final temperatures
                            #if len(critical_points) > 0:
                                #for j2 in critical_points:
                                    #axs[0, 1].axvline(x=j2, color='orange', linestyle='--', linewidth=4);



                            axs[0, 1].set_xlabel('Temperature', fontsize=24);
                            axs[0, 1].set_ylabel('Scattering', fontsize=24);
                            axs[0, 1].set_title('Summary ', fontsize=38);


                            axs[0, 1].legend(['4PL Regression','Cloud Point', 'Transtion Temperatures'], fontsize=22);
                            plt.rc('xtick', labelsize=18) ;
                            plt.rc('ytick', labelsize=18) ;

                            #Adding title and saving plot
                            fig.suptitle(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']"), fontsize=40)
                            fig.savefig(output + "/" + str(i1) + "nm" + "/" + str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']") +".png")
                            plt.close('all')

                            #Updating the text file to export the data with information from the current run
                            f1 = open(str(output) + "/" + "Parameters_4PL_" + str(i1).strip('"[]"') + "nm.txt", "a")
                            #f1.write(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip(''"[]") + ", " + str(i3).strip(''"[]") +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+ "Critical_Points/Transition_Temperatures" +", "+ str(critical_points).strip('"[]"') +"\n"+ "Inflection_Points/Cloud_Points" +", "+ str(cloud_point_x).strip('"[]"') +"\n"+ "Delta_Temperature" +", "+ str(delta_T).strip('"[]"') +"\n"+ "Delta_Scattering" +", "+ str(delta_Abs).strip('"[]"') +"\n"+"\n")
                            f1.write(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip(''"[]") + ", " + str(i3).strip(''"[]") +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+ "Inflection_Point/Cloud_Point Temperature" +", "+ str(c_).strip('"[]"') +"\n" + "Inflection_Point/Cloud_Point Scattering" +", "+ str(c_y).strip('"[]"')+"\n"+ "Hill's Slope" +", "+ str(b_).strip('"[]"')+"\n"+"\n")
                            f1.close()
                            
                        except:
                            pass
        
        #When calculating the parameters
        print("\n" + "Parameters were successfully calculated! ")
              
    print("\n")
    print("Done!")
    print("\n")
    print("# ===================================================== #")
    print("\n")
    

    
###  ======================================================================================================================  ##


"""
Created by Leo Dettori on 2021.07.22.
"""

#Defines the function of the 5PL_regression model
def func_5PL(x, a, b, c, d, g):
    return d + ((a-d)/((1+(x/c)**b)**g))

#Defines the function of the 4PL_regression model to aid with the initial guess for the 5PL fit
def func_4PL(x, a, b, c, d):
    return d + ((a-d)/(1+(x/c)**b))


#Applies the model
def find_parameters_5PL_regression(experiment, file_name, output):
    #Fits data to a Four Parameter Logistic Regression model
    
    #Initial message
    print("Calculating parameters...")
    print("\n")
    
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.optimize as opt
    import math
    import os
    from sympy import diff, solveset, lambdify, symbols, Eq, Reals, evalf
    
    
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
        
    
    #Creates a Parameters folder to store the results in an orderly fashion
    #Checks all folders in the slected ouput directory
    folders_2 = next(os.walk(output))[1]   #Compiles a list of all folder within this folder
    #print(folders_2)
    #Updates output destination with the name of the mother file
    output = output + "/" + "Parameters_5PL"
        
    #Checks if Parameters folder was already created, if yes, the program already ran once and it will end
    if "Parameters_5PL" in folders_2:
        print("\n" + "Parameters_5PL folder was already created! ")
        print("\n" + "Finding_Parameters program will not recalculate the parameters.")  
                
    #If Parameters folder was not created yet, it will be created now and the program will proceed    
    else:
        os.mkdir(output)
        print("\n"+"Parameters_5PL folder to store results was successfully created in the output location!")


        #Starts to loop through the wavelengths
        for i1 in experiment:
            
            #Creates the text file to export the data for the current wavelength
            f1 = open(str(output) + "/" + "Parameters_5PL_" + str(i1).strip('"[]"') + "nm.txt", "a")
            f1.write(str(i1).strip('"[]"')+ "nm" +"\n"+"\n")
            f1.close()

            #Creates a folder to store results of current wavelength
            os.mkdir(output + "/" + str(i1) + "nm")

            #starts to loop through the samples in each wavelength
            for i2 in experiment[str(i1)]:

                    #starts to loop through the temeperature programs for each sample for each wavelength
                    for i3 in experiment[str(i1)][str(i2)]:


                        #Performing Four Parameter Logistic Regression model

                        #Prepares/resets the variables for this run:
                        cloud_point_x = ''
                        cloud_point_y = []
                        counter_y = 0   #helps when plotting cloud points
                        critical_points = ''
                        delta_T = ''
                        delta_Abs = ''
                        
                        a_ = ''
                        b_ = ''
                        c_ = ''
                        d_ = ''
                        g_ = ''
                        y_fit = []
                        c_y = ''
                        xx = []
                        y1 = []
                        y2 = []
                        
                        ai = ''
                        bi = ''
                        ci = ''
                        di = ''
                        gi = ''
                        initial = []
                        



                        #Defining x and y   #if we're doing cooling, we need to re-arrange data from lowest to highest temp
                        if i3 == 'Cooling':
                            x = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Temp"]))
                            y = list(reversed(experiment[str(i1)][str(i2)]['Cooling']["Abs"]))
                            
                        #Defining x and y when heating
                        if i3 == 'Heating':
                            x = experiment[str(i1)][str(i2)]['Heating']["Temp"]
                            y = experiment[str(i1)][str(i2)]['Heating']["Abs"]

                        #print("x = " + str(x))
                        #print("y = " + str(y))
                        
                        print(str(i1)+"_"+str(i2)+"_"+str(i3))
                        
                        try:
                            
                            #Calculating initial guess for the regression from a 4PL regression
                            #(ai, bi, ci, di), _ = opt.curve_fit(func_4PL, x, y);
                            
                            ai = y[0]
                            bi = (y[-1]-y[0])/(x[-1]-x[0])
                            ci = (x[0]+x[-1])/2
                            di = y[-1]   
                                                        
                            gi = 1   #when g = 1, the 5PL becomes a 4PL
                
                            
                            #Organizing the parameters
                            initial = [ai,bi,ci,di,gi]


                            #Finding parameters using regression model
                            (a_, b_, c_, d_, g_), _ = opt.curve_fit(func_5PL, x, y, p0=initial);

                            #Applying parameters to fit the data
                            y_fit = func_5PL(x, a_, b_, c_, d_, g_)  #c_ is the cloudpoint in a 5PL regression model when g_ = 1

                            #print(c_)


                            #Plotting results
                            fig, axs = plt.subplots(2, 2, figsize =(30, 23));
                            axs[0, 0].plot(x, y, 'o' , markersize=10);
                            axs[0, 0].plot(x, y_fit, 'b', linewidth=3);
                            axs[0, 0].grid('on');
                            axs[0, 0].legend(['Data', '5PL Regression'], fontsize=22);
                            axs[0, 0].set_xlabel('Temperature', fontsize=24);
                            axs[0, 0].set_ylabel('Scattering', fontsize=24);
                            axs[0, 0].set_title('Five Parameters Logistic Regression', fontsize=35);


                            #print("\n")


                            #Calculating Estimation of First and Second Derivatives                       
                            #Defining x_ as a variable for sympy
                            x_ = symbols('x_')
                            #Applying parameters and x_ to define equation
                            equation = d_ + ((a_-d_)/((1+(x_/c_)**b_)**g_))
                            
                            #From calculating the derivatives beforehand without applying the parameters a_, b_, c_, d_
                            deriv_1 = -b_*g_*(x_/c_)**b_*(a_ - d_)*((x_/c_)**b_ + 1)**(-g_)/(x_*((x_/c_)**b_ + 1))
                            deriv_2 = b_*g_*(x_/c_)**b_*(a_ - d_)*((x_/c_)**b_ + 1)**(-g_)*(b_*g_*(x_/c_)**b_/((x_/c_)**b_ + 1) + b_*(x_/c_)**b_/((x_/c_)**b_ + 1) - b_ + 1)/(x_**2*((x_/c_)**b_ + 1))
                            
                            
                            #Finding y(absorbance) for the cloiud point (c_)
                            c_y = equation.evalf(subs={x_:c_})
                            
                            #Finding first derivative
                            #firstDeriv = equation.diff(x_)
                            #print(firstDeriv)
                            #Finding second derivative
                            #secondDeriv = equation.diff(x_, 2)
                            #print(secondDeriv)
                            #print(deriv_2)
                            #critical_Points = solveset(Eq(firstDeriv, 0), x_)
                            #print(critical_Points)
                            #critical_PointsY = [equation.subs(x_, a) for a in critical_Points]
                            #Defining a vector according to data so we can plot the derivatives
                            xx = np.linspace(x[0], x[-1], 1000)
                            #Evaluating the vector for each derivative so they can be used for plotting
                            for w in xx:
                                y1.append(deriv_1.evalf(subs={x_:w}))
                                y2.append(deriv_2.evalf(subs={x_:w}))
   
                            #print(y1)
                            
                            #Plotting First Derivative Estimation data
                            axs[1, 0].plot(xx, y1, color='orange', linewidth=3);
                            axs[1, 0].grid('on');
                            axs[1, 0].legend(['1st Derivative'], fontsize=22);
                            axs[1, 0].set_xlabel('Temperature', fontsize=24);
                            axs[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 0].set_title('1st Derivative Estimation', fontsize=35);
                            
                            #Plotting Second Derivative Estimation data
                            axs[1, 1].plot(xx, y2, color='green', linewidth=3);
                            axs[1, 1].grid('on');
                            axs[1, 1].legend(['2nd Derivative'], fontsize=22);
                            axs[1, 1].set_xlabel('Temperature', fontsize=24);
                            axs[1, 1].axhline(y=0, color='r', linestyle='--', linewidth=2.5);
                            axs[1, 1].set_title('2nd Derivative Estimation', fontsize=35);



                            #Reporting the Critical points:
                            #For this, we interpolate the first derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            #m_1 = len(yder)
                            #rec_s_1 = m_1-math.sqrt(2*m_1)
                            #Finds the Critical points
                            #critical_points = interpolate.sproot(interpolate.splrep(xnew, yder, s= rec_s_1))
                            #Reports the Critical Point(s)
                            #print("The " + str(len(critical_points)) +" Critical points are: " + str(critical_points).strip('[]'))
                            #print(yder)



                            #print("\n")




                            #Calculating the Inflection/Cloud point:
                            #For this, we interpolate the second derivative of the data and look for its roots
                            #Prepare the smoothness coefficient for the new cubic spline interpolation
                            #m_2 = len(yder_2)
                            #rec_s_2 = m_2-math.sqrt(2*m_2)
                            #Finds the Cloud Point
                            #cloud_point_x = interpolate.sproot(interpolate.splrep(xnew, yder_2, s= rec_s_2))
                            #Reports the Cloud Point(s)
                            #print("Temperature at the Inflection/Cloud point is: " + str(cloud_point_x).strip('[]'))


                            #print("\n")


                            #Give temperature and get absorbance (Finding absorbance for each cloud_point)
                            #Choose your x:
                            #for j in cloud_point_x:
                                #x_give = j
                                #y_given = interpolate.splev(x_give, tck, der=0, ext=0)   # if ext=0, return the extrapolated value.

                                #print("For the Cloud Point Temperature (" + str(x_give).strip('[]') + "), the Scattering is " + str(y_given).strip('[]'))

                                #print("\n")

                                #Updates cloud_point_y with cloud_point_x's absrobance
                                #cloud_point_y.append(y_given)


                            #Calculating delta Temperature (Tfinal - Tinitial) and delta Scattering (Absfinal - Absinitial)
                            #if len(critical_points) > 1:                         
                                #delta_T = critical_points[-1] - critical_points[0]
                                #delta_Abs = interpolate.splev(critical_points[-1], tck, der=0, ext=0) - interpolate.splev(critical_points[0], tck, der=0, ext=0)

                                #print("Delta Temperature is "+str(delta_T))
                                #print("Delta Scattering is "+str(delta_Abs))
                                #print("\n")


                            #Calculating LLPS_Capacity
                            #if len(critical_points) > 1: 
                                #LLPS_Cap = interpolate.splint(critical_points[0], critical_points[-1], tck)

                                #print("LLPS Capacity is: " +str(LLPS_Cap))
                                #print("\n")


                            #Plotting Summary Plot
                            axs[0, 1].plot(x, y_fit, 'b', linewidth=3);
                            axs[0, 1].grid('on');
                            
                            #Plotting Cloud Point on Summary Plot
                            #axs[0, 1].plot(c_, c_y , '.', color='green', markersize=35);


                            #if cloud_point_x != '':
                            #if len(cloud_point_x) > 0:
                                #for j1 in cloud_point_x:                        
                                    #axs[0, 1].plot(j1, cloud_point_y[counter_y] , '.', color='green', markersize=35);

                                    #counter_y = counter_y + 1   #Updates handy counter to help plot cloud point


                            #Plotting lines on initial and final temperatures
                            #if len(critical_points) > 0:
                                #for j2 in critical_points:
                                    #axs[0, 1].axvline(x=j2, color='orange', linestyle='--', linewidth=4);



                            axs[0, 1].set_xlabel('Temperature', fontsize=24);
                            axs[0, 1].set_ylabel('Scattering', fontsize=24);
                            axs[0, 1].set_title('Summary ', fontsize=38);


                            axs[0, 1].legend(['5PL Regression','Cloud Point', 'Transtion Temperatures'], fontsize=22);
                            plt.rc('xtick', labelsize=18) ;
                            plt.rc('ytick', labelsize=18) ;

                            #Adding title and saving plot
                            fig.suptitle(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']"), fontsize=40)
                            fig.savefig(output + "/" + str(i1) + "nm" + "/" + str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip("['']") +".png")
                            plt.close('all')

                            #Updating the text file to export the data with information from the current run
                            #f1 = open(str(output) + "/" + "Parameters_5PL_" + str(i1).strip('"[]"') + "nm.txt", "a")
                            #f1.write(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip(''"[]") + ", " + str(i3).strip(''"[]") +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+ "Critical_Points/Transition_Temperatures" +", "+ str(critical_points).strip('"[]"') +"\n"+ "Inflection_Points/Cloud_Points" +", "+ str(cloud_point_x).strip('"[]"') +"\n"+ "Delta_Temperature" +", "+ str(delta_T).strip('"[]"') +"\n"+ "Delta_Scattering" +", "+ str(delta_Abs).strip('"[]"') +"\n"+"\n")
                            #f1.write(str(experiment[str(i1)][str(i2)][str(i3)]["run_name"]).strip(''"[]") + ", " + str(i3).strip(''"[]") +"\n"+ "Temperature" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Temp"]).strip('"[]"') +"\n"+ "Scattering" + ", " + str(experiment[str(i1)][str(i2)][str(i3)]["Abs"]).strip('"[]"') +"\n"+ "Inflection_Point/Cloud_Point Temperature" +", "+ str(c_).strip('"[]"') +"\n" + "Inflection_Point/Cloud_Point Scattering" +", "+ str(c_y).strip('"[]"')+"\n"+"\n")
                            #f1.close()
                            
                        except:
                            pass
        
        #When calculating the parameters
        print("\n" + "Parameters were successfully calculated! ")
              
    print("\n")
    print("Done!")
    print("\n")
    print("# ===================================================== #")
    print("\n")