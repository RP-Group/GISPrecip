

class TestModel:
    def test_model(self):
        """Test the model with the selected GMI and Surface Precipitation data."""
        # This method is implemented to train the model
        self.dlg.Log("Testing model with selected GMI and Surface Precipitation data...")

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # write feature attributes
        checkedLayers_GMI = self.dlg.comboBox_TestGMI.checkedItems()
        selectedLayer_GMI = self.get_layer_by_name(checkedLayers_GMI[0])
        bands, long, lat = self.get_gmi_data(selectedLayer_GMI)

        # Assuming the surface precipitation layer is selected
        checkedLayers_SurfPrecip = self.dlg.comboBox_TestSurfPrecip.checkedItems()
        selectedLayer_SurfPrecip = self.get_layer_by_name(checkedLayers_SurfPrecip[0])
        surfPrecip, long, lat = self.get_surf_precip_data(selectedLayer_SurfPrecip)

        # Preprocess the data
        bands, surfPrecip, long, lat = self.preprocess_data(bands, surfPrecip, long, lat, normalize=True, under_sample=False)

        # Evaluate the model
        y_pred = self.model.predict(bands)
        self.dlg.Log("Model evaluation:")
        self.dlg.Log(classification_report(surfPrecip, y_pred))

        # Confusion matrix
        cm = confusion_matrix(surfPrecip, y_pred)
        self.dlg.Log("Confusion Matrix:")
        self.dlg.Log(cm)

        # Export the results to a netCDF4 file and load it as a raster layer
        long_width, lat_height = self.get_long_lat(selectedLayer_GMI)
        filepath = self.dlg.fileWidget_TestOutput.lineEdit().value()
        if not filepath:
            filepath = os.path.join(os.getcwd(), 'Temp', 'test_output.nc')
        self.export_to_netCDF4_file(len(long_width), len(lat_height), long, lat, y_pred, filepath)

        # Calculate model metrics
        y_pred = y_pred.flatten()
        y_true = surfPrecip.flatten()
        bias, mse, mae, smape_value, lin_corr = self.get_model_metrics(y_true, y_pred)

        # Update the table with model metrics
        self.dlg.tableWidget_ModelMetrics.setItem(0, 0, QTableWidgetItem(f"{bias:.4f}"))
        self.dlg.tableWidget_ModelMetrics.setItem(0, 1, QTableWidgetItem(f"{mse:.4f}"))
        self.dlg.tableWidget_ModelMetrics.setItem(0, 2, QTableWidgetItem(f"{mae:.4f}"))
        self.dlg.tableWidget_ModelMetrics.setItem(0, 3, QTableWidgetItem(f"{smape_value:.4f}"))
        self.dlg.tableWidget_ModelMetrics.setItem(0, 4, QTableWidgetItem(f"{lin_corr:.4f}"))

        # Log the testing completion
        self.dlg.progressBar_RunTest.setValue(100)
        self.dlg.Log("Model testing completed.")
