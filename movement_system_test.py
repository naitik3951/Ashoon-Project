import json
while True:
    #Player command
    command = input("> ").lower()

    #Movement
    if command == "north" or "n":
        current_room = rooms[current_room]["north"]
    elif command == "south" or "s":
        current_room = rooms[current_room]["south"]
    elif command == "east" or "e":
        current_room = rooms[current_room]["east"]
    elif command == "west" or "w":
        current_room = rooms[current_room]["west"]
