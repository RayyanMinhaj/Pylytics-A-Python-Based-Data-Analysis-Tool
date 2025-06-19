import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from pathlib import Path
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder

class Visualizer:
    def __init__(self, dataset_manager, data_explorer, graphs_dir="graphs"):
        """
        Initialize the Visualizer with dataset manager and data explorer.
        
        Args:
            dataset_manager: Instance of DatasetManager
            data_explorer: Instance of DataExplorer
            graphs_dir: Directory to save generated plots
        """
        self.dataset_manager = dataset_manager
        self.data_explorer = data_explorer
        self.graphs_dir = graphs_dir
        
        Path(self.graphs_dir).mkdir(parents=True, exist_ok=True)
        
        # Set style for better-looking plots
        plt.style.use('default')
        sns.set_palette("husl")

    
    def create_histogram(self, dataset_name: str, column_name: str, bins: int = 30) -> str:
        """
        Create a histogram for a numerical column.
        
        Args:
            dataset_name: Name of the dataset
            column_name: Name of the numerical column
            bins: Number of bins for the histogram
            
        Returns:
            str: Path to the saved plot file
        """
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
            
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataset")
            
        # Check if column is numerical
        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numerical")
        
        plt.figure(figsize=(10, 6))
        plt.hist(df[column_name].dropna(), bins=bins, edgecolor='black', alpha=0.7)
        plt.title(f'Histogram of {column_name} in {dataset_name}')
        plt.xlabel(column_name)
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        # Save plot
        filename = f"{dataset_name}_{column_name}_histogram.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    
    
    def create_bar_chart(self, dataset_name: str, column_name: str, top_n: int = 10) -> str:
        """
        Create a bar chart for a categorical column.
        
        Args:
            dataset_name: Name of the dataset
            column_name: Name of the categorical column
            top_n: Number of top categories to show
            
        Returns:
            str: Path to the saved plot file
        """
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
            
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataset")
        
        # Check if column is categorical
        if not (pd.api.types.is_categorical_dtype(df[column_name])) or (pd.api.types.is_object_dtype(df[column_name])):
            raise ValueError(f"Warning: Column '{column_name}' appears to be numeric. Bar charts work best with categorical data!")
        
        
        # Get value counts
        value_counts = df[column_name].value_counts().head(top_n)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(value_counts)), value_counts.values, alpha=0.7)
        plt.title(f'Top {top_n} Categories in {column_name} ({dataset_name})')
        plt.xlabel('Categories')
        plt.ylabel('Count')
        plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save plot
        filename = f"{dataset_name}_{column_name}_barchart.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    
    
    
    def create_heatmap(self, dataset_name: str, columns: Optional[List[str]] = None) -> str:
        """
        Create a correlation heatmap for numerical and categorical columns.
        Categorical columns are automatically encoded using label encoding.
        
        Args:
            dataset_name: Name of the dataset
            columns: List of columns to include (if None, uses all columns)
            
        Returns:
            str: Path to the saved plot file
        """
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        # Create a copy for encoding
        df_encoded = df.copy()
        
        # Get columns to use
        if columns is None:
            columns_to_use = df.columns.tolist()
        else:
            columns_to_use = [col for col in columns if col in df.columns]
        
        if len(columns_to_use) < 2:
            raise ValueError("Need at least 2 columns for correlation heatmap")
        
        # Apply label encoding to categorical columns
        le = LabelEncoder()
        
        for col in columns_to_use:
            if df_encoded[col].dtype == 'object' or df_encoded[col].dtype.name == 'category':
                # Handle missing values before encoding
                df_encoded[col] = df_encoded[col].fillna('Missing')
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        
        # Calculate correlation matrix
        corr_matrix = df_encoded[columns_to_use].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.2f')
        plt.title(f'Correlation Heatmap for {dataset_name}\n(Categorical columns encoded)')
        plt.tight_layout()
        
        # Save plot
        filename = f"{dataset_name}_correlation_heatmap.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath

    
    
    
    def create_scatter_plot(self, dataset_name: str, x_column: str, y_column: str) -> str:
        """
        Create a scatter plot for two numerical columns.
        
        Args:
            dataset_name: Name of the dataset
            x_column: Name of the column for the x-axis
            y_column: Name of the column for the y-axis
        Returns:
            str: Path to the saved plot file
        """
        df = self.dataset_manager.get_dataset(dataset_name)
        if df is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError(f"One or both columns '{x_column}', '{y_column}' not found in dataset")
        
        if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
            raise ValueError(f"Both columns must be numeric for a scatter plot")
        
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_column], df[y_column], alpha=0.7)
        plt.title(f'Scatter Plot of {y_column} vs {x_column} in {dataset_name}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot
        filename = f"{dataset_name}_{y_column}_vs_{x_column}_scatter.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath 