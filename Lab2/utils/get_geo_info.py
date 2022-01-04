import osgeo.ogr as ogr
import osgeo.osr as osr
import pyproj
import sys
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns



def get_attribute_filter(shapefile: ogr.DataSource, max_output: int, filter_str: str):
    def show_info(layer, featureNum):
        feature = get_feature(layer, featureNum)
        geometry = get_geometry_ref(feature)
        featureName = feature.GetField("name")
        population = feature.GetField('population')
        print(f"\n\tГеооб’єкт {featureNum} - {featureName} з популяцією {population}. Координати геооб’єкта; {geometry.GetPoint()}")

    for layer_num in range(shapefile.GetLayerCount()):
        layer = get_layer(shapefile, layer_num)
        total_features = layer.GetFeatureCount()

        print(f"\tШар {layer_num} містить {total_features} геооб’єктів ДО фільтрації.")
        layer.SetAttributeFilter(filter_str)
        total_featuresAfter = layer.GetFeatureCount()

        print(f"\tШар {layer_num} містить {total_featuresAfter} геооб’єктів ПІСЛЯ фільтрації.\n")
        if 0 <= max_output <= total_features:
            for featureNum in range(max_output):
                show_info(layer, featureNum)


def get_feature_attributes(shapefile: ogr.DataSource, feat_num: int):
    for layer_num in range(shapefile.GetLayerCount()):
        layer = get_layer(shapefile, layer_num)
        total_features = layer.GetFeatureCount()
        if feat_num <= total_features:
            feat = get_feature(layer, feat_num)
            dct = feat.items()
            for k, v in dct.items():
                print(f"\t\t{k} : {v}")


def get_length(shapefile_area: ogr.DataSource, shapefile_length: ogr.DataSource, feature_place_num: int):
    for layer_num in range(shapefile_area.GetLayerCount()):
        layer = get_layer(shapefile_area, layer_num)
        total_features = layer.GetFeatureCount()
        print(f"\nШар {layer_num} містить {total_features} геооб’єктів.")
        feature = get_feature(layer, feature_place_num)
        geometry = get_geometry_ref(feature)
        geom_name = geometry.GetGeometryName()
        print(f"\t\tГеооб’єкт #{feature_place_num} - {feature.GetField('name')}")
        print(f"\t\tТип геооб’єкта: {geom_name}.\n")

        layer2 = get_layer(shapefile_length, 0)
        feature2 = get_feature(layer2, feature_place_num)
        geometry2 = get_geometry_ref(feature2)

        layer2.SetSpatialFilter(geometry)
        transform = get_transform(layer, 3031)

        geometry2.Transform(transform)
        length = geometry2.Length()
        print(f"Геооб’єкт {feature.GetField('name')} має довжину {round(length,2)} м^2.\n")


def get_area(shapefile: ogr.DataSource, feature_num: int):
    for layer_num in range(shapefile.GetLayerCount()):
        layer = get_layer(shapefile, layer_num)
        total_features = layer.GetFeatureCount()
        print(f"\tШар {layer_num} містить {total_features} геооб’єктів.")

        feature = get_feature(layer, feature_num)
        geometry = get_geometry_ref(feature)
        transform = get_transform(layer, 3857)

        geometry.Transform(transform)
        featureName = feature.GetField("name")

        geom_area = geometry.GetArea()
        print(f"\tГеооб’єкт №{feature_num} {featureName} - Площа: {round(geom_area,2)} м^2")



def get_format(shapefile: ogr.DataSource):
    for layer_num in range(shapefile.GetLayerCount()):
        layer = get_layer(shapefile, layer_num)
        print(f"\tФормат: {layer.GetSpatialRef()}")


def get_distance(long1, lat1, long2, lat2):
    geod = pyproj.Geod(ellps="WGS84")
    anglel, angle2, distance = geod.inv(long1, lat1, long2, lat2)
    return distance


def get_center(north, south, east, west):
    center_point_x = (north[0] + south[0] + east[0] + west[0]) / 4
    center_point_y = (north[1] + south[1] + east[1] + west[1]) / 4
    return [center_point_x, center_point_y]


