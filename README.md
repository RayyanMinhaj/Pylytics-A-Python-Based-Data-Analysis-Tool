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
    |   └── report_generator.py           #Generates a summary report for dataset
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
- `analyze <dataset_name>` - Interactive data analysis (summary stats, missing data, frequency counts, filtering)
- `clean <dataset_name>` - Data cleaning (remove duplicates, handle missing values)
- `help` - List all available commands
- `exit` - Exit the program
- `report <dataset_name>` - Generate a detailed analysis report for a dataset
- `visualize <dataset_name>` - Interactive visualization menu (histogram, bar chart, heatmap, scatter plot)
---

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

---



## Example - Filtering and Cleaning a Dataset

1. **Filter a dataset:**
You can filter your dataset using custom conditions (similar to pandas query syntax).  

```
pylytics> analyze my_dataset
Select analysis type:
...
4. Filter data

Enter your choice (1-5): 4
Enter filter condition (e.g., age > 25 and country == "USA"):
> sepal_length > 5.0
```

2. **Clean duplicates:**
```
pylytics> analyze my_dataset
Select analysis type:
...
5. Clean duplicates

Enter your choice (1-5): 5
Specify columns for duplicate check (leave empty for all columns):
Enter column names separated by comma:
> 
```

---

## Example - Generating a Report

1. Generate a report for a dataset:
```
pylytics> report my_dataset
Report generated and saved to: reports/my_dataset_report.txt
```
The report includes:
- Dataset overview (shape, last modified)
- Column information (types, missing values)
- Missing values summary
- Numerical columns summary (all statistics)
- Categorical columns summary (frequency counts)
- Analyses performed (filtering, cleaning, etc.)
- End of file marker

---

## Example - Visualization

1. Visualize your data:
```
pylytics> visualize my_dataset

Select plot type:
1. Histogram
2. Bar Chart
3. Heatmap
4. Scatter Plot

Enter your choice (1-4): 4

Available columns: sepal_length, sepal_width, petal_length, petal_width
Enter the column name for the x-axis: sepal_length
Enter the column name for the y-axis: petal_width
Scatter plot for 'petal_width' vs 'sepal_length' generated and saved as 'my_dataset_petal_width_vs_sepal_length_scatter.png'.
```

**Visualization Options:**
- **Histogram:** For a single numeric column. Prompts for number of bins.
- **Bar Chart:** For a single categorical column. Shows top categories.
- **Heatmap:** Correlation heatmap for all columns (categorical columns are encoded automatically).
- **Scatter Plot:** For two numeric columns. Prompts for x and y columns.

---