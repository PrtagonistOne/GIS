from utils.get_geo_info import analyze_geometry, get_shapefile, get_layer


shapefile = get_shapefile("../shapefile/UKR_adm1.shp", False)
layer = get_layer(shapefile, 0)

feature = layer.GetFeature(2)  # Cernivtsi
geometry = feature.GetGeometryRef()

analyze_geometry(geometry)
