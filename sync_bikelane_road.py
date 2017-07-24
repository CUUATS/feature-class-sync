import arcpy
import os

GDB_PATH = 'G:\CUUATS\Sustainable Neighborhoods Toolkit\Data\SustainableNeighborhoodsToolkit.gdb'
BIKE_NAME = 'BicyclePedestrianPath'
STREET_NAME = 'GISC_Join'

arcpy.env.workspace = GDB_PATH
arcpy.env.overwriteOutput = True

class SyncBikeRoad(object):
    def __init__(self, GDB_PATH, STREET_NAME, BIKE_NAME):
        #TODO: work on keeping temp file in memory
        self.GDB_PATH = GDB_PATH
        self.STREET_NAME = STREET_NAME
        self.BIKE_NAME = BIKE_NAME
        self.intersect_name = None
        self.split_bike = None
        self.bike_centroid = None
        self.street_centroid = None
        self.street_centroid_bike = None
        self.stree_bike = None

    def createIntersection(self):
        """
        Create a point layer where the bike lane intersect with street
        :param street: string of street name
        :param bike: string of bike name
        :return: name point layer of intersections
        """
        intersect_name = "st_bi_intersect"
        arcpy.Intersect_analysis([self.STREET_NAME, self.BIKE_NAME],
                                 intersect_name,
                                 output_type = "POINT")
        self.intersect_name = intersect_name

    def splitLineAtPoint(self):
        """
        Split the bike lane where it intersect street layer
        :return: 
        """
        split_bike = "bike_split"
        arcpy.SplitLineAtPoint_management(self.BIKE_NAME,
                                          self.intersect_name,
                                          split_bike,
                                          search_radius=3)
        self.split_bike = split_bike


    def findCentroid(self):
        """
        Find the centroid to both the bike and street feature class
        :return: 
        """
        bike_cent = "bike_cent"
        street_cent = "street_cent"
        arcpy.FeatureToPoint_management(self.split_bike, bike_cent)
        arcpy.FeatureToPoint_management(self.STREET_NAME, street_cent)
        self.bike_centroid = bike_cent
        self.street_centroid = street_cent

    def joinCentroid(self):
        out_feature = "streetCent_bike"
        arcpy.SpatialJoin_analysis(self.street_centroid,
                                   self.bike_centroid,
                                   out_feature,
                                   search_radius=50
                                   )
        self.street_centroid_bike = out_feature

    def joinToStreet(self):
        out_feature = "streetCL"
        street_bike = arcpy.SpatialJoin_analysis(self.STREET_NAME,
                                   self.street_centroid_bike,
                                   out_feature,
                                   search_radius=3)
        fields = arcpy.ListFields(street_bike, "*_1")
        for field in fields:
            arcpy.DeleteField_management(street_bike, field.name)


    def deleteTempFC(self):
        arcpy.Delete_management(self.intersect_name)
        arcpy.Delete_management(self.split_bike)
        arcpy.Delete_management(self.bike_centroid)
        arcpy.Delete_management(self.street_centroid)
        arcpy.Delete_management(self.street_centroid_bike)




def subsetFeatureClass(fc, attr,
                      out_lyr = None,
                      selection_type = "NEW_SELECTION"):
    """
    Subset feature and create a new feature class in the same geodatabase
    :param fc: Input feature class
    :param attr: SQL command to subset the feature class
    :param out_lyr: Output feature class name (optional)
    :param selection_type: (optional)
    :return: Name of the new feature class
    """
    if out_lyr == None:
        out_lyr = fc + "_lyr"

    arcpy.MakeFeatureLayer_management(fc, out_lyr)
    arcpy.SelectLayerByAttribute_management(out_lyr, selection_type, attr)
    arcpy.CopyFeatures_management(out_lyr, os.path.join(GDB_PATH, out_lyr))
    return(out_lyr)


if __name__ == '__main__':
    subsetStr = """
    PathType = 6 or 
    PathType = 8 or
    PathType = 9 or
    PathType = 10
    """
    BIKE_NAME = subsetFeatureClass(BIKE_NAME, subsetStr)
    a = SyncBikeRoad(GDB_PATH, STREET_NAME, BIKE_NAME)
    a.createIntersection()
    a.splitLineAtPoint()
    a.findCentroid()
    a.joinCentroid()
    a.joinToStreet()
    a.deleteTempFC()

