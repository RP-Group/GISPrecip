from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QTableWidgetItem
from qgis.core import QgsProject, QgsRasterLayer

import numpy as np

from netCDF4 import Dataset

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, mean_absolute_error
from scipy.stats import pearsonr
from imblearn.under_sampling import RandomUnderSampler

from scipy.interpolate import griddata

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .GIS_Precip_dialog import GISPrecipDialog
from .Model_utils import ModelUtils
from .TrainModel import TrainModel
from .TestModel import TestModel
import os.path
from pathlib import Path

class Assessment:

    # CALCULA AS METRICAS
    def get_model_metrics(self, y_true, y_pred):
        self.dlg.Log("Calculating model metrics...")

        bias = np.mean(y_pred - y_true)
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)

        def smape(y_true, y_pred):
            # return 100 * np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))
            return np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))

        smape_value = smape(y_true, y_pred)
        lin_corr = np.corrcoef(y_true, y_pred)[0, 1]

        self.dlg.Log("Model metrics calculated.")
        return bias, mse, mae, smape_value, lin_corr
