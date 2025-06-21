# Realtime_IoT_PacketAnomalyDetector

A full-stack Python-based tool to monitor, detect, and visualize anomalous network packets in real-time using Scapy, machine learning, and an interactive Flask dashboard.

Look of the Website
![image](https://github.com/user-attachments/assets/ad802f22-b293-4918-8645-89e1022ed740)

Website Link: https://packet-anomaly-detector.onrender.com/

## Features

*  **Live Packet Capture** with Scapy
*  **Anomaly Detection** using Isolation Forest
*  **Interactive Dashboard** built with Flask
*  **Filter by Protocol / Port**
*  **Anomaly Table** with export as PDF
*  **Dark/Light Mode Toggle**
*  **Graphs**:

  * Bar chart (Anomalies per Protocol)
  * Pie chart (Anomaly distribution)
  * Time series chart (Anomalies over time)

## 🗂 Folder Structure

```
packet-anomaly-detector/
├── app/
│   ├── dashboard.py              # Flask server & UI logic
│   ├── templates/
│   │   └── dashboard.html        # UI template
│   └── static/
│       ├── anomaly_chart.png
│       ├── anomaly_pie.png
│       ├── anomaly_time.png
│       └── style.css
├── data/
│   ├── processed_packets.csv
│   └── processed_packets_labeled.csv
├── models/
│   └── anomaly_model.pkl         # ML model (e.g., Isolation Forest)
├── scripts/
│   ├── packet_sniffer.py         # Capture packets with Scapy
│   ├── feature_extractor.py      # Extract relevant features
│   └── detect_anomalies.py       # Label anomalies and output
├── utils/
│   └── logger.py                 # Logging setup
├── static/
│   └── anomaly_export.pdf        # Exported anomaly table
├── requirements.txt
├── main.py                       # Unified entry point
└── README.md
```

##  How to Run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run anomaly detection pipeline**

   ```bash
   python scripts/detect_anomalies.py
   ```

3. **Start the dashboard**

   ```bash
   python app/dashboard.py
   ```

4. **Visit** [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

##  Requirements

* Python 3.8+
* Packages: `Flask`, `matplotlib`, `pandas`, `fpdf`, `scikit-learn`, `scapy`

##  Customization

* You can train your own model and save it as `models/anomaly_model.pkl`.
* Customize theme in `style.css` or edit the embedded styles in `dashboard.html`.
* Easily replace or add new plots in `dashboard.py`.

##  Tips

* Ensure `data/processed_packets_labeled.csv` exists before launching the dashboard.
* Graphs are saved to `app/static/`, which is auto-created if missing.
* Toggle mode uses a `data-theme` attribute and `localStorage` to persist preference.
