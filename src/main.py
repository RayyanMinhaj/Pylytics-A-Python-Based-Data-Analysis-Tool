import argparse
import sys
from dataset_manager import DatasetManager
from data_explorer import DataExplorer

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
    print(f"\n{CYAN}========= PyLytics - All Commands =========={RESET}\n")
    
    # Dataset Management Commands
    print(f"{PURPLE}Dataset Management:{RESET}")
    print("load [file_path] [dataset_name]")
    print("    - Load a dataset from a CSV file")
    print("list")
    print("    - List all loaded datasets")
    print("view [dataset_name] [n_rows]")
    print("    - View first N rows of a dataset")
    print("remove [dataset_name]")
    print("    - Remove a dataset")
    
    # Data Exploration Commands
    print(f"\n{PURPLE}Data Exploration & Analysis:{RESET}")
    print("analyze [dataset_name]")
    print("      1. Summary statistics (mean, median, std dev)")
    print("      2. Missing data report")
    print("      3. Frequency counts")
    print("      4. Filter data (e.g., 'age > 25 and country == \"USA\"')")
    print("      5. Clean duplicates (remove duplicate rows)")
    
    # System Commands
    print(f"\n{PURPLE}System:{RESET}")
    print("help")
    print("    - Show this help message")
    print("exit")
    print("    - Exit the program")
    
    print(f"\n{CYAN}====================================={RESET}\n")

