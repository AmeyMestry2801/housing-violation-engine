# # # # # # # # import streamlit as st, os, shutil
# # # # # # # # from engine import ProsecutionEngine

# # # # # # # # st.set_page_config(page_title="TEV Cached Engine", layout="wide")
# # # # # # # # st.title("⚖️ Housing Project: High-Speed Dashboard")

# # # # # # # # v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # # # # # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")

# # # # # # # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # # # # # # out_dir = 'data/output/salesforce_ready_images3'

# # # # # # # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # # # # # # --- CACHE NOTIFICATION ---
# # # # # # # # cache_file = engine.get_cache_path(v_path)
# # # # # # # # if os.path.exists(cache_file):
# # # # # # # #     st.info(f"⚡ Fast-Track Enabled: Mapping for this video is already cached.")

# # # # # # # # c1, c2, c3 = st.columns(3)

# # # # # # # # if c1.button("1. Extract Metadata"):
# # # # # # # #     import subprocess
# # # # # # # #     log_path = "data/logs/temp_gps.csv"
# # # # # # # #     os.makedirs("data/logs", exist_ok=True)
# # # # # # # #     with st.spinner("Extracting..."):
# # # # # # # #         subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # # # # # # #     st.session_state['log_path'] = log_path
# # # # # # # #     st.success("GPS Metadata Ready")

# # # # # # # # if c2.button("2. Map Parcels"):
# # # # # # # #     # If cache exists, we don't even need the log_path from Step 1
# # # # # # # #     if os.path.exists(cache_file) or 'log_path' in st.session_state:
# # # # # # # #         l_path = st.session_state.get('log_path', "data/logs/temp_gps.csv")
# # # # # # # #         results = engine.process_mapping(l_path, v_path)
# # # # # # # #         st.session_state['results'] = results
# # # # # # # #         st.dataframe(results[['verified_address', 'sbl', 'dist_meters']])
# # # # # # # #     else: st.error("Run Step 1 or select a cached video.")

# # # # # # # # if c3.button("3. Update Dashboard"):
# # # # # # # #     if 'results' in st.session_state:
# # # # # # # #         if os.path.exists(out_dir): shutil.rmtree(out_dir)
# # # # # # # #         os.makedirs(out_dir, exist_ok=True)
# # # # # # # #         with st.spinner("Generating Grid..."):
# # # # # # # #             engine.extract_frames(v_path, st.session_state['results'], uploader)
# # # # # # # #         st.success("Dashboard Ready!")
# # # # # # # #     else: st.error("Run Step 2 First")

# # # # # # # # # --- AUTO-GALLERY ---
# # # # # # # # st.markdown("---")
# # # # # # # # if os.path.exists(out_dir):
# # # # # # # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])
# # # # # # # #     for i in range(0, len(files), 3):
# # # # # # # #         cols = st.columns(3)
# # # # # # # #         for j in range(3):
# # # # # # # #             if i+j < len(files):
# # # # # # # #                 cols[j].image(os.path.join(out_dir, files[i+j]), caption=files[i+j])

# # # # # # # import streamlit as st, os, shutil
# # # # # # # from engine import ProsecutionEngine

# # # # # # # st.set_page_config(page_title="TEV Clean Dashboard", layout="wide")
# # # # # # # st.title("⚖️ Housing Project: Clean Evidence Dashboard")

# # # # # # # v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # # # # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")

# # # # # # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # # # # # out_dir = 'data/output/salesforce_ready_images3'

# # # # # # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # # # # c1, c2, c3 = st.columns(3)

# # # # # # # if c1.button("1. Extract Metadata"):
# # # # # # #     import subprocess
# # # # # # #     log_path = "data/logs/temp_gps.csv"
# # # # # # #     os.makedirs("data/logs", exist_ok=True)
# # # # # # #     with st.spinner("Processing..."):
# # # # # # #         subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # # # # # #     st.session_state['log_path'] = log_path
# # # # # # #     st.success("GPS Metadata Ready")

# # # # # # # if c2.button("2. Map Parcels"):
# # # # # # #     if 'log_path' in st.session_state:
# # # # # # #         results = engine.process_mapping(st.session_state['log_path'], v_path)
# # # # # # #         st.session_state['results'] = results
# # # # # # #         st.dataframe(results[['verified_address', 'sbl', 'dist_meters']])
# # # # # # #     else: st.error("Run Step 1 First.")

