from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def convert_to_all_bases(decimal_value):
    # Separar la parte entera y la parte fraccionaria
    if '.' in decimal_value:
        integer_part, fractional_part = decimal_value.split('.')
        integer_part = int(integer_part)
        fractional_part = float('0.' + fractional_part)
    else:
        integer_part = int(decimal_value)
        fractional_part = 0

    result = {
        'decimal': decimal_value,
        'binary': f"{bin(integer_part)[2:]}.{fraction_to_base(fractional_part, 2)}" if fractional_part else bin(integer_part)[2:],
        'octal': f"{oct(integer_part)[2:]}.{fraction_to_base(fractional_part, 8)}" if fractional_part else oct(integer_part)[2:],
        'hexadecimal': f"{hex(integer_part)[2:].upper()}.{fraction_to_base(fractional_part, 16).upper()}" if fractional_part else hex(integer_part)[2:].upper(),
    }
    return result

def fraction_to_base(fraction, base, precision=10):
    result = []
    while fraction and len(result) < precision:
        fraction *= base
        digit = int(fraction)
        result.append(hex(digit)[2:] if base == 16 else str(digit))
        fraction -= digit
    return ''.join(result) if result else '0'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    decimal_value = None
    if data.get('decimal'):
        decimal_value = data['decimal']
    elif data.get('binary'):
        decimal_value = str(int(data['binary'], 2))
    elif data.get('octal'):
        decimal_value = str(int(data['octal'], 8))
    elif data.get('hexadecimal'):
        decimal_value = str(int(data['hexadecimal'], 16))
    else:
        return jsonify({'error': 'No valid input provided'})

    result = convert_to_all_bases(decimal_value)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8006)
