def displayMatrix(matrix):
    for i in matrix:
        for j in i:
            print(j,end = ' ')
        print()
    return matrix

def transpose(matrix):
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j]
    return matrix

def determinant(matrix):
    #Reducing the N order matrix to 2x2s and evaluating them
    if len(matrix)==2:
        return matrix[1][1]*matrix[0][0] - matrix[1][0]*matrix[0][1]
    else:
        det = 0
        for i in range(len(matrix)):
            subMatrix = [[] for alpha in range(len(matrix[0])-1)]
            subMatrixElementSelectionKey = 0
            topElement = matrix[0][i]
            for j in range(1,len(matrix)):
                for k in range(len(matrix)):
                    if k==i:
                        continue
                    else:
                        subMatrix[j-1].append(matrix[j][k])
                        subMatrixElementSelectionKey+=1
            det+=(-1)**(i)*matrix[0][i]*determinant(subMatrix)
        return det
                

N = int(input("Enter N for NxN matrix: "))
matrix = [[int(i) for i in input().split()] for j in range(N)]
print(N)

displayMatrix(transpose(matrix))
print(determinant(matrix))
print(determinant(matrix)-determinant(transpose(matrix)))