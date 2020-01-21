from enum import Enum


class RunConf(Enum):
    GRADIENT = "gradient"
    DIJKSTRA = "dijkstra"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
