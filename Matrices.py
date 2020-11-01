class Matrix:
    def __init__(self, N):
        self.N = self.order = self.dimensions = N
        self.matrix = self.constructMatrix()

    def __str__(self):
        self.displayMatrix()
        return ''
    
    def constructMatrix(self):
        return [[int(i) for i in input().split()] for j in range(self.N)]

    def displayMatrix(self):
        for i in self.matrix:
            for j in i:
                print(j,end = ' ')
            print()
        return self.matrix

    def isSymmetric(self):
        return self.matrix == self.transpose()

    def transpose(self):
        for i in range(len(self.matrix)):
            #Iterating throught the matrix by increasing column number every time to not make the net result 0 change
            for j in range(i, len(self.matrix)):
                #Swapping the matrix elements in transpose conditions
                self.matrix[i][j],self.matrix[j][i] = self.matrix[j][i],self.matrix[i][j]
        return self.matrix

    def determinant(self):
        #Reducing the N order matrix to 2x2s and evaluating them
        #Alternatively they can be converted to 1x1s and they don't need to be evaulated, but time complexity might be more in some cases
        #Like this:
        # if len(matrix) == 1:
        #     return matrix[0][0]
        if len(self.matrix)==2:
            return self.matrix[1][1]*self.matrix[0][0] - self.matrix[1][0]*self.matrix[0][1]
        
        else:
            self.det = 0
            for i in range(len(self.matrix)):
                self.subMatrix = SubMatrix(len(self.matrix[0])-1)
                topElement = self.matrix[0][i]
                #j starts from 1 to exclude the first row in the determinant calculation
                for j in range(1,len(self.matrix)):
                    for k in range(len(self.matrix)):
                        #k==i is excluded for subMatrix calculation
                        if k==i:
                            continue
                        else:
                            self.subMatrix.matrix[j-1].append(self.matrix[j][k])
                #cofactor is calculated
                self.det+=(-1)**(i)*topElement*self.subMatrix.determinant()
            return self.det

#Creating a class SubMatrix that has all methods of Matrix but the form of creation is different. This one unlike Matrix is not user defined.
class SubMatrix(Matrix):
    def __init__(self, N):
        self.matrix = [[] for alpha in range(N)]

if __name__ == "__main__":   
    N = int(input("Enter N for NxN matrix: "))
    matrix = Matrix(N)
    print(f"{matrix.determinant()} is the determinant of this matrix")