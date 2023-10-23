import random
import os

def main():
    pixels = [
            {
                "char": "w",
                "top": ["s","w"], 
                "bottom": ["s", "w"], 
                "left": ["s", "w"], 
                "right": ["s", "w"], 
            },
            {
                "char": "s",
                "top": ["g","w"], 
                "bottom": ["g", "w"], 
                "left": ["g", "w"], 
                "right": ["g", "w"], 
            },
            {
                "char": "b",
                "top": ["g","f"], 
                "bottom": ["g", "f"], 
                "left": ["g", "f"], 
                "right": ["g", "f"], 
            },
            {
                "char": "f",
                "top": ["b","f"], 
                "bottom": ["b", "f"], 
                "left": ["b", "f"], 
                "right": ["b", "f"], 
            },
            {
                "char": "g",
                "top": ["g","b","s"], 
                "bottom": ["g", "b", "s"],
                "left": ["g", "b", "s"],
                "right": ["g", "b", "s"],
            }
        ]

    w = 10
    outcomes = [[pixels.copy() for _ in range(w)] for _ in range(w)]
    image = [["."] * w for _ in range(w)]

    stop = w * w

    while stop > 0:
        os.system("clear")
        match = False
        for i in range(w):
            for j in range(w):
                if len(outcomes[i][j]) == 1:
                    char = outcomes[i][j][0]["char"]
                    image[i][j] = char
                    stop -= 1
                    match = True
                    print('match', i, j)
                    outcomes[i][j] = []
                    if i > 0:
                        outcomes[i-1][j] = list(filter(lambda x: char in x["bottom"], outcomes[i-1][j]))
                    if i < len(outcomes) - 1:
                        outcomes[i+1][j] = list(filter(lambda x: char in x["top"], outcomes[i+1][j]))
                    if j > 0:
                        outcomes[i][j-1] = list(filter(lambda x: char in x["right"], outcomes[i][j-1]))
                    if j < len(outcomes[i]) - 1:
                        outcomes[i][j+1] = list(filter(lambda x: char in x["left"], outcomes[i][j+1]))

        if not match:
            # Find the min non zero
            mini = 0
            minj = 0
            min_non_zero = 100
            for i in range(w):
                for j in range(w):
                    if len(outcomes[i][j]) > 0 and len(outcomes[i][j]) < min_non_zero:
                        min_non_zero = len(outcomes[i][j])
                        mini = i
                        minj = j
            print("no match", mini, minj)
            if len(outcomes[mini][minj]) > 0:
                k = random.randint(0, len(outcomes[mini][minj]) - 1)
                outcomes[mini][minj] = [outcomes[mini][minj][k]]

        for r in image:
            for c in r:
                print(c, end=" ")
            print()
        print("stop: ", stop)
        for r in outcomes:
            for c in r:
                print(len(c), end=" ")
            print()

if __name__ == "__main__":
    main()
