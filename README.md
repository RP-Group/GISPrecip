
# GISPrecip - Precipitation Classification and Estimation

## Overview

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

1. Create a virtual enviroment and install the dependencis
```bash
    python3 -m venv GISPrecip
    source GISPrecip/bin/activate
    pip install scikit-learn numpy netCDF4 scipy imbalanced-learn
```

2. Open the python console in QGIS and open the editor.

3. Open the requirements.py file, update the venv path and run

Wait for the "Packages installed added" message

### 4. Load the Plugin in QGIS

1. Open QGIS and go to the **Plugins** menu.
2. Select **Manage and Install Plugins**.
3. Choose the **Install from ZIP** option and browse to the folder where the plugin was cloned.
4. Select the plugin directory and install it.

### 5. Start Using the Plugin

Once the plugin is installed, you can launch it:

The plugin interface will open, and you can start analyzing precipitation data.

## User Manual

Documentation
