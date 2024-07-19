class LinearModel:
    def __init__(self):
        self.optimization_type = None
        self.type = 'primal'
        self.variable_num = 0
        self.constraint_num = 0

        # variable coeffs in the objective function
        self.c_vector = []

        # constraints coeffs
        self.a_matrix = []

        # constraints RHS
        self.b_vector = []

        # variables and constraints signs
        self.constraint_signs = []
        self.variable_signs = []

    def input(self):
        self.optimization_type = input("Enter the type of the problem (max/min): ")
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

    def input_gui(self, optimization_type, variable_num, constraint_num, c_vector, a_matrix, constraint_signs, b_vector, variable_signs):
        self.optimization_type = optimization_type
        self.variable_num = variable_num
        self.constraint_num = constraint_num
        self.c_vector = c_vector
        self.a_matrix = a_matrix
        self.constraint_signs = constraint_signs
        self.b_vector = b_vector
        self.variable_signs = variable_signs

    def test_example(self):
        self.optimization_type = 'min'

        self.variable_num = 3
        self.constraint_num = 5
        self.c_vector = [3, -2, 4]
        self.a_matrix = [[3, 5, 4], [6, 1, 3], [7, -2, -1], [1, -2, 5], [4, 7, -2]]
        self.constraint_signs = ['>=', '>=', '<=', '>=', '=']
        self.b_vector = [7, 4, 10, 3, 2]
        self.variable_signs = ['>=', '>=', 'free']

    def min_normalizer(self):
        for i in range(self.constraint_num):
                if self.constraint_signs[i] == '<=':
                    self.constraint_signs[i] = '>='
                    for j in range(self.variable_num):
                        self.a_matrix[i][j] *= -1
                    self.b_vector[i] *= -1
    
    def max_normalizer(self):
        for i in range(self.constraint_num):
                if self.constraint_signs[i] == '>=':
                    self.constraint_signs[i] = '<='
                    for j in range(self.variable_num):
                        self.a_matrix[i][j] *= -1
                    self.b_vector[i] *= -1

    def model_normalizer(self):
        if self.optimization_type == 'min':
            self.min_normalizer()
        elif self.optimization_type == 'max':
            self.max_normalizer()

    def dual_calculator(self):
        # normalizing the model
        self.model_normalizer()

        # creating the dual model
        dual = LinearModel()
        dual.type = 'dual'
        
        # changing the type of optimization
        dual.optimization_type = 'min' if self.optimization_type == 'max' else 'max'

        # swapping the number of constraints and variables
        dual.variable_num = self.constraint_num
        dual.constraint_num = self.variable_num

        # the c vector of the dual is the b vector of the primal
        for i in range(dual.variable_num):
            dual.c_vector.append(self.b_vector[i])

        # the a matrix of the dual is the transpose of the a matrix of the primal
        for i in range(dual.constraint_num):
            constraint = []
            for j in range(dual.variable_num):
                constraint.append(self.a_matrix[j][i])
            dual.a_matrix.append(constraint)
            dual.constraint_signs.append('=')
            dual.b_vector.append(self.c_vector[i])
        
        # setting the dual model variable signs
        # min to max
        for i in range(dual.variable_num):
            if self.constraint_signs[i] == '=':
                dual.variable_signs.append('free')
            elif self.constraint_signs[i] == '>=':
                if self.optimization_type == 'min':
                    dual.variable_signs.append('>=')
                else:
                    dual.variable_signs.append('<=')
            elif self.constraint_signs[i] == '<=':
                if self.optimization_type == 'min':
                    dual.variable_signs.append('<=')
                else:
                    dual.variable_signs.append('>=') 
        
        # setting the dual model constraints signs
        for i in range(dual.constraint_num):
            if self.variable_signs[i] == 'free':
                dual.constraint_signs[i] = '='
            elif self.variable_signs[i] == '>=':
                if self.optimization_type == 'min':
                    dual.constraint_signs[i] = '<='
                else:
                    dual.constraint_signs[i] = '>='
            elif self.variable_signs[i] == '<=':
                if self.optimization_type == 'min':
                    dual.constraint_signs[i] = '>='
                else:
                    dual.constraint_signs[i] = '<='
        return dual
    
    def print_model(self):
        # printing the objective function
        print(self.obj_func_str())
        # print("max z = " if self.optimization_type == 'max' else "min z = ", end='')
        
        # str = "".join([f"{' +' if val > 0 else ' -'} {abs(val)}{'x' if self.type == 'primal' else 'y'}{i+1}" for i, val in enumerate(self.c_vector)])
        # print(str[1:])
        
        # printing the constraints
        print("s.t.")
        lines = self.constraints_str_list()
        print("\n".join(lines))

        # printing the sign of the variables
        print(self.var_signs_str())

    def constraints_str_list(self):
        lines = []
        for i, row in enumerate(self.a_matrix):
            str = "".join([f"{' +' if val > 0 else ' -'} {abs(val)}{'x' if self.type == 'primal' else 'y'}{i+1}" for i, val in enumerate(row)])
            str += ' '
            str += f"{self.constraint_signs[i]} {self.b_vector[i]}"
            lines.append(str)
        return lines
    
    def obj_func_str(self):
        str = ""
        str += "".join("max z =" if self.optimization_type == 'max' else "min z =")
        str += "".join([f"{' +' if val > 0 else ' -'} {abs(val)}{'x' if self.type == 'primal' else 'y'}{i+1}" for i, val in enumerate(self.c_vector)])
        return str

    def var_signs_str(self):
        str = ''
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
        
        str += ''.join('and ')

        for i in range(len(non_negative_variables)):
            str += ''.join(f"{non_negative_variables[i]}")
            if i != len(non_negative_variables) - 1:
                str += ''.join(', ')
        if len(non_negative_variables) > 0:
                if len(free_variables) > 0 or len(non_positive_variables) > 0:
                    str += ''.join(">= 0 and ")
                else:
                    str += ''.join(">= 0")
        for i in range(len(non_positive_variables)):
            str += ''.join(f"{non_positive_variables[i]}")
            if i != len(non_positive_variables) - 1:
                str += ''.join(', ')
        if len(non_positive_variables) > 0:
                if len(free_variables) > 0:
                    str += ''.join("<= 0 and ")
                else:
                    str += ''.join("<= 0")
        for i in range(len(free_variables)):
            str += ''.join(f"{free_variables[i]} URS")
            if i != len(free_variables) - 1:
                str += ''.join(', ')
        return str


# # example Usage
# model = LinearModel()
# if input("Do you want to enter your model? (y/n): ") == 'y':
#     model.input()
# else:
#     model.test_example()

# print('\nGiven Model:')
# model.print_model()

# dual = model.dual_calculator()

# print('\nNormalized Model:')
# model.print_model()

# print('\nDual Model:')
# dual.print_model()