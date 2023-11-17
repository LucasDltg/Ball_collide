
class Ball:

    def __init__(self, x_pos=0, y_pos=0, x_speed=0, y_speed=0, size=0, color=(255, 0, 0), mass=1):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.size = size
        self.color = color
        self.mass = mass

    def isColliding(self, b: 'Ball'):
        x_dif = (self.x_pos + self.size / 2) - (b.x_pos + b.size / 2)
        y_dif = (self.y_pos + self.size / 2) - (b.y_pos + b.size / 2)

        if x_dif * x_dif + y_dif * y_dif < (self.size + b.size) * (self.size + b.size) / 4:
            return True
        return False

    def resolveCollision(self, b: 'Ball'):
        normal = [self.x_pos + self.size / 2 - b.x_pos - b.size / 2, self.y_pos + self.size / 2 - b.y_pos - b.size / 2]
        distance = (normal[0] ** 2 + normal[1] ** 2) ** 0.5

        if distance != 0:
            unit_normal = [normal[0]/distance, normal[1]/distance]

            relative_velocity = [self.x_speed - b.x_speed, self.y_speed - b.y_speed]

            dot_product = relative_velocity[0] * unit_normal[0] + relative_velocity[1] * unit_normal[1]

            impulse = (2.0 * dot_product) / (self.mass + b.mass)

            self.x_speed -= impulse * b.mass * unit_normal[0]
            self.y_speed -= impulse * b.mass * unit_normal[1]
            b.x_speed += impulse * self.mass * unit_normal[0]
            b.y_speed += impulse * self.mass * unit_normal[1]

            overlap = (self.size+b.size)/2 - distance
            move = [overlap * unit_normal[0], overlap * unit_normal[1]]

            self.x_pos += move[0] / 2
            self.y_pos += move[1] / 2
            b.x_pos -= move[0] / 2
            b.y_pos -= move[1] / 2
