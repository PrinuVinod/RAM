# RAM (Resource Allocation Manager)

## Project Overview

RAM is a framework designed to evaluate the severity of disasters in specific regions and optimize the distribution of ration supplies. This project focuses on the Kuttanad area and flood scenarios.

## Directory Structure

- `data/`: Contains geographical and historical data.
- `scripts/`: Python scripts for data collection, processing, impact assessment, and resource allocation.
- `notebooks/`: Jupyter notebooks for interactive analysis.
- `README.md`: Project documentation.
- `requirements.txt`: List of required Python packages.

## How to Run

1. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the scripts in the following order:

    ```bash
    python scripts/data_collection.py
    python scripts/data_processing.py
    python scripts/impact_assessment.py
    python scripts/resource_allocation.py
    ```

3. For interactive analysis, open the Jupyter notebook:

    ```bash
    jupyter notebook notebooks/RAM_analysis.ipynb
    ```

## Dependencies

- pandas
- geopandas
- requests
