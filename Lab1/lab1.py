from utils.get_geo_info import get_distance, get_center, find_four_points, find_points, get_shapefile, get_layer, get_feature, get_layers_and_features
# Знайти найсхідніші і найзахідніші точки досліджуваної території

shapefile = get_shapefile("shapefile/UKR_adm1.shp", False)
num_layers = shapefile.GetLayerCount()

layerList = get_layers_and_features(shapefile, num_layers)

for i in range(len(layerList)):
    print("Шар {} має просторову прив’язку {}".format(
        i, layerList[i][0]))  # spatialRef
    print("Шар {} містить {} геооб’єктів: ".format(
        i, layerList[i][1]))  # numFeatures

layer = get_layer(shapefile, 0)

final_results = {'northest': None, 'southest': None}

for featureNum in range(layerList[0][1]):
    feature = get_feature(layer, featureNum)
    feature_name = feature.GetField("NAME_1")
    print(f"\nГеооб’єкт {featureNum} під назвою {feature_name}")
    geometry = feature.GetGeometryRef()

    results = {'north': None, 'south': None}
    find_points(geometry, results)
    print(f"Найпівнічніша точка: ({results['north'][0]:.4f}, {results['north'][1]:.4f})")
    print(f"Найпівденніша точка: ({results['south'][0]:.4f}, {results['south'][1]:.4f})")

# Знайти центральну точку певної адміністративної одиниці (або природного об’єкту).
feature_num = 2  # Чернівці
feature = get_feature(layer, feature_num)
feature_name = feature.GetField("NAME_1")
print("Геооб’єкт {} під назвою {}".format(feature_num, feature_name))
geometry = feature.GetGeometryRef()

points = find_four_points(geometry, 'east', 'west', 'north', 'south')

east_point = [points['east'][0], points['east'][1]]
west_point = [points['west'][0], points['west'][1]]
north_point = [points['north'][0], points['north'][1]]
south_point = [points['south'][0], points['south'][1]]

centerPoint = get_center(north_point, south_point, east_point, west_point)

print("\tНайпівнічніша точка: ( {:0.4f}, {:0.4f} )".format(north_point[0], north_point[1]))
print("\tНайпівденніша точка: ( {:0.4f}, {:0.4f} )".format(south_point[0], south_point[1]))
print("\tНайсхідніша точка: ( {:0.4f}, {:0.4f} )".format(east_point[0], east_point[1]))
print("\tНайзахідніша точка: ( {:0.4f}, {:0.4f} )".format(west_point[0], west_point[1]))
print("\n\tЦентральна точка: ( {:0.4f}, {:0.4f} )".format(centerPoint[0], centerPoint[1]))

# Знайти відстань між центральними точками
feature_num = 13  # Львів
feature = get_feature(layer, feature_num)
feature_name = feature.GetField("NAME_1")
print("Геооб’єкт {} під назвою {}".format(feature_num, feature_name))
geometry = feature.GetGeometryRef()

points = find_four_points(geometry, 'east', 'west', 'north', 'south')

east_point = [points['east'][0], points['east'][1]]
west_point = [points['west'][0], points['west'][1]]
north_point = [points['north'][0], points['north'][1]]
south_point = [points['south'][0], points['south'][1]]

centerPoint_2 = get_center(north_point, south_point, east_point, west_point)

print("\tНайпівнічніша точка: ( {:0.4f}, {:0.4f} )".format(north_point[0], north_point[1]))
print("\tНайпівденніша точка: ( {:0.4f}, {:0.4f} )".format(south_point[0], south_point[1]))
print("\tНайсхідніша точка: ( {:0.4f}, {:0.4f} )".format(east_point[0], east_point[1]))
print("\tНайзахідніша точка: ( {:0.4f}, {:0.4f} )".format(west_point[0], west_point[1]))
print("\n\tЦентральна точка: ( {:0.4f}, {:0.4f} )".format(centerPoint_2[0], centerPoint_2[1]))
lat1, long1 = centerPoint[1], centerPoint[0]
lat2, long2 = centerPoint_2[1], centerPoint_2[0]

distance = get_distance(long1, lat1, long2, lat2)
print('\nВідстань {:0.0f} кілометрів\n'.format(distance / 1000))
