from flask import Flask, render_template_string, request, jsonify, render_template, redirect, url_for, Response, json
from prometheus_client import Counter, generate_latest, Histogram, Gauge, Summary

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests',
    ['method', 'endpoint']
)

CURRENT_USERS = Gauge(
    'current_users',
    'Current number of active users'
)

PROCESSING_TIME = Summary(
    'processing_time_seconds',
    'Processing time of some task in seconds'
)

@app.route('/')
def hello_world():
    with REQUEST_DURATION.labels(method='GET', endpoint='/').time():
        REQUEST_COUNT.labels(method='GET', endpoint='/', status_code=200).inc()
        CURRENT_USERS.inc()
        PROCESSING_TIME.observe(0.5)

    return render_template('index.html')

@app.route('/result/', methods=['POST','GET'])
def result():
    if request.method == 'POST':
       # Get the bmi, status, weight and height from the ajax request
        data = request.get_json()

        # Check if the input data is valid
        if not all(data.get(field) for field in ['bmi', 'status', 'height', 'weight']):
            return jsonify({'error': 'Invalid or missing input data'}), 400

        # Get the bmi, status, weight and height from the ajax request
        bmi = data['bmi']
        status = data['status']
        height = data['height']
        weight = data['weight']

        # Read diet plans from JSON file
        with open('diet_plans.json', 'r') as file:
            all_diet_plans = json.load(file)

        diet_plan = all_diet_plans.get(status,[])

        # Read workout plans from JSON file
        with open('workout_plans.json', 'r') as file:
            all_workout_plans = json.load(file)

        workout_plans = all_workout_plans.get(status,[])

        return render_template('result.html', height=height, weight=weight, bmi=bmi, status=status, diet_plans=diet_plan, workout_plans=workout_plans)
    
    return jsonify({'error': 'Method not allowed'}), 405

        
        
# Custom metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/decrement_users', methods=['POST'])
def decrement_users():
    CURRENT_USERS.dec()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
