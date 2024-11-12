from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Función para el método de bisección
def biseccion(f, a, b, tol):
    n = 0
    try:
        fa = f(a)
        fb = f(b)
    except Exception as e:
        return None, None, f"Error al evaluar la función: {e}"

    # Verificar si los límites son correctos (a < b)
    if a >= b:
        return None, None, "El límite inferior debe ser menor que el límite superior."

    # Verificar si hay signos opuestos en a y b
    if fa * fb >= 0:
        return None, None, "El intervalo no contiene una raíz adecuada (la función debe tener signos opuestos en a y b)."

    iteraciones = []  # Lista para almacenar las iteraciones
    while (b - a) / 2.0 > tol:
        n += 1
        midpoint = (a + b) / 2.0
        try:
            fm = f(midpoint)
        except Exception as e:
            return None, None, f"Error al evaluar la función en el punto medio: {e}"

        # Guardar la iteración
        iteraciones.append({
            'iteracion': n,
            'a': a,
            'b': b,
            'fa': fa,               # Valor de f(a)
            'fb': fb,               # Valor de f(b)
            'midpoint': midpoint,   # Punto medio (rn)
            'fm': fm,               # Valor de f(midpoint)
            'error_relativo': abs((b - a) / 2.0)  # Error relativo
        })

        if fm == 0:
            return midpoint, 0, iteraciones  # Raíz exacta
        elif fa * fm < 0:
            b = midpoint
            fb = fm  # Actualiza fb
        else:
            a = midpoint
            fa = fm  # Actualiza fa

    return (a + b) / 2.0, abs(b - a) / 2.0, iteraciones

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Leer la función, los límites y la tolerancia
            funcion_str = request.form["funcion"]
            a = float(request.form["a"])
            b = float(request.form["b"])
            tol = float(request.form["tol"])

            # Convertir la función en una función de Python
            f = lambda x: eval(funcion_str, {"x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, 
                                             "cot": sp.cot, "asin": sp.asin, "acos": sp.acos, 
                                             "atan": sp.atan, "exp": sp.exp, "ln": sp.log})

            # Ejecutar el método de bisección
            raiz, error, iteraciones = biseccion(f, a, b, tol)

            if raiz is None:
                resultado = iteraciones  # Mostramos el error que viene del método de bisección
            else:
                resultado = f"Raíz aproximada: {raiz}, Error: {error}, Iteraciones: {len(iteraciones)}"

        except Exception as e:
            resultado = f"Error en los datos ingresados: {e}"
            iteraciones = None

        # Pasar la función `enumerate` al contexto de la plantilla
        return render_template("index.html", resultado=resultado, iteraciones=iteraciones)

    return render_template("index.html", resultado=None, iteraciones=None)

if __name__ == '__main__':
    app.run(port=8010)
