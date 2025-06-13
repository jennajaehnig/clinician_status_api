from shapely import Point, Polygon


def clinician_out_of_range(clinician_id, json_data):
    """
    This function checks if a clinician is out of range based on their position and the defined polygon coordinates.
    It returns True if the clinician is out of range, otherwise returns False.
    """
    clinician_pos, polygon_coords = parse_json(json_data)
    if not clinician_pos or not polygon_coords:
        print(f"Clinician {clinician_id} has invalid position or polygon coordinates.")
        return True
    if not point_inside_polygon(clinician_pos, polygon_coords):
        print(f"Clinician {clinician_id} is out of range.")
        return True
    # print(f"Clinician {clinician_id} is in range.")
    return False
    
def point_inside_polygon(point_coords, polygon_coords):
    """
    This function checks if a point (clinician) is inside any of the polygons defined by polygon_coords.
    The polygons represent the zone that a clinician is expected to be in.
    """
    point = Point(point_coords)
    for coords in polygon_coords:
        # print(f"Checking polygon with coordinates: {coords}")
        polygon = Polygon(coords)
        if polygon.intersects(point):
            return True
    return False


def parse_json(json_data):
    """
    This function parses the JSON data to extract the clinician's position and the polygon coordinates.
    """
    if not json_data or "features" not in json_data:
        print("Invalid JSON data or missing 'features' key.")
        return None, None
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