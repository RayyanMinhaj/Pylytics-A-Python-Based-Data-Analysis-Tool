import os
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple


class DatasetManager:
    """
    A class to manage datasets in the PyLytics tool.
    
    This class handles:
    - Loading datasets from CSV files
    - Storing datasets in organized folders
    - Managing dataset metadata - v v important since well be using it for stats, and tracking modifications!!
    - Viewing dataset information
    - Removing datasets
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Args:
            data_dir (str): Directory where datasets will be stored
        """
        # Set up the data directory path
        self.data_dir = Path(data_dir)
        
        # Dictionary to store loaded datasets in memory
        self.datasets: Dict[str, pd.DataFrame] = {}
        
        # Path to the metadata file
        self.metadata_file = self.data_dir / "metadata.json"
        
        # Create data directory and load metadata
        self._ensure_data_dir()
        self._load_metadata()

    def _ensure_data_dir(self) -> None:
        """Create the data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _load_metadata(self) -> None:
        """
        Load dataset metadata from JSON file.
        If metadata file doesn't exist, create an empty one.
        """
        # Try to load existing metadata
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            # Create new metadata if file doesn't exist
            self.metadata = {}
            self._save_metadata()

    def _save_metadata(self) -> None:
        """Save the current metadata to a JSON file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def load_dataset(self, file_path: str, dataset_name: str) -> bool:
        """
        Load a dataset from a CSV file and store it in the system.
        
        Steps:
        1. Check if dataset name is already in use
        2. Read the CSV file
        3. Create a directory for the dataset
        4. Save the dataset
        5. Update metadata
        
        Args:
            file_path (str): Path to the CSV file
            dataset_name (str): Name to assign to the dataset
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Check if dataset name is already in use
            if dataset_name in self.datasets:
                raise ValueError(f"Dataset name '{dataset_name}' already exists")

            # Step 2: Read the CSV file
            df = pd.read_csv(file_path)
            
            # Step 3: Store dataset in memory
            self.datasets[dataset_name] = df # Eemember this is a dictionary, where key is the dataset name and value is the dataframe
            
            # Step 4: Create dataset directory
            dataset_dir = self.data_dir / dataset_name
            dataset_dir.mkdir(exist_ok=True)
            
            # Step 5: Save dataset to file
            output_path = dataset_dir / f"{dataset_name}.csv"
            df.to_csv(output_path, index=False)
            
            # Step 6: Update metadata with dataset information
            self.metadata[dataset_name] = {
                "file_path": str(output_path),
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "last_modified": pd.Timestamp.now().isoformat()
            }
            self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            return False

    def list_datasets(self) -> List[Tuple[str, Dict]]:
        """
        Get a list of all loaded datasets with their metadata.
        
        Returns:
            List[Tuple[str, Dict]]: List of (dataset_name, metadata) pairs
        """
        # Eempty list to store dataset information
        dataset_list = []
        
        # Iterate through each dataset in metadata
        for name, info in self.metadata.items():
            # Add tuple of (dataset_name, metadata) to the list
            dataset_list.append((name, info))
            
        return dataset_list

    def view_dataset(self, dataset_name: str, n_rows: int = 5) -> Optional[pd.DataFrame]:
        """
        View the first N rows of a dataset.
        
        Args:
            dataset_name (str): Name of the dataset to view
            n_rows (int): Number of rows to display (default: 5)
            
        Returns:
            Optional[pd.DataFrame]: First N rows of the dataset, or None if not found
        """
        # Check if dataset exists in metadata
        if dataset_name not in self.metadata:
            print(f"Dataset '{dataset_name}' not found")
            return None
            
        # If dataset is not in memory, load it from disk
        if dataset_name not in self.datasets:
            try:
                file_path = self.metadata[dataset_name]["file_path"]
                self.datasets[dataset_name] = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error loading dataset from disk: {str(e)}")
                return None
            
        # Return first N rows
        return self.datasets[dataset_name].head(n_rows)

    def remove_dataset(self, dataset_name: str) -> bool:
        """
        Remove a dataset from the system.
        
        Steps:
        1. Check if dataset exists
        2. Remove from memory
        3. Delete dataset files
        4. Update metadata
        
        Args:
            dataset_name (str): Name of the dataset to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Check if dataset exists
            if dataset_name not in self.datasets:
                raise ValueError(f"Dataset '{dataset_name}' not found")
                
            # Step 2: Remove from memory
            del self.datasets[dataset_name] 
            
            # Step 3: Remove dataset files
            dataset_dir = self.data_dir / dataset_name
            if dataset_dir.exists():
                # Delete all files in the dataset directory
                for file in dataset_dir.iterdir():
                    os.remove(file)
                # Remove the empty directory
                dataset_dir.rmdir()
            
            # Step 4: Update metadata
            del self.metadata[dataset_name]
            self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Error removing dataset: {str(e)}")
            return False 