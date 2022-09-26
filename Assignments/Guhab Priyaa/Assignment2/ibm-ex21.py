if __name__ == '__main__':
    N = int(input())
    commands = {
        "insert": lambda x, y, z: x.insert(y, z),
        "print": lambda x: print(x),
        "remove": lambda x, y: x.remove(y),
        "append": lambda x, y: x.append(y),
        "sort": lambda x: x.sort(),
        "pop": lambda x: x.pop(),
        "reverse": lambda x: x.reverse(),
    }
    out = []
    for i in range(N):        
        a = input()
        split_a = a.split(' ')
        command = split_a[0]
        try:
            commands[command](out, int(split_a[1]), int(split_a[2]))
        except IndexError:
            try:
                commands[command](out, int(split_a[1]))
            except IndexError:
                commands[command](out)