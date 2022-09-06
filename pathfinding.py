def find_start(list):
    for i in range(len(list)):
        if list[i].__contains__("s"):
            return (i, list[i].index("s"))



a = [[0,0,0,"e"],
     [0,0,1,0],
     ["s",0,0,0]
     ]


print(find_start(a))