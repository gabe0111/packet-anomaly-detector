import os, sys
print("PWD:", os.getcwd(), "DIRS:", os.listdir("."))
if "data" in os.listdir("."):
    print("data folder contents:", os.listdir("data"))
else:
    print("data folder missing at runtime")

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from fpdf import FPDF
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import setup_logger

app = Flask(__name__)
logger = setup_logger(__name__)

@app.route("/", methods=["GET"])
def home():
    logger.info("Dashboard accessed via GET")
    data_path = "data/processed_packets_labeled.csv"
    if not os.path.exists(data_path):
        logger.warning("CSV file missing, starting with empty dataset.")
        df = pd.DataFrame(columns=['src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'anomaly'])
    else:
        df = pd.read_csv(data_path)

    protocol = request.args.get("protocol")
    port = request.args.get("port")

    if protocol:
        df = df[df["protocol"] == int(protocol)]
    if port:
        df = df[(df["src_port"] == int(port)) | (df["dst_port"] == int(port))]

    total_packets = len(df)
    anomalies = df[df["anomaly"] == -1]
    anomaly_count = len(anomalies)
    anomaly_percent = round((anomaly_count / total_packets) * 100, 2) if total_packets > 0 else 0

    os.makedirs("app/static", exist_ok=True)

    # ✅ Generate frequency data
    freq = anomalies["protocol"].value_counts()

    # ✅ Bar Chart
    plt.figure(figsize=(4, 3))
    freq.plot(kind='bar', color='crimson')
    plt.title("Anomalies per Protocol")
    plt.tight_layout()
    plt.savefig("app/static/anomaly_chart.png")
    plt.close()

    # ✅ Pie Chart
    plt.figure(figsize=(4, 3))
    freq.plot.pie(autopct='%1.1f%%')
    plt.title("Anomaly Protocol Distribution")
    plt.tight_layout()
    plt.savefig("app/static/anomaly_pie.png")
    plt.close()

    # ✅ Time Chart (if time column doesn't exist, use dummy)
    if not anomalies.empty:
        anomalies['timestamp'] = pd.to_datetime('now')  # Replace with real time if available
        anomalies.set_index('timestamp').resample('1T').size().plot()
        plt.title("Anomalies Over Time")
        plt.tight_layout()
        plt.savefig("app/static/anomaly_time.png")
        plt.close()
    else:
        # Show blank graph
        plt.figure()
        plt.text(0.5, 0.5, 'No anomalies to display', ha='center', va='center')
        plt.axis('off')
        plt.savefig("app/static/anomaly_time.png")
        plt.close()

    return render_template("dashboard.html",
                           total_packets=total_packets,
                           anomaly_count=anomaly_count,
                           anomaly_percent=anomaly_percent,
                           anomaly_table=anomalies.to_dict(orient='records'),
                           filter_protocol=protocol or "",
                           filter_port=port or "")

@app.route("/export_pdf")
def export_pdf():
    df = pd.read_csv("data/processed_packets_labeled.csv")
    anomalies = df[df["anomaly"] == -1]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Anomalous Packets", ln=True, align='C')

    col_width = pdf.w / 6
    row_height = 10

    for _, row in anomalies.iterrows():
        for val in row.values:
            pdf.cell(col_width, row_height, str(val), border=1)
        pdf.ln(row_height)

    pdf_path = "app/static/anomaly_export.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

from flask import jsonify

@app.route("/api/anomalies", methods=["POST"])
def receive_anomalies():
    try:
        data = request.get_json()
        if not data or "anomalies" not in data:
            return jsonify({"error": "Invalid data"}), 400

        anomalies = data["anomalies"]
        df = pd.DataFrame(anomalies)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/processed_packets_labeled.csv", index=False)
        logger.info(f"Received and saved {len(df)} anomalies.")
        return jsonify({"message": "Anomalies saved successfully"}), 200

    except Exception as e:
        logger.error(f"Error receiving anomalies: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
