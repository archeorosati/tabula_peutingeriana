from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingOutputNumber,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class TabulaPeutingeriana(QgsProcessingAlgorithm):

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return TabulaPeutingeriana()

    def name(self):
        return 'roman_miles'

    def displayName(self):
        return self.tr('Tabula Peutingeriana')

    def group(self):
        return self.tr('Tabula Peutingeriana')

    def groupId(self):
        return 'tabulapeutingeriana'

    def shortHelpString(self):
        return self.tr('Tabula Peutingeriana, from a Roman Road Network (lines) it returns the roman miles (points) in the tabula peutingeriana ways')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT',
                self.tr('Input vector layer'),
                types=[QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                'ROMAN_MILES_OUTPUT',
                self.tr('Roman Miliaria'),
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                'ROMAN_MILIA_OUTPUT',
                self.tr('Roman Milia')
            )
        )
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # First, we get the count of features from the INPUT layer.
        # This layer is defined as a QgsProcessingParameterFeatureSource
        # parameter, so it is retrieved by calling
        # self.parameterAsSource.
        input_featuresource = self.parameterAsSource(parameters,
                                                     'INPUT',
                                                     context)
        numfeatures = input_featuresource.featureCount()
        if feedback.isCanceled():
            return {}
            
        milia_result = processing.run(
            'native:pointsalonglines',
            {
                # Here we pass on the original parameter values of INPUT
                # and BUFFER_OUTPUT to the buffer algorithm.
                'INPUT': parameters['INPUT'],
                'OUTPUT': parameters['ROMAN_MILES_OUTPUT'],
                'DISTANCE':1480,
                'START_OFFSET':1480,
                'END_OFFSET':0,
            },
            # Because the linetopoint algorithm is being run as a step in
            # another larger algorithm, the is_child_algorithm option
            # should be set to True
            is_child_algorithm=True,
            #
            # It's important to pass on the context and feedback objects to
            # child algorithms, so that they can properly give feedback to
            # users and handle cancelation requests.
            context=context,
            feedback=feedback)
            
        # Check for cancelation
        if feedback.isCanceled():
            return {}

        # Run the separate mila count algorithm using the buffer result
        # as an input.
        miliaria_result = processing.run(
            'native:addautoincrementalfield',
            {
                # Here we pass the 'OUTPUT' value from the linetopoint's result
                # dictionary off to the milia count child algorithm.
                'INPUT': milia_result['OUTPUT'],
                'FIELD_NAME':'miliarium',
                'START':1,'GROUP_FIELDS':['id'],
                'SORT_EXPRESSION':'',
                'SORT_ASCENDING':False,
                'SORT_NULLS_FIRST':False,
                'OUTPUT':parameters['ROMAN_MILIA_OUTPUT']

            },
            is_child_algorithm=True,
            context=context,
            feedback=feedback)

        if feedback.isCanceled():
            return {}

        # Return the results
        return {'ROMAN_MILES_OUTPUT': milia_result['OUTPUT'],
        'ROMAN_MILIA_OUTPUT': miliaria_result['OUTPUT']}