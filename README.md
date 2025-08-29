<div displey="flex" align="center">
<img width="25%" alt="icon" src="https://github.com/user-attachments/assets/4c9a170c-e749-483c-902f-0a447a4a4d29" />

# GISPrecip - Precipitation Classification and Estimation

</div>

This repository contains the source code for a **QGIS Plugin** that focuses on **Precipitation Classification and Estimation**. The plugin enables users to classify precipitation data, estimate precipitation events, and visualize these data within the QGIS environment. The plugin provides an interactive tool to analyze precipitation data and proposes the development of a plugin that combines regression and classification for precipitation estimation and classification, integrating satellite and radar data into a single workflow. It provides evaluation and visualization capabilities directly within QGIS, promoting greater accessibility and speed in conducting meteorological studies.

## Features

- **Precipitation Classification:** Classifies precipitation data using classifications models.
- **Precipitation Estimation:** Estimates precipitation events using regressions models.
- **Interactive Data Visualization:** Visualizes precipitation data in QGIS for better analysis and decision-making.

## Technologies Required

This plugin is built using the following technologies:

- **QGIS:** The plugin is designed to be used within QGIS, an open-source GIS application.
- **Python:** The plugin is developed in Python, leveraging QGIS's Python API (PyQGIS) for integration.

## Installation

To install and use the plugin, follow these steps:

### 1. Clone the repository

```bash
git clone git@github.com:RP-Group/GISPrecip.git
```

### 2. Compress the folder

Compress plugin folder to zip.


### 3. Virtual environment and dependencies in QGIS

1. Create a virtual enviroment and install the dependencies
```bash
    python3 -m venv GISPrecip
    source GISPrecip/bin/activate
    pip install scikit-learn numpy netCDF4 scipy imbalanced-learn
```

2. Open the python console in QGIS and open the editor.
<img width="750"  alt="Screenshot from 2025-08-29 06-13-59" src="https://github.com/user-attachments/assets/3cc43d74-a27a-4056-b67c-e779d41997cb" />

<img width="750" alt="Screenshot from 2025-08-29 06-15-02" src="https://github.com/user-attachments/assets/b14e9ecb-b607-4172-a79b-7c13dc8131bf" />

3. Open the requirements.py file, update the venv path and run.

<img width="750" alt="Screenshot from 2025-08-29 06-52-29" src="https://github.com/user-attachments/assets/410fe239-356c-4b2f-9ff1-d1864c31b323" />


Wait for the "Packages installed added" message.

### 4. Load the Plugin in QGIS

1. Open QGIS and go to the **Plugins** menu.
2. Select **Manage and Install Plugins**.

<img width="750" height="213" alt="Screenshot from 2025-08-29 06-53-31" src="https://github.com/user-attachments/assets/4819c005-ce14-4c46-896c-625cf2f159c1" />

3. Choose the **Install from ZIP** option and browse to the folder where the plugin was cloned.

<img width="750" height="312" alt="Screenshot from 2025-08-29 06-54-04" src="https://github.com/user-attachments/assets/1d4cc35a-bffb-4cf0-8744-0380c200d499" />

4. Select the plugin directory and install it.

<img width="750" height="192" alt="Screenshot from 2025-08-29 06-55-26" src="https://github.com/user-attachments/assets/91b5b900-5b77-4ea3-a13e-f20258f70515" />



### 5. Start Using the Plugin

Once the plugin is installed, you can launch it:

The plugin interface will open, and you can start analyzing precipitation data.

## User Manual

Documentation
