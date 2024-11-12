from flask import Flask, render_template, request
from sympy import symbols, sympify, SympifyError

app = Flask(__name__)

x = symbols('x')

# Función del método de Regla Falsa
def regla_falsa(func, a, b, tol, max_iter=100):
    try:
        # Intentamos convertir la función a un objeto simbólico
        f = sympify(func)
    except SympifyError:
        return None, "La función proporcionada no es válida.", [], None, None

    iteraciones = []
    fa = f.subs(x, a)
    fb = f.subs(x, b)

    # Verificamos si hay un cambio de signo en el intervalo
    if fa * fb > 0:
        return None, "No hay raíces en el intervalo dado o hay un número par de raíces.", [], None, None

    raiz = None
    i = 0
    while i < max_iter:
        r = (a * fb - b * fa) / (fb - fa)
        fr = f.subs(x, r)

        # Guardamos la iteración
        iteraciones.append({
            'iteracion': i,
            'a': a,
            'b': b,
            'r': r,
            'f(r)': fr,
            'error_relativo': abs(fr)
        })

        # Verificamos la tolerancia
        if abs(fr) < tol:
            raiz = r
            return raiz, f"Raíz aproximada: {r}", iteraciones, abs(fr), i

        # Actualizamos los valores
        if fa * fr < 0:
            b = r
            fb = fr
        else:
            a = r
            fa = fr

        i += 1

    return None, "Se alcanzó el número máximo de iteraciones sin encontrar la raíz.", iteraciones, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    iteraciones = []
    error = None
    precision = None

    if request.method == 'POST':
        try:
            funcion = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            tol = float(request.form['tol'])

            # Incluimos un límite de iteraciones
            max_iter = 100

            # Llamamos a la función de Regla Falsa
            resultado, mensaje, iteraciones, precision, _ = regla_falsa(funcion, a, b, tol, max_iter)

            if not resultado:
                error = mensaje
        except Exception as e:
            error = f"Error: {e}"

    return render_template('index.html', resultado=resultado, iteraciones=iteraciones, precision=precision, error=error)
if __name__ == '__main__':
    app.run(port=8002)