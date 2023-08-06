from random import randint
import json


class Game:
    def __init__(self, field_size):
        self.snake = [(field_size // 2 + 1, field_size // 2 + 1)]  # field starts at 1; (1, 1) is the top left corner
        self.field_size = field_size
        self.orientation = 0  # 0 = Up, 1 = Right, 2 = Down, 3 = Left
        self.apples = []

        self.max_apples = 1
        self.max_score = self.field_size ** 2
        self.orientation_switch = {
            0: (0, -1),
            1: (1, 0),
            2: (0, 1),
            3: (-1, 0),
        }
        try:
            with open("scores.json") as f:
                scores = json.loads(f.read())
                self.scores = scores

                if str(self.field_size) in scores.keys():
                    self.highscore = scores[str(self.field_size)]
                else:
                    self.highscore = 0
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            self.highscore = 0
            self.scores = {}

    def set_apple(self):
        if self.max_score > len(self.apples) + self.score:
            while apple_location := (randint(1, self.field_size), randint(1, self.field_size)):
                if apple_location not in self.snake and apple_location not in self.apples:
                    self.apples.append(apple_location)
                    break

    def move(self):
        # check what next field would be
        # check if its a wall → lose
        # check if its an apple → grow and move
        # else: it's empty → move
        orientation = self.orientation_switch[self.orientation]
        head = self.snake[-1]
        next_field = (head[0] + orientation[0], head[1] + orientation[1])
        # print(head, next_field)

        if all([0 < pos <= self.field_size for pos in next_field]) and next_field not in self.snake:
            # next_field is not inside a wall, so we can walk
            self.snake.append(next_field)

            # should we delete the last piece?
            if next_field in self.apples:
                self.apples.pop(self.apples.index(next_field))
                print(self.max_apples - len(self.apples))

                for i in range(self.max_apples - len(self.apples)):
                    print(i)
                    self.set_apple()
            else:
                self.snake.pop(0)

            return True
        else:
            return False

    def draw_field(self):
        print("🟧" * (self.field_size + 2))
        for y in range(1, self.field_size + 1):
            print("🟧", end="")
            for x in range(1, self.field_size + 1):
                field = (x, y)

                if field in self.apples:
                    print("🍎", end="")
                elif field == self.snake[-1]:
                    print("😳", end="")
                elif field in self.snake:
                    print("🔲", end="")
                else:
                    print("🟫", end="")

            print("🟧")
        print("🟧" * (self.field_size + 2))

    @property
    def score(self):
        return len(self.snake)

    def add_another_apple(self):
        self.max_apples += 1

    def end_game(self):
        if self.score > self.highscore:
            with open("scores.json", "w") as f:
                self.scores[str(self.field_size)] = self.score
                f.write(json.dumps(self.scores))



