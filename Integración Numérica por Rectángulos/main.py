from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Función que define la integral por el método de los rectángulos
def rectangulo_integration(fx, a, b, n):
    # Definir las funciones trigonométricas, inversas y matemáticas de SymPy
    x = sp.symbols('x')
    f = sp.sympify(fx, locals={
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'log': sp.log, 'exp': sp.exp, 'sqrt': sp.sqrt
    })

    # Convertir los límites a floats
    a = float(a)
    b = float(b)

    # Calcular el ancho de los subintervalos
    h = (b - a) / n
    result = {'left': 0, 'right': 0, 'middle': 0}

    # Cálculo para el método del punto extremo izquierdo
    for i in range(n):
        result['left'] += f.subs(x, a + i * h)

    # Cálculo para el método del punto extremo derecho
    for i in range(1, n + 1):
        result['right'] += f.subs(x, a + i * h)

    # Cálculo para el método del punto medio
    for i in range(n):
        result['middle'] += f.subs(x, a + (i + 0.5) * h)

    # Multiplicar por el ancho del subintervalo
    for key in result:
        result[key] = float(result[key] * h)

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    result = None
    error = None

    try:
        # Obtener datos del formulario
        fx = request.form['fx']
        a = request.form['a']
        b = request.form['b']
        n = request.form['n']

        # Asegúrate de que los valores de a, b y n sean válidos
        a = float(a)
        b = float(b)
        n = int(n)

        # Llamar a la función para calcular la integral
        result = rectangulo_integration(fx, a, b, n)
    except Exception as e:
        error = f"Error: {str(e)}"

    # Devolver la plantilla con los resultados y mantener los valores en los campos del formulario
    return render_template('index.html', result=result, error=error, fx=fx, a=a, b=b, n=n)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
