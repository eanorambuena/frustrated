import numpy as np
import math


class Camera3d():

    def __init__(self, alpha = 60, beta = 60, near = 0.25, far = 6000) -> None:
        self.alpha = alpha
        self.beta = beta
        self.near = near
        self.far = far
        self.transform_matrix = self.calculate_transform_matrix()

    def calculate_transform_matrix(self):
        delta = self.far - self.near
        term_a = (self.far + self.near) / delta
        term_b = (2 * self.near * self.far) / delta
        return np.array(
            [
                [math.tan(self.alpha),                   0,      0,      0],
                [                   0, math.tan(self.beta),      0,      0],
                [                   0,                   0, term_a, term_b],
                [                   0,                   0,     -1,      0],
            ]
        )

    def calculate_point(self, np_point):
        position = np.append(np_point, np_point[-1])
        transformed_position = position.dot(self.transform_matrix)
        transformed_position /= transformed_position[-1]
        return transformed_position[0], transformed_position[1]


class Object3d():
    def __init__(self, model, position, rotation) -> None:
        self.vertex_buffer, self.edge_buffer, self.eobj_edge_buffer = self.obj_to_model(model)
        self.position = position
        self.rotation = rotation

    def obj_to_model(self, file_name):
        with open(file_name, "r") as file:
            vertex_buffer = []
            edge_buffer = []
            eobj_edge_buffer = []
            for line in file:
                if line.startswith("v "):
                    line = line.replace("v ", "").strip().split(" ")
                    vertex_buffer.append(np.array(
                        [float(component) for component in line]
                    ))
                elif line.startswith("f "):
                    line = line.replace("f ", "").strip().split(" ")
                    edge_buffer.append(
                        [int(component.split("/")[0]) - 1 for component in line]
                    )
                elif line.startswith("e "):
                    line = line.replace("e ", "").strip().split(" ")
                    eobj_edge_buffer.append(
                        [int(component) - 1 for component in line]
                    )   

        return vertex_buffer, edge_buffer, eobj_edge_buffer

    @property
    def points(self):
        model = []
        for point in self.vertex_buffer:
            model.append(point + self.position)
        return model
