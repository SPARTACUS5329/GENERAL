def displayMatrix(matrix):
    for i in matrix:
        for j in i:
            print(j,end = ' ')
        print()
    return matrix

def transpose(matrix):
    for i in range(len(matrix)):
        #Iterating throught the matrix by increasing column number every time to not make the net result 0 change
        for j in range(i, len(matrix)):
            #Swapping the matrix elements in transpose conditions
            matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j]
    return matrix

def determinant(matrix):
    #Reducing the N order matrix to 2x2s and evaluating them
    #Alternatively they can be converted to 1x1s and they don't need to be evaulated, but time complexity might be more in some cases
    #Like this:
    # if len(matrix) == 1:
    #     return matrix[0][0]
    if len(matrix)==2:
        return matrix[1][1]*matrix[0][0] - matrix[1][0]*matrix[0][1]
    
    else:
        det = 0
        for i in range(len(matrix)):
            subMatrix = [[] for alpha in range(len(matrix[0])-1)]
            topElement = matrix[0][i]
            #j starts from 1 to exclude the first row in the determinant calculation
            for j in range(1,len(matrix)):
                for k in range(len(matrix)):
                    #k==i is excluded for subMatrix calculation
                    if k==i:
                        continue
                    else:
                        subMatrix[j-1].append(matrix[j][k])
            #cofactor is calculated
            det+=(-1)**(i)*topElement*determinant(subMatrix)
        return det
                
if __name__ == "__main__":   
    N = int(input("Enter N for NxN matrix: "))
    matrix = [[int(i) for i in input().split()] for j in range(N)]
    displayMatrix(transpose(matrix))
    print(f"{determinant(matrix)} is the determinant of this matrix")
    print(f"{determinant(matrix)-determinant(transpose(matrix))} is a simple check to see the determinant works. Because det(A) = det(transpose(A))")
