import argparse
import sys
from dataset_manager import DatasetManager

# ANSI color code escape sequences
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  



def print_help():
    """Print detailed help information for all available commands."""
    print("\n========= PyLytics - All Commands =========\n")
    print("- load [file_path] [dataset_name]: Load a dataset from a CSV file.")
    print("- list: List all loaded datasets.")
    print("- view [dataset_name] [N]: View the first N rows of a dataset")
    print("- analyze [dataset_name]: Perform data analysis on a dataset")
    print("- visualize [dataset_name]: Generate visualizations for a dataset")
    print("- clean [dataset_name]: Perform data cleaning operations.")
    print("- report [dataset_name]: Generate a report for a dataset.")
    print("- help: Show this help message")
    print("- exit: Exit the program.")
    
    
    print("\n=====================================\n")

def main():
    dataset_manager = DatasetManager()

    print(f"\n{CYAN}=== PyLytics - Data Management Tool ==={RESET}")
    print("\nEnter 'help' to see all the commands\n")
    print(f"{CYAN}====================================={RESET}\n")

    while True:
        try:
            user_input = input(f"{CYAN}pylytics> {RESET}").strip()
            
            if not user_input:
                continue
                
            # Parsing arguments
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]
            
            if command == "exit":
                print(f"\n{PURPLE}Thank you for using PyLytics!{RESET}\n")
                sys.exit(0)
                
            elif command == "help":
                print_help()
                
            elif command == "load":
                if len(args) != 2:
                    print(f"{YELLOW}Usage: load <file_path> <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: load C:\\Users\\user\\Downloads\\data.csv my_dataset{RESET}")
                    print("\n")

                    continue
                    
                file_path, dataset_name = args
                if dataset_manager.load_dataset(file_path, dataset_name):
                    print(f"{GREEN}Successfully loaded dataset '{dataset_name}'{RESET}")
                    
            elif command == "list":
                datasets = dataset_manager.list_datasets()
                if not datasets:
                    print(f"{YELLOW}No datasets are loaded yet. Load a dataset using the load command.{RESET}")
                else:
                    print(f"\n{BLUE}Loaded datasets:{RESET}")
                    i=0
                    for name, info in datasets:
                        print(f"{i+1}. {name} (Rows: {info['rows']}, Columns: {info['columns']})")
                        i+=1
                    print("\n")
                        
            elif command == "view":
                if len(args) < 1:
                    print(f"{YELLOW}Usage: view <dataset_name> [n_rows]{RESET}")
                    print(f"{YELLOW}Example: view my_dataset 10{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                n_rows = int(args[1]) if len(args) > 1 else 5
                
                df = dataset_manager.view_dataset(dataset_name, n_rows)
                if df is not None:
                    print(f"\nFirst {n_rows} rows of '{dataset_name}':")
                    print(df)
                    
            elif command == "remove":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: remove <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: remove my_dataset{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                if dataset_manager.remove_dataset(dataset_name):
                    print(f"{GREEN}Successfully removed the dataset: '{dataset_name}'{RESET}")
                    
            else:
                print(f"{RED}Unknown command: {command}{RESET}")
                print(f"{YELLOW}Type 'help' to see all available commands{RESET}")
                print("\n")
                
        except Exception as e:
            print(f"{RED}Error: {str(e)}{RESET}")

if __name__ == "__main__":
    main() 