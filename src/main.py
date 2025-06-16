import argparse
import sys
from dataset_manager import DatasetManager

def print_help():
    """Print detailed help information for all available commands."""
    print("\n========= PyLytics - All Commands =========\n")
    print("load <file_path> <dataset_name>")
    print("    - Load a dataset from a CSV file")
    print("    - Example: load C:\\Users\\user\\Downloads\\data.csv my_dataset")
    
    print("\nlist")
    print("    - Display all loaded datasets with their details")
    print("    - Shows number of rows, columns, and last modified time")
    
    print("\nview <dataset_name> [n_rows]")
    print("    - View the first N rows of a dataset")
    print("    - If n_rows is not specified, shows first 5 rows")
    print("    - Example: view my_dataset 10")
    
    print("\nremove <dataset_name>")
    print("    - Remove a dataset from the system")
    print("    - Example: remove my_dataset")
    

    print("\nhelp")
    print("    - Display this help message")
    
    print("\nexit")
    print("    - Exit the program")
    
    print("\n=====================================\n")

def main():
    dataset_manager = DatasetManager()

    print("\n=== PyLytics - Data Management Tool ===")
    print("\Enter 'help' to see all the commands\n")
    print("=====================================\n")

    while True:
        try:
            user_input = input("pylytics> ").strip()
            
            if not user_input:
                continue
                
            # Parsing arguments
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]
            
            if command == "exit":
                print("Thanks for using PyLytics!")
                sys.exit(0)
                
            elif command == "help":
                print_help()
                
            elif command == "load":
                if len(args) != 2:
                    print("Usage: load <file_path> <dataset_name>")
                    print("Example: load C:\\Users\\user\\Downloads\\data.csv my_dataset")
                    continue
                    
                file_path, dataset_name = args
                if dataset_manager.load_dataset(file_path, dataset_name):
                    print(f"Successfully loaded dataset '{dataset_name}'")
                    
            elif command == "list":
                datasets = dataset_manager.list_datasets()
                if not datasets:
                    print("No datasets loaded")
                else:
                    print("\nLoaded datasets:")
                    for name, info in datasets:
                        print(f"\n{name}:")
                        print(f"  Rows: {info['rows']}")
                        print(f"  Columns: {info['columns']}")
                        #print(f"  Last modified: {info['last_modified']}")
                        
            elif command == "view":
                if len(args) < 1:
                    print("Usage: view <dataset_name> [n_rows]")
                    print("Example: view my_dataset 10")
                    continue
                    
                dataset_name = args[0]
                n_rows = int(args[1]) if len(args) > 1 else 5
                
                df = dataset_manager.view_dataset(dataset_name, n_rows)
                if df is not None:
                    print(f"\nFirst {n_rows} rows of '{dataset_name}':")
                    print(df)
                    
            elif command == "remove":
                if len(args) != 1:
                    print("Usage: remove <dataset_name>")
                    print("Example: remove my_dataset")
                    continue
                    
                dataset_name = args[0]
                if dataset_manager.remove_dataset(dataset_name):
                    print(f"Successfully removed the dataset: '{dataset_name}'")
                    
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' to see all available commands")
                
        except KeyboardInterrupt:
            print("\nThanks for using PyLytics!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 