def find_four_points(geometry: ogr.Geometry, a: str = None, b: str = None, c: str = None, d: str = None):
    results = {a: None, b: None,
               c: None, d: None}
    for i in range(geometry.GetGeometryCount()):
        geom = geometry.GetGeometryRef(i)
        for i in range(geom.GetPointCount()):
            x, y, z = geom.GetPoint(i)
            for direction in [a, b, c, d]:
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

    for layer_num in range(num_layers):
        layer = get_layer(shp, layer_num)
        spatial_ref = layer.GetSpatialRef().ExportToProj4()
        num_features = layer.GetFeatureCount()
        layer_list.append([spatial_ref, num_features])
    return layer_list


def get_feature(layer, feature_num) -> ogr.Feature:
    return layer.GetFeature(feature_num)


def get_geometry_ref(feature) -> ogr.Geometry:
    return feature.GetGeometryRef()


def get_transform(layer: ogr.Layer, epsg_num: int = 3031):
    # Prepare a transformation between projections
    src_srs = layer.GetSpatialRef()
    tgt_srs = osr.SpatialReference()
    tgt_srs.ImportFromEPSG(epsg_num)
    return osr.CoordinateTransformation(src_srs, tgt_srs)


def get_nearby(shapefile: ogr.DataSource, feat_num: int):
    for layer_num in range(shapefile.GetLayerCount()):
        layer = get_layer(shapefile, layer_num)
        num_features = layer.GetFeatureCount()
        if feat_num <= num_features:
            feature = get_feature(layer, feat_num)
            feat_name = feature.GetField('name')
            geometry = get_geometry_ref(feature)
            geom2 = geometry.Buffer(0.15)
            layer.SetSpatialFilter(geom2)
            num_features = layer.GetFeatureCount()
            print(f"\nШар {layer_num} містить {num_features} геооб’єктів що знаходяться в {feat_name}.\n")
            for feat in layer:
                print(
                    f"\t\tГеооб'єкт {feat.GetField('name')} з координатами: {feat.GetGeometryRef().GetPoint()}.\n")


def visualize():
    sns.set(style="whitegrid", palette ="pastel", color_codes = True)
    sns.mpl.rc("figure", figsize = (10, 6))

    # opening the vector map
    sf = shp.Reader('to_visualize/District_Boundary.shp')

    def read_shapefile(sf):
        fields = [x[0] for x in sf.fields][1:]
        records = [list(i) for i in sf.records()]
        shps = [s.points for s in sf.shapes()]
        df = pd.DataFrame(columns=fields, data=records)
        # assigning the coordinates
        df = df.assign(coords=shps)
        return df

    df = read_shapefile(sf)
    print(df.shape)
    print(df.sample(5))

    def plot_shape(id, s=None):
        plt.figure()

        ax = plt.axes()
        ax.set_aspect('equal')

        shape_ex = sf.shape(id)
        # for i in list(range(156)):
        #     print(sf.shape(i).shapeTypeName)
        x_lon = np.zeros((len(shape_ex.points), 1))

        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]

        plt.plot(x_lon, y_lat)
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, s, fontsize=10)

        plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
        return x0, y0

    DIST_NAME = "JAIPUR"
    # to get the id of the city map to be plotted
    com_id = df[df.DIST_NAME == "JAIPUR"].index.values[0]
    plot_shape(com_id, DIST_NAME)

    sf.shape(com_id)

    def plot_map(sf, x_lim=None, y_lim=None, figsize=(11, 9)):
        plt.figure(figsize=figsize)
        id = 0
        for shape in sf.shapeRecords():
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y, 'k')

            if (x_lim is None) & (y_lim is None):
                x0 = np.mean(x)
                y0 = np.mean(y)
                plt.text(x0, y0, id, fontsize=10)
            id = id + 1

        if (x_lim is not None) & (y_lim is not None):
            plt.xlim(x_lim)
            plt.ylim(y_lim)

    plot_map(sf)
    plt.show()