# # # # # # # if c3.button("3. Update Dashboard"):
# # # # # # #     if 'results' in st.session_state:
# # # # # # #         # Clear old images
# # # # # # #         if os.path.exists(out_dir): shutil.rmtree(out_dir)
# # # # # # #         os.makedirs(out_dir, exist_ok=True)
# # # # # # #         with st.spinner("Filtering and Extracting..."):
# # # # # # #             engine.extract_frames(v_path, st.session_state['results'], uploader)
# # # # # # #         st.success("Dashboard Cleaned and Updated!")
# # # # # # #     else: st.error("Run Step 2 First")

# # # # # # # st.markdown("---")
# # # # # # # st.header("📸 Evidence Gallery")
# # # # # # # if os.path.exists(out_dir):
# # # # # # #     # --- UI FILTER: Skip files starting with '0' ---
# # # # # # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg') and not f.startswith('0')])
    
# # # # # # #     for i in range(0, len(files), 3):
# # # # # # #         cols = st.columns(3)
# # # # # # #         for j in range(3):
# # # # # # #             if i+j < len(files):
# # # # # # #                 cols[j].image(os.path.join(out_dir, files[i+j]), caption=files[i+j])


# # # # # # import streamlit as st, os, shutil
# # # # # # from engine import ProsecutionEngine

# # # # # # st.set_page_config(page_title="TEV Clean Presentation", layout="wide")
# # # # # # st.title("⚖️ Third Estate Ventures: Verified Dashboard")

# # # # # # v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # # # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")

# # # # # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # # # # out_dir = 'data/output/presentation_gallery'

# # # # # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # # # c1, c2, c3 = st.columns(3)

# # # # # # if c1.button("1. Extract GPS"):
# # # # # #     import subprocess
# # # # # #     log_path = "data/logs/temp_gps.csv"
# # # # # #     os.makedirs("data/logs", exist_ok=True)
# # # # # #     subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # # # # #     st.session_state['log_path'] = log_path
# # # # # #     st.success("GPS Metadata Ready")

# # # # # # if c2.button("2. Map Parcels"):
# # # # # #     if 'log_path' in st.session_state:
# # # # # #         results = engine.process_mapping(st.session_state['log_path'])
# # # # # #         st.session_state['results'] = results
# # # # # #         st.dataframe(results[['verified_address', 'sbl']])
# # # # # #     else: st.error("Run Step 1 First")

# # # # # # if c3.button("3. Update Gallery"):
# # # # # #     if 'results' in st.session_state:
# # # # # #         # HARD CLEAR of the output folder to remove those '0' images permanently
# # # # # #         if os.path.exists(out_dir):
# # # # # #             shutil.rmtree(out_dir)
# # # # # #         os.makedirs(out_dir, exist_ok=True)
        
# # # # # #         engine.extract_frames(v_path, st.session_state['results'], uploader)
# # # # # #         st.success("Gallery Sanitized and Updated.")
# # # # # #     else: st.error("Run Step 2 First")

# # # # # # st.markdown("---")
# # # # # # st.header("📸 Evidence Gallery")
# # # # # # if os.path.exists(out_dir):
# # # # # #     # One last UI check: don't display anything starting with '0'
# # # # # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg') and not f.strip().startswith('0')])
# # # # # #     for i in range(0, len(files), 3):
# # # # # #         cols = st.columns(3)
# # # # # #         for j in range(3):
# # # # # #             if i+j < len(files):
# # # # # #                 img_name = files[i+j]
# # # # # #                 cols[j].image(os.path.join(out_dir, img_name), caption=img_name)


# # # # # import streamlit as st, os, shutil
# # # # # from engine import ProsecutionEngine

# # # # # st.set_page_config(page_title="TEV Demo Mode", layout="wide")
# # # # # st.title("⚖️ Third Estate Ventures: Evidence Pipeline")

# # # # # v_path = st.sidebar.text_input("GoPro Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")

# # # # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # # # out_dir = 'data/output/presentation_gallery'

# # # # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # # c1, c2, c3 = st.columns(3)

# # # # # if c1.button("1. Extract Metadata"):
# # # # #     import subprocess
# # # # #     log_path = "data/logs/temp_gps.csv"
# # # # #     os.makedirs("data/logs", exist_ok=True)
# # # # #     subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # # # #     st.session_state['log_path'] = log_path
# # # # #     st.success("GPS Metadata Ready")

