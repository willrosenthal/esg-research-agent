import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import requests

app = Flask(__name__)

client = OpenAI()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    company_name = request.json['company_name']
    questions = get_questions(company_name)
    try:
        responses = get_openai_responses(questions)
    except Exception as e:
        app.logger.error(f"Failed to get responses: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(responses)


def get_openai_responses(questions):
    responses = {}
    for key, question in questions:
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[{"role": "user", "content": question}]
        )
        responses[key] = parse_response(response.choices[0].message.content)
    return responses


def get_questions(company_name):
    return [
        ("humanRightsPolicy", f"Answer with a 'Yes.' or 'No.' answer—Does {company_name} have a human rights policy? " + 
                        "Now, provide a brief explanation of your answer. " +
                        "Finally, provide a legitimate source (and URL if possible) dated from before 2024, that proves your explanation true! Do not speak in first-person."),
        ("esgTraining", f"Answer with a 'Yes.' or 'No.' answer—Does {company_name} provide human rights or ESG training to employees? " +
                        "Now, provide a brief explanation of your answer. " +
                        "Finally, provide a legitimate source (and URL if possible) dated from before 2024, that proves your explanation true! Do not speak in first-person."),
        ("scope1Emissions", f"Answer with a 'Yes.' or 'No.' answer—Does {company_name} track Scope 1 emissions? " + 
                        "Now, provide a brief explanation of your answer. " +
                        "Finally, provide a legitimate source (and URL if possible) dated from before 2024, that proves your explanation true! Do not speak in first-person.")
    ]


def parse_response(response):
    parts = response.strip().split('\n\n')

    result = {
        "answer": "No data available",
        "explanation": "No explanation available",
        "source": "No source available"
    }

    if len(parts) > 0:
        result["answer"] = parts[0].strip()
    if len(parts) > 1:
        result["explanation"] = parts[1].strip()
    if len(parts) > 2:
        result["source"] = parts[2].strip()

    return result


# def validate_url(url):
#     try:
#         response = requests.get(url, timeout=7)
#         return response.status_code == 200
#     except requests.RequestException:
#         return False


if __name__ == '__main__':
    app.run(debug=True)