#!/usr/bin/env python
# coding: utf-8

# In[1]:


def user():
    '''Function that asks for the user for values that will be used throughout the rest of the program.'''
    try: 
        population = int(input('What is the approximate population size of your town/city/country? ')) #Asks the user for the total population (number of individuals who can become suseptible.)
        daily_rise = int(input('What was the rise in number of cases in your area today? ')) #Asks the user for the the number of cases (Thus the number of infectives in the first day)
        num_gen= int(input('How many days would you like to simulate? ')) #The number of generations indicated how many data points the user wants.
    except:
        print('Error: Please enter numbers only and try again.')
        covid_model()
    high_or_low = input('Would you like the transmission rate to be a high or low estimate? Please enter "High" or "Low". ').capitalize() #Asks the user for what type of estimate they would like
    try:
        if high_or_low == 'Low': #if the user wants a low estimate
            low_estimate = {'England':0.8, 'Northen Ireland':0.9, 'Scotland':0.8, 'Wales':0.8} #low estimates for UK values
            country = input('What country in the UK is your population from? ').capitalize() #answer used to select from the dictionary
            trans_rate = low_estimate[country] #pulls the estimate from the dictionary
            return trans_rate, country, num_gen, daily_rise, population
        
        else: # For high estimate
            high_estimate={'England':1.0, 'Northen Ireland':1.1, 'Scotland':1.0, 'Wales':1.0} #high estimates for UK values
            country = input('What country in the UK is your population from? ').capitalize() #answer used to select from the dictionary
            trans_rate = high_estimate[country] #pulls the estimate from the dictionary
            return trans_rate, country, num_gen, daily_rise, population
    except:
        print('Error: {} is not a valid entry. Please enter a country in the UK and try again. Enter all lower case.'.format(country))
        covid_model()
        


# In[2]:


