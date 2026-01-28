import pandas as pd
import matplotlib.pyplot as plt

# Read log file
df = pd.read_csv("logs.csv")

print("\n--- LLM Observability Logs ---\n")
print(df)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plot 1: Latency over time
plt.figure(figsize=(8,4))
plt.plot(df['timestamp'], df['latency'], marker='o')
plt.title("LLM Latency Over Time")
plt.xlabel("Time")
plt.ylabel("Latency (seconds)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Cost per request
plt.figure(figsize=(8,4))
plt.plot(range(len(df)), df['cost'], marker='o')
plt.title("Cost per LLM Request")
plt.xlabel("Request Number")
plt.ylabel("Cost ($)")
plt.tight_layout()
plt.show()

# Plot 3: Token usage per request
plt.figure(figsize=(8,4))
plt.plot(range(len(df)), df['tokens'], marker='o')
plt.title("Token Usage per Request")
plt.xlabel("Request Number")
plt.ylabel("Tokens")
plt.tight_layout()
plt.show()
