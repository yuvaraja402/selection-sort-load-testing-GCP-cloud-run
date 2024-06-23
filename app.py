from flask import Flask, request, jsonify
import time
import psutil
import os

app = Flask(__name__)

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

@app.route('/sort')
def sort_input():
    try:
        start_time = time.time()

        numbers = request.args.get('numbers')
        if not numbers:
            return jsonify({"error": "Please provide a list of numbers as a query parameter 'numbers'"}), 400
        
        # Convert the input string into a list of integers
        numbers_list = list(map(int, numbers.split(',')))
        
        sorted_numbers = selection_sort(numbers_list.copy())  # Use a copy to preserve the original list

        # Measure execution time
        execution_time = time.time() - start_time

        # Get current process information
        process = psutil.Process(os.getpid())
        cpu_usage = process.cpu_percent(interval=1.0)  # Measure CPU usage over 1 second
        memory_info = process.memory_info()
        ram_usage = memory_info.rss / (1024 ** 2)  # Convert from bytes to MB

        return jsonify({
            "input_numbers": numbers_list,
            "sorted_numbers": sorted_numbers,
            "execution_time_seconds": execution_time,
            "cpu_usage_percent": cpu_usage,
            "ram_usage_mb": ram_usage
        })
    except ValueError:
        return jsonify({"error": "Invalid input. Ensure all elements are integers."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
