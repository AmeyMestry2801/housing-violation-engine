# Housing Violation Engine 🏠🛰️

An end-to-end autonomous platform that digitizes municipal property auditing by integrating **Open-Vocabulary Computer Vision** with **GIS Spatial Logic**.

## 🚀 Key Features
- **Zero-Shot Detection:** Uses **YOLOv8-World** to identify violations (peeling paint, high grass) via natural language prompts.
- **Sub-meter Spatial Accuracy:** Leverages a **KDTree index** to match GoPro telemetry to official **Erie County Parcel** data.
- **Vector Projection:** Solves the "Side-of-Street" orientation problem using 90° perpendicular geometry.
- **Human-in-the-Loop (HITL):** A browser-based tagging workspace (HTML/JS) for legal verification and JSON export.

## 🛠️ Tech Stack
- **Backend:** Python, PyTorch, Scipy (KDTree), Geopandas
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Tools:** ExifTool, Salesforce API, Streamlit

## 📂 Project Structure
- `app.py`: Main Streamlit application and HITL workspace.
- `engine.py`: Backend logic for GIS mapping and AI inference.
- `index.html` / `app.js`: Standalone browser-based image tagging prototype.
- `yolov8s-world.pt`: Pre-trained open-vocabulary weights.

## ⚙️ Installation & Setup
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/AmeyMestry2801/housing-violation-engine.git](https://github.com/AmeyMestry2801/housing-violation-engine.git)
   ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the Application**
    ```bash
    streamlit run app.py
    ```

Note: This project requires ExifTool to be installed on your system path to extract GoPro metadata.

macOS: brew install exiftool

Windows: Download the executable from https://exiftool.org
## 📊 Impact

85% Reduction in manual property audit time.

0.2s Lookup Latency for property owner and SBL retrieval.

Automated generation of legal Notices of Violation.

## 👥 Contributors

Amey Mestry: Backend Architecture, GIS Engineering, AI Model Integration.

Zakir: Frontend Tagging Prototype, UI/UX State Management.


## 🔄 System Workflow
1. **Telemetry Extraction:** `ExifTool` pulls GPS/IMU data from GoPro GPMF streams.
2. **Spatial Mapping:** `engine.py` uses a **KDTree** to snap coordinates to the **Erie County Parcel Dataset**, identifying the exact **SBL** and **Owner Name**.
3. **AI Inference:** `YOLOv8-World` performs zero-shot detection on the video frames.
4. **Verification:** The `app.py` (Streamlit) and `index.html` (Frontend) allow an inspector to verify the AI results.
5. **Export:** Final records are pushed to a **Salesforce Sandbox** via API for legal enforcement.

## 📊 Data Requirements
To run this project locally, ensure the following structure in your `/data` directory:
- `parcels.shp`: Erie County Parcel shapefile.
- `video_logs/`: Raw GoPro `.mp4` files for processing.
- `owner_records.csv`: (Optional) Local lookup table for property owner names.




