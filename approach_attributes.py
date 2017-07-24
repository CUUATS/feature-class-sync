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

Approach = factory(
    r'C:\Users\mjy11187\Desktop\Temp.gdb\StreetIntersectionApproach',
    follow_relationships=False)

for approach in Approach.objects.all():
    segment = seg_map.get(str(approach.StreetID), None)
    if not segment:
        print 'Approach %i: no match' % (approach.OBJECTID,)
        continue

    segment.Matches = segment.Matches + 1
    matchDirField = 'Matches' + approach.LegDirection
    setattr(segment, matchDirField, getattr(segment, matchDirField) + 1)
    print 'Approach %i: matched' % (approach.OBJECTID,)

    for (app_field, seg_field) in FIELD_MAP.items():
        value = getattr(segment, seg_field + approach.LegDirection)
        if value is not None:
            setattr(approach, app_field, value)

    approach.save()
    segment.save()
