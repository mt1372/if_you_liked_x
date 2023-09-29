from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)


# fixes CORS issues by using access headers
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST")
    return response


# Set the OpenAI key and other configurations with environment variables
# with open("keys.txt", "r", encoding="utf-8-sig") as file:
#  key = file.read().strip()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/recommend", methods=["POST"])
def recommend():
    books = request.json["books"]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You get books and return one well thought-out recommendation that hasn't been listed. After your response, put a semicolon, space, and then only the ISBN number. Do not include the word ISBN.",
            },
            {"role": "user", "content": f"{', '.join(books)}"},
        ],
    )

    recommendation = response["choices"][0]["message"]["content"]
    ISBN = recommendation.split("; ")[1]
    ISBN = "".join([c for c in ISBN if c.isdigit()])

    recommendation = recommendation.split("; ")[0] + "."
    return jsonify(recommendation=recommendation, ISBN=ISBN)


if __name__ == "__main__":
    app.run()
