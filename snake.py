#import sense_emu for emulator, sense_hat for when sense hat is connected
from sense_hat import SenseHat
from random import choice, randint
from time import sleep

#sense hat
sense = SenseHat()

#constants
S = [0,128,0] #GREEN
F = [255,0,0] #RED
O = [0,0,0]   #OFF
REFRESH_INTERVAL = 0.5

#function to "render" new frame
def render_frame(Snake, food) -> None:
    frame = [O for i in range(0,64)]
    frame[food[1]*8 + food[0]] = F
    for a in Snake.coordinates:
        frame[a[1]*8 + a[0]] = S
    sense.set_pixels(frame)

#function to spawn food, set start = True
def spawn_food(Snake, start=False) -> tuple:
    if start:
        return (randint(1,6), randint(1,6))
    else:
        locations = [(i,j) for i in range(0,8) for j in range(0,8)]
        possible_locations = [a for a in locations if a not in Snake.coordinates]
        return choice(possible_locations)

#snake class
class Snake():
    def __init__(self, initial_x, initial_y) -> None:
        self.coordinates = [(initial_x, initial_y)]
        self.vector = (1,0) #right
        self.direction_map = DIRECTION_MAP = {"up": (0,-1), "down": (0,1), "right": (1,0), "left": (-1,0), "middle": self.vector}

    #function to check if snake has bitten itself
    def check_bitten_itself(self) -> bool:
        for i in range(0,len(self.coordinates) - 2):
            if self.coordinates[0] == self.coordinates[i+1]:
                return True
        return False

    #function to check if snake has crashed against wall
    def check_crash(self) -> bool:
        if -1 < self.coordinates[0][0]< 8 and -1 < self.coordinates[0][1] < 8:
            return False
        else:
            return True

    #function to translate last joystick event to vector
    def event_to_vector(self) -> None:
        events = sense.stick.get_events()
        if events:
            new_vector = self.direction_map[events[0].direction]
            if len(self.coordinates) == 1 or (abs(self.vector[0]), abs(self.vector[1])) != (abs(new_vector[0]), abs(new_vector[1])):
                self.vector = new_vector

    #function to check if snake has eaten the food
    def check_food(self,food) -> bool:
        self.event_to_vector()
        if (self.coordinates[0][0] + self.vector[0], self.coordinates[0][1] + self.vector[1]) == food:
            return True
        else:
            return False

    #function to move the snake. direction = True for when no direction is given
    def move(self) -> None:
        for i in range(len(self.coordinates)-1, -1, -1):
            if i != 0:
                self.coordinates[i] = self.coordinates[i - 1]
            else:
                self.coordinates[0] = (self.coordinates[0][0] + self.vector[0], self.coordinates[0][1] + self.vector[1])

    #function to grow the snake when the food is eaten
    def grow(self, food) -> None:
        self.coordinates.insert(0,food)

if __name__ == "__main__":
    snake = Snake(0,3)
    food = spawn_food(snake, start = True)
    sense.show_message("3 2 1", text_colour=F, scroll_speed=0.1)
    render_frame(snake, food)
    while True:
        if snake.check_food(food):
            snake.grow(food)
            food = spawn_food(snake)
        else:
            snake.move()
        if snake.check_crash() or snake.check_bitten_itself():
            sleep(REFRESH_INTERVAL)
            score = len(snake.coordinates) -1
            sense.show_message(f"You lost SCORE {score}", scroll_speed=0.05, text_colour=F)
            break
        else:
            render_frame(snake, food)
            sleep(REFRESH_INTERVAL)
