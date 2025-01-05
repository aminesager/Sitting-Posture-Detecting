from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    
    # After processing, redirect to the result page
    return redirect(url_for('result_page'))

@app.route('/result')
def result_page():
    # Render the result page HTML
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
