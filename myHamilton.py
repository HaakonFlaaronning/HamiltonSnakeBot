class MyHamilton():
    def __init__(self):
        self.graph = []
        self.path = []

    def makeHamiltonPath(self, rows, cols, matrix):
        if(rows%2 == 0 or cols%2 == 0):
            self.path.append(0)
            if(rows%2 != 0):
                dir = "down"
                currentColumn = 0
                for number in range(cols):
                    if(dir == "down"):
                        for i in range(1,rows):
                            self.path.append(matrix[i][currentColumn].nodeNumber)

                            if(i == rows-1):
                                self.path.append(self.path[len(self.path)-1]+1)
                                currentColumn += 1
                                dir = "up"
                    elif(dir == "up"):
                        if(self.path[len(self.path)-1] != rows*cols-1):
                            for i in range(rows-1,0,-1):
                                self.path.append(matrix[i][currentColumn].nodeNumber)
                                if(i == 1):
                                    self.path.append(self.path[len(self.path) - 1] + 1)
                                    currentColumn += 1
                                    dir = "down"
                        else:
                            for i in range(rows-1,-1,-1):
                                self.path.append(matrix[i][currentColumn].nodeNumber)
                            for j in range (cols-1,0,-1):
                                self.path.append(matrix[0][j].nodeNumber)
            elif (cols % 2 != 0):
                dir = "right"
                currentRow = 0
                for number in range(rows):
                    if (dir == "right"):
                        for i in range(1, cols):
                            self.path.append(matrix[currentRow][i].nodeNumber)

                            if (i == cols - 1):
                                self.path.append(self.path[len(self.path) - 1] + cols)
                                currentRow += 1
                                dir = "left"
                    elif (dir == "left"):
                        if (self.path[len(self.path) - 1] != rows * cols - 1):
                            for i in range(cols - 1, 0, -1):
                                self.path.append(matrix[currentRow][i].nodeNumber)

                                if (i == 1):
                                    self.path.append(self.path[len(self.path) - 1] + cols)
                                    currentRow += 1
                                    dir = "right"
                        else:
                            for i in range(cols - 1, -1, -1):
                                self.path.append(matrix[currentRow][i].nodeNumber)
                            for j in range(cols-1, 0,-1):
                                self.path.append(matrix[j][0].nodeNumber)
                #print(self.path)
        else:
            print("No hamilton path found")




