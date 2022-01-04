import osgeo.ogr as ogr
import pyproj


def get_distance(long1, lat1, long2, lat2):
    geod = pyproj.Geod(ellps="WGS84")
    anglel, angle2, distance = geod.inv(long1, lat1, long2, lat2)
    return distance

def get_center(north, south, east, west):
    center_point_x = (north[0] + south[0] + east[0] + west[0]) / 4
    center_point_y = (north[1] + south[1] + east[1] + west[1]) / 4
    return [center_point_x, center_point_y]


def find_four_points(geometry: ogr.Geometry, directionA: str = None, directionB: str = None, directionC: str = None, directionD: str = None):
    results = {directionA: None, directionB: None,
               directionC: None, directionD: None}
    for i in range(geometry.GetGeometryCount()):
        geom = geometry.GetGeometryRef(i)
        for i in range(geom.GetPointCount()):
            x, y, z = geom.GetPoint(i)
            for direction in [directionA, directionB, directionC, directionD]:
                if direction == 'north':
                    if results[direction] is None or results[direction][1] < y:
                        results[direction] = (x, y)
                elif direction == 'south':
                    if results[direction] is None or results[direction][1] > y:
                        results[direction] = (x, y)
                elif direction == 'west':
                    if results[direction] is None or results[direction][0] > x:
                        results[direction] = (x, y)
                elif direction == 'east':
                    if results[direction] is None or results[direction][0] < x:
                        results[direction] = (x, y)
    return results

def find_points(geometry, results):
    for i in range(geometry.GetPointCount()):
        x, y, z = geometry.GetPoint(i)
        if results['north'] is None or results['north'][1] < y:
            results['north'] = (x, y)
        if results['south'] is None or results['south'][1] > y:
            results['south'] = (x, y)
    for i in range(geometry.GetGeometryCount()):
        find_points(geometry.GetGeometryRef(i), results)


def analyze_geometry(geometry: ogr.Geometry, indent=0):
    s = [" " * indent, geometry.GetGeometryName()]
    if geometry.GetPointCount() > 0:
        s.append(" з {} точками даних".format(geometry.GetPointCount()))
    if geometry.GetGeometryCount() > 0:
        s.append(" містить:")
    print(" " .join(s))
    for i in range(geometry.GetGeometryCount()):
        analyze_geometry(geometry.GetGeometryRef(i), indent + 1)


def get_shapefile(filename, boolean: False) -> ogr.DataSource:
    return ogr.Open(filename, boolean)


def get_layer(shp, layer_num) -> ogr.Layer:
    return shp.GetLayer(layer_num)


def get_layers_and_features(shp: ogr.DataSource, num_layers: int, layer_list=None):
    if layer_list is None:
        layer_list = []

    for layerNum in range(num_layers):
        layer = get_layer(shp, layerNum)
        spatial_ref = layer.GetSpatialRef().ExportToProj4()
        num_features = layer.GetFeatureCount()
        layer_list.append([spatial_ref, num_features])
    return layer_list


def get_feature(layer, feature_num) -> ogr.Feature:
    return layer.GetFeature(feature_num)
