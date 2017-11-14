import heapq


# create class for grid/graph
class Grid:
    def __init__(self, width, height):
        # define attributes for use with grid/graph
        self.width = width
        self.height = height
        self.position_list = []
        self.no_go_list = []
        self.square_size = 20
        self.create_grid()
        
    def create_grid(self):
        for x in range(0, self.width, self.square_size):
            for y in range(0, self.height, self.square_size):
                self.position_list.append((x // self.square_size, y // self.square_size))

    def define_neighbours(self, position):
        # take position input list of [x, y], and return list of available positions [x, y]
        neighbours = []
        return_neighbours = []
##        up_neighbour = [position[0], position[1] - 1]
##        down_neighbour = [position[0], position[1] + 1]
##        left_neighbour = [position[0] - 1, position[1]]
##        right_neighbour = [position[0] + 1, position[1]]
        neighbours.append((position[0], position[1] - 1))
        neighbours.append((position[0], position[1] + 1))
        neighbours.append((position[0] - 1, position[1]))
        neighbours.append((position[0] + 1, position[1]))
        for neighbour in neighbours:
            if neighbour in self.position_list:
                return_neighbours.append(neighbour)
        return return_neighbours
                
    def remove_position(self, position):
        # self.no_go_list.append(position)
        self.position_list.remove(position)

    def add_position(self, position):
        self.position_list.append(position)
        
    def find_grid_position(self, item, location):
        x_pos = item.rect.x - location.rect.x
        y_pos = item.rect.y - location.rect.y
        x_pos = x_pos // self.square_size
        y_pos = y_pos // self.square_size
        return (x_pos, y_pos)
        
    def place_in_position(self, position, item, location):
        x_pos = position[0]
        y_pos = position[1]
        x_pos *= self.square_size
        y_pos *= self.square_size
        x_pos += location.rect.x
        y_pos += location.rect.y
        item.rect.x = x_pos
        item.rect.y = y_pos


# create class for priority queue, for use with a* search
class Priority_Queue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]