from OpenGL.GL import *
from math import *
from model.gradient_agent.AgentGradient import Agent
#from model.agent.Agent import Agent
from model.gradient_agent.RunConf import RunConf

class AgentGfx:
    def __init__(self, position: [float, float], map_position: [int, int], angle: float, color: [float, float, float],
        maze, direct, stairs_garderobe, end_goal_frame, current_frame, moving_chance, MapConf, which_map=0, bound_size=2):
        self.map_position = map_position #position of the agent per pixel.
        self.position = position # position of the agent in the grid
        self.angle = radians(angle)
        self.color = color
        exits = list(zip(range(40, 60), [99] * 20))
        self.MapConf = MapConf
        self.agent = Agent((map_position[0], map_position[1]), exits, direct, maze, stairs_garderobe, end_goal_frame, current_frame, moving_chance, self.MapConf, which_map, bound_size)
        self.fx_pos = (0, 0)

    def move(self):
        result = self.agent.move()
        return result

    def draw(self, radius):
        direction = [cos(self.agent.facing_angle) + self.position[0], sin(self.agent.facing_angle) + self.position[1]]

        if self.agent.PATHING_CONFIG == RunConf.GRADIENT:
            glColor3f(0, 1, 0)
        else:
            glColor3f(1, 0, 0)

        # draw circle

        posx, posy = self.fx_pos
        sides = 8

        # draw circle filling
        glBegin(GL_POLYGON)
        for vertex in range(sides):
            angle = float(vertex) * 2.0 * pi / sides
            glVertex2f(cos(angle) * radius + posx, sin(angle) * radius + posy)
        glEnd()

        # draw circle outline
        glLineWidth(0.2)
        glColor3f(self.color[0], self.color[1], self.color[2])

        glBegin(GL_LINE_LOOP)
        for vertex in range(sides):
            angle = float(vertex) * 2.0 * pi / sides
            glVertex2f(cos(angle) * radius + posx, sin(angle) * radius + posy)
        glEnd()

        # draw direction line
        vec = [(direction[0] - self.position[0]), (direction[1] - self.position[1])]

        vec_len = sqrt(pow(vec[0], 2) + pow(vec[1], 2)) / 5
        vec[0] = vec[0] / vec_len * radius
        vec[1] = vec[1] / vec_len * radius

        glLineWidth(0.1)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_LINES)
        glVertex2f(self.position[0], self.position[1])
        glVertex2f(self.position[0] + vec[0], self.position[1] - vec[1])
        glEnd()

        return self.agent.PATHING_CONFIG
