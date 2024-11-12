from flask import Flask, render_template, request, jsonify
import sympy as sp
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    funcion = data.get('funcion', '')
    valor_x = data.get('valor_x', '')

    # Definir la variable simbólica x
    x = sp.symbols('x')

    # Definir las funciones trigonométricas, sus inversas y la constante de Euler
    funciones = {
        'sin': sp.sin,
        'cos': sp.cos,
        'tan': sp.tan,
        'csc': sp.csc,
        'sec': sp.sec,
        'cot': sp.cot,
        'asin': sp.asin,
        'acos': sp.acos,
        'atan': sp.atan,
        'acsc': sp.acsc,
        'asec': sp.asec,
        'acot': sp.acot,
        'exp': sp.exp,  # Función exponencial para e^x
        'ln': sp.log 
    }

    try:
        # Reemplazar ^ con ** para la potencia
        funcion = funcion.replace('^', '**')

        # Asegurar que los coeficientes sean explícitos en la multiplicación con la variable
        funcion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion)

        # Interpretar la función con SymPy, utilizando las funciones trigonométricas y exponenciales definidas
        funcion_sympy = sp.sympify(funcion, locals=funciones)

        # Convertir valor_x a una expresión simbólica
        valor_x_sympy = sp.sympify(valor_x)

        # Evaluar la función en el valor dado de x, manteniendo la forma simbólica
        resultado_simplificado = funcion_sympy.subs(x, valor_x_sympy)

        # Obtener el valor numérico del resultado
        resultado_numerico = resultado_simplificado.evalf()

    except Exception as e:
        return jsonify({'error': f"Error en la función: {e}"})

    return jsonify({
        'expresion': str(resultado_simplificado),
        'resultado': str(resultado_numerico)
    })

if __name__ == '__main__':
    app.run(port=8008)
