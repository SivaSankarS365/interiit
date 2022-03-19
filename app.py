from crypt import methods
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from models.companies import search_companies

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def ping_server():
    return "Server is running now!"


@app.route("/search", methods=["GET"])
def search():
    company_name = request.args.get("company_name")
    companies = search_companies(company_name)
    # print(companies)
    a = []
    for company in companies:
        a.append({
            "cik": company[0],
            "company_name": company[1],
            "company_logo": company[2],
            "ticker": company[3]
        })
    return jsonify(a)


@app.route("/create")
def create_companies():
    return True


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