def calculations(trans_rate, country, num_gen, daily_rise, population):
    '''Function to Calculate the number of individuals who gain immunity each generation without the inclusion of a vaccine.'''
    
    
    print('The transmission rate for {} is {}. '.format(country, trans_rate)) #informs the user of the information they did not directly imput
    mr= 0.036 #the UK mortality rate for the corona virus
    zero_death = (daily_rise*mr) #number of individuals that died from the cases the user provided (at time zero)
    zero_immunity = daily_rise - zero_death #number of individuals that gained immunity from the cases the user provides (at time zero)
    
    gen = range(1, num_gen + 1) #list of all generations
    total_cases = [daily_rise] #a list of all the cases - that for now only includes the daily rise
    total_immunity = [zero_immunity] #list of number of individuals immune each generation
    total_death = [zero_death] #list of number of individuals died each generation
    total_generation= [0] #creates a list of the generation numbers
    immune_list = [zero_immunity] #Sum of total immunity each generation
    immune_percentage=[]# immune_list in percentage of population 
    gen_death = [zero_death] #Sum of total death each generation
    death_percentage = []#gen_death in percentage of population
    infections = [zero_immunity]#Sum of total infection each generation
    infect_percentage =[]#infections in percentage of populations
    
    #Use of collection idea comes from http://stackoverflow.com/questions/4151320/efficient-circular-buffer 
    import collections
    infectious = collections.deque(maxlen=3) #create a list/queue which holds a maximum of three items
    infectious.append(daily_rise)  #appends the first group of individuals provided by the user to the infectious list
   
    for t in gen: #Sequences through all generations
        
        sum_cases = sum(total_cases) #sums all the number of cases
        
        if daily_rise == 0: #if total number of cases is larger than the population or there are no more cases
            
            print('All of the population has been processed.')
            recovered = sum(total_immunity) #number of people who recovered
            total_infectious = sum(infectious)
            I= total_infectious #number of people who are infectious 
            portion_infected = I/population #the portion of the individuals who are infectious (infectious/population)
            not_in_population = (recovered + sum(total_death)) #sum of the people no longer susceptible either immune or dead
            S = (population-not_in_population) #removes those who are not susceptible from the population
            portion_S = (S/population) #portion of the people susceptible
            new_cases = portion_S*I*trans_rate #number of new cases: portion of individuals in the population who are suseptible * infected (contagious) * transmission rate
            infectious.append(new_cases)
            total_cases.append(new_cases)#adds to the total number of cases
            
            death = (new_cases)*0.036 #portion of those infected who died
            total_death.append(death) #adds to the total number of deaths
            immunity = new_cases - death #individuals who are immune that generation
            total_immunity.append(immunity) #adds to the total number of immune
            print('On day {}, there were {:.0f} total cases, after an increase of {:.0f}. {:.0f} people became immune, and {:.0f} died.'.format(t, sum(total_cases), 
                                                                                                                               new_cases, immunity, death))
            print('After {} day(s) of COVID, {:.0f} number of people will be immune, with {:.0f} total people dying'.format(t,sum(total_immunity)), sum(total_death)) 
            daily_rise = new_cases
            print(' ')
            immune_list.append(sum(total_immunity))
            break
           
        else:
            recovered = sum(total_immunity) #number of people who recovered
            total_infectious = sum(infectious)
            I= total_infectious #number of people who are infectious 
            portion_infected= I/population #the portion of the individuals who are infectious in a population
            not_in_population = (recovered + sum(total_death)) #sum of the people no longer suseptible either immune or dead
            S = (population-not_in_population) #removes those who are not suseptible from the population
            portion_S = (S/population) #portion of the people suseptible
            new_cases = portion_S*I*trans_rate #number of new cases: portion of individuals in the population who are suseptible * infected (contagious) * transmission rate
            infectious.append(new_cases)
            if new_cases <= 0.5:
                pass
            else:
                total_generation.append(t) #adds a number to the total generation
                total_cases.append(new_cases) #adds to the total number of cases
                death = (new_cases)*0.036 #portion of those infected who died

                if death < 1:
                    total_death.append(1) #adds to the total number of deaths
                else:
                    total_death.append(death) #adds to the total number of deaths
                immunity = new_cases - death #individuals who are immune that generation

                if immunity < 1:
                        total_immunity.append(1) 
                else:
                    total_immunity.append(immunity) #adds to the total number of immune
                print('On day {}, there were {:.0f} total cases, after an increase of {:.0f}. {:.0f} people became immune, and {:.0f} died.'.format(t, sum(total_cases), 
                                                                                                                               new_cases, immunity, death))
                print('After {} day(s) of COVID, {:.0f} number of people will be immune, with {:.0f} total people dying'.format(t,sum(total_immunity), sum(total_death)))
                daily_rise = new_cases
                print(' ')
                immune_list.append(sum(total_immunity))
                infections.append(sum(total_cases))
                gen_death.append(sum(total_death))
   
   #The percentage of population is calculated and added to the list
    
    for immune in immune_list:
        percentage=immune/population*100 #calculates immunity as a percentage of total population
        immune_percentage.append(percentage)
    for infect in infections:
        inf_percentage = infect/population*100 #calculates infected as a percentage of total population
        infect_percentage.append(inf_percentage)
    for d in gen_death:
        death_p = d/population*100 #calculates death as a percentage of total population
        death_percentage.append(death_p)
    
    return total_cases, total_immunity, total_death, total_generation, immune_list, immune_percentage, infect_percentage, death_percentage


# In[3]:


def table(total_cases, total_immunity, total_death, total_generation, immune_list, immune_percentage,infect_percentage, death_percentage):
    
    '''Function to display table and save to a file the data to be displayed in a graph'''
    
    
    #imports a software libraries needed to complete the program
    
    import pandas as pd
    import numpy as np
    
    #creates a dictionary of the number of generations vs the percentage of individuals with immunity, that are infected and that have died
    
    data = {
    'Number of Days': total_generation,
    'Percentage of Immune Individuals': immune_percentage,
    'Percentage of infections': infect_percentage,
    'Percentage of deaths': death_percentage
        }
    
    #prints the information in data to a table
    table = pd.DataFrame.from_dict(data,orient='index')
    table = table.transpose()
    print(table)
    numpy_array = table.to_numpy()
    print(' ')
    
    decide = input('Do you want to save the report to a file? Enter yes or no: ').capitalize() #ask if they want to save a file
    if decide == 'Yes': #If they input yes
       
        print('Your file name will be "ImmunityTable"') 

        how = input('How would you like your file to be opened? Enter append or write: ').capitalize() #ask how they want the data to be saved

            #confirm_how = input('Confirm editing format with yes or no: ').capitalize() #ask for confirmation

            #if confirm_how == 'No':#if enter no
               # how = input('How would you like your file to be opened? Enter append or write: ') #allowed to enter again

        if how == 'Write': #write the following into the provided file
            file = open('ImmunityTable', 'w')
            np.savetxt('ImmunityTable' , numpy_array, fmt = "%d")
            file.close()
            print('I have successfully saved the data under "ImmunityTable". The program is complete.')

        elif how == 'Append': #append the following into the provided file
            file = open('ImmunityTable', 'a')
            np.savetxt('ImmunityTable' , numpy_array, fmt = "%d")
            file.close()
            print('I have successfully saved the data under "ImmunityTable" The program is complete.')
            
        else:
            print('Error: I do not understand command "{}". Please enter either "Write" or "Append" and try again.'.format(how))
            covid_model()
    
    else:#if the user doesn't want to save a file.
        print('Okay, I will not save the data. The program is complete.')


