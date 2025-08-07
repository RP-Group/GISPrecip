from qgis.core import QgsProject, QgsRasterLayer

import numpy as np

from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler

import os.path

"""

    FUNCOES QUE FAZEM PARTE DA CLASSE MODEL

"""

class ModelUtils:

    # INICIA O PLUGIN (UI)
    def initGui(self):
        icon_path = ':/plugins/GIS_Precip/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GIS Precip'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.first_start = True


    # REMOVE DA INTERFACE DO QGIS TODOS OS ELEMENTOS
    # QUE O PLUGIN ADICIONOU AO SER CARREGADO.
    def unload(self):
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&GISPrecip'),
                action)
            self.iface.removeToolBarIcon(action)

    # PEGA OS LAYERS
    def get_layer_by_name(self, layer_name, idx=0):
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            return layers[idx]
        else:
            return None

    # PEGA O DIRETORIO DO PROJETO
    def get_project_or_working_directory(self):
        project = QgsProject.instance()

        project_filepath = project.fileName()

        if project_filepath:
            project_directory = os.path.dirname(project_filepath)
        else:
            project_directory = os.getcwd()
        return project_directory

    # PEGA A LON/LAT DO LAYER
    def get_long_lat(self, layer):

        self.dlg.Log("Extracting longitude and latitude from layer: {}".format(layer.name()))

        # Assuming the layer has a CRS with geographic coordinates
        crs = layer.crs()
        if crs.isGeographic():
            extent = layer.extent()
            long = np.linspace(extent.xMinimum(), extent.xMaximum(), layer.width())
            lat = np.linspace(extent.yMinimum(), extent.yMaximum(), layer.height())
            self.dlg.Log("Longitude and latitude extracted successfully.")
            return long, lat
        else:
            self.dlg.Log("Layer CRS is not geographic. Cannot extract longitude and latitude.")
            return None, None




    # PRE-PROCESSA OS DADOS DO GMI E TARGET

    def preprocess_GMI_data(self, gmi_data, long, lat, normalize=True):
        """Preprocess the GMI and surface precipitation data."""
        self.dlg.Log("Preprocessing GMI data...")

        # Check if the data is valid
        mask = np.isfinite(gmi_data).all(axis=1)
        # Check if the data is masked
        if np.ma.isMaskedArray(gmi_data):
            mask &= ~np.ma.getmaskarray(gmi_data).any(axis=1)
        # Remove invalid samples
        gmi_data = gmi_data[mask]
        long = long[mask]
        lat = lat[mask]

        if normalize:
            # Normalize the GMI data
            scaler = StandardScaler()
            # gmi_data = self.scaler.fit_transform(gmi_data)
            gmi_data = scaler.fit_transform(gmi_data)

        self.dlg.Log("Data preprocessing completed.")
        return gmi_data, long, lat








