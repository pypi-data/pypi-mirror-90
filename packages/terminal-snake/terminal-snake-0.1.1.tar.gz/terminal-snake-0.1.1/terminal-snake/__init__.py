from game import Game

KEYBINDINGS = {
        "w": 0,
        "a": 3,
        "s": 2,
        "d": 1,
    }


def main(game):
    game.set_apple()
    while True:
        game.draw_field()
        while (go := input("> ").lower()) not in ["w", "a", "s", "d"]:
            print(":(")

        game.orientation = KEYBINDINGS[go]

        if not game.move():
            print("You lost!")
            break

        if game.score == game.max_score:
            print("You won!")

        game.max_apples = max((1, game.score // 5))
    game.end_game()
    print(f"Score: {game.score}")


if __name__ == '__main__':
    game = Game(5)
    main(game)

