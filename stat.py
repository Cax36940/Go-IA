import os


B = 0
W = 0

for i in range(10):
    print(i)
    stream = os.popen("python3 namedGame_noprint.py myPlayer_simple randomPlayer_noprint")
    output = stream.read()
    if output == "Winner: BLACK\n":
        B += 1
    else :
        W += 1


print("myPlayer : " + str(B))
print("randomPlayer : " + str(W))
