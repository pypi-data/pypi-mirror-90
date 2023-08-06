import numpy as np
from scipy.spatial.transform import Rotation as R


class BoundingBox3D:
    def __init__(self, vertices):
        """Create a 3D Bounding Box

        Args:
            vertices (np.ndarray): Array of bounding box vertices with shape (8, 3)
        """
        assert vertices.shape == (8, 3)
        self.vertices = vertices

    @staticmethod
    def from_center_rotation_dimension(center, rotation, dimensions, use_degrees=False):
        x_c, y_c, z_c = center
        w, h, d = dimensions

        # Get the un-rotated location of the point
        # with the smallest x, y, and z
        min_x = x_c - w / 2.0
        min_y = y_c - h / 2.0
        min_z = z_c - d / 2.0
        x, y, z = min_x, min_y, min_z

        # Create the corners (building off the smallest corner)
        corners = np.array(
            [
                [x, y, z],  # 0 -> 1, 3, 4
                [x, y + h, z],  # 1 -> 0, 2, 5
                [x + w, y + h, z],  # 2 -> 1, 3, 6
                [x + w, y, z],  # 3 -> 0, 2, 7
                [x, y, z + d],  # 4 -> 0, 5, 7
                [x, y + h, z + d],  # 5 -> 1, 4, 6
                [x + w, y + h, z + d],  # 6 -> 2, 5, 7
                [x + w, y, z + d],  # 7 -> 0, 3, 4
            ]
        )

        # Apply the rotation
        rotation = R.from_euler("xyz", rotation, degrees=use_degrees)
        corners = rotation.apply(corners)

        self.vertices = corners

    @property
    def triangle_vertices(self):
        # Triangle vertex connections (for triangle meshes)
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
        triangle_vertices = np.vstack([i, j, k])
        return triangle_vertices

    @property
    def edges(self):
        # Create the edges
        edges = np.array(
            [
                [0, 1],
                [0, 3],
                [0, 4],
                [1, 2],
                [1, 5],
                [2, 3],
                [2, 6],
                [3, 7],
                [4, 5],
                [4, 7],
                [5, 6],
                [6, 7],
            ]
        )
        return edges
