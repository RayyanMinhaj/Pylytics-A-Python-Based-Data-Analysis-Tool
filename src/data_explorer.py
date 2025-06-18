import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple

class DataExplorer:
    """
    A class to handle data exploration and analysis features.
    
    This class provides functionality for:
    - Computing summary statistics
    - Handling missing data
    - Getting frequency counts
    - Filtering data
    - Cleaning data (removing duplicates)
    """
    
    def __init__(self, dataset_manager):
        """
        Initialize DataExplorer with a dataset manager.

        """
        self.dataset_manager = dataset_manager
        

        
    def get_summary_statistics(self, dataset_name: str) -> Dict[str, Dict]:
        """
        Calculate summary statistics for numerical columns.
        
        Args:
            dataset_name: Name of the dataset to analyze
            
        Returns:
            Dictionary containing statistics for each numerical column
        """
        try:
            # Step 1: Get dataset from manager
            df = self.dataset_manager.get_dataset(dataset_name)
            if df is None:
                raise ValueError(f"Dataset '{dataset_name}' not found")
            
            # Step 2: Initialize results dictionary (dict of dicts)
            stats = {}
            
            # Step 3: Get numerical columns only
            numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
            
            # Step 4: Calculate statistics for each numerical column
            for col in numerical_cols:
                stats[col] = {
                    'count': int(df[col].count()),
                    'mean': round(float(df[col].mean()), 4),
                    'median': round(float(df[col].median()), 4),
                    'std': round(float(df[col].std()), 4),
                    'min': round(float(df[col].min()), 4),
                    '25%': round(float(df[col].quantile(0.25)), 4),
                    '50%': round(float(df[col].quantile(0.50)), 4),
                    '75%': round(float(df[col].quantile(0.75)), 4),
                    'max': round(float(df[col].max()), 4)
                }
            
            return stats
            
        except Exception as e:
            print(f"Error calculating summary statistics: {str(e)}")
            return {}
            
    
    def get_missing_data_info(self, dataset_name: str) -> Dict[str, Dict]:
        """
        Get information about missing values in the dataset.
        
        Args:
            dataset_name: Name of the dataset to analyze
            
        Returns:
            Dictionary containing missing value information for each column
        """
        try:
            # Step 1: Get dataset from manager
            df = self.dataset_manager.get_dataset(dataset_name)
            if df is None:
                raise ValueError(f"Dataset '{dataset_name}' not found")
            
            # Step 2: Initialize results dictionary
            missing_info = {} # dict of dicts
            total_rows = len(df)
            
            # Step 3: Calculate missing values for each column
            for column in df.columns:
                missing_count = df[column].isnull().sum()
                
                if missing_count > 0:  # Only include columns with missing values (you obviously wouldnt want to go through all the columns)
                    missing_info[column] = {
                        'count': int(missing_count),
                        'percentage': round(float(missing_count / total_rows * 100), 1)
                    }
            
            return missing_info
            
        except Exception as e:
            print(f"Error analyzing missing data: {str(e)}")
            return {}
            



            
    def get_frequency_counts(self, dataset_name: str) -> Dict[str, Dict]:
        """
        Get frequency counts for categorical columns.
        
        Args:
            dataset_name: Name of the dataset to analyze
            
        Returns:
            Dictionary containing value counts for each categorical column
        """
        try:
            # Step 1: Get dataset from manager
            df = self.dataset_manager.get_dataset(dataset_name)
            if df is None:
                raise ValueError(f"Dataset '{dataset_name}' not found")
            
            # Step 2: Initialize results dictionary
            freq_counts = {} # dict of dicts
            
            # Step 3: Get categorical columns (including object and category dtypes)
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
            # Step 4: Calculate frequency counts for each categorical column
            for col in categorical_cols:
                value_counts = df[col].value_counts() # Pandas function that counts how many times each unique value appears in a column.
                
                freq_counts[col] = {
                    'counts': value_counts.to_dict(),
                    'total_unique': len(value_counts)
                }
            
            return freq_counts
            
        except Exception as e:
            print(f"Error calculating frequency counts: {str(e)}")
            return {}





    def filter_dataset(self, dataset_name: str, condition: str) -> Optional[pd.DataFrame]:
        """
        Filter dataset based on a condition string.
        
        Args:
            dataset_name: Name of the dataset to filter
            condition: String condition (e.g., "age > 25 and country == 'USA'")
            
        Returns:
            Filtered DataFrame or None if error
        """
        try:
            # Step 1: Get dataset from manager
            df = self.dataset_manager.get_dataset(dataset_name)
            if df is None:
                raise ValueError(f"Dataset '{dataset_name}' not found")
            
            # Step 2: Apply the filter condition
            filtered_df = df.query(condition)
            
            # Step 3: Return None if no rows match the condition
            if len(filtered_df) == 0:
                print("No rows match the specified condition")
                return None
                
            return filtered_df
            
        except Exception as e:
            print(f"Error filtering dataset: {str(e)}")
            return None





    def clean_duplicates(self, dataset_name: str, subset: Optional[List[str]] = None) -> Tuple[Optional[pd.DataFrame], int]:
        """
        Remove duplicate rows from the dataset.
        
        Args:
            dataset_name: Name of the dataset to clean
            subset: Optional list of columns to consider for duplicates
            
        Returns:
            Tuple of (cleaned DataFrame, number of duplicates removed)
            or (None, 0) if error
        """
        try:
            # Step 1: Get dataset from manager
            df = self.dataset_manager.get_dataset(dataset_name)
            if df is None:
                raise ValueError(f"Dataset '{dataset_name}' not found")
            
            # Step 2: Get initial row count
            initial_count = len(df)
            
            # Step 3: Remove duplicates
            if subset:
                df_cleaned = df.drop_duplicates(subset=subset)
            else:
                df_cleaned = df.drop_duplicates()
            
            # Step 4: Calculate number of duplicates removed
            duplicates_removed = initial_count - len(df_cleaned)
            
            return df_cleaned, duplicates_removed
            
        except Exception as e:
            print(f"Error removing duplicates: {str(e)}")
            return None, 0



    def remove_rows_with_missing(self, dataset_name: str):
        """
        Remove rows with any missing values from the dataset.
        Args:
            dataset_name: Name of the dataset to clean
        Returns:
            DataFrame with rows containing missing values removed
        """
        # Step 1: Get dataset from manager
        df = self.dataset_manager.get_dataset(dataset_name)
        
        if df is None:
            print(f"Dataset '{dataset_name}' not found.")
            return None
        
        # Step 2: Remove rows with missing values
        return df.dropna()




    def fill_missing_with_mean(self, dataset_name: str):
        """
        Fill missing values in numerical columns with the mean of each column.
        Args:
            dataset_name: Name of the dataset to clean
        Returns:
            DataFrame with missing values in numerical columns filled with mean
        """
        
        # Step 1: Get dataset from manager
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            print(f"Dataset '{dataset_name}' not found.")
            return None
        
        # Step 2: Copy dataset
        cleaned_df = df.copy()
        
        # Step 3: Fill missing values with mean
        num_cols = cleaned_df.select_dtypes(include=['int64', 'float64']).columns
        
        for col in num_cols:
            mean_val = cleaned_df[col].mean()
            cleaned_df[col].fillna(mean_val, inplace=True)
        
        return cleaned_df

    
    
    
    
    
    def fill_missing_with_mode(self, dataset_name: str):
        """
        Fill missing values in categorical columns with the mode (most frequent value).
        Args:
            dataset_name: Name of the dataset to clean
        Returns:
            DataFrame with missing values in categorical columns filled with mode
        """
        
        # Step 1: Get dataset from manager
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            print(f"Dataset '{dataset_name}' not found.")
            return None
        
        # Step 2: Copy dataset
        cleaned_df = df.copy()
        
        # Step 3: Fill missing values with mode
        cat_cols = cleaned_df.select_dtypes(include=['object', 'category']).columns
        
        for col in cat_cols:
            mode_val = cleaned_df[col].mode(dropna=True)
            
            if not mode_val.empty:
                cleaned_df[col].fillna(mode_val[0], inplace=True)
        
        return cleaned_df 