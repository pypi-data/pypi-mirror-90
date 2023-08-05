import random

wins = 0


for trial in range(1000000):
    secret = random.randint(1, 1000)
    guess = random.randint(1, 1000)
    if secret == guess:
        other = (secret + 1) % 1000
    else:
        other = secret

    guess = other

    if guess == secret:
        wins += 1

print(wins)