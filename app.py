from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def search_github_users(domain, tech):
    query = f"{domain} {tech} in:description"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        repos = data.get("items", [])[:5]

        results = []
        for repo in repos:
            results.append({
                "repo_name": repo["name"],
                "owner": repo["owner"]["login"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"]
            })

        return results
    return []

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []

    if request.method == "POST":
        domain = request.form["domain"]
        tech = request.form["tech"]
        recommendations = search_github_users(domain, tech)

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)