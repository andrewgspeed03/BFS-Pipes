import collections

def findConSinks(filePath):

    #dictionary marking delta coordinate relation of each opening of the pipe
    pipeCons = {
        '═': [(-1, 0), (1, 0)],        
        '║': [(0, 1), (0, -1)],        
        '╔': [(0, -1), (1, 0)],        
        '╗': [(0, -1), (-1, 0)],      
        '╚': [(1, 0), (0, 1)],         
        '╝': [(-1, 0), (0, 1)],         
        '╠': [(0, 1), (0, -1), (1, 0)], 
        '╣': [(-1, 0), (0, -1), (0, 1)], 
        '╦': [(0, -1), (-1, 0), (1, 0)], 
        '╩': [(0, 1), (-1, 0), (1, 0)]   
    }

    #parses through the input and adds all elements to grid dictionary and tracks starting location of the source
    def readInput(filePath):
        with open(filePath, 'r', encoding='utf-8') as file:
            data = file.readlines()
        grid, src = {}, None
        for line in data:
            obj, x, y = line.strip().split()
            x, y = int(x), int(y)
            grid[(x, y)] = obj
            if obj == '*': 
                src = (x, y)
        return grid, src

    #returns possible coordinates for a connection to a given element
    def getNeighbors(x, y, ele):
        if ele in pipeCons:
            return [(x + dx, y + dy) for dx, dy in pipeCons[ele]]
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] #default case if not a pipe
    
    #returns a dictionary of all connected coordinates to the provided coordinate
    def allCon(coord, grid):
        conCoords = getNeighbors(coord[0], coord[1], grid[coord])
        neighbors = []

        for c in conCoords: 
            if c in grid:
                test = grid[c]
                temp = getNeighbors(c[0],c[1], test)
                if coord in temp:
                    neighbors.append(c)

        return {coord:neighbors}

    #Breadth First Search Algorithm to Trace from Source to Sinks
    def bfs(grid, fullGrid, source):
        queue, visited, conSinks = collections.deque([source]), set(), set()

        while queue:
            temp = queue.popleft()
            visited.add(temp)

            #finds connected elements
            for i in grid[temp]:
                if i not in visited:
                    queue.append(i)
                    #Checks if the current element connected to the source is a sink
                    if fullGrid[i].isupper():
                        conSinks.add(fullGrid[i])

        return conSinks

    fullGrid, source = readInput(filePath)
    conCoords = {}

    #creates dictionary of all connected coordinates in the grid
    for ele in fullGrid:
        conCoords.update(allCon(ele, fullGrid))

    #return sorted string of connected sinks
    return "".join(sorted(bfs(conCoords, fullGrid, source)))

file_path = 'C:/Users/aache/projects/BFS Pipes/src/coding_qual_input.txt'  # Replace with your input file path
print(findConSinks(file_path))