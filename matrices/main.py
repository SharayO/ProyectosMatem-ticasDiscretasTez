from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para realizar la operación de matrices
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Obtener el tamaño de la matriz
        size = int(request.form.get('size'))

        # Obtener las matrices ingresadas por el usuario
        matrix_a = []
        for i in range(size):
            row = []
            for j in range(size):
                value = float(request.form.get(f'a_{i}_{j}'))  # Obtenemos el valor de cada celda de la matriz A
                row.append(value)
            matrix_a.append(row)

        # Convertir la matriz A a un objeto numpy
        matrix_a = np.array(matrix_a)

        # Procesar la matriz B de manera similar
        matrix_b = []
        for i in range(size):
            row = []
            for j in range(size):
                value = float(request.form.get(f'b_{i}_{j}'))  # Obtenemos el valor de cada celda de la matriz B
                row.append(value)
            matrix_b.append(row)

        matrix_b = np.array(matrix_b)

        # Obtener la operación seleccionada
        operation = request.form.get('operation')

        # Realizamos la operación seleccionada
        if operation == 'add':
            result = matrix_a + matrix_b
        elif operation == 'multiply':
            result = matrix_a @ matrix_b
        else:
            return "Operación no soportada"

        return render_template('index.html', result=result, size=size)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8045)
