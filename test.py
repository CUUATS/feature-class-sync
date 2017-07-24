from cuuats.datamodel import feature_class_factory as factory

FIELD_MAP = {
    'RTLCrossedB': 'RTL_lanescrossed_',
    'LTLCrossedB': 'LTL_lanescrossed_',
    'MaxLanes': 'MaxLanes_',
    'RTLConfiguration': 'RTL_Conf_',
    'LTLConfiguration': 'LTL_Conf_',
    'RTLLength': 'RTL_Len_',
    # 'LTLLength': 'LTL_Len_',
    'BikeApproachAlign': 'bike_AA_',
}

Segment = factory(r'C:\Users\mjy11187\Desktop\Temp.gdb\GISC_join_local')
seg_map = dict([(str(s.StreetID), s) for s in Segment.objects.all()])