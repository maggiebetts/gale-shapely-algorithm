# File: pa1.py
# Author: Kera Hernandez and Maggie Betts  
# Date: February 22, 2024
# Description: Program that implements the Gale-Shapley algorithm
# that solves a more general version of the stable matching problem
from time import process_time

def gale_shapley(filename):
    """
    Runs Gale-Shapley algorithm on input
    from file filename
    """

    # Open file
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("Could not open file")
        return None

    # Read input
    s_time = process_time()

    # read in input and initialize any data structures here
    # initialize data structures
    lines = f.readlines()
    hospital_ranks = []
    student_ranks = []
    first_line = lines[0].split()
    num_hospitals = int(first_line[0])
    num_students = int(first_line[1])

    hospital_positions = list(map(int, lines[1].split()))

    # create list of rankings for each hospital
    for line in lines[2:2+num_hospitals]:
        hospital_ranks.append(list(map(int, line.split())))

    for line in lines[2+num_hospitals:]:
        student_ranks.append(list(map(int, line.split())))


    # Close file
    f.close()
    f_time = process_time()
    print(f"Time to read file = {f_time - s_time}")

    
    
    s_assigned_h = [None] * num_students
    
    hospitals_positions_remaining = {} #dictionary of hospitals and their remaining positions

    #create list of currently unmatched hospitals
    unmatched_hospitals = []
    for hospital in range(num_hospitals-1, -1, -1):
        hospitals_positions_remaining[hospital] = hospital_positions[hospital]
        unmatched_hospitals.append(hospital) 

    #determine the number of total open positions to fill
    num_positions = 0
    for positions in hospital_positions:
        num_positions += positions

    while unmatched_hospitals:
        h = unmatched_hospitals.pop(-1)

        for s in hospital_ranks[h]:
             #if a hospital has proposed to every student 
            if hospitals_positions_remaining[h] == 0:
                break

            elif hospitals_positions_remaining[h] != 0:

                #gets student preference list
                ranks = {}
                i = 0
                for hospital in student_ranks[s]:
                    ranks[hospital] = i 
                    i += 1

                if s_assigned_h[s] is None:
                    if ranks.get(h) != None:
                        s_assigned_h[s] = h

                        hospitals_positions_remaining[h] -= 1


                else:
                    current_hospital = s_assigned_h[s]
                    current_hospital_rank = ranks[current_hospital]
                    

                    #if s prefers new hospital to old partner
                    if ranks.get(h) != None:
                        new_hospital_rank = ranks[h]
                        if new_hospital_rank < current_hospital_rank:
                            s_assigned_h[s] = h
            
                            #change remaining positions 
                            hospitals_positions_remaining[h] -= 1    
                            hospitals_positions_remaining[current_hospital] += 1
                            
                            if hospitals_positions_remaining[current_hospital] == 1:
                                unmatched_hospitals.append(current_hospital)

    
    return s_assigned_h