def main():
    dataset_manager = DatasetManager()
    data_explorer = DataExplorer(dataset_manager)

    print(f"\n{CYAN}=== PyLytics - Data Management Tool ==={RESET}")
    print("\nEnter 'help' to see all the commands\n")
    print(f"{CYAN}====================================={RESET}\n")

    while True:
        try:
            user_input = input(f"{CYAN}pylytics> {RESET}").strip()
            
            if not user_input:
                continue
                
            # Parsing arguments
            parts = user_input.split() # ['view', 'iris', '10']
            command = parts[0].lower() # 'view'
            args = parts[1:] # ['iris', '10']
            
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
                    print(f"{GREEN}Successfully loaded dataset '{dataset_name}'\n{RESET}")
                    
            elif command == "list":
                datasets = dataset_manager.list_datasets()
                if not datasets:
                    print(f"{YELLOW}No datasets are loaded yet. Load a dataset using the load command.{RESET}")
                else:
                    print(f"\n{CYAN}Loaded datasets:{RESET}")
                    i=0
                    for name, info in datasets:
                        print(f"{i+1}. {name} (Rows: {info['rows']}, Columns: {info['columns']})")
                        i+=1
                    print("\n")
                    
            elif command == "view":
                if len(args) < 1 or len(args) > 2:
                    print(f"{YELLOW}Usage: view <dataset_name> [n_rows]{RESET}")
                    print(f"{YELLOW}Example: view my_dataset 10{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                n_rows = int(args[1]) if len(args) > 1 else 5
                
                df = dataset_manager.view_dataset(dataset_name, n_rows)
                if df is not None:
                    print(f"\n{CYAN}First {n_rows} rows of '{dataset_name}':{RESET}")
                    print(df)
                    print("\n")
                    
            elif command == "analyze":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: analyze <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: analyze sales_data{RESET}")
                    print("\n")
                    continue
                
                dataset_name = args[0]

                print("\nSelect analysis type:")
                print("1. Summary statistics")
                print("2. Missing data report")
                print("3. Frequency counts")
                print("4. Filter data")
                print("5. Clean duplicates")
                
                try:
                    choice = input("Enter your choice (1-5): ").strip()
                    print("\n")  
                    
                    # Summary statistics
                    if choice == "1":
                        stats = data_explorer.get_summary_statistics(dataset_name)
                        
                        if stats:
                            print(f"Summary statistics for '{dataset_name}':")
                            
                            for col, col_stats in stats.items():
                                print(f"- {CYAN}{col}:{RESET}")
                                print(f"  - Mean: {col_stats['mean']}")
                                print(f"  - Median: {col_stats['median']}")
                                print(f"  - Std Dev: {col_stats['std']}")
                                print("\n")
                            print("\n")

                    
                    
                    # Missing data report
                    elif choice == "2":
                        missing_info = data_explorer.get_missing_data_info(dataset_name)
                        
                        if missing_info:
                            print(f"Missing data report for '{dataset_name}':")
                            
                            for col, info in missing_info.items():
                                print(f"- {CYAN}{col}:{RESET}")
                                print(f"  - Missing values: {info['count']}")
                                print(f"  - Missing percentage: {info['percentage']}%")
                                print("\n")
                            print("\n")
                        else:
                            print(f"{GREEN}No missing values found in the dataset!{RESET}\n")
                            
                    
                    
                    
                    # Frequency counts
                    elif choice == "3":
                        freq_counts = data_explorer.get_frequency_counts(dataset_name)
                        
                        if freq_counts:
                            print(f"Frequency counts for '{dataset_name}':")
                        
                            for col, info in freq_counts.items():
                                print(f"- {CYAN}{col}: ({info['total_unique']} unique values):{RESET}")
                                
                                for value, count in list(info['counts'].items())[:5]:  # ONly showing top 5 for conciseness
                                    print(f"  - {value}: {count}")
                                
                                if info['total_unique'] > 5:
                                    print("  - ...")
                        
                            print("\n")
                            
                    
                    
                    
                    # Filter data
                    elif choice == "4":
                        print(f"{CYAN}Enter filter condition (e.g., age > 25 and country == \"USA\"):{RESET}")
                        
                        condition = input("> ").strip()
                        filtered_df = data_explorer.filter_dataset(dataset_name, condition)
                        
                        if filtered_df is not None:
                            print(f"\n{CYAN}Filtered results ({len(filtered_df)} rows):{RESET}")
                            print(filtered_df.head())
                            
                        
                            print("\n")

                    
                    
                    
                    
                    
                    # Clean duplicates
                    elif choice == "5":
                        print(f"{CYAN}Specify columns for duplicate check (leave empty for all columns):{RESET}")
                        print("Enter column names separated by comma:")
                        cols = input("> ").strip()
                        subset = [col.strip() for col in cols.split(',')] if cols.strip() else None
                        cleaned_df, duplicates_removed = data_explorer.clean_duplicates(dataset_name, subset)
                        if cleaned_df is not None:
                            print(f"\n{GREEN}Removed {duplicates_removed} duplicate rows{RESET}")
                            if duplicates_removed > 0:
                                print(f"\n{CYAN}First few rows of cleaned dataset:{RESET}")
                                print(cleaned_df.head())
                            print("\n")
                            
                    
                    
                    
                    else:
                        print(f"{RED}Invalid choice. Please enter a number between 1 and 5.{RESET}\n")
                        
                except ValueError as e:
                    print(f"{RED}Error: {str(e)}{RESET}\n")
                    
            elif command == "filter":
                if len(args) < 2:
                    print(f"{YELLOW}Usage: filter <dataset_name> <condition>{RESET}")
                    print(f"{YELLOW}Example: filter iris 'sepal_length > 5'{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                condition = ' '.join(args[1:])
                
                filtered_df = data_explorer.filter_dataset(dataset_name, condition)
                if filtered_df is not None:
                    print(f"\n{CYAN}Filtered results ({len(filtered_df)} rows):{RESET}")
                    print(filtered_df.head())
                    print("\n")
                    
            elif command == "clean":
                if len(args) != 2 or args[0].lower() != "duplicates":
                    print(f"{YELLOW}Usage: clean duplicates <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: clean duplicates my_dataset{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[1]
                cleaned_df, duplicates_removed = data_explorer.clean_duplicates(dataset_name)
                
                if cleaned_df is not None:
                    print(f"{GREEN}Removed {duplicates_removed} duplicate rows from '{dataset_name}'{RESET}")
                    if duplicates_removed > 0:
                        print(f"\n{CYAN}First few rows of cleaned dataset:{RESET}")
                        print(cleaned_df.head())
                    print("\n")
                    
            elif command == "remove":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: remove <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: remove my_dataset{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                if dataset_manager.remove_dataset(dataset_name):
                    print(f"{GREEN}Successfully removed the dataset: '{dataset_name}'\n{RESET}")
                    
            else:
                print(f"{RED}Unknown command: {command}{RESET}")
                print(f"{YELLOW}Type 'help' to see all available commands{RESET}")
                print("\n")
                
        except Exception as e:
            print(f"{RED}Error: {str(e)}{RESET}")

if __name__ == "__main__":
    main() 