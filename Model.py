from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.core import QgsProject, QgsRasterLayer

from .GIS_Precip_dialog import GISPrecipDialog
from .TrainModel import TrainModel
from .TestModel import TestModel
import os.path

"""

    CLASSE PRINCIPAL - FUNCIONALIDADES DA ABA DO PLUGIN ** MODEL **

"""

class Model:
    def __init__(self, iface):
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GISPrecip_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GISPrecip')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        self.model = None
        self.scaler = None


    # MAIN PLUGIN
    def run(self):
        if self.first_start == True:
            self.first_start = False
            self.dlg = GISPrecipDialog()

            # TREINA, PREDIZ E TESTA MODELO
            self.dlg.button_TrainModel.clicked.connect(TrainModel.train_model(self))
            self.dlg.button_Predict.clicked.connect(TrainModel.predict_model(self))
            self.dlg.button_RunTest.clicked.connect(TestModel.test_model(self))
            # self.dlg.button_ExportModel.clicked.connect(self.train_model)

        self.dlg.Log("Plugin initialized.")

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.dlg.Log(os.getcwd())
        # self.write_to_netCDF4_file()

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # LIMPA OS INPUTS DO COMBOBOX
        self.dlg.comboBox_InputGMI.clear()
        self.dlg.comboBox_InputSurfPrecip.clear()
        # self.dlg.lineEdit.clear()

        # POPULA OS COMBOBOX COM OS LAYERS
        self.dlg.comboBox_InputGMI.addItems([layer.name() for layer in layers])
        self.dlg.comboBox_TestGMI.addItems([layer.name() for layer in layers])
        self.dlg.comboBox_InputSurfPrecip.addItems([layer.name() for layer in layers])
        self.dlg.comboBox_TestSurfPrecip.addItems([layer.name() for layer in layers])
        self.dlg.comboBox_ForecastGMI.addItems([layer.name() for layer in layers])

        # LIMPA E DEPOIS ADICIONA OS MODELOS NOS COMBOBOX
        self.dlg.comboBox_InputModel.clear()
        self.dlg.comboBox_InputModel.addItems(["SVM", "Random Forest", "Decision Tree", "AdaBoost", "MLP Regressor"])

        # Set the file dialogs
        # self.dlg.fileWidget_TestOutput.setFilter("All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif);;netCFD(*.nc)")
        directory = self.get_project_or_working_directory()
        self.dlg.fileWidget_TestOutput.lineEdit().setValue(os.path.join(directory, 'Output', 'test_output.nc'))
        self.dlg.fileWidget_ErrorOutput.lineEdit().setValue(os.path.join(directory, 'Output', 'error_output.nc'))
        self.dlg.fileWidget_ForecastOutput.lineEdit().setValue(os.path.join(directory, 'Output', 'forecast_output.nc'))

        # # write feature attributes
        # selectedLayerIndex = self.dlg.comboBox_InputGMI.currentIndex()
        # selectedLayer = layers[selectedLayerIndex].layer()
        # self.dlg.Log(selectedLayer.bandCount())
        # mask = True
        # self.dlg.Log(selectedLayer.as_numpy(mask, [1]))

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