# # # # # if c2.button("2. Map & Verify"):
# # # # #     if 'log_path' in st.session_state:
# # # # #         results = engine.process_mapping(st.session_state['log_path'])
# # # # #         st.session_state['results'] = results
# # # # #         st.dataframe(results[['verified_address', 'sbl']])
# # # # #         st.info(f"Identified {len(results)} high-confidence properties.")
# # # # #     else: st.error("Run Step 1 First")

# # # # # if c3.button("3. Update Dashboard Images"):
# # # # #     if 'results' in st.session_state:
# # # # #         if os.path.exists(out_dir):
# # # # #             shutil.rmtree(out_dir)
# # # # #         os.makedirs(out_dir, exist_ok=True)
        
# # # # #         with st.spinner("Extracting High-Res Frames..."):
# # # # #             engine.extract_frames(v_path, st.session_state['results'], uploader)
# # # # #         st.success("Dashboard Updated.")
# # # # #     else: st.error("Run Step 2 First")

# # # # # st.markdown("---")
# # # # # st.header("📸 Evidence Gallery")
# # # # # if os.path.exists(out_dir):
# # # # #     # Sort and double-check limit for UI display
# # # # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg') and not f.strip().startswith('0')])[:12]
    
# # # # #     for i in range(0, len(files), 3):
# # # # #         cols = st.columns(3)
# # # # #         for j in range(3):
# # # # #             if i+j < len(files):
# # # # #                 img_name = files[i+j]
# # # # #                 cols[j].image(os.path.join(out_dir, img_name), caption=img_name)

# # # # import streamlit as st, os, shutil, pandas as pd
# # # # from engine import ProsecutionEngine

# # # # st.set_page_config(page_title="TEV Calibration Dashboard", layout="wide")
# # # # st.title("⚖️ Evidence Engine: Live Calibration Mode")

# # # # # Sidebar
# # # # v_path = st.sidebar.text_input("GoPro Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")
# # # # # SLIDER: This is how we fix the "Off-by-one"
# # # # time_adj = st.sidebar.slider("Calibration Offset (ms)", -2000, 2000, 0, step=100)

# # # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # # out_dir = 'data/output/calibration_gallery'
# # # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # c1, c2, c3 = st.columns(3)

# # # # if c1.button("1. Extract Metadata"):
# # # #     import subprocess
# # # #     log_path = "data/logs/temp_gps.csv"
# # # #     os.makedirs("data/logs", exist_ok=True)
# # # #     subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # # #     st.session_state['log_path'] = log_path
# # # #     st.success("GPS Metadata Ready")

# # # # if c2.button("2. Map Verified Parcels"):
# # # #     if 'log_path' in st.session_state:
# # # #         results = engine.process_mapping(st.session_state['log_path'])
# # # #         st.session_state['results'] = results
# # # #         # Displays the table with SBL
# # # #         st.dataframe(results[['verified_address', 'sbl', 'dist_meters']])
# # # #     else: st.error("Run Step 1 First")

# # # # if c3.button("3. Sync & Update Gallery"):
# # # #     if 'results' in st.session_state:
# # # #         if os.path.exists(out_dir): shutil.rmtree(out_dir)
# # # #         os.makedirs(out_dir, exist_ok=True)
# # # #         # Pass the calibration_ms slider value here
# # # #         engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
# # # #         st.success("Gallery Updated with Offset Applied.")
# # # #     else: st.error("Run Step 2 First")

# # # # # Gallery View
# # # # st.markdown("---")
# # # # if os.path.exists(out_dir):
# # # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])
# # # #     for i in range(0, len(files), 3):
# # # #         cols = st.columns(3)
# # # #         for j in range(3):
# # # #             if i+j < len(files):
# # # #                 cols[j].image(os.path.join(out_dir, files[i+j]), caption=files[i+j])

# # # import streamlit as st, os, shutil, pandas as pd
# # # from engine import ProsecutionEngine

# # # st.set_page_config(page_title="TEV Prosecution Engine", layout="wide")
# # # st.title("⚖️ Third Estate Ventures: Evidence & Compliance")

# # # # --- SIDEBAR ---
# # # v_path = st.sidebar.text_input("GoPro Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")
# # # time_adj = st.sidebar.slider("Fine-tune Sync (ms)", -2000, 2000, 0, step=100)

# # # shape_path = '/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp'
# # # out_dir = 'data/output/presentation_gallery'
# # # engine = ProsecutionEngine(shape_path, out_dir)

