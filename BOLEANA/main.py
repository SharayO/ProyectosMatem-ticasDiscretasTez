from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def boolean_calculator(expression, values):
    try:
        # Reemplazar operadores booleanos simbólicos por sus equivalentes en Python
        expression = expression.replace('∧', ' and ')
        expression = expression.replace('∨', ' or ')
        expression = expression.replace('¬', ' not ')
        expression = expression.replace('⊕', ' != ')
        expression = expression.replace('⊼', ' not (')  # Inicia NAND
        expression = expression.replace('⊽', ' not (')   # Inicia NOR

        # Reemplazar las variables A, B, C con sus valores
        for var, val in values.items():
            expression = expression.replace(var, str(val))

        # Añadir paréntesis de cierre para NAND y NOR
        expression = expression.replace('not (', 'not (') + ')' * (expression.count('not ('))

        # Evaluar la expresión en un entorno seguro
        result = eval(expression)
        return bool(result)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    a = request.form.get('a')
    b = request.form.get('b')
    c = request.form.get('c')
    expression = request.form.get('operation')

    # Mapear Verdadero/Falso a 1/0
    values = {
        'A': int(a),
        'B': int(b),
        'C': int(c)
    }

    result = boolean_calculator(expression, values)

    return jsonify({'result': result})

@app.route('/generate_table', methods=['POST'])
def generate_table():
    expression = request.form.get('operation')
    table = []

    # Generar todas las combinaciones posibles de A, B, C
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                values = {'A': a, 'B': b, 'C': c}
                result = boolean_calculator(expression, values)
                table.append({'A': a, 'B': b, 'C': c, 'Resultado': result})

    return jsonify({'table': table})

if __name__ == '__main__':
    app.run(port=8005)

