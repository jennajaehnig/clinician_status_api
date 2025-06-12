from shapely import Point, Polygon


def clinician_out_of_range(clinician_id, json_data):
    clinician_pos, polygon_coords = parse_json(json_data)
    # print(f"Clinician {clinician_id} position: {clinician_pos}")
    # print(f"Polygon coordinates: {polygon_coords}")
    if not point_inside_polygon(clinician_pos, polygon_coords):
        print(f"Clinician {clinician_id} is out of range.")
        return True
    print(f"Clinician {clinician_id} is in range.")
    return False

    
def point_inside_polygon(point_coords, polygon_coords):
    point = Point(point_coords)
    for coords in polygon_coords:
        # print(f"Checking polygon with coordinates: {coords}")
        polygon = Polygon(coords)
        if polygon.intersects(point):
            return True
    return False


def parse_json(json_data):
    features = json_data.get("features")
    point_coords = None
    polygon_coords = []
    # print(f"Parsing JSON data")
    for feature in features:
        if feature.get("geometry").get("type") == "Point":
            point_coords = feature.get("geometry").get("coordinates")
        elif feature.get("geometry").get("type") == "Polygon":
            polygon_coords.append(feature.get("geometry").get("coordinates"))
    # print(f"Json data parsed")
    return point_coords, polygon_coords[0]