# # # # --- PIPELINE STEPS ---
# # # c1, c2, c3 = st.columns(3)

# # # if c1.button("1️⃣ Extract Metadata"):
# # #     import subprocess
# # #     log_path = "data/logs/temp_gps.csv"
# # #     os.makedirs("data/logs", exist_ok=True)
# # #     subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# # #     st.session_state['log_path'] = log_path
# # #     st.success("GPS Metadata Ready")

# # # if c2.button("2️⃣ Map Golden List"):
# # #     if 'log_path' in st.session_state:
# # #         results = engine.process_mapping(st.session_state['log_path'])
# # #         st.session_state['results'] = results
# # #         st.dataframe(results[['verified_address', 'sbl']])
# # #     else: st.error("Run Step 1 First")

# # # if c3.button("3️⃣ Sync Evidence"):
# # #     if 'results' in st.session_state:
# # #         if os.path.exists(out_dir): shutil.rmtree(out_dir)
# # #         os.makedirs(out_dir, exist_ok=True)
# # #         engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
# # #         st.success("Gallery Updated with Golden List.")
# # #     else: st.error("Run Step 2 First")

# # # # --- PHASE 2: VIOLATION PROCESSING ---
# # # if os.path.exists(out_dir) and len(os.listdir(out_dir)) > 0:
# # #     st.markdown("---")
# # #     st.header("📸 Evidence Dashboard")
    
# # #     # Display Gallery
# # #     files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])
# # #     for i in range(0, min(len(files), 12), 3):
# # #         cols = st.columns(3)
# # #         for j in range(3):
# # #             if i+j < len(files):
# # #                 cols[j].image(os.path.join(out_dir, files[i+j]), caption=files[i+j])

# # #     st.markdown("---")
# # #     st.header("⚖️ Violation Compliance Workflow")
    
# # #     proc_mode = st.radio("Select Action Mode:", ["🔍 Detect Violation (AI Scan)", "🏷️ Tag Violation (Manual)"], horizontal=True)

# # #     if proc_mode == "🔍 Detect Violation (AI Scan)":
# # #         if st.button("🚀 Run AI Vision Scan"):
# # #             with st.spinner("Analyzing structural code compliance..."):
# # #                 # Simulation of AI results
# # #                 st.info("AI Analysis: 4 properties flagged for 'High Grass', 2 for 'Property Maintenance - Paint'.")
# # #                 st.success("Scan Complete. Insights exported to JSON.")

# # #     elif proc_mode == "🏷️ Tag Violation (Manual)":
# # #         target_img = st.selectbox("Select Property to Tag:", files)
# # #         st.image(os.path.join(out_dir, target_img), width=500)
        
# # #         t1, t2 = st.columns(2)
# # #         with t1:
# # #             st.checkbox("High Grass / Weeds")
# # #             st.checkbox("Structural Blight")
# # #             st.checkbox("Trash / Debris")
# # #         with t2:
# # #             st.checkbox("Unlicensed Vehicle")
# # #             st.text_input("Inspector Notes")
# # #             if st.button("💾 Finalize Tagging"):
# # #                 st.success(f"Legal documentation for {target_img.split(',')[0]} locked for Salesforce upload.")


# # import streamlit as st, os, shutil, pandas as pd
# # from engine import ProsecutionEngine

# # st.set_page_config(page_title="TEV Final Demo", layout="wide")
# # st.title("⚖️ Evidence Engine: Final Optimized Pipeline")

# # v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# # uploader = st.sidebar.text_input("Inspector", "Amey Gopal Mestry")
# # time_adj = st.sidebar.slider("Calibration (ms)", -2000, 2000, 0, step=100)

# # engine = ProsecutionEngine('/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp', 'data/output/SALESFORCE')

# # c1, c2, c3 = st.columns(3)

# # if c1.button("1. Extract Metadata"):
# #     import subprocess
# #     log_path = f"data/logs/gps_{engine.get_video_hash(v_path)}.csv"
# #     os.makedirs("data/logs", exist_ok=True)
# #     if not os.path.exists(log_path):
# #         subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
# #     st.session_state['log_path'] = log_path
# #     st.success("GPS Metadata Ready")

# # if c2.button("2. Map Verified Parcels"):
# #     if 'log_path' in st.session_state:
# #         results = engine.process_mapping(st.session_state['log_path'], v_path)
# #         st.session_state['results'] = results
# #         # Displays the 12 Golden Houses
# #         st.dataframe(results[['verified_address', 'sbl', 'owner']])
# #     else: st.error("Run Step 1 First")

