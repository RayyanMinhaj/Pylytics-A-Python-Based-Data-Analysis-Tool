# PyLytics - A Python-Based Data Analysis Tool

PyLytics is a lightweight CLI tool to manage, explore, and visualize CSV datasets with ease, all from your terminal!


## Folder Structure
```
PyLytics/
    ├── data/          #Stores the dataset files
    |   ├── dataset1/    #Stores dataset1 data (CSV etc)
    |   |   └── data_1.csv
    |   └── dataset2/    #Stores dataset2 data (CSV etc)
    |       └── data_2.csv
    ├── reports/       # Stores generated reports (text, CSV, images)
    ├── src/          #Stores the main Python source code
    |   ├── dataset_manager.py  #Class for dataset management
    |   ├── data_explorer.py    #Core functions for data exploration and analysis
    |   ├── visualizer.py       #Core functions for visualisation
    |   ├── main.py             #Command-line interface logic
    |   └── utils.py           #Utility functions (e.g., loading/saving data)
    ├── tests/        #Will work on it if time allows
    ├── config/     
    |   └── config.json  
    ├── README.md      
    └── requirements.txt 
```

## How to Run PyLytics!

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Pylytics.git
cd Pylytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the Program:
```bash
python src/main.py
```

### Available Commands (for now!)

- `load <file_path> <dataset_name>` - Load a dataset (CSV file)
- `list` - List all loaded datasets
- `view <dataset_name> [n_rows]` - View first N rows of a dataset
- `remove <dataset_name>` - Remove a dataset from memory
- `help` - List all available commands
- `exit` - Exit the program

### Example - Loading a Dataset

1. Load a dataset:
```
pylytics> load C:\Users\user\Downloads\Iris.csv my_dataset
```

2. List loaded datasets:
```
pylytics> list
```

3. View dataset contents:
```
pylytics> view my_dataset 10
```

4. Remove a dataset:
```
pylytics> remove my_dataset
```
