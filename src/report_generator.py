import os
from pathlib import Path
from typing import Any


def generate_report(dataset_manager, data_explorer, dataset_name: str, reports_dir: str = "reports") -> str:
    """
    Generate a detailed analysis report for a dataset and save it as a text file.
    
    Args:
        dataset_manager: Instance of DatasetManager
        data_explorer: Instance of DataExplorer
        dataset_name (str): Name of the dataset
        reports_dir (str): Directory to save the report
    
    Returns:
        str: Path to the saved report file

    """

    # Step 1: Ensure reports directory exists
    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    
    # Step 2: Get dataset and metadata
    df = dataset_manager.get_dataset(dataset_name)
    metadata = dataset_manager.metadata.get(dataset_name, {})
    
    if df is None or not metadata:
        raise ValueError(f"Dataset '{dataset_name}' not found.")
    
    # Step 3: Header
    lines = []
    lines.append("================================================")
    lines.append("PyLytics Data Analysis Report")
    lines.append("================================================\n")
    


    # Step 4: Dataset Overview
    lines.append("\nDATASET OVERVIEW:")
    lines.append("------------------------------------------------")
    lines.append(f"  Name: {dataset_name}")
    lines.append(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    lines.append(f"  Last Modified: {metadata.get('last_modified', 'N/A')}")
    lines.append("")



    # Step 5: Column Information
    lines.append("\n\nCOLUMN INFORMATION:")
    lines.append("-" * 58)
    lines.append(f"{'Column Name':<25} {'Type':<15} {'Missing Values':<15}")
    lines.append("-" * 58)
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        lines.append(f"{col:<25} {dtype:<15} {missing:<15}")
    lines.append("")



    # Step 5.5: Missing Values Summary this is incooreect ir should pivk from metadata
    lines.append("\nMISSING VALUES SUMMARY:")
    lines.append("-" * 70)
    lines.append(f"{'Column Name':<25} {'Type':<15} {'Missing':<10} {'% Missing':<10}")
    lines.append("-" * 70)
    total_rows = len(df)
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        percent = (missing / total_rows * 100) if total_rows > 0 else 0
        lines.append(f"{col:<25} {dtype:<15} {missing:<10} {percent:<10.2f}")
    lines.append("")




    # Step 6: Numerical Columns Summary
    num_stats = data_explorer.get_summary_statistics(dataset_name)
    if num_stats:
        lines.append("\n\nNUMERICAL COLUMNS SUMMARY:")
        lines.append("-" * 115)
        stat_names = list(next(iter(num_stats.values())).keys())
        lines.append(f"{'Column Name':<20} " + " ".join([f"{stat:<10}" for stat in stat_names]))
        lines.append("-" * 115)
        for col, stats in num_stats.items():
            lines.append(f"{col:<20} " + " ".join([f"{str(stats[stat]):<10}" for stat in stat_names]))
        lines.append("")


    
    # Step 7: Categorical Columns Summary
    cat_stats = data_explorer.get_frequency_counts(dataset_name)
    if cat_stats:
        lines.append("\n\nCATEGORICAL COLUMNS SUMMARY:")
        lines.append("------------------------------------------------")
        for col, info in cat_stats.items():
            lines.append(f"  {col} (unique: {info['total_unique']}):")
            for value, count in info['counts'].items():
                lines.append(f"    {value}: {count}")
            lines.append("")
    
    
    
    
    # Step 8: Analyses Performed
    analyses = metadata.get("analyses_performed", [])
    lines.append("\n\nANALYSES PERFORMED:")
    lines.append("------------------------------------------------")
    if analyses:
        for desc in analyses:
            lines.append(f"  - {desc}")
    else:
        lines.append("  None recorded.")
    lines.append("")
    
    

    
    # Step 9: End of file
    lines.append("======================= End of Report =======================")
    


    # Step 10: Write to file
    report_path = os.path.join(reports_dir, f"{dataset_name}_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    return report_path 