from utils.get_geo_info import get_layer, get_shapefile, find_points

shapefile = get_shapefile("../shapefile/UKR_adm1.shp", False)

layer = get_layer(shapefile, 0)


feature = layer.GetFeature(2)

geometry = feature.GetGeometryRef()

results = {'north': None, 'south': None}
find_points(geometry, results)
print("Найпівнічніша точка: ({:.4f}, {:.4f})".format(results['north'][0], results['north'][1]))
print("найпівденніша точка: ({:.4f}, {:.4f})". format(results['south'][0], results['south'][1]))
