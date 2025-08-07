from qgis.core import QgsProject, QgsRasterLayer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPRegressor

import os.path


"""

    CLASSE PARA TREINAMENTO E PREDICAO DO MODELO

"""

class TrainModel:

    # PRE-PROCESSAMENTO DOS DADOS DO LAYER GMI (FEATURES)
    def get_gmi_data(self, gmi_layer):
        self.dlg.Log("Preprocessing GMI data layer: {}".format(gmi_layer.name()))

        mask = True
        arr = gmi_layer.as_numpy(mask)  # 13 bands, size is (bands, lat, long) -> (bands, width, height)
        long, lat = self.get_long_lat(gmi_layer)

        # Create a grid of coordinates
        long_coords, lat_coords = np.meshgrid(lat, long, indexing='ij')

        # Flatten everything
        long_flat = long_coords.flatten()
        lat_flat = lat_coords.flatten()
        data_flat = arr.reshape(13, -1).T  # shape (width*height, bands)

        # # Concatenate
        # output = np.column_stack((x_flat, y_flat, data_flat))  # shape (width*height, (long,lat,bands))

        self.dlg.Log("GMI data preprocessing completed for layer: {}".format(gmi_layer.name()))
        return data_flat, long_flat, lat_flat

    # CAPTURA OS DADOS DO LAYER SURFACE PRECIPITATION (TARGET)
    def get_surf_precip_data(self, surf_precip_layer):
        self.dlg.Log("Preprocessing surface precipitation data layer: {}".format(surf_precip_layer.name()))

        mask = True
        arr = surf_precip_layer.as_numpy(mask) # size is (surface_precip, lat, long) -> (surface_precip, width, height)
        long, lat = self.get_long_lat(surf_precip_layer)

        # Create a grid of coordinates
        long_coords, lat_coords = np.meshgrid(lat, long, indexing='ij')

        # Flatten everything
        long_flat = long_coords.flatten()
        lat_flat = lat_coords.flatten()
        data_flat = arr.reshape(1, -1).T  # shape (width*height, surface_precip)

        # # Concatenate
        # output = np.column_stack((x_flat, y_flat, data_flat))  # shape (width*height, (long,lat,surface_precip))

        self.dlg.Log("Surface precipitation data preprocessing completed for layer: {}".format(surf_precip_layer.name()))
        return data_flat, long_flat, lat_flat


    # CONVERTE OS DADOS PARA BINARIO COM LIMIAR (NO RAIN/RAIN)
    def preprocess_data_classifier(self, gmi_data, surf_precip_data, long, lat, normalize=True, under_sample=False):
        self.dlg.Log("Preprocessing GMI and surface precipitation data...")

        # Check if the data is valid
        mask = np.isfinite(gmi_data).all(axis=1) & np.isfinite(surf_precip_data).flatten()
        # Check if the data is masked
        if np.ma.isMaskedArray(gmi_data):
            mask &= ~np.ma.getmaskarray(gmi_data).any(axis=1)
        if np.ma.isMaskedArray(surf_precip_data):
            mask &= ~np.ma.getmaskarray(surf_precip_data).flatten()
        # Remove invalid samples
        gmi_data = gmi_data[mask]
        surf_precip_data = surf_precip_data[mask]
        long = long[mask]
        lat = lat[mask]

        # Convert precipitation to binary label (rain/no rain)
        surf_precip_data = (surf_precip_data > 0.1).astype(int)  # 0 = no rain, 1 = rain

        if normalize:
            # Normalize the GMI data
            scaler = StandardScaler()
            # gmi_data = self.scaler.fit_transform(gmi_data)
            gmi_data = scaler.fit_transform(gmi_data)

        if under_sample:
            gmi_data, surf_precip_data = RandomUnderSampler(random_state=42).fit_resample(gmi_data, surf_precip_data)

        self.dlg.Log("Data preprocessing completed.")
        return gmi_data, surf_precip_data, long, lat

    # CONVERTE OS DADOS PARA BINARIO COM LIMIAR (NO RAIN/RAIN)
    def preprocess_data_classifier(self, gmi_data, surf_precip_data, long, lat, normalize=True, under_sample=False):
        self.dlg.Log("Preprocessing GMI and surface precipitation data...")

        # Check if the data is valid
        mask = np.isfinite(gmi_data).all(axis=1) & np.isfinite(surf_precip_data).flatten()
        # Check if the data is masked
        if np.ma.isMaskedArray(gmi_data):
            mask &= ~np.ma.getmaskarray(gmi_data).any(axis=1)
        if np.ma.isMaskedArray(surf_precip_data):
            mask &= ~np.ma.getmaskarray(surf_precip_data).flatten()
        # Remove invalid samples
        gmi_data = gmi_data[mask]
        surf_precip_data = surf_precip_data[mask]
        long = long[mask]
        lat = lat[mask]

        # Convert precipitation to binary label (rain/no rain)
        surf_precip_data = (surf_precip_data > 0.1).astype(int)  # 0 = no rain, 1 = rain

        if normalize:
            # Normalize the GMI data
            scaler = StandardScaler()
            # gmi_data = self.scaler.fit_transform(gmi_data)
            gmi_data = scaler.fit_transform(gmi_data)

        if under_sample:
            gmi_data, surf_precip_data = RandomUnderSampler(random_state=42).fit_resample(gmi_data,
                                                                                          surf_precip_data)

        self.dlg.Log("Data preprocessing completed.")
        return gmi_data, surf_precip_data, long, lat

    def train_model_classifier(self):
        self.dlg.Log("Training model with selected GMI and Surface Precipitation data...")

        layers = QgsProject.instance().layerTreeRoot().children()

        checkedLayers_GMI = self.dlg.comboBox_InputGMI.checkedItems()
        selectedLayer_GMI = self.get_layer_by_name(checkedLayers_GMI[0])
        bands, long, lat = self.get_gmi_data(selectedLayer_GMI)

        checkedLayers_SurfPrecip = self.dlg.comboBox_InputSurfPrecip.checkedItems()
        selectedLayer_SurfPrecip = self.get_layer_by_name(checkedLayers_SurfPrecip[0])
        surfPrecip, long, lat = self.get_surf_precip_data(selectedLayer_SurfPrecip)

        # Preprocess the data
        bands, surfPrecip, long, lat = self.preprocess_data(bands, surfPrecip, long, lat, normalize=True, under_sample=True)

        # Create and train the SVM model
        model_name = self.dlg.comboBox_InputModel.currentText()
        if model_name == "SVM":
            self.model = SVC(kernel='rbf', C=100, gamma='scale', class_weight='balanced')  # use balanced weights if rain is rare
        elif model_name == "Random Forest":
            self.model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
        elif model_name == "Decision Tree":
            self.model = DecisionTreeClassifier(class_weight='balanced')
        elif model_name == "AdaBoost":
            self.model = AdaBoostClassifier(n_estimators=100, random_state=42)
        elif model_name == "MLP Regressor":
            self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        self.model.fit(bands, surfPrecip)

        # Log the training completion
        self.dlg.progressBar_TrainModel.setValue(100)
        self.dlg.Log("Model training completed.")


    def train_model_regressor(self):
        self.dlg.Log("Training model with selected GMI and Surface Precipitation data...")

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # write feature attributes
        checkedLayers_GMI = self.dlg.comboBox_InputGMI.checkedItems()
        selectedLayer_GMI = self.get_layer_by_name(checkedLayers_GMI[0])
        bands, long, lat = self.get_gmi_data(selectedLayer_GMI)

        # Assuming the surface precipitation layer is selected
        checkedLayers_SurfPrecip = self.dlg.comboBox_InputSurfPrecip.checkedItems()
        selectedLayer_SurfPrecip = self.get_layer_by_name(checkedLayers_SurfPrecip[0])
        surfPrecip, long, lat = self.get_surf_precip_data(selectedLayer_SurfPrecip)

        # Preprocess the data
        bands, surfPrecip, long, lat = self.preprocess_data_regressor(bands, surfPrecip, long, lat, normalize=True, under_sample=True)

        # Create and train the SVM model
        model_name = self.dlg.comboBox_InputModel.currentText()
        if model_name == "MLP Regressor":
            self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        self.model.fit(bands, surfPrecip)

        # Log the training completion
        self.dlg.progressBar_TrainModel.setValue(100)
        self.dlg.Log("Model training completed.")


    def predict_model(self):
        """Test the model with the selected GMI data."""
        # This method is implemented to train the model
        self.dlg.Log("Predicting model with selected GMI data...")

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # write feature attributes
        checkedLayers_GMI = self.dlg.comboBox_TestGMI.checkedItems()
        selectedLayer_GMI = self.get_layer_by_name(checkedLayers_GMI[0])
        bands, long, lat = self.get_gmi_data(selectedLayer_GMI)

        # Preprocess the data
        bands, long, lat = self.preprocess_GMI_data(bands, long, lat, normalize=True)

        # Evaluate the model
        y_pred = self.model.predict(bands)

        # Export the results to a netCDF4 file and load it as a raster layer
        long_width, lat_height = self.get_long_lat(selectedLayer_GMI)
        filepath = self.dlg.fileWidget_ForecastOutput.lineEdit().value()
        if not filepath:
            filepath = os.path.join(os.getcwd(), 'Temp', 'forecast_output.nc')
        self.export_to_netCDF4_file(len(long_width), len(lat_height), long, lat, y_pred, filepath)

        # Log the prediction completion
        self.dlg.progressBar_Predict.setValue(100)
        self.dlg.Log("Model prediction completed.")


