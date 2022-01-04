from utils.get_geo_info import get_feature, get_shapefile, get_layers_and_features, get_layer


shapefile = get_shapefile("../shapefile/UKR_adm1.shp", False)


numLayers = shapefile.GetLayerCount()
print("Файл фігур містить {} шарів".format(numLayers))

layerList = get_layers_and_features(shapefile, numLayers)
# print(len(layerList))
for i in range(len(layerList)):
    print("Шар {} має просторову прив’язку {}".format(
        i, layerList[i][0]))  # spatialRef
    print("Шар {} містить {} геооб’єктів: ".format(
        i, layerList[i][1]))  # numFeatures

layer = get_layer(shapefile, 0)
schema = []
# feature = layer.GetFeature(2)
# ldefn = layer.GetLayerDefn()
#
# for n in range(ldefn.GetFieldCount()):
#     fdefn = ldefn.GetFieldDefn(n)
#     schema.append(fdefn.name)
# print(schema)
# feature_name = feature.GetField('NAME_1')
# print(feature_name)

for featureNum in range(layerList[0][1]):
    feature = get_feature(layer, feature_num=featureNum)
    feature_name = feature.GetField("NAME_1")
    print("Геооб’єкт {} під назвою {}".format(featureNum, feature_name))
