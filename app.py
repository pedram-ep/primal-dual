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
from main import LinearModel


class PrimalDualCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.nums_validator = QRegularExpressionValidator(QRegularExpression(r"^[0-9]+$"))
        self.int_validator = QRegularExpressionValidator(QRegularExpression(r"^-?[0-9]+$"))

        self.initializer()
    
    def initializer(self):
        self.be_model = LinearModel()

        self.var_int = 1
        self.cons_int = 1

        self.setWindowTitle("Primal to Dual Calculator")
        self.resize(400, 300)

        # numbers method widgets
        self.var_num = QLineEdit()
        self.cons_num = QLineEdit()
        self.accept_numbers = QPushButton("Next")
        self.nums_widget = QWidget()

        # calculator method widget
        self.optimization_type = QComboBox()
        self.obj_coeffs = []
        self.constraints = []
        self.constraint_signs = []
        self.rhs_values = []
        self.variable_signs = []
        self.calc_accept_button = QPushButton("Accept")
        self.calculator_layout = QVBoxLayout()
        self.calc_widget = QWidget()

        # show models method widget
        self.exit = QPushButton("Exit")
        # self.restart = QPushButton("Start a new conversion")
        self.models_layout = QVBoxLayout()
        self.models_widget = QWidget()

        # calling functions
        self.numbers_input()

        self.widget_stack = QStackedWidget()
        self.setCentralWidget(self.widget_stack)
        self.widget_stack.addWidget(self.nums_widget)
        self.widget_stack.setCurrentWidget(self.nums_widget)

    def numbers_input(self):
        # numbers layout
        var_text = QLabel()
        var_text.setText("Enter the number of variables: ")
        var_text.setFixedWidth(170)
        
        self.var_num.setValidator(self.nums_validator)
        self.var_num.setPlaceholderText("Variables Number")
        self.var_num.setFixedWidth(130)
        
        cons_text = QLabel()
        cons_text.setText("Enter the number of constraints: ")
        cons_text.setFixedWidth(170)
        
        self.cons_num.setValidator(self.nums_validator)
        self.cons_num.setPlaceholderText("Constraints Number")
        self.cons_num.setFixedWidth(130)
        
        self.accept_numbers.clicked.connect(lambda: self.accept_numbers_input())

        nums_layout = QGridLayout()
        nums_layout.addWidget(var_text, 0, 0)
        nums_layout.addWidget(self.var_num, 0, 1)
        nums_layout.addWidget(cons_text, 1, 0)
        nums_layout.addWidget(self.cons_num, 1, 1)
        nums_layout.addWidget(self.accept_numbers, 2, 0)

        # numbers widget
        self.nums_widget.setLayout(nums_layout)
    
    def calculator(self):
        # objective function layout
        obj_func_layout = QHBoxLayout()

        
        self.optimization_type.addItems(["max", "min"])
        objective_function_text = QLabel()
        objective_function_text.setText("z = ")
        obj_func_layout.addWidget(self.optimization_type)
        obj_func_layout.addWidget(objective_function_text)

        
        for i in range(self.var_int):
            coeff = QLineEdit()
            coeff.setPlaceholderText(f'c_{i+1}')
            coeff.setValidator(self.int_validator)
            variable = QLabel()
            variable.setText(f'x{i+1}')
            obj_func_layout.addWidget(coeff)
            obj_func_layout.addWidget(variable)
            self.obj_coeffs.append(coeff)
        
        # constraints layout
        constraints_layout = QGridLayout()
        constraints_layout.addWidget(QLabel("s.t."), 0, 0)
        for i in range(self.cons_int):
            coeffs_line = []
            for j in range(self.var_int):
                coeff = QLineEdit()
                coeff.setPlaceholderText(f'a_({i+1},{j+1})')
                coeff.setValidator(self.int_validator)

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
            rhs_value.setValidator(self.int_validator)
            constraints_layout.addWidget(rhs_value, i+1, 2*(int(self.var_num.text())+1)+1)
            self.rhs_values.append(rhs_value)
        
        # variable signs layout
        variable_signs_layout = QHBoxLayout()
        variable_signs_layout.addWidget(QLabel("and"))
        for i in range(self.var_int):
            variable = QLabel()
            variable.setText(f', x_{i+1}') if i != 0 else variable.setText('x_1')
            variable_signs_layout.addWidget(variable)

            sign = QComboBox()
            sign.addItems(['>= 0', 'urs', '<= 0'])
            variable_signs_layout.addWidget(sign)

            self.variable_signs.append(sign)
        
        # accept button
        
        self.calc_accept_button.clicked.connect(lambda: self.accept_calc_input())
        accept_layout = QVBoxLayout()
        accept_layout.addWidget(QLabel(''))
        accept_layout.addWidget(self.calc_accept_button)

        # calculator layout

        self.calculator_layout.addLayout(obj_func_layout)
        self.calculator_layout.addLayout(constraints_layout)
        self.calculator_layout.addLayout(variable_signs_layout)
        self.calculator_layout.addLayout(accept_layout)

        # calculator widget
        self.calc_widget.setLayout(self.calculator_layout)

    def accept_numbers_input(self):
        self.var_int = int(self.var_num.text()) if self.var_num.text() != '' else 2
        self.cons_int = int(self.cons_num.text()) if self.cons_num.text() != '' else 1
        self.calculator()
        self.widget_stack.addWidget(self.calc_widget)
        self.widget_stack.setCurrentIndex((self.widget_stack.currentIndex() + 1) % self.widget_stack.count())
    
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

        self.show_models()
        self.widget_stack.addWidget(self.models_widget)
        self.widget_stack.setCurrentIndex((self.widget_stack.currentIndex() + 1) % self.widget_stack.count())
    
    def show_models(self):
        # show primal model
        primal_model = QVBoxLayout()

        primal_text = QLabel()
        primal_text.setText('Primal Model: ')
        primal_text.setStyleSheet("font-size: 16px;")
        primal_model.addWidget(primal_text, alignment=Qt.AlignmentFlag.AlignTop)

        # objective function
        obj_func_line = QLineEdit()
        obj_func_line.setText(self.be_model.obj_func_str())
        obj_func_line.setReadOnly(True)
        primal_model.addWidget(obj_func_line, alignment=Qt.AlignmentFlag.AlignTop)

        # constraints
        primal_model.addWidget(QLabel("s.t."))
        lines = self.be_model.constraints_str_list()
        for i in range(self.be_model.constraint_num):
            constraint_line = QLineEdit()
            constraint_line.setText(lines[i])
            constraint_line.setReadOnly(True)
            primal_model.addWidget(constraint_line, alignment=Qt.AlignmentFlag.AlignVCenter)

        # variable signs
        primal_model.addWidget(QLabel(''))
        variable_signs = QLineEdit()
        variable_signs.setText(self.be_model.var_signs_str())
        variable_signs.setReadOnly(True)
        primal_model.addWidget(variable_signs, alignment=Qt.AlignmentFlag.AlignBottom)

        ######
        # show dual model
        dual_model = QVBoxLayout()
        
        dual_text = QLabel()
        dual_text.setText('Dual Model: ')
        dual_text.setStyleSheet("font-size: 16px;")
        dual_model.addWidget(dual_text, alignment=Qt.AlignmentFlag.AlignTop)

        # objective function
        dual_obj_func_line = QLineEdit()
        dual_obj_func_line.setText(self.d_be_model.obj_func_str())
        dual_obj_func_line.setReadOnly(True)
        dual_model.addWidget(dual_obj_func_line, alignment=Qt.AlignmentFlag.AlignTop)

        # constraints
        dual_model.addWidget(QLabel("s.t."))
        dual_lines = self.d_be_model.constraints_str_list()
        for i in range(self.d_be_model.constraint_num):
            constraint_line = QLineEdit()
            constraint_line.setText(dual_lines[i])
            constraint_line.setReadOnly(True)
            dual_model.addWidget(constraint_line, alignment=Qt.AlignmentFlag.AlignVCenter)

        # variable signs
        dual_model.addWidget(QLabel(''))
        dual_variable_signs = QLineEdit()
        dual_variable_signs.setText(self.d_be_model.var_signs_str())
        dual_variable_signs.setReadOnly(True)
        dual_model.addWidget(dual_variable_signs, alignment=Qt.AlignmentFlag.AlignBottom)

        # answers layout
        answers = QHBoxLayout()
        answers.addLayout(primal_model)
        answers.addLayout(dual_model)

        # buttons layout
        self.exit.clicked.connect(lambda: self.close())
        # self.restart.clicked.connect(lambda: self.widget_stack.setCurrentIndex((self.widget_stack.currentIndex() + ) % self.widget_stack.count()) and self.initializer())

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.exit)
        # buttons_layout.addWidget(self.restart)


        # show models layout
        
        self.models_layout.addLayout(answers)
        self.models_layout.addLayout(buttons_layout)

        # show models widget
        
        self.models_widget.setLayout(self.models_layout)


def main():
    app =  QApplication([])
    window = PrimalDualCalculator()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()