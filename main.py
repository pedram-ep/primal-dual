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


    def test_example(self):
        self.type = 'min'

        self.variable_num = 3
        self.constraint_num = 5
        self.c_vector = [3, -2, 4]
        self.a_matrix = [[3, 5, 4], [6, 1, 3], [7, -2, -1], [1, -2, 5], [4, 7, -2]]
        self.constraint_signs = ['>=', '>=', '<=', '>=', '>=']
        self.b_vector = [7, 4, 10, 3, 2]
        self.variable_signs = ['>=', '>=', '>=']


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
        # printing the objective function
        print("\nmax z = " if self.type == 'max' else "\nmin z = ", end='')
        
        for i in range(self.variable_num):
            if i+1 < self.variable_num:
                print(f"{self.c_vector[i]}x{i+1} + ", end='')
            else:
                print(f"{self.c_vector[i]}x{i+1}", end='')
        
        # printing the constraints
        print("\ns.t.")

        for i in range(self.constraint_num):
            for j in range(self.variable_num):
                if j+1 < self.variable_num:
                    print(f"{self.a_matrix[i][j]}x{j+1} + ", end='')
                else:
                    print(f"{self.a_matrix[i][j]}x{j+1} ", end='')
            print(f"{self.constraint_signs[i]} {self.b_vector[i]}")
        

        # printing the sign of the variables
        non_negative_variables = []
        non_positive_variables = []
        free_variables = []
        for i in range(len(self.variable_signs)):
            if self.variable_signs[i] == '>=':
                non_negative_variables.append(f"x{i+1}")
            elif self.variable_signs[i] == '<=':
                non_positive_variables.append(f"x{i+1}")
            else:
                free_variables.append(f"x{i+1}")
        print('and ', end='')
        for i in range(len(non_negative_variables)):
            print(f"{non_negative_variables[i]}", end=' ')
            if i != len(non_negative_variables) - 1:
                print(', ', end='')
        if len(non_negative_variables) > 0:
                if len(free_variables) > 0 or len(non_positive_variables) > 0:
                    print(">= 0 and ", end='')
                else:
                    print(">= 0", end='')
        for i in range(len(non_positive_variables)):
            print(f"{non_positive_variables[i]}", end=' ')
            if i != len(non_positive_variables) - 1:
                print(', ', end='')
        if len(non_positive_variables) > 0:
                if len(free_variables) > 0:
                    print("<= 0 and ", end='')
                else:
                    print("<= 0", end='')
        for i in range(len(free_variables)):
            print(f"{free_variables[i]} is free", end=' ')
            if i != len(free_variables) - 1:
                print(', ', end='')
        if len(free_variables) > 0:
                print("is free", end='')
        print()

# example Usage
model = LinearModel()
model.test_example()
model.print_model()
dual = model.dual_calculator()
dual.print_model()