# # if c3.button("3. Update Gallery"):
# #     if 'results' in st.session_state:
# #         engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
# #         st.session_state['gallery_ready'] = True
# #         st.success("Gallery Ready")

# # if 'gallery_ready' in st.session_state:
# #     st.markdown("---")
# #     # Show the 12 perfect images
# #     gal = 'data/output/SALESFORCE/demo_gallery'
# #     files = sorted([f for f in os.listdir(gal) if f.endswith('.jpg')])
# #     for i in range(0, len(files), 3):
# #         cols = st.columns(3)
# #         for j in range(3):
# #             if i+j < len(files): cols[j].image(os.path.join(gal, files[i+j]), caption=files[i+j])

# #     st.markdown("---")
# #     if st.button("4. Detect Violation"):
# #         # This will now correctly find 'owner' even from cache
# #         final_df = engine.generate_salesforce_deliverables(v_path, st.session_state['results'], uploader, time_adj)
# #         st.success("Salesforce CSV & Annotated Images Ready!")
# #         st.dataframe(final_df)


# import streamlit as st, os, shutil, pandas as pd
# from engine import ProsecutionEngine

# st.set_page_config(page_title="TEV Prosecution Engine", layout="wide")
# st.title("Third Estate Ventures: Final Pipeline")

# # MUNICIPAL LABELS (From app.js prototype)
# WATCHER_LABELS = [
#     "Peeling Paint", "Vehicles on Unpaved", "Overgrown Vegetation", 
#     "Bad Roof", "Broken Window", "Rubbish", "Damaged Siding", "Abandoned"
# ]

# v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# uploader = st.sidebar.text_input("Inspector Name", "Amey Gopal Mestry")
# time_adj = st.sidebar.slider("Calibration (ms)", -2000, 2000, 0, step=100)

# engine = ProsecutionEngine('/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp', 'data/output/SALESFORCE')

# c1, c2, c3 = st.columns(3)

# if c1.button("1. Extract Metadata"):
#     import subprocess
#     log_path = f"data/logs/gps_{engine.get_video_hash(v_path)}.csv"
#     os.makedirs("data/logs", exist_ok=True)
#     if not os.path.exists(log_path):
#         subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
#     st.session_state['log_path'] = log_path
#     st.success("GPS Metadata Ready")

# if c2.button("2. Map Verified Parcels"):
#     if 'log_path' in st.session_state:
#         st.session_state['results'] = engine.process_mapping(st.session_state['log_path'], v_path)
#         st.dataframe(st.session_state['results'][['verified_address', 'sbl', 'owner']])
#     else: st.error("Run Step 1 First")

# if c3.button("3. Update Gallery"):
#     if 'results' in st.session_state:
#         engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
#         st.session_state['gallery_ready'] = True
#         st.success("Gallery Updated")

# if 'gallery_ready' in st.session_state:
#     st.markdown("---")
#     st.header("Step 4: AI Violation Detection")
#     if st.button("Run AI Vision Scan"):
#         with st.spinner("AI Scanning via YOLOv8-World..."):
#             st.session_state['ai_results'] = engine.generate_salesforce_deliverables(v_path, st.session_state['results'], uploader, time_adj)
#             st.success("AI Scan Complete.")

#     if 'ai_results' in st.session_state:
#         st.markdown("---")
#         st.header("Step 5: Inspector Verification (Tagging)")
#         ann_dir = 'data/output/SALESFORCE/final_compliance_images'
#         all_images = sorted([f for f in os.listdir(ann_dir) if f.endswith('.jpg')])
#         selected_img = st.selectbox("Select Image to Verify:", all_images)
        
#         t_col1, t_col2 = st.columns([2, 1])
#         with t_col1:
#             st.image(os.path.join(ann_dir, selected_img), use_column_width=True)
        
#         with t_col2:
#             st.subheader("Manual Review")
#             addr = selected_img.split(" (Detection)")[0]
#             row_data = st.session_state['ai_results'][st.session_state['ai_results']['Address'] == addr].iloc[0]
            
#             # FIXED: Corrected label selection logic to avoid final_label warning
#             chosen_violation = st.selectbox("Confirm Violation Category:", WATCHER_LABELS, index=2)
#             notes = st.text_area("Add Inspector Notes:", "AI detected potential structural blight.")
            
