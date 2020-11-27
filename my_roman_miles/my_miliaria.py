projectus = QgsProject.instance()
regina_viarum = projectus.mapLayersByName('Appia Antica')[0]

metior = {
    'INPUT': regina_viarum,
    'DISTANCE':1480,
    'START_OFFSET':1480,
    'END_OFFSET':0,
    'OUTPUT':'memory:miliaria'
}

result = processing.run("native:pointsalonglines", metior)
projectus.addMapLayer(result['OUTPUT'])

milia = projectus.mapLayersByName('miliaria')[0]

from qgis.PyQt.QtCore import QVariant
pr = milia.dataProvider()
pr.addAttributes([QgsField("miliarium", QVariant.Int)
                ])
milia.updateFields()

expression1 = QgsExpression('$id')
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(regina_viarum))

with edit(milia):
    for f in milia.getFeatures():
        context.setFeature(f)
        f['miliarium'] = expression1.evaluate(context)
        milia.updateFeature(f)

milia.updateExtents()

QgsProject.instance().addMapLayer(milia)