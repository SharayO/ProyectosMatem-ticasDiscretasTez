from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Función para calcular las derivadas
def calcular_derivadas(funcion_str):
    x = sp.symbols('x')
    try:
        # Agregar las funciones trigonométricas, exponenciales y logarítmicas
        funcion_sympy = eval(funcion_str, {"x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, 
                                           "cot": sp.cot, "asin": sp.asin, "acos": sp.acos, 
                                           "atan": sp.atan, "exp": sp.exp, "ln": sp.log})
    except Exception as e:
        return None, f"Error al procesar la función para derivadas: {e}"

    derivadas = []
    for i in range(1, 7):  # Calcula hasta la sexta derivada
        derivada = sp.diff(funcion_sympy, x, i)
        derivadas.append(sp.simplify(derivada))
    return derivadas, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Leer la función
            funcion_str = request.form["funcion"]

            # Calcular derivadas
            derivadas, error_derivadas = calcular_derivadas(funcion_str)
            if error_derivadas:
                derivadas = None
                resultado = error_derivadas
            else:
                resultado = "Derivadas calculadas correctamente."

        except Exception as e:
            resultado = f"Error en los datos ingresados: {e}"
            derivadas = None

        # Pasar la función `enumerate` al contexto de la plantilla
        return render_template("index.html", resultado=resultado, derivadas=derivadas, enumerate=enumerate)

    return render_template("index.html", resultado=None, derivadas=None, enumerate=enumerate)

if __name__ == '__main__':
    app.run(port=8007)