#             if st.button("Save Verified Tag"):
#                 if 'verified_list' not in st.session_state: st.session_state['verified_list'] = []
                
#                 entry = {
#                     "SBL": row_data['SBL'], "Address": addr, "Owner": row_data['Owner'],
#                     "Violation": chosen_violation, # Now correctly using the selectbox value
#                     "Notes": notes, "Image_ID": selected_img
#                 }
#                 st.session_state['verified_list'] = [i for i in st.session_state['verified_list'] if i['Address'] != addr]
#                 st.session_state['verified_list'].append(entry)
#                 st.toast(f"Saved: {addr}")

# if 'verified_list' in st.session_state and len(st.session_state['verified_list']) > 0:
#     st.markdown("---")
#     st.header("📤 Salesforce Final Export")
#     st.dataframe(pd.DataFrame(st.session_state['verified_list']))
#     if st.button("🏁 Finalize & Push to Salesforce"):
#         csv_path = engine.finalize_salesforce_csv(st.session_state['verified_list'])
#         st.balloons()
#         st.success(f"Final CSV saved: {csv_path}")

# import streamlit as st, os, shutil, pandas as pd
# from engine import ProsecutionEngine

# st.set_page_config(page_title="TEV Final Demo", layout="wide")
# st.title("Third Estate Ventures")

# WATCHER_LABELS = ["Peeling Paint", "Vehicles on Unpaved", "Overgrown Vegetation", "Bad Roof", "Broken Window", "Rubbish", "Damaged Siding", "Abandoned"]

# v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
# uploader = st.sidebar.text_input("Inspector Name", "Amey Gopal Mestry")
# time_adj = st.sidebar.slider("Calibration (ms)", -2000, 2000, 0, step=100)

# engine = ProsecutionEngine('/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp', 'data/output/SANDBOX_PUSH')

# c1, c2, c3 = st.columns(3)

# if c1.button("1. Extract Metadata"):
#     import subprocess
#     log_path = f"data/logs/gps_{engine.get_video_hash(v_path)}.csv"
#     os.makedirs("data/logs", exist_ok=True)
#     if not os.path.exists(log_path):
#         subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
#     st.session_state['log_path'] = log_path
#     st.success("GPS Metadata Ready")

# if c2.button("2. Map & Generate CSV"):
#     if 'log_path' in st.session_state:
#         st.session_state['results'] = engine.process_mapping(st.session_state['log_path'], v_path)
#         st.success("Mapping CSV Saved to `salesforce_data`.")
#         st.dataframe(st.session_state['results'][['verified_address', 'sbl', 'owner']])
#     else: st.error("Run Step 1 First")

# if c3.button("3. Update Gallery"):
#     if 'results' in st.session_state:
#         engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
#         st.session_state['gallery_ready'] = True
#     else: st.error("Run Step 2 First")

# # DISPLAY STEP 3 GALLERY
# if 'gallery_ready' in st.session_state:
#     st.markdown("---")
#     st.header("Step 3 Gallery")
#     gal_dir = 'data/output/SANDBOX_PUSH/demo_gallery'
#     files = sorted([f for f in os.listdir(gal_dir) if f.endswith('.jpg')])
#     for i in range(0, len(files), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             if i+j < len(files): cols[j].image(os.path.join(gal_dir, files[i+j]), caption=files[i+j])

#     st.markdown("---")
#     st.header("Step 4: AI Pre-Detection Scan")
#     if st.button("Run AI Vision Scan"):
#         with st.spinner("AI analyzing via YOLOv8-World..."):
#             st.session_state['ai_results'] = engine.generate_salesforce_deliverables(v_path, st.session_state['results'], uploader, time_adj)
#             st.success("AI Scan Complete.")

# # STEP 5: VERIFICATION WITH SAFETY GATE
# if 'ai_results' in st.session_state:
#     st.markdown("---")
#     st.header("Step 5: Inspector Verification")
#     ann_dir = 'data/output/SANDBOX_PUSH/final_compliance_images'
#     all_images = sorted([f for f in os.listdir(ann_dir) if f.endswith('.jpg')])
    
#     if all_images:
#         selected_img = st.selectbox("Select Evidence for Audit:", all_images)
        
#         # SAFETY CHECK: Only show UI if selected_img is NOT None
#         if selected_img:
#             t1, t2 = st.columns([2, 1])
#             with t1:
#                 st.image(os.path.join(ann_dir, selected_img), use_column_width=True)
#             with t2:
#                 addr = selected_img.split(" (Detection)")[0]
#                 row_data = st.session_state['ai_results'][st.session_state['ai_results']['Address'] == addr].iloc[0]
                
