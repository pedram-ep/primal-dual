class LinearModel:
    def __init__(self):
        self.type = None
        self.variable_num = 0
        self.constraint_num = 0
        self.c_vector = []
        self.a_matrix = []
        self.b_vector = []
        self.constraint_signs = []
        self.variable_signs = []

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
            self.constraint_signs.append(input(f"Enter the sign of the constraint {i+1} (<=, =, >=): "))
            self.b_vector.append(int(input(f"Enter the value of the RHS of the constraint {i+1}: ")))
        
        print("Enter the declaration of the variables:")
        for i in range(self.variable_num):
            self.variable_signs.append(input(f"Enter the sign of x{i+1} (>=, free, <=): "))


    def dual_calculator(self):
        dual = LinearModel()
        dual.type = 'min' if self.type == 'max' else 'max'
        dual.variable_num = self.constraint_num
        dual.constraint_num = self.variable_num

        for i in range(dual.variable_num):
            dual.c_vector.append(self.b_vector[i])

        for i in range(dual.constraint_num):
            constraint = []
            for j in range(dual.variable_num):
                constraint.append(self.a_matrix[j][i])
            dual.a_matrix.append(constraint)
            dual.constraint_signs.append('=')
            dual.b_vector.append(self.c_vector[i])
        
        for i in range(dual.constraint_num):
            if self.variable_signs[i] == '<=':
                dual.variable_signs.append('>=') 
            elif self.variable_signs[i] == '>=':
                dual.variable_signs.append('<=') 
            else:
                dual.variable_signs.append('free')
        
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
            print(f"{self.constraint_signs[i]} {self.b_vector[i]}")
    
# Example Usage

model = LinearModel()
model.input()
model.print_model()
dual = model.dual_calculator()
dual.print_model()