# In[4]:


def graph(total_cases,total_immunity,total_death, total_generation,immune_list, immune_percentage, infect_percentage, death_percentage):
    '''Function which prints a graph of established data'''
    
    import pandas as pd
    
    
    tdf= pd.read_csv("ImmunityTable",sep=" ") #reads file to collect the data
    tdf.shape
    tdf=pd.read_csv("ImmunityTable",sep=" ",names=["Number of days", "Immunity (% of population)", "Infections (% of population)", "Deaths (% of population)"]) #creates headers for the graph
    tdf.head()
    tdf.plot(x="Number of days",y=["Immunity (% of population)","Deaths (% of population)","Infections (% of population)"], title='Immunity without Vaccine') #plots the data
    


# In[5]:


def vac_user():
    
    '''Function to ask the user for the vaccine data and efficiency, and calculate how many people become immune from 
    the vaccine per generation'''  
    
    vac_name = input("What is the brand name of the vaccine used? ")
    try:
        efficiency =input(("What is the efficiency of the vaccine in percentage? (Enters number only. Do not include '%') "))
        effi_dec = (int(efficiency)/100)
    except:
        print('Error: Please enter numbers only and try again.')
        efficiency =input(("What is the efficiency of the vaccine in percentage? (Enters number only. Do not include '%') "))
        effi_dec = (int(efficiency)/100) 
    try:
        vac_people = int(input(("How many people are being vaccinated in your population per day? ")))
        vac_immunity= (vac_people *effi_dec) #calculates how many people are becoming immune from the vaccine per generation
    except:
        print('Error: Please enter numbers only and try again.')
        vac_people = int(input(("How many people are being vaccinated in your population per day? ")))
        vac_immunity= (vac_people *effi_dec) #calculates how many people are becoming immune from the vaccine per generation
    
    return vac_immunity


# In[6]:


def vac_calculations(trans_rate, country, num_gen, daily_rise, population):
    '''Function to Calculate the number of individuals who gain immunity each generation WITH the inclusion of a vaccine.'''
    
    vac_immunity = vac_user()
    
    print('The transmission rate for {} is {}. '.format(country, trans_rate)) #informs the user of the information they did not directly imput
    mr= 0.036 #the UK mortality rate for the corona virus
    zero_death = (daily_rise*mr) #number of individuals that died from the cases the user provided (at time zero)
    zero_immunity = daily_rise - zero_death #number of individuals that gained immunity from the cases the user provides (at time zero)
   
    gen = range(1, num_gen + 1) #list of all generations
    vac_total_cases = [daily_rise] #a list of all the cases - that for now only includes the daily rise
    vac_total_immunity = [zero_immunity] #list of number of individuals immune each generation
    vac_total_death = [zero_death] #list of number of individuals died each generation
    vac_total_generation= [0] #creates a list of the generation numbers
    total_vac = [0]
    vac_immune_list = [zero_immunity] #Sum of total immunity each generation
    vac_immune_percentage=[]# vac_immune_list in percentage of population
    vac_gen_death = [0]#Sum of total death each generation
    vac_death_percentage = []#vac_gen_death in percentage of population
    vac_infections = [zero_immunity]#Sum of total infection each generation
    vac_infect_percentage =[]#vac_infections in percentage of population
    immune_from_vaccine = [0]#sum of total immunity just from vaccines in each generation
    percent_immune_vaccine=[]#immune_from_vaccine as percentage of population
    

    
    #Use of collection idea comes from http://stackoverflow.com/questions/4151320/efficient-circular-buffer 
    import collections
    infectious = collections.deque(maxlen=3) #create a list/queue which holds a maximum of three items
    infectious.append(daily_rise) #appends the first group of individuals provided by the user to the infectious list
   
    for t in gen: #Sequences through all generations
        
        sum_cases = sum(vac_total_cases) #sums all the number of cases
        
        if daily_rise == 0: #if total number of cases is larger than the population or there are no more cases
            
            print('All of the population has been processed.')
            recovered = sum(vac_total_immunity) #number of people who recovered
            total_infectious = sum(vac_infections)
            I= total_infectious #number of people who are infectious 
            portion_infected = I/population #the portion of the individuals who are infectious over population
            not_in_population = (recovered + sum(vac_total_death)) #sum of the people no longer suseptible either immune or dead
            S = (population-not_in_population) #removes those who are not suseptible from the population
            portion_S = (S/population) #portion of the people suseptible
            new_cases = portion_S*I*trans_rate #number of new cases: portion of individuals in the population who are suseptible * infected (contagious) * transmission rate
            infectious.append(new_cases)
            vac_total_cases.append(new_cases)#adds to the total number of cases
            
            death = (new_cases)*0.036 #portion of those infected who died
            vac_total_death.append(death) #adds to the total number of deaths
            immunity = new_cases - death #individuals who are immune that generation
            vac_total_immunity.append(immunity) #adds to the total number of immune
            print('On day {}, there were {:.0f} total cases, after an increase of {:.0f}. {:.0f} people became immune, and {:.0f} died.'.format(t, sum(vac_total_cases), 
                                                                                                                               new_cases, immunity, death))
            print('After {} day(s) of COVID, {:.0f} number of people will be immune, with {:.0f} total people dying'.format(t,sum(vac_total_immunity), sum(vac_total_death))) 
            daily_rise = new_cases
            print(' ')
            immune_list.append(sum(vac_total_immunity))
            break
           
        else:
            recovered = sum(vac_total_immunity) #number of people who recovered
            total_infectious = sum(vac_infections)
            I= total_infectious #number of people who are infectious 
            portion_infected= I/population #the portion of the individuals who sre infectious over total population
            not_in_population = (recovered + sum(vac_total_death)) #sum of the people no longer suseptible either immune or dead
            S = (population-not_in_population) #removes those who are not suseptible from the population
            portion_S = (S/population) #portion of the people suseptible
            new_cases = portion_S*I*trans_rate #number of new cases: portion of individuals in the population who are suseptible * infected (contagious) * transmission rate
            infectious.append(new_cases)
            if new_cases <= 0.5:
                pass
            else:
                vac_total_generation.append(t) #adds a number to the total generation
                vac_total_cases.append(new_cases) #adds to the total number of cases
                death = (new_cases)*0.036 #portion of those infected who died

                if death < 1:
                    vac_total_death.append(1) #adds to the total number of deaths
                else:
                    vac_total_death.append(death) #adds to the total number of deaths
                
                vaccine_gen= vac_immunity
                total_vac.append(vaccine_gen)
                immunity = new_cases + vaccine_gen - death #individuals who are immune that generation

                if immunity < 1:
                        vac_total_immunity.append(1) 
                else:
                    vac_total_immunity.append(immunity) #adds to the total number of immune
                print('On day {}, there were {:.0f} total cases, after an increase of {:.0f}. {:.0f} people became immune, and {:.0f} died.'.format(t, sum(vac_total_cases), 
                                                                                                                               new_cases, immunity, death))
                print('After {} day(s) of COVID, {:.0f} number of people will be immune, with {:.0f} total people dying'.format(t,sum(vac_total_immunity), sum(vac_total_death))) 
                  
                daily_rise = new_cases
                print(' ')
                vac_immune_list.append(sum(vac_total_immunity))
                vac_infections.append(sum(vac_total_cases))
                vac_gen_death.append(sum(vac_total_death))
                immune_from_vaccine.append(sum(total_vac))
    #The percentage is calculated and added to the list
    
    for immune in vac_immune_list:
        percentage= (immune/population)*100 #calculates immune as a percentage of total population
        vac_immune_percentage.append(percentage) # adds it to list
    for infect in vac_infections:
        inf_percentage = (infect/population)*100 #calculates infected as a percentage of total population
        vac_infect_percentage.append(inf_percentage)
    for d in vac_gen_death:
        death_p = (d/population)*100 #calculates death as a percentage of total population
        vac_death_percentage.append(death_p)
    for v in immune_from_vaccine:
        vaccine_p = (v/population)*100 #calculates immune from vaccine as a percentage of total population
        percent_immune_vaccine.append(vaccine_p)
    
    return vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine


# In[7]:


