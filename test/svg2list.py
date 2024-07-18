import svgpathtools
from xml.dom import minidom

def svg_to_points(svg_path):
    # Parse the SVG path
    doc = minidom.parse(svg_path)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()
    

    # Initialize an empty list to store the points
    points = []

    # Iterate over the path segments
    for path_string in path_strings:
        path = svgpathtools.parse_path(path_string)
        for segment in path:
            # Check if the segment is a Line or CubicBezier
            if isinstance(segment, svgpathtools.Line):
                # Add the start and end points of the line to the list
                points.append(segment.start)
                points.append(segment.end)
            elif isinstance(segment, svgpathtools.CubicBezier):
                # Add the start, control1, control2, and end points of the cubic bezier to the list
                points.append(segment.start)
                points.append(segment.control1)
                points.append(segment.control2)
                points.append(segment.end)

    # Return the list of points
    return points

def points_to_svg(points):
    # Initialize an empty path
    path = svgpathtools.Path()

    # Iterate over the points in pairs
    for i in range(0, len(points) - 1, 2):
        # Create a Line segment from the current point to the next point
        line = svgpathtools.Line(points[i], points[i + 1])
        # Add the line segment to the path
        path.append(line)

    # Return the SVG path
    return path.d()

svg_path = 'training\\trainingDataset\\Van Helsing__78.svg'
points = svg_to_points(svg_path)
print(points)
svg_path = points_to_svg(points)
with open('output.svg', 'w') as f:
    f.write(svg_path)