#                 st.warning(f"SYSTEM DETECTED: {row_data['AI_Detection']}")
#                 final_violation = st.selectbox("Inspector Final Label:", WATCHER_LABELS, index=2)
#                 notes = st.text_area("Audit Notes:", "Verified via human-in-the-loop review.")
                
#                 if st.button("Confirm Record for Sandbox"):
#                     if 'verified_list' not in st.session_state: st.session_state['verified_list'] = []
#                     st.session_state['verified_list'] = [i for i in st.session_state['verified_list'] if i['Address'] != addr]
#                     st.session_state['verified_list'].append({
#                         "SBL": row_data['SBL'], "Address": addr, "Owner": row_data['Owner'],
#                         "System_Detection": row_data['AI_Detection'], "Inspector_Label": final_violation,
#                         "Notes": notes, "Image_ID": selected_img
#                     })
#                     st.toast(f"Record Staged: {addr}")

# if 'verified_list' in st.session_state and len(st.session_state['verified_list']) > 0:
#     st.markdown("---")
#     st.header("Staged Records (Sandbox)")
#     st.dataframe(pd.DataFrame(st.session_state['verified_list']))
#     if st.button("Final Push to Sandbox"):
#         csv_path = engine.finalize_salesforce_csv(st.session_state['verified_list'])
#         st.balloons()
#         st.success(f"SUCCESS: Pushed to Sandbox. Final CSV: {csv_path}")



import streamlit as st, os, shutil, pandas as pd
from engine import ProsecutionEngine

st.set_page_config(page_title="TEV Final Demo", layout="wide")
st.title("⚖️ Third Estate Ventures: Final Pipeline")

WATCHER_LABELS = ["Peeling Paint", "Vehicles on Unpaved", "Overgrown Vegetation", "Bad Roof", "Broken Window", "Rubbish", "Damaged Siding", "Abandoned"]

v_path = st.sidebar.text_input("Video Path", "/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/GoPro-1776428412/GX010008.mp4")
uploader = st.sidebar.text_input("Inspector Name", "Amey Gopal Mestry")
time_adj = st.sidebar.slider("Calibration (ms)", -2000, 2000, 0, step=100)

engine = ProsecutionEngine('/Users/bhavingaikwad/Documents/DS_project/HousingViolationProject/data/reference/eriecounty_parcels_2025_1205/eriecounty_parcels_120525.shp', 'data/output/SANDBOX_PUSH')

c1, c2, c3 = st.columns(3)

if c1.button("1. Extract Metadata"):
    import subprocess
    log_path = f"data/logs/gps_{engine.get_video_hash(v_path)}.csv"
    os.makedirs("data/logs", exist_ok=True)
    if not os.path.exists(log_path):
        subprocess.run(f"exiftool -ee -p '$GPSDateTime,$GPSLatitude,$GPSLongitude' '{v_path}' > {log_path}", shell=True)
    st.session_state['log_path'] = log_path
    st.success("GPS Metadata Ready")

if c2.button("2. Map & Generate CSV"):
    if 'log_path' in st.session_state:
        st.session_state['results'] = engine.process_mapping(st.session_state['log_path'], v_path)
        st.success("Mapping CSV Saved.")
        st.dataframe(st.session_state['results'][['verified_address', 'sbl', 'owner']])
    else: st.error("Run Step 1 First")

if c3.button("3. Update Gallery"):
    if 'results' in st.session_state:
        engine.extract_frames(v_path, st.session_state['results'], uploader, time_adj)
        st.session_state['gallery_ready'] = True
    else: st.error("Run Step 2 First")

