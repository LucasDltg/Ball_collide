
class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary  # Represents the rectangular region
        self.capacity = capacity  # Maximum number of objects in a node
        self.objects = []  # Objects stored in the quadtree
        self.divided = False  # Indicates if the quadtree has been divided

        # Subdivided regions
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def insert(self, ball):
        if not self.boundary.contains_point(ball.x_pos, ball.y_pos):
            return False  # The ball does not fit in the quadtree

        if len(self.objects) < self.capacity:
            self.objects.append(ball)
            return True  # Successfully inserted the ball

        if not self.divided:
            self.subdivide()

        return (
            self.northwest.insert(ball)
            or self.northeast.insert(ball)
            or self.southwest.insert(ball)
            or self.southeast.insert(ball)
        )

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width
        h = self.boundary.height

        nw_boundary = Rectangle(x, y, w / 2, h / 2)
        ne_boundary = Rectangle(x + w / 2, y, w / 2, h / 2)
        sw_boundary = Rectangle(x, y + h / 2, w / 2, h / 2)
        se_boundary = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)

        self.northwest = QuadTree(nw_boundary, self.capacity)
        self.northeast = QuadTree(ne_boundary, self.capacity)
        self.southwest = QuadTree(sw_boundary, self.capacity)
        self.southeast = QuadTree(se_boundary, self.capacity)

        self.divided = True

    def query(self, range_boundary, found_balls):
        if not self.boundary.intersects(range_boundary):
            return

        for ball in self.objects:
            if range_boundary.contains_point(ball.x_pos, ball.y_pos):
                found_balls.append(ball)

        if self.divided:
            self.northwest.query(range_boundary, found_balls)
            self.northeast.query(range_boundary, found_balls)
            self.southwest.query(range_boundary, found_balls)
            self.southeast.query(range_boundary, found_balls)


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains_point(self, x, y):
        return (
            self.x <= x <= self.x + self.width
            and self.y <= y <= self.y + self.height
        )

    def intersects(self, other):
        return not (
            other.x > self.x + self.width
            or other.x + other.width < self.x
            or other.y > self.y + self.height
            or other.y + other.height < self.y
        )
