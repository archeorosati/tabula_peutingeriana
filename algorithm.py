####

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

params = {'INPUT': milia,
    'FIELD_NAME':'miliarium',
    'START':1,'GROUP_FIELDS':['id'],
    'SORT_EXPRESSION':'',
    'SORT_ASCENDING':False,
    'SORT_NULLS_FIRST':False,
    'OUTPUT':'memory:my_roman_mile'
}

result = processing.run("native:addautoincrementalfield", params)
projectus.addMapLayer(result['OUTPUT'])

to_be_deleted = projectus.mapLayersByName('miliaria')[0]
projectus.removeMapLayer(to_be_deleted.id())
