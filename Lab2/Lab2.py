from utils.get_geo_info import get_shapefile, get_format, get_area, get_length, get_feature_attributes,\
    get_attribute_filter, get_nearby, visualize


def main():
    shapefile = get_shapefile("shapefiles/gis_osm_places_free_1.shp", False)
    shapefile_places = get_shapefile("shapefiles/gis_osm_places_a_free_1.shp", False)
    shapefile_roads = get_shapefile("shapefiles/gis_osm_roads_free_1.shp", False)
    shapefile_rivers = get_shapefile("shapefiles/gis_osm_waterways_free_1.shp", False)


#  Перевірити проекції завантажених даних
    get_format(shapefile)

#  Знайти площу деякої адміністративної одиниці
    get_area(shapefile_places, 0)

#  Знайти довжину доріг (річок) в межах певної адміністративної одиниці'
    get_length(shapefile_places, shapefile_roads, 0)

    #  Відфільтрувати точки за вимогою (належністю до певної адміністративної одиниці)
    #  Вивести точки, що відповідають умові з вказанням географічних координат.')

    get_feature_attributes(shapefile, 1)
    print()
    max_output = 5
    get_attribute_filter(shapefile, 3, "population > 0")


    # Знайти точки, що знаходяться в околі від певного об’єкту (адміністративної одиниці, водного об’єкту, дороги).
    # Вивести їх з вказанням географічних координат.')
    get_nearby(shapefile, 2)

    # Візуалізувати дані у вигляді багатошарової векторної та растрової карт

    visualize()

    shapefile.Destroy()
    shapefile_places.Destroy()
    shapefile_roads.Destroy()
    shapefile_rivers.Destroy()


if __name__ == "__main__":
    main()
