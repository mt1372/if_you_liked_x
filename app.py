from flask import Flask, request, jsonify
import openai

app = Flask(__name__)


#fixes CORS issues by using access headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


# Set the OpenAI key and other configurations with environment variables
with open('keys.txt', 'r', encoding='utf-8-sig') as file:
 #   key = file.read().strip()
    openai.api_key = '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'

@app.route('/recommend', methods=['POST'])
def recommend():
    books = request.json['books']
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a book recommender. You get books and return one thoughtful recommendation."},
            {"role": "user", "content": f"{', '.join(books)}"}
        ]
    )
    
    recommendation = response['choices'][0]['message']['content']
    return jsonify(recommendation=recommendation)

if __name__ == '__main__':
    app.run()
