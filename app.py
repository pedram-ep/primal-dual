from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QLineEdit, QPushButton, QLabel, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QStackedWidget
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
import re
from main import LinearModel
# import 

integer_pattern = re.compile(r"^[0-9]+$")


class PrimalDualCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.regex = QRegularExpression(r"^[0-9]+$")
        self.validator = QRegularExpressionValidator(self.regex)

        self.be_model = LinearModel()

        self.var_int = 1
        self.cons_int = 1

        self.setWindowTitle("Primal to Dual Calculator")
        self.resize(400, 300)

        # calling functions
        self.numbers_input()

        self.widget_stack = QStackedWidget()
        self.setCentralWidget(self.widget_stack)
        self.widget_stack.addWidget(self.nums_widget)
        self.widget_stack.setCurrentWidget(self.nums_widget)
        self.accept_numbers.clicked.connect(lambda: self.accept_numbers_input())

    def numbers_input(self):
        # numbers layout
        var_text = QLabel()
        var_text.setText("Enter the number of variables: ")
        var_text.setFixedWidth(170)
        self.var_num = QLineEdit()
        self.var_num.setValidator(self.validator)
        self.var_num.setPlaceholderText("Variables Number")
        self.var_num.setFixedWidth(130)
        
        cons_text = QLabel()
        cons_text.setText("Enter the number of constraints: ")
        cons_text.setFixedWidth(170)
        self.cons_num = QLineEdit()
        self.cons_num.setValidator(self.validator)
        self.cons_num.setPlaceholderText("Constraints Number")
        self.cons_num.setFixedWidth(130)

        self.accept_numbers = QPushButton("Accept")

        nums_layout = QGridLayout()
        nums_layout.addWidget(var_text, 0, 0)
        nums_layout.addWidget(self.var_num, 0, 1)
        nums_layout.addWidget(cons_text, 1, 0)
        nums_layout.addWidget(self.cons_num, 1, 1)
        nums_layout.addWidget(self.accept_numbers, 2, 0)

        # numbers widget
        self.nums_widget = QWidget()
        self.nums_widget.setLayout(nums_layout)
    
    def calculator(self):
        # objective function layout
        obj_func_layout = QHBoxLayout()

        self.optimization_type = QComboBox()
        self.optimization_type.addItems(["max", "min"])
        objective_function_text = QLabel()
        objective_function_text.setText("z = ")
        obj_func_layout.addWidget(self.optimization_type)
        obj_func_layout.addWidget(objective_function_text)

        self.obj_coeffs = []
        for i in range(self.var_int):
            coeff = QLineEdit()
            coeff.setPlaceholderText(f'c_{i+1}')
            variable = QLabel()
            variable.setText(f'x{i+1}')
            obj_func_layout.addWidget(coeff)
            obj_func_layout.addWidget(variable)
            self.obj_coeffs.append(coeff)
        
        # constraints layout
        constraints_layout = QGridLayout()
        constraints_layout.addWidget(QLabel("s.t."), 0, 0)
        self.constraints = []
        self.constraint_signs = []
        self.rhs_values = []
        for i in range(self.cons_int):
            coeffs_line = []
            for j in range(self.var_int):
                coeff = QLineEdit()
                coeff.setPlaceholderText(f'a_({i+1},{j+1})')

                variable = QLabel()
                variable.setText(f'x_({i+1},{j+1})')
                
                constraints_layout.addWidget(coeff, i+1, 2*(j+1))
                constraints_layout.addWidget(variable, i+1, 2*(j+1)+1)
                coeffs_line.append(coeff)
            self.constraints.append(coeffs_line)

            sign = QComboBox()
            sign.addItems(['<=', '=', '>='])
            constraints_layout.addWidget(sign, i+1, 2*(int(self.var_num.text())+1))
            self.constraint_signs.append(sign)

            rhs_value = QLineEdit()
            rhs_value.setPlaceholderText(f'b_{i+1}')
            constraints_layout.addWidget(rhs_value, i+1, 2*(int(self.var_num.text())+1)+1)
            self.rhs_values.append(rhs_value)
        
        # variable signs layout
        variable_signs_layout = QHBoxLayout()
        variable_signs_layout.addWidget(QLabel("and"))
        self.variable_signs = []
        for i in range(self.var_int):
            variable = QLabel()
            variable.setText(f', x_{i+1}') if i != 0 else variable.setText('x_1')
            variable_signs_layout.addWidget(variable)

            sign = QComboBox()
            sign.addItems(['>= 0', 'urs', '<= 0'])
            variable_signs_layout.addWidget(sign)

            self.variable_signs.append(sign)
        
        # accept button
        accept_button = QPushButton("Accept")
        accept_button.clicked.connect(lambda: self.accept_calc_input())
        accept_layout = QVBoxLayout()
        accept_layout.addWidget(QLabel(''))
        accept_layout.addWidget(accept_button)

        # calculator layout
        self.calculator_layout = QVBoxLayout()
        self.calculator_layout.addLayout(obj_func_layout)
        self.calculator_layout.addLayout(constraints_layout)
        self.calculator_layout.addLayout(variable_signs_layout)
        self.calculator_layout.addLayout(accept_layout)

        # calculator widget
        self.calc_widget = QWidget()
        self.calc_widget.setLayout(self.calculator_layout)

    def accept_numbers_input(self):
        self.var_int = int(self.var_num.text()) if self.var_num.text() != '' else 2
        self.cons_int = int(self.cons_num.text()) if self.cons_num.text() != '' else 1
        self.calculator()
        self.widget_stack.addWidget(self.calc_widget)
        self.widget_stack.setCurrentIndex((self.widget_stack.currentIndex() + 1) % self.widget_stack.count())
        self.resize((self.var_int)*400, (self.cons_int+4)*25)
    
    def accept_calc_input(self):
        variable_signs = []
        for sign in self.variable_signs:
            if sign.currentText() == 'urs':
                variable_signs.append('free')
            elif sign.currentText() == '>= 0':
                variable_signs.append('>=')
            else:
                variable_signs.append('<=')

        self.be_model.input_gui(
            self.optimization_type.currentText(),
            self.var_int,
            self.cons_int,
            [int(coeff.text()) for coeff in self.obj_coeffs],
            [[int(coeff.text()) for coeff in line] for line in self.constraints],
            [sign.currentText() for sign in self.constraint_signs],
            [int(rhs.text()) for rhs in self.rhs_values],
            [sign for sign in variable_signs]
        )

        self.d_be_model = self.be_model.dual_calculator()
        self.be_model.print_model()
        self.d_be_model.print_model()

        self.show_models()
        self.widget_stack.addWidget(self.models_widget)
        self.widget_stack.setCurrentIndex((self.widget_stack.currentIndex() + 1) % self.widget_stack.count())
    
    def show_models(self):
        # show primal model
        primal_model = QVBoxLayout()

        primal_text = QLabel()
        primal_text.setText('Primal Model: ')
        primal_text.setStyleSheet("font-size: 16px;")
        primal_model.addWidget(primal_text)

        # objective function
        obj_func_line = QLineEdit()
        obj_func_line.setText(self.be_model.obj_func_str())
        obj_func_line.setReadOnly(True)
        primal_model.addWidget(obj_func_line)

        # constraints
        primal_model.addWidget(QLabel("s.t."))
        lines = self.be_model.constraints_str_list()
        for i in range(self.be_model.constraint_num):
            constraint_line = QLineEdit()
            constraint_line.setText(lines[i])
            constraint_line.setReadOnly(True)
            primal_model.addWidget(constraint_line)

        # variable signs
        primal_model.addWidget(QLabel(''))
        variable_signs = QLineEdit()
        variable_signs.setText(self.be_model.var_signs_str())
        variable_signs.setReadOnly(True)
        primal_model.addWidget(variable_signs)

        ######
        # show dual model
        dual_model = QVBoxLayout()
        
        dual_text = QLabel()
        dual_text.setText('Dual Model: ')
        dual_text.setStyleSheet("font-size: 16px;")
        dual_model.addWidget(dual_text)

        # objective function
        dual_obj_func_line = QLineEdit()
        dual_obj_func_line.setText(self.d_be_model.obj_func_str())
        dual_obj_func_line.setReadOnly(True)
        dual_model.addWidget(dual_obj_func_line)

        # constraints
        dual_model.addWidget(QLabel("s.t."))
        dual_lines = self.d_be_model.constraints_str_list()
        for i in range(self.d_be_model.constraint_num):
            constraint_line = QLineEdit()
            constraint_line.setText(dual_lines[i])
            constraint_line.setReadOnly(True)
            dual_model.addWidget(constraint_line)

        # variable signs
        dual_model.addWidget(QLabel(''))
        dual_variable_signs = QLineEdit()
        dual_variable_signs.setText(self.d_be_model.var_signs_str())
        dual_variable_signs.setReadOnly(True)
        dual_model.addWidget(dual_variable_signs)


        # show models layout
        self.models_layout = QHBoxLayout()
        self.models_layout.addLayout(primal_model)
        self.models_layout.addLayout(dual_model)

        # show models widget
        self.models_widget = QWidget()
        self.models_widget.setLayout(self.models_layout)




app = QApplication([])

window = PrimalDualCalculator()
window.show()

app.exec()