# --- STEP 3 GALLERY ---
if 'gallery_ready' in st.session_state:
    st.markdown("---")
    st.header("📸 Step 3: Verified Parcel Gallery")
    gal_dir = 'data/output/SANDBOX_PUSH/demo_gallery'
    files = sorted([f for f in os.listdir(gal_dir) if f.endswith('.jpg')])
    for i in range(0, len(files), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(files): cols[j].image(os.path.join(gal_dir, files[i+j]), caption=files[i+j])

    st.markdown("---")
    st.header("🚀 Step 4: AI Pre-Detection Scan")
    if st.button("Run AI Vision Scan"):
        with st.spinner("AI scanning via YOLOv8-World..."):
            st.session_state['ai_results'] = engine.generate_salesforce_deliverables(v_path, st.session_state['results'], uploader, time_adj)
            st.success("AI Scan Complete.")

# --- STEP 5: VERIFICATION ---
if 'ai_results' in st.session_state:
    st.markdown("---")
    st.header("🏷️ Step 5: Inspector Workspace (Human-in-the-Loop)")
    
    ann_dir = 'data/output/SANDBOX_PUSH/final_compliance_images'
    all_images = sorted([f for f in os.listdir(ann_dir) if f.endswith('.jpg')])
    selected_img = st.selectbox("Select Evidence for Audit:", all_images)
    
    if selected_img:
        addr = selected_img.split(" (Detection)")[0]
        row_data = st.session_state['ai_results'][st.session_state['ai_results']['Address'] == addr].iloc[0]
        
        # KEY FIX: Initialize a list for THIS specific property if it doesn't exist
        # This prevents the AI from substituting your work later.
        if f"active_tags_{addr}" not in st.session_state:
            # We convert the AI detection string into a list to start with
            st.session_state[f"active_tags_{addr}"] = [row_data['AI_Detection'].title()]

        t1, t2 = st.columns([2, 1])
        with t1:
            st.image(os.path.join(ann_dir, selected_img), use_column_width=True)
        
        with t2:
            st.subheader("Manage Violations")
            st.write("Review the list below. You can delete AI errors or add your own.")

            # FEATURE: DELETE AI or Manual Violations
            current_tags = st.session_state[f"active_tags_{addr}"]
            updated_tags = current_tags.copy()
            
            for tag in current_tags:
                cols = st.columns([4, 1])
                cols[0].info(f"📍 {tag}")
                if cols[1].button("🗑️", key=f"del_{tag}_{addr}"):
                    updated_tags.remove(tag)
                    st.session_state[f"active_tags_{addr}"] = updated_tags
                    st.rerun()

            st.markdown("---")
            
            # FEATURE: ADD Manual Violations
            # Pulling from your WATCHER_LABELS (Peeling Paint, Broken Window, etc.)
            new_violation = st.selectbox("Add Missing Violation:", WATCHER_LABELS)
            if st.button("➕ Add to List"):
                if new_violation not in st.session_state[f"active_tags_{addr}"]:
                    st.session_state[f"active_tags_{addr}"].append(new_violation)
                    st.rerun()

            notes = st.text_area("Audit Notes:", "Evidence verified for legal correspondence.")

            # FINAL STEP: SAVE THE COMBINED LIST
            if st.button("🏁 Finalize Documentation"):
                if 'verified_list' not in st.session_state: 
                    st.session_state['verified_list'] = []
                
                # We save the ENTIRE list as 'Final_Violations'
                final_entry = {
                    "SBL": row_data['SBL'],
                    "Address": addr,
                    "Owner": row_data['Owner'],
                    "Final_Violations": st.session_state[f"active_tags_{addr}"], 
                    "Notes": notes,
                    "Image_ID": selected_img
                }
                
                # Update the main staging list
                st.session_state['verified_list'] = [i for i in st.session_state['verified_list'] if i['Address'] != addr]
                st.session_state['verified_list'].append(final_entry)
                st.success(f"Final list generated for {addr} with {len(st.session_state[f'active_tags_{addr}'])} violations.")
# --- PHASE 3: NOTICES ---
if 'verified_list' in st.session_state and len(st.session_state['verified_list']) > 0:
    st.markdown("---")
    st.header("📄 Phase 3: Official Correspondence")
    verified_df = pd.DataFrame(st.session_state['verified_list'])
    
    sel_notice_addr = st.selectbox("Generate Notice for Property:", verified_df['Address'].tolist())
    record_for_notice = [r for r in st.session_state['verified_list'] if r['Address'] == sel_notice_addr][0]
    
    if st.button("📝 Generate Official Notice"):
        notice_text = engine.generate_violation_notice(record_for_notice)
        st.text_area("Correspondence Template:", value=notice_text, height=350)
        st.download_button("📥 Download Notice", data=notice_text, file_name=f"NOV_{record_for_notice['SBL']}.txt")

    st.markdown("---")
    if st.button("🏁 Final Push to Sandbox"):
        csv_path = engine.finalize_salesforce_csv(st.session_state['verified_list'])
        st.balloons()
        st.success(f"SUCCESS: Pushed to Sandbox. Final CSV: {csv_path}")