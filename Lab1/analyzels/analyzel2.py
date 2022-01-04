from utils.get_geo_info import get_shapefile, get_layer

shapefile = get_shapefile("../shapefile/UKR_adm1.shp", False)

layer = get_layer(shapefile, 0)

# for i in range(layer.GetFeatureCount()):
feature = layer.GetFeature(2)
feature_name = feature.GetField('NAME_1')

print(f"Геооб’єкт {feature_name} має наступні атрибути:\n")
attributes = feature.items()

for key, value in attributes.items():
    print(f"{key} = {value}")

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()
print(f"Геометрія {feature_name} Геооб’єкту представляє собою {geometryName} ")
