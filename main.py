class LinearModel:
    def __init__(self):
        self.type = None
        self.variable_num = 0
        self.constraint_num = 0
        self.c_vector = []
        self.a_matrix = []
        self.b_vector = []

    def input(self):
        self.type = input("Enter the type of the problem (max/min): ")
        self.variable_num = int(input("Enter the number of variables: "))
        self.constraint_num = int(input("Enter the number of constraints: "))

        print("Enter the coefficients of the objective function:")
        for i in range(self.variable_num):
            self.c_vector.append(int(input(f"Enter the coefficient of x{i+1}: ")))

        print("Enter the coefficients of the constraints:")
        for i in range(self.constraint_num):
            constraint = []
            for j in range(self.variable_num):
                constraint.append(int(input(f"Enter the coefficient of x{j+1} in constraint {i+1}: ")))
            self.a_matrix.append(constraint)
            self.b_vector.append(int(input(f"Enter the value of the RHS of the constraint {i+1}: ")))

    def dual_calculator(self):
        dual = LinearModel()
        dual.type = 'max' if self.type == 'min' else 'min'
        dual.variable_num = self.constraint_num
        dual.constraint_num = self.variable_num
        dual.c_vector = self.b_vector

        for i in range(self.variable_num):
            constraint = []
            for j in range(self.constraint_num):
                constraint.append(self.a_matrix[j][i])
            dual.a_matrix.append(constraint)
            dual.b_vector.append(self.c_vector[i])

        return dual
    
    def print_model(self):
        if self.type == 'max':
            print("\nmax z = ", end='')
        elif self.type == 'min':
            print("\nmin z = ", end='')
        
        for i in range(self.variable_num):
            print(f"{self.c_vector[i]}x{i+1} + ", end='')
        
        print("\ns.t.")

        for i in range(self.constraint_num):
            for j in range(self.variable_num):
                print(f"{self.a_matrix[i][j]}x{j+1} + ", end='')
            print(" <= 0")
    
# Example Usage

model = LinearModel()
model.input()
model.print_model()
dual = model.dual_calculator()
dual.print_model()