def vac_table(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine):
    '''Function to display table and save to a file the data to be displayed in a graph, WITH include of vaccine data'''
 
    #imports a software libraries needed to complete the program
    import pandas as pd
    import numpy as np
    
    #creates a dictionary of the number of generations vs the sum of the individuals with immunity,immunity just from vaccine,that are infected and have died
    data = {
    'Number of Days': vac_total_generation,
    'Percentage of immune individuals (Vaccine Included)': vac_immune_percentage,
    'Percentage of Infections': vac_infect_percentage,
    'Percentage of Deaths': vac_death_percentage,
    'Percentage of immune because of the vaccine': percent_immune_vaccine
        }
    
    #prints the information in data to a table
    table = pd.DataFrame(data)
    print(vac_table)
    numpy_array = table.to_numpy()
    print(' ')
    
    
    decide = input('Do you want to save the report to a file? Enter yes or no: ').capitalize() #ask if they want to save a file
    if decide == 'Yes': #If they input yes
       
        print('Your file name will be "ImmunityTable"') 

        how = input('How would you like your file to be opened? Enter append or write: ').capitalize() #ask how they want the data to be saved

            #confirm_how = input('Confirm editing format with yes or no: ').capitalize() #ask for confirmation

            #if confirm_how == 'No':#if enter no
               # how = input('How would you like your file to be opened? Enter append or write: ') #allowed to enter again

        if how == 'Write': #write the following into the provided file
            file = open("VacImmunityTable", 'w')
            np.savetxt("VacImmunityTable" , numpy_array, fmt = "%d")
            file.close()
            print('I have successfully saved the data under "VacImmunityTable". The program is complete.')

        elif how == 'Append': #append the following into the provided file
            file = open("VacImmunityTable", 'a')
            np.savetxt("VacImmunityTable" , numpy_array, fmt = "%d")
            file.close()
            print('I have successfully saved the data under "VacImmunityTable" The program is complete.')
            
        else:
            print('Error: I do not understand command "{}". Please enter either "Write" or "Append" and try again.'.format(how))
            covid_model()
    
    else:#if the user doesn't want to save a file.
        print('Okay, I will not save the data. The program is complete.')
    


# In[8]:


def vac_graph(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine):
    '''Function which prints a graph of established vaccinen data'''
    import pandas as pd
    
    tdf= pd.read_csv("VacImmunityTable",sep=" ") #reads file to collect the data
    tdf.shape
    tdf=pd.read_csv("VacImmunityTable",sep=" ",names=["Number of days", "Immune- Natural/Vaccine (% of Population)", "Infections (% of Population)", "Number of Deaths (% of Population)", 'Vaccine Immunity Only (% of the Population)']) #creates headers for the graph
    tdf.head()
    tdf.plot(x="Number of days",y= ["Immune- Natural/Vaccine (% of Population)", "Infections (% of Population)", "Number of Deaths (% of Population)", 'Vaccine Immunity Only (% of the Population)'], title=('Immunity with Vaccine'))
    


# In[9]:


def covid_model():
    '''Function which runs all the program:non vaccine and vaccine and asks user if the parameters should stay the same  '''
    #functions for model without vaccine 
    trans_rate, country, num_gen, daily_rise, population = user()
    total_cases,total_immunity,total_death, total_generation, immune_list,immune_percentage, infect_percentage, death_percentage = calculations(trans_rate, country, num_gen, daily_rise, population)
    table(total_cases,total_immunity,total_death, total_generation,immune_list,immune_percentage, infect_percentage, death_percentage)
    graph(total_cases,total_immunity,total_death, total_generation,immune_list,immune_percentage, infect_percentage, death_percentage)
    vac_decide = input('Do you want to run the vaccine simulation with the same values? Enter yes or no: ').capitalize()
    #functions for model with vaccine
    if vac_decide == 'Yes':
        #user function not necessary,as the values will be used previous user()
        vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine = vac_calculations(trans_rate, country, num_gen, daily_rise, population)
        vac_table(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine)
        vac_graph(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine)
    else:
        trans_rate, country, num_gen, daily_rise, population = user() #user function needed to redine parameters
        vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine = vac_calculations(trans_rate, country, num_gen, daily_rise, population)
        vac_table(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine)
        vac_graph(vac_total_cases, vac_total_immunity, vac_total_death, vac_total_generation, vac_immune_list, vac_immune_percentage, vac_infect_percentage, vac_death_percentage, percent_immune_vaccine)

