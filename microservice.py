from flask import Flask, jsonify, request

app = Flask(__name__)

# Global dictionary to store numbers for different endpoints
numbers_dict = {'p': [], 'f': [], 'e': [], 'r': []}
window_size = 10  # Default window size


def calculate_average(numbers):
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)


@app.route('/numbers/<string:number_id>', methods=['GET', 'POST'])
def handle_numbers(number_id):
    global numbers_dict

    if request.method == 'POST':
        try:
            number = float(request.json['number'])
            if number_id in numbers_dict:
                numbers_dict[number_id].append(number)
                # Trim numbers if the list exceeds window size
                if len(numbers_dict[number_id]) > window_size:
                    numbers_dict[number_id] = numbers_dict[number_id][-window_size:]
                return jsonify({'message': 'Number added successfully'}), 200
            else:
                return jsonify({'error': f'Invalid number id: {number_id}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    elif request.method == 'GET':
        if number_id in numbers_dict:
            average = calculate_average(numbers_dict[number_id])
            return jsonify({'average': average}), 200
        else:
            return jsonify({'error': f'Invalid number id: {number_id}'}), 400


@app.route('/config/window_size', methods=['GET', 'POST'])
def config_window_size():
    global window_size

    if request.method == 'POST':
        try:
            new_window_size = int(request.json['window_size'])
            if new_window_size > 0:
                window_size = new_window_size
                return jsonify({'message': 'Window size updated successfully'}), 200
            else:
                return jsonify({'error': 'Window size must be greater than 0'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    elif request.method == 'GET':
        return jsonify({'window_size': window_size}), 200


if __name__ == '__main__':
    app.run(debug=True)
