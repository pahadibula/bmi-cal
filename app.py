from flask import Flask, render_template_string, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
       # Get the bmi, status, weight and height from the ajax request
        data = request.get_json()
        bmi = data['bmi']
        status = data['status']
        height = data['height']
        weight = data['weight']

        return render_template('result.html', height=height, weight=weight, bmi=bmi, status=status)
        
        

if __name__ == '__main__':
    app.run(debug=True)