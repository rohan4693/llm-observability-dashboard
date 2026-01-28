from flask import Flask, render_template, request
import time, random, csv
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid threading issues
import matplotlib.pyplot as plt
import os


app = Flask(__name__)

def simulated_llm(prompt):
    start = time.time()
    fake_latency = random.uniform(0.5, 3)
    time.sleep(fake_latency)

    response = f"Simulated response for: {prompt}"
    latency = round(time.time() - start, 2)
    prompt_tokens = len(prompt.split())
    response_tokens = random.randint(10, 30)  # simulate variable response size
    tokens = prompt_tokens + response_tokens

    # Simulate different pricing (like real LLM APIs)
    cost_per_token = random.choice([0.000008, 0.00001, 0.000012])
    cost = round(tokens * cost_per_token, 5)

    return response, latency, tokens, cost

def log_data(prompt, response, latency, tokens, cost):
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),
            prompt,
            response,
            latency,
            tokens,
            cost
        ])

@app.route("/", methods=["GET", "POST"])
def index():
    response = latency = tokens = cost = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        response, latency, tokens, cost = simulated_llm(prompt)
        log_data(prompt, response, latency, tokens, cost)
    return render_template("index.html",
                           response=response,
                           latency=latency,
                           tokens=tokens,
                           cost=cost)

@app.route("/dashboard")
def dashboard():
    df = pd.read_csv("logs.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Absolute path to static/graphs
    base_dir = app.root_path
    graph_dir = os.path.join(base_dir, "static", "graphs")

    # Ensure directory exists
    os.makedirs(graph_dir, exist_ok=True)

    # Latency graph
    latency_path = os.path.join(graph_dir, "latency.png")
    plt.figure(figsize=(5,3), dpi=100)
    plt.plot(df["timestamp"], df["latency"], marker="o")
    plt.title("LLM Latency Over Time")
    plt.xlabel("Time")
    plt.ylabel("Latency (seconds)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(latency_path)
    plt.close()

    # Cost graph
    cost_path = os.path.join(graph_dir, "cost.png")
    plt.figure(figsize=(5,3), dpi=100)
    plt.plot(range(len(df)), df["cost"], marker="o")
    plt.title("Cost Per Request")
    plt.xlabel("Request Number")
    plt.ylabel("Cost ($)")
    plt.tight_layout()
    plt.savefig(cost_path)
    plt.close()

    # Tokens graph
    tokens_path = os.path.join(graph_dir, "tokens.png")
    plt.figure(figsize=(5,3), dpi=100)
    plt.plot(range(len(df)), df["tokens"], marker="o")
    plt.title("Tokens Used Per Request")
    plt.xlabel("Request Number")
    plt.ylabel("Tokens")
    plt.tight_layout()
    plt.savefig(tokens_path)
    plt.close()

    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)
