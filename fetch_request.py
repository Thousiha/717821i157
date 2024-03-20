import asyncio
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Global set to store fetched numbers
fetched_numbers = set()


async def fetch_number(url):
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()  # Raise exception if response status is not 2xx
        data = response.json()
        return data.get('number')
    except (requests.RequestException, ValueError):
        return None


@app.route('/fetch-number', methods=['POST'])
def handle_fetch_number():
    try:
        url = request.json['url']
    except KeyError:
        return jsonify({'error': 'Missing URL parameter'}), 400

    # Asynchronously fetch the number
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(fetch_number(url))
    number = loop.run_until_complete(asyncio.wait_for(future, timeout=0.5))

    if number is not None:
        fetched_numbers.add(number)

    return jsonify({'number': number}), 200


@app.route('/fetched-numbers', methods=['GET'])
def get_fetched_numbers():
    return jsonify({'fetched_numbers': list(fetched_numbers)}), 200


if __name__ == '__main__':
    app.run(debug=True)
