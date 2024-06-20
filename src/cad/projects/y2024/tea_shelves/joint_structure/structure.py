import numpy as np
from shapely.geometry import Polygon

from cad.common.lasercut import Model, MultipartModel


def plane_from_points(p1, p2, p3):
    v1 = p2 - p1
    v2 = p3 - p1
    normal = np.cross(v1, v2)
    A, B, C = normal
    D = -np.dot(normal, p1)
    return A, B, C, D


def point_on_plane(point, plane):
    A, B, C, D = plane
    return np.isclose(A * point[0] + B * point[1] + C * point[2] + D, 0)


def edge_on_plane(edge, plane):
    return point_on_plane(edge[0], plane) and point_on_plane(edge[1], plane)


def point_in_polygon_2d(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def edge_in_polygon_3d(edge, polygon, plane):
    A, B, C, D = plane
    if C != 0:
        proj_polygon = [(p[0], p[1]) for p in polygon]
        proj_edge = [(edge[0][0], edge[0][1]), (edge[1][0], edge[1][1])]
    elif B != 0:
        proj_polygon = [(p[0], p[2]) for p in polygon]
        proj_edge = [(edge[0][0], edge[0][2]), (edge[1][0], edge[1][2])]
    else:
        proj_polygon = [(p[1], p[2]) for p in polygon]
        proj_edge = [(edge[0][1], edge[0][2]), (edge[1][1], edge[1][2])]

    return point_in_polygon_2d(proj_edge[0], proj_polygon) and point_in_polygon_2d(
        proj_edge[1], proj_polygon
    )


def edges_colinear(edge1, edge2):
    vec1 = edge1[1] - edge1[0]
    vec2 = edge2[1] - edge2[0]
    cross_product = np.cross(vec1, vec2)
    return np.all(np.isclose(cross_product, 0))


def edges_overlap_or_contiguous(edge1, edge2):
    direction = edge1[1] - edge1[0]
    line1_start = np.dot(edge1[0], direction)
    line1_end = np.dot(edge1[1], direction)
    line2_start = np.dot(edge2[0], direction)
    line2_end = np.dot(edge2[1], direction)

    if line1_start > line1_end:
        line1_start, line1_end = line1_end, line1_start

    if line2_start > line2_end:
        line2_start, line2_end = line2_end, line2_start

    overlap_start = max(line1_start, line2_start)
    overlap_end = min(line1_end, line2_end)

    if overlap_start <= overlap_end:
        # Convert back to 3D points
        t_start = (overlap_start - line1_start) / (line1_end - line1_start)
        t_end = (overlap_end - line1_start) / (line1_end - line1_start)
        segment_start = edge1[0] + t_start * direction
        segment_end = edge1[0] + t_end * direction
        return [segment_start, segment_end]
    return None


def deduplicate_segments(segments):
    # Convert each NumPy array to a tuple
    tuples = [tuple(tuple(arr) for arr in segment) for segment in segments]

    # Use a set to remove duplicates
    unique_tuples = set(tuples)

    # Convert each tuple back to a NumPy array
    unique_segments = [np.array(tuple).reshape(-1, 3) for tuple in unique_tuples]

    return unique_segments


def polygons_butt_up(polygon1, polygon2):
    plane1 = plane_from_points(polygon1[0], polygon1[1], polygon1[2])
    plane2 = plane_from_points(polygon2[0], polygon2[1], polygon2[2])

    butt_up_segments = []

    # Check each edge of polygon1 against plane2
    for i in range(len(polygon1)):
        edge1 = (polygon1[i], polygon1[(i + 1) % len(polygon1)])
        if edge_on_plane(edge1, plane2):
            for j in range(len(polygon2)):
                edge2 = (polygon2[j], polygon2[(j + 1) % len(polygon2)])
                if edges_colinear(edge1, edge2):
                    overlap_segment = edges_overlap_or_contiguous(edge1, edge2)
                    if overlap_segment:
                        butt_up_segments.append(overlap_segment)
                elif edge_in_polygon_3d(edge1, polygon2, plane2):
                    butt_up_segments.append([edge1[0], edge1[1]])

    # Check each edge of polygon2 against plane1
    for i in range(len(polygon2)):
        edge1 = (polygon2[i], polygon2[(i + 1) % len(polygon2)])
        if edge_on_plane(edge1, plane1):
            for j in range(len(polygon1)):
                edge2 = (polygon1[j], polygon1[(j + 1) % len(polygon1)])
                if edges_colinear(edge1, edge2):
                    overlap_segment = edges_overlap_or_contiguous(edge1, edge2)
                    if overlap_segment:
                        butt_up_segments.append(overlap_segment)
                elif edge_in_polygon_3d(edge1, polygon1, plane1):
                    butt_up_segments.append([edge1[0], edge1[1]])

    # Deduplicate segments
    butt_up_segments = deduplicate_segments(butt_up_segments)

    return butt_up_segments


def rect(x, y, z, dx=0, dy=0, dz=0):
    """One of dx, dy, dz will always be 0, which denotes the plane the rect is in"""

    if dz == 0:
        return np.array(
            [
                [x, y, z],
                [x + dx, y, z],
                [x + dx, y + dy, z],
                [x, y + dy, z],
            ]
        )
    elif dy == 0:
        return np.array(
            [
                [x, y, z],
                [x + dx, y, z],
                [x + dx, y, z + dz],
                [x, y, z + dz],
            ]
        )
    else:
        return np.array(
            [
                [x, y, z],
                [x, y + dy, z],
                [x, y + dy, z + dz],
                [x, y, z + dz],
            ]
        )


class Structure:
    def __init__(self):
        self.polys = []

    def rotate_poly_to_xy(self, vertices):
        # Calculate the normal vector using the cross product of two edges
        edge1 = vertices[1] - vertices[0]
        edge2 = vertices[2] - vertices[0]
        normal_vector = np.cross(edge1, edge2)
        normal_vector = normal_vector / np.linalg.norm(
            normal_vector
        )  # Normalize the normal vector

        if np.allclose(normal_vector, [0, 0, 1]):
            return vertices, np.eye(3)

        normal_vector *= -1

        # Function to create a rotation matrix that aligns vec1 to vec2
        def rotation_matrix_from_vectors(vec1, vec2):
            a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (
                vec2 / np.linalg.norm(vec2)
            ).reshape(3)
            v = np.cross(a, b)
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            rotation_matrix = np.eye(3) + kmat + kmat @ kmat * ((1 - c) / (s**2))
            return rotation_matrix

        # Create the rotation matrix to align the normal vector with the Z-axis
        z_axis = np.array([0, 0, 1])
        rotation_matrix = rotation_matrix_from_vectors(normal_vector, z_axis)

        # Apply the rotation matrix to each vertex to transform the polygon to the XY plane
        transformed_vertices = [rotation_matrix @ vertex for vertex in vertices]

        # Compute the inverse rotation matrix
        inverse_rotation_matrix = np.linalg.inv(rotation_matrix)

        return transformed_vertices, inverse_rotation_matrix

    def get_multi_model(self):
        model = MultipartModel(5)
        model.n_bins = 5

        model.perimeter_bounds = (0, 0, 295, 580)

        for poly in self.polys:
            transformed_poly, inverse_rotation_matrix = self.rotate_poly_to_xy(poly)

            # Convert to shapely polygon
            poly_shapely = Polygon([(p[0], p[1]) for p in transformed_poly])

            m = Model()

            m.add_poly(poly_shapely)

            model.add_model(m).renderer.multmatrix(inverse_rotation_matrix)

        return model

    def rect(self, x, y, z, dx=0, dy=0, dz=0):
        self.polys.append(rect(x, y, z, dx, dy, dz))


if __name__ == "__main__":
    # Example usage:
    # polygon1 = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    # polygon2 = np.array([[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]])

    polygon1 = rect(0, 0, 0, dx=1, dy=1)
    polygon2 = rect(0, 0, 0, dx=1, dz=1)

    print(polygons_butt_up(polygon1, polygon2))
