from search import find_KT
from util import *
from time import time, sleep
import sys
import os
from pyfiglet import Figlet

MAX = 800000 # Cycle limit for search algorithm
H_PROB = 1 # Probability that Warnsdorff’s Rule is conformed to when adding Node objects to Frontier


def main():
    try:
        print("\nA personal project by Ariq Koh -- Github ID: sellmenn\n")
        f = Figlet(font='slant')
        print(f.renderText("Knight's Tour"))
        sleep(2)
        # Estimate runtime
        est = estimate_runtime(MAX)
        try:
            # For command-line argument execution
            var, length, write = str(sys.argv[1]).upper(), int(sys.argv[2]), True
            if var != "OPEN" and var != "CLOSED": raise ValueError
            print(f"\nConfiguration menu:\nDepth of search: {MAX}\nEstimated runtime: {est:.0f} seconds\nVariant: {var.capitalize()}\nLength of board: {length}\nWrite to file: {write}")
            proceed = False
            while not proceed:
                confirm = input("Confirm configuration (y/n): ").lower()
                if confirm == "y": proceed = True
                elif confirm == "n": raise ValueError
        except:
            # If no command-line input provided, or invalid command line input
            print("\nCommand line argument usage: python3 analyse.py open/closed length\n")
            print(f"Configuration menu:\nDepth of search: {MAX}\nEstimated runtime: {est:.0f} seconds")
            # Prompt user for variant
            var = input("Search 'open' or 'closed' variants: ").upper()
            if var != "OPEN" and var != "CLOSED": raise ValueError
            # Prompt user for length of board
            length = int(input("Length of board: "))
            # Prompt user to check if solutions should be saved to files
            write_to_file = (input("Write solutions to file? (y/n): ").lower())
            if write_to_file == "y": write = True
            elif write_to_file == "n": write = False
            else: raise ValueError
        try:
            analyse_KT(length=int(length), limit=MAX, h_prob=H_PROB, var=var.upper(), csv_file=f"{var.capitalize()}_KT.csv", write=write)
        except:
            print("Invalid input.\n Command line argument usage: python3 analyse.py open/closed length.")
    except EOFError:
        print("\nProgram terminated!\n")
        return 0
    except ValueError:
        print("Unexpected input! Program terminated.\n")
        return 1


def analyse_KT(length=8, limit=500000, h_prob=1, var="OPEN", csv_file="OpenTour.csv", write=True):
    # Create directory 'Results' if it does not already exist
    if not os.path.exists("Results"): 
        os.makedirs("Results") 
    print(f"\nSearching for solutions to {var.capitalize()} Knight's Tour.\nBoard size: {length}*{length}\nH_PROB: {h_prob}\nSearch depth: {limit} per coordinate")
    # Initialise count and start time
    start_time = time()
    total_count = 0
    # Write csv file headers
    with open(f"Results/{csv_file}", "w") as file:
        file.write("iterations, start coordinate, number of solutions\n")
    # For each coordinate on the board
    for i in range(length):
        for j in range(length):
            print(f"\nStarting coordinate ({i}, {j}):")
            # Obtain number of solutions while writing them into txt files
            solution_count = find_KT(length=length, start=(i, j), h_prob=h_prob, var=var, limit=limit, file_name=f"Results/{var.capitalize()}_{i}{j}.txt", write=write)
            # Add to solution count
            total_count += solution_count
            print(f"{solution_count} tours found ({total_count}). ", end="")
            if write:
                print(f"Refer to Results/{var.capitalize()}_{i}{j}.txt.")
            else: print()
            # Append count to csv file
            with open(f"Results/{csv_file}", "a") as file:
                file.write(f'{limit}, "{(i, j)}", {solution_count}\n')
    elapsed_time = time() - start_time
    print(f"\nSearch completed for {var.capitalize()} Knight's Tour in {elapsed_time:.2f} seconds.\nBoard size: {length}*{length}\nH_PROB: {h_prob}\nSearch limit: {limit} / start coordinate\n{total_count} tours found.")


def estimate_runtime(iterations):
    return iterations * 0.00065


if __name__ == "__main__":
    main()

