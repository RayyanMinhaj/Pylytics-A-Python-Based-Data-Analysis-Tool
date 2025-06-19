import argparse
import sys
import os
import pandas as pd
import numpy as np
from dataset_manager import DatasetManager
from data_explorer import DataExplorer
from report_generator import ReportCreator
from visualizer import Visualizer
from modeling import LinearRegressionModel, LogisticRegressionModel, KMeansModel, BaseModel
                    

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

    # Data Cleaning Commands
    print(f"\n{PURPLE}Data Cleaning:{RESET}")
    print("clean [dataset_name]")
    print("      1. Remove duplicates")
    print("      2. Handle missing values")
    
    # System Commands
    print(f"\n{PURPLE}System:{RESET}")
    print("help")
    print("    - Show this help message")
    print("exit")
    print("    - Exit the program")
    
    # New commands
    print(f"\n{PURPLE}Modeling Commands:{RESET}")
    print("model <dataset_name>")
    print("    - Train a model on the dataset")
    print("predict")
    print("    - Predict using a trained model")
    
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
                
                try:
                    choice = input("Enter your choice (1-4): ").strip()
                    print() 
                    
                    if choice == "1":
                        stats = data_explorer.get_summary_statistics(dataset_name)
                        
                        if stats:
                            print(f"Summary statistics for '{dataset_name}':")
                            
                            for col, col_stats in stats.items():
                                print(f"- {CYAN}{col}:{RESET}")
                                print(f"  - Count: {col_stats['count']}")
                                print(f"  - Mean: {col_stats['mean']}")
                                print(f"  - Median: {col_stats['median']}")
                                print(f"  - Std Dev: {col_stats['std']}")
                                print(f"  - Min: {col_stats['min']}")
                                print(f"  - 25%: {col_stats['25%']}")
                                print(f"  - 50%: {col_stats['50%']}")
                                print(f"  - 75%: {col_stats['75%']}")
                                print(f"  - Max: {col_stats['max']}")
                                print("\n")
                            #print("\n")

                    
                    
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
                            
                    
                    
                    
                    elif choice == "3":
                        freq_counts = data_explorer.get_frequency_counts(dataset_name)
                        
                        if freq_counts:
                            print(f"{CYAN}Frequency counts for '{dataset_name}':{RESET}")
                        
                            for col, info in freq_counts.items():
                                print(f"- {GREEN}{col} ({info['total_unique']} unique values):{RESET}")
                                
                                for value, count in list(info['counts'].items())[:5]:  # Showing top 5 for conciseness
                                    print(f"  - {value}: {count}")
                                
                                if info['total_unique'] > 5:
                                    print("  - ...")
                            
                                print("\n")
                        
                            print("\n")
                            
                    
                    
                    
                    elif choice == "4":
                        print(f"{CYAN}Enter filter condition (e.g., age > 25 and country == \"USA\"):{RESET}")
                        
                        condition = input("> ").strip()
                        filtered_df = data_explorer.filter_dataset(dataset_name, condition)
                        
                        if filtered_df is not None:
                            print(f"\n{CYAN}Filtered results ({len(filtered_df)} rows):{RESET}")
                            print(filtered_df.head())
                            
                            print("\nWould you like to save this filtered dataset? (y/n)")
                            save_choice = input("> ").strip().lower()
                            
                            if save_choice == 'y':
                                print("\nEnter name for the filtered dataset:")
                                new_name = input("> ").strip()
                                analysis_desc = f"Filtered with condition: {condition}"
                                dataset_manager.update_dataset(new_name, filtered_df, analysis_desc)
                                print(f"{GREEN}Filtered dataset updated as '{new_name}'{RESET}")
                            print("\n")
                    
                    
                    
                    else:
                        print(f"{RED}Invalid choice. Please enter a number between 1 and 4.{RESET}\n")
                        
                except ValueError as e:
                    print(f"{RED}Error: {str(e)}{RESET}\n")
                    
                    
            elif command == "clean":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: clean <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: clean my_dataset{RESET}")
                    print("\n")
                    continue
                
                dataset_name = args[0]
                print("\nSelect cleaning option:")
                print("1. Remove duplicates")
                print("2. Handle missing values")
                
                
                clean_choice = input("Enter your choice (1-2): ").strip()
                
                
                if clean_choice == "1":
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

                            print("\nWould you like to update the original dataset? (y/n)")
                            update_choice = input("> ").strip().lower()
                            if update_choice == 'y':
                                analysis_desc = f"Removed duplicates on columns: {', '.join(subset) if subset else 'all columns'}"
                                dataset_manager.update_dataset(dataset_name, cleaned_df, analysis_desc)
                                print(f"{GREEN}Dataset '{dataset_name}' updated successfully{RESET}")
                        print("\n")
                
                
                elif clean_choice == "2":
                    print("\nHandle missing values:")
                    print("1. Remove rows with missing values")
                    print("2. Fill missing values with mean (numerical columns)")
                    print("3. Fill missing values with mode (categorical columns)")

                    missing_choice = input("Enter your choice (1-3): ").strip()

                    if missing_choice == "1":
                        cleaned_df = data_explorer.remove_rows_with_missing(dataset_name)
                        
                        if cleaned_df is not None:
                            print(f"\n{GREEN}Rows with missing values dropped. Remaining rows: {len(cleaned_df)}{RESET}")
                            print(cleaned_df.head())


                            print("\nWould you like to update the original dataset? (y/n)")
                            update_choice = input("> ").strip().lower()
                            if update_choice == 'y':
                                analysis_desc = "Removed rows with missing values"
                                dataset_manager.update_dataset(dataset_name, cleaned_df, analysis_desc)
                                print(f"{GREEN}Dataset '{dataset_name}' updated successfully{RESET}")
                            print("\n")
                    
                    
                    elif missing_choice == "2":
                        cleaned_df = data_explorer.fill_missing_with_mean(dataset_name)
                        
                        if cleaned_df is not None:
                            print(f"\n{GREEN}Missing values in numeric columns filled with column mean.{RESET}")
                            print(cleaned_df.head())


                            print("\nWould you like to update the original dataset? (y/n)")
                            update_choice = input("> ").strip().lower()
                            if update_choice == 'y':
                                analysis_desc = "Filled missing values in numeric columns with mean"
                                dataset_manager.update_dataset(dataset_name, cleaned_df, analysis_desc)
                                print(f"{GREEN}Dataset '{dataset_name}' updated successfully{RESET}")
                            print("\n")
                    
                    
                    elif missing_choice == "3":
                        cleaned_df = data_explorer.fill_missing_with_mode(dataset_name)
                        
                        if cleaned_df is not None:
                            print(f"\n{GREEN}Missing values in categorical columns filled with column mode.{RESET}")
                            print(cleaned_df.head())

                            
                            print("\nWould you like to update the original dataset? (y/n)")
                            update_choice = input("> ").strip().lower()
                            if update_choice == 'y':
                                analysis_desc = "Filled missing values in categorical columns with mode"
                                dataset_manager.update_dataset(dataset_name, cleaned_df, analysis_desc)
                                print(f"{GREEN}Dataset '{dataset_name}' updated successfully{RESET}")
                            print("\n")
                    
                    else:
                        print(f"{RED}Invalid choice. Please enter a number between 1 and 3.{RESET}\n")
                    
            
            
                    
            elif command == "remove":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: remove <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: remove my_dataset{RESET}")
                    print("\n")
                    continue
                    
                dataset_name = args[0]
                print(dataset_name)

                if dataset_manager.remove_dataset(dataset_name):
                    print(f"{GREEN}Successfully removed the dataset: '{dataset_name}'\n{RESET}")
                    
            
            elif command == "report":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: report <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: report my_dataset{RESET}")
                    print("\n")
                    continue
                
                dataset_name = args[0]
                
                try:
                    
                    reporter = ReportCreator(dataset_manager, data_explorer)
                    report_path = reporter.generate_report(dataset_name)
                    
                    print(f"{GREEN}Report generated and saved to: {report_path}{RESET}")
                
                except Exception as e:
                    print(f"{RED}Error generating report: {str(e)}{RESET}")
            
            
            
            elif command == "visualize":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: visualize <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: visualize my_dataset{RESET}")
                    print("\n")
                    continue
                
                dataset_name = args[0]
                
                try:
                    visualizer = Visualizer(dataset_manager, data_explorer)
                    
                    print("\nSelect plot type:")
                    print("1. Histogram")
                    print("2. Bar Chart")
                    print("3. Heatmap")
                    print("4. Scatter Plot")
                    
                    choice = input("\nEnter your choice (1-4): ").strip()
                    
                    if choice == "1":
                        # Show available columns
                        metadata = dataset_manager.metadata.get(dataset_name, {})
                        columns = metadata.get("column_names", [])
                        print(f"\nAvailable columns: {', '.join(columns)}")
                        column_name = input("Enter the column name for the histogram: ").strip()
                        
                        # Validate column exists
                        if column_name not in columns:
                            print(f"Error: Column '{column_name}' not found in dataset. Please choose from the available columns.")
                            continue
                            
                        bins_input = input("Enter number of bins (default 30): ").strip()
                        bins = int(bins_input) if bins_input.isdigit() else 30
                        filepath = visualizer.create_histogram(dataset_name, column_name, bins)
                        filename = os.path.basename(filepath)
                        print(f"Histogram for '{column_name}' generated and saved as '{filename}'.")
                    
                    elif choice == "2":
                        # Show available columns
                        metadata = dataset_manager.metadata.get(dataset_name, {})
                        columns = metadata.get("column_names", [])
                        print(f"\nAvailable columns: {', '.join(columns)}")
                        column_name = input("Enter the column name for the bar chart: ").strip()
                        
                        # Validate column exists
                        if column_name not in columns:
                            print(f"Error: Column '{column_name}' not found in dataset. Please choose from the available columns.")
                            continue
                            
                        filepath = visualizer.create_bar_chart(dataset_name, column_name)
                        filename = os.path.basename(filepath)
                        print(f"Bar chart for '{column_name}' generated and saved as '{filename}'.")
                    
                    elif choice == "3":
                        filepath = visualizer.create_heatmap(dataset_name)
                        filename = os.path.basename(filepath)
                        print(f"Heatmap generated and saved as '{filename}'.")
                    
                    elif choice == "4":
                        # Scatter Plot
                        metadata = dataset_manager.metadata.get(dataset_name, {})
                        columns = metadata.get("column_names", [])
                        print(f"\nAvailable columns: {', '.join(columns)}")
                        x_column = input("Enter the column name for the x-axis: ").strip()
                        y_column = input("Enter the column name for the y-axis: ").strip()
                        
                        # Validate columns exist
                        if x_column not in columns or y_column not in columns:
                            print(f"Error: One or both columns not found in dataset. Please choose from the available columns.")
                            continue
                        
                        # Validate columns are numeric
                        df = dataset_manager.get_dataset(dataset_name)
                        if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
                            print(f"Error: Both columns must be numeric for a scatter plot.")
                            continue
                        
                        filepath = visualizer.create_scatter_plot(dataset_name, x_column, y_column)
                        filename = os.path.basename(filepath)
                        print(f"Scatter plot for '{y_column}' vs '{x_column}' generated and saved as '{filename}'.")
                    
                    else:
                        print(f"{RED}Invalid choice. Please enter a number between 1 and 4.{RESET}")
                
                except Exception as e:
                    print(f"{RED}Error creating plot: {str(e)}{RESET}")
            
            
            
            elif command == "model":
                if len(args) != 1:
                    print(f"{YELLOW}Usage: model <dataset_name>{RESET}")
                    print(f"{YELLOW}Example: model my_dataset{RESET}")
                    print("\n")
                    continue
                
                dataset_name = args[0]
                df = dataset_manager.get_dataset(dataset_name)
                
                if df is None:
                    print(f"{RED}Dataset '{dataset_name}' not found.{RESET}")
                    continue
                
                columns = list(df.columns)
                print("\nSelect modeling type:")
                print("1. Linear Regression")
                print("2. Classification (Logistic Regression)")
                print("3. Clustering (KMeans)")
                
                model_choice = input("Enter your choice (1-3): ").strip()
                
                
                
                if model_choice == "1":
                    print(f"\nAvailable columns: {', '.join(columns)}")
                    target = input("Enter target column: ").strip()
                    
                    if target not in columns:
                        print(f"{RED}Target column not found.{RESET}")
                        return
                    
                    features = input("Enter feature columns (comma-separated, or leave blank for all except target): ").strip()
                    
                    if features:
                        feature_cols = [c.strip() for c in features.split(',') if c.strip() and c.strip() != target] 
                    
                    else:
                        feature_cols = [c for c in columns if c != target]
                    
                    
                    
                    model_name = f"{dataset_name}_{target}_linreg"
                    model_instance = LinearRegressionModel()
                    model, score, X_test, y_test, y_pred = model_instance.train(df, feature_cols, target, model_name)
                    
                    
                    if model is not None:
                        print(f"{GREEN}Linear Regression model trained and saved as models/{model_name}.joblib{RESET}")
                        print(f"R^2 Score: {score:.4f}")
                
                
                
                elif model_choice == "2":
                    print(f"\nAvailable columns: {', '.join(columns)}")
                    target = input("Enter target column: ").strip()
                    
                    if target not in columns:
                        print(f"{RED}Target column not found.{RESET}")
                        return
                    
                    features = input("Enter feature columns (comma-separated, or leave blank for all except target): ").strip()
                    
                    if features:
                        feature_cols = [c.strip() for c in features.split(',') if c.strip() and c.strip() != target]
                    else:
                        feature_cols = [c for c in columns if c != target]
                    
                    
                    model_name = f"{dataset_name}_{target}_logreg"
                    model_instance = LogisticRegressionModel()
                    model, acc, prec, rec, f1, report, X_test, y_test, y_pred = model_instance.train(df, feature_cols, target, model_name)
                    
                    if model is not None:
                        print(f"{GREEN}Classification model trained and saved as models/{model_name}.joblib{RESET}")
                        print(f"Accuracy: {acc:.4f}\nPrecision: {prec:.4f}\nRecall: {rec:.4f}\nF1 Score: {f1:.4f}")
                        print(f"\nClassification Report:\n{report}")
                        
                        save_cm = input("Would you like to save a confusion matrix plot? (y/n): ").strip().lower()
                        
                        if save_cm == 'y':
                            cm_path = model_instance.save_confusion_matrix(y_test, y_pred, model_name)
                            print(f"Confusion matrix saved as {cm_path}")
                
                
                
                
                elif model_choice == "3":
                    print(f"\nAvailable columns: {', '.join(columns)}")
                    features = input("Enter feature columns for clustering (comma-separated): ").strip()
                    
                    if not features:
                        print(f"{RED}You must specify feature columns for clustering.{RESET}")
                        return
                    
                    feature_cols = [c.strip() for c in features.split(',') if c.strip()]
                    
                    n_clusters = input("Enter number of clusters (default 3): ").strip()
                    n_clusters = int(n_clusters) if n_clusters.isdigit() else 3
                    
                    
                    model_name = f"{dataset_name}_kmeans_{n_clusters}clusters"
                    model_instance = KMeansModel()
                    model, labels = model_instance.train(df, feature_cols, n_clusters, model_name)
                    
                    
                    if model is not None:
                        print(f"{GREEN}KMeans clustering model trained and saved as models/{model_name}.joblib{RESET}")
                        print(f"Cluster labels assigned. Example: {labels[:10]}")
                
                
                
                else:
                    print("Exiting modeling menu.")
                    continue

            
            
            
            elif command == "predict":
                # Use BaseModel directly since we only need list_models and load_model
                model_instance = BaseModel()
                models = model_instance.list_models()
                
                if not models:
                    print(f"{YELLOW}No trained models found. Please train a model first using the 'model' command.{RESET}")
                    continue
                
                print("\nAvailable models:")
                for idx, m in enumerate(models):
                    print(f"{idx+1}. {m}")
                model_choice = input("Enter the number of the model to use: ").strip()
                
                if not model_choice.isdigit():
                    print(f"{RED}Invalid input. Please enter a number corresponding to the model.{RESET}")
                    continue
                
                
                model_idx = int(model_choice) - 1
                if model_idx < 0 or model_idx >= len(models):
                    print(f"{RED}Invalid model selection.{RESET}")
                    continue
                
                model_file = models[model_idx]
                
                model = model_instance.load_model(model_file.replace('.joblib',''))
                
                if model is None:
                    print(f"{RED}Model file not found. Please check the model name or train a new model.{RESET}")
                    continue
                
                
                # Try to infer feature names from model or ask user
                print("Enter feature values for prediction:")
                
                # Try to get feature names from model (works for sklearn linear/logistic regression)
                feature_names = getattr(model, 'feature_names_in_', None)
                
                if feature_names is None:
                    n_features = int(input("Number of features required: ").strip())
                    feature_names = [input(f"Feature {i+1} name: ").strip() for i in range(n_features)]
                
                
                feature_values = []
                
                for fname in feature_names:
                    val = input(f"{fname}: ").strip()
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                    feature_values.append(val)
                
                X_input = np.array(feature_values).reshape(1, -1)
                
                try:
                    pred = model.predict(X_input)
                    print(f"\n\n{GREEN}Prediction: {pred[0]}{RESET}")
                except Exception as e:
                    print(f"{RED}Error making prediction: {str(e)}{RESET}")
                    
            else:
                print(f"{RED}Unknown command: {command}{RESET}")
                print(f"{YELLOW}Type 'help' to see all available commands{RESET}")
                print("\n")
                
        
        
        except Exception as e:
            print(f"{RED}Error: {str(e)}{RESET}")





if __name__ == "__main__":
    main() 