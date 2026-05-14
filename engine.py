# # # # # # # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # # # # # # from scipy.spatial import KDTree
# # # # # # # # from datetime import datetime

# # # # # # # # class ProsecutionEngine:
# # # # # # # #     def __init__(self, shapefile_path, output_dir):
# # # # # # # #         self.output_dir = output_dir
# # # # # # # #         self.cache_dir = "data/cache"
# # # # # # # #         os.makedirs(output_dir, exist_ok=True)
# # # # # # # #         os.makedirs(self.cache_dir, exist_ok=True)
        
# # # # # # # #         # Load Shapefile
# # # # # # # #         self.gdf = gpd.read_file(shapefile_path)
# # # # # # # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
# # # # # # # #         self.gdf = self.gdf.to_crs("EPSG:2262") 
# # # # # # # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # # # # # # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # # # # # # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        
# # # # # # # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # # # # # # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # # # # # # #     def get_cache_path(self, video_path):
# # # # # # # #         # Creates a unique filename for the cache based on the video name
# # # # # # # #         video_name = os.path.basename(video_path).split('.')[0]
# # # # # # # #         return os.path.join(self.cache_dir, f"{video_name}_mapped.csv")

# # # # # # # #     def process_mapping(self, log_path, video_path):
# # # # # # # #         cache_path = self.get_cache_path(video_path)
        
# # # # # # # #         # CACHE CHECK: If we already did the work, just return it
# # # # # # # #         if os.path.exists(cache_path):
# # # # # # # #             print(f"⚡ Loading cached mapping for {video_path}")
# # # # # # # #             return pd.read_csv(cache_path)

# # # # # # # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # # # # # # #         gps['original_index'] = gps.index 
        
# # # # # # # #         def dms_to_dec(s):
# # # # # # # #             try:
# # # # # # # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # # # # # # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # # # # # # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # # # # # # #             except: return 0.0

# # # # # # # #         gps['lat'] = gps['lat_raw'].apply(dms_to_dec)
# # # # # # # #         gps['lon'] = gps['lon_raw'].apply(dms_to_dec)
# # # # # # # #         gps = gps[(gps['lat'] != 0)].copy()

# # # # # # # #         # Your individual vector math
# # # # # # # #         gps['d_lat'] = gps['lat'].diff().rolling(window=5).mean()
# # # # # # # #         gps['d_lon'] = gps['lon'].diff().rolling(window=5).mean()

# # # # # # # #         look_left_coords = []
# # # # # # # #         OFFSET_METERS = 15 
# # # # # # # #         for i in range(len(gps)):
# # # # # # # #             lat, lon = gps['lat'].iloc[i], gps['lon'].iloc[i]
# # # # # # # #             dy, dx = gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # # # # # # #             if pd.isna(dy) or (dx == 0): look_left_coords.append((lat, lon))
# # # # # # # #             else:
# # # # # # # #                 mag = np.sqrt(dx**2 + dy**2)
# # # # # # # #                 offset_deg = OFFSET_METERS / 111139
# # # # # # # #                 look_left_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # # # # # # #         distances, indices = self.tree.query(look_left_coords)
# # # # # # # #         gps['verified_address'] = self.gdf.iloc[indices]['ADDRESS'].values
# # # # # # # #         gps['sbl'] = self.gdf.iloc[indices]['SBL'].values
# # # # # # # #         gps['dist_meters'] = distances * 111139 

# # # # # # # #         df_unique = gps[gps['dist_meters'] < 60].copy()
# # # # # # # #         df_final = df_unique.loc[df_unique.groupby('verified_address')['dist_meters'].idxmin()].copy()
        
# # # # # # # #         # SAVE TO CACHE
# # # # # # # #         df_final.to_csv(cache_path, index=False)
# # # # # # # #         return df_final

# # # # # # # #     def extract_frames(self, video_path, df_results, uploader):
# # # # # # # #         cap = cv2.VideoCapture(video_path)
# # # # # # # #         fps = cap.get(cv2.CAP_PROP_FPS)
# # # # # # # #         for _, row in df_results.iterrows():
# # # # # # # #             try:
# # # # # # # #                 dt_obj = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S")
# # # # # # # #                 ts_str = dt_obj.strftime("%m%d%y%H%M%S")
# # # # # # # #             except: ts_str = "050126000000"
# # # # # # # #             filename = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts_str}] ({uploader}).jpg"
# # # # # # # #             frame_no = int(row['original_index'] * (fps / 10))
# # # # # # # #             cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
# # # # # # # #             ret, frame = cap.read()
# # # # # # # #             if ret:
# # # # # # # #                 cv2.imwrite(os.path.join(self.output_dir, filename), frame)
# # # # # # # #         cap.release()


# # # # # # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # # # # # from scipy.spatial import KDTree
# # # # # # # from datetime import datetime

# # # # # # # class ProsecutionEngine:
# # # # # # #     def __init__(self, shapefile_path, output_dir):
# # # # # # #         self.output_dir = output_dir
# # # # # # #         self.cache_dir = "data/cache"
# # # # # # #         os.makedirs(output_dir, exist_ok=True)
# # # # # # #         os.makedirs(self.cache_dir, exist_ok=True)
        
# # # # # # #         # Load Shapefile
# # # # # # #         self.gdf = gpd.read_file(shapefile_path)
# # # # # # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
# # # # # # #         self.gdf = self.gdf.to_crs("EPSG:2262") 
# # # # # # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # # # # # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # # # # # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        
# # # # # # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # # # # # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # # # # # #     def get_cache_path(self, video_path):
# # # # # # #         video_name = os.path.basename(video_path).split('.')[0]
# # # # # # #         return os.path.join(self.cache_dir, f"{video_name}_mapped.csv")

# # # # # # #     def process_mapping(self, log_path, video_path):
# # # # # # #         cache_path = self.get_cache_path(video_path)
# # # # # # #         if os.path.exists(cache_path):
# # # # # # #             return pd.read_csv(cache_path)

# # # # # # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # # # # # #         gps['original_index'] = gps.index 
        
# # # # # # #         def dms_to_dec(s):
# # # # # # #             try:
# # # # # # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # # # # # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # # # # # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # # # # # #             except: return 0.0

# # # # # # #         gps['lat'] = gps['lat_raw'].apply(dms_to_dec)
# # # # # # #         gps['lon'] = gps['lon_raw'].apply(dms_to_dec)
# # # # # # #         gps = gps[(gps['lat'] != 0)].copy()

# # # # # # #         # Vector Math
# # # # # # #         gps['d_lat'] = gps['lat'].diff().rolling(window=5).mean()
# # # # # # #         gps['d_lon'] = gps['lon'].diff().rolling(window=5).mean()

# # # # # # #         look_left_coords = []
# # # # # # #         OFFSET_METERS = 15 
# # # # # # #         for i in range(len(gps)):
# # # # # # #             lat, lon = gps['lat'].iloc[i], gps['lon'].iloc[i]
# # # # # # #             dy, dx = gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # # # # # #             if pd.isna(dy) or (dx == 0): look_left_coords.append((lat, lon))
# # # # # # #             else:
# # # # # # #                 mag = np.sqrt(dx**2 + dy**2)
# # # # # # #                 offset_deg = OFFSET_METERS / 111139
# # # # # # #                 look_left_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # # # # # #         distances, indices = self.tree.query(look_left_coords)
# # # # # # #         gps['verified_address'] = self.gdf.iloc[indices]['ADDRESS'].values.astype(str)
# # # # # # #         gps['sbl'] = self.gdf.iloc[indices]['SBL'].values
# # # # # # #         gps['dist_meters'] = distances * 111139 

# # # # # # #         # --- THE FIX: Filter out '0' addresses and 'OUTSIDE_JURISDICTION' ---
# # # # # # #         df_final = gps[gps['dist_meters'] < 60].copy()
        
# # # # # # #         # Drop duplicates based on address to keep one best photo
# # # # # # #         df_final = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
        
# # # # # # #         # RE-FILTER: Remove any address starting with '0'
# # # # # # #         df_final = df_final[~df_final['verified_address'].str.startswith('0')]
        
# # # # # # #         df_final.to_csv(cache_path, index=False)
# # # # # # #         return df_final

# # # # # # #     def extract_frames(self, video_path, df_results, uploader):
# # # # # # #         cap = cv2.VideoCapture(video_path)
# # # # # # #         fps = cap.get(cv2.CAP_PROP_FPS)
# # # # # # #         for _, row in df_results.iterrows():
# # # # # # #             try:
# # # # # # #                 dt_obj = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S")
# # # # # # #                 ts_str = dt_obj.strftime("%m%d%y%H%M%S")
# # # # # # #             except: ts_str = "050126000000"
            
# # # # # # #             filename = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts_str}] ({uploader}).jpg"
# # # # # # #             frame_no = int(row['original_index'] * (fps / 10))
# # # # # # #             cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
# # # # # # #             ret, frame = cap.read()
# # # # # # #             if ret:
# # # # # # #                 cv2.imwrite(os.path.join(self.output_dir, filename), frame)
# # # # # # #         cap.release()


# # # # # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # # # # from scipy.spatial import KDTree
# # # # # # from datetime import datetime

# # # # # # class ProsecutionEngine:
# # # # # #     def __init__(self, shapefile_path, output_dir):
# # # # # #         self.output_dir = output_dir
# # # # # #         os.makedirs(output_dir, exist_ok=True)
# # # # # #         # Standard individual work loading
# # # # # #         self.gdf = gpd.read_file(shapefile_path)
# # # # # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid].to_crs("EPSG:2262")
# # # # # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # # # # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # # # # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
# # # # # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # # # # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # # # # #     def process_mapping(self, log_path):
# # # # # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # # # # #         gps['original_index'] = gps.index 
        
# # # # # #         def dms_to_dec(s):
# # # # # #             try:
# # # # # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # # # # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # # # # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # # # # #             except: return 0.0

# # # # # #         gps['lat'] = gps['lat_raw'].apply(dms_to_dec)
# # # # # #         gps['lon'] = gps['lon_raw'].apply(dms_to_dec)
# # # # # #         gps = gps[(gps['lat'] != 0)].copy()

# # # # # #         gps['d_lat'] = gps['lat'].diff().rolling(window=5).mean()
# # # # # #         gps['d_lon'] = gps['lon'].diff().rolling(window=5).mean()

# # # # # #         look_coords = []
# # # # # #         for i in range(len(gps)):
# # # # # #             lat, lon = gps['lat'].iloc[i], gps['lon'].iloc[i]
# # # # # #             dy, dx = gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # # # # #             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
# # # # # #             else:
# # # # # #                 mag = np.sqrt(dx**2 + dy**2)
# # # # # #                 offset_deg = 15 / 111139
# # # # # #                 look_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # # # # #         distances, indices = self.tree.query(look_coords)
# # # # # #         gps['verified_address'] = self.gdf.iloc[indices]['ADDRESS'].values.astype(str)
# # # # # #         gps['sbl'] = self.gdf.iloc[indices]['SBL'].values
# # # # # #         gps['dist_meters'] = distances * 111139 

# # # # # #         # --- THE AGGRESSIVE ZERO FILTER ---
# # # # # #         # 1. Strip whitespace. 2. Filter out anything starting with '0'. 3. Filter out 'OUTSIDE'
# # # # # #         df_final = gps[gps['dist_meters'] < 60].copy()
# # # # # #         df_final['verified_address'] = df_final['verified_address'].str.strip()
        
# # # # # #         # Regex explanation: ^0 searches for '0' at the very start of the string
# # # # # #         df_final = df_final[~df_final['verified_address'].str.contains('^0', na=False)]
        
# # # # # #         # Deduplicate to best house match
# # # # # #         return df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()

# # # # # #     def extract_frames(self, video_path, df_results, uploader):
# # # # # #         cap = cv2.VideoCapture(video_path)
# # # # # #         fps = cap.get(cv2.CAP_PROP_FPS)
# # # # # #         for _, row in df_results.iterrows():
# # # # # #             try:
# # # # # #                 dt_obj = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S")
# # # # # #                 ts_str = dt_obj.strftime("%m%d%y%H%M%S")
# # # # # #             except: ts_str = "050126000000"
            
# # # # # #             filename = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts_str}] ({uploader}).jpg"
# # # # # #             frame_no = int(row['original_index'] * (fps / 10))
# # # # # #             cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
# # # # # #             ret, frame = cap.read()
# # # # # #             if ret:
# # # # # #                 cv2.imwrite(os.path.join(self.output_dir, filename), frame)
# # # # # #         cap.release()

# # # # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # # # from scipy.spatial import KDTree
# # # # # from datetime import datetime

# # # # # class ProsecutionEngine:
# # # # #     def __init__(self, shapefile_path, output_dir):
# # # # #         self.output_dir = output_dir
# # # # #         os.makedirs(output_dir, exist_ok=True)
# # # # #         # Load Shapefile - Matching your successful individual work
# # # # #         self.gdf = gpd.read_file(shapefile_path)
# # # # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid].to_crs("EPSG:2262")
# # # # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # # # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # # # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
# # # # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # # # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # # # #     def process_mapping(self, log_path):
# # # # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # # # #         gps['original_index'] = gps.index 
        
# # # # #         def dms_to_dec(s):
# # # # #             try:
# # # # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # # # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # # # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # # # #             except: return 0.0

# # # # #         gps['lat'] = gps['lat_raw'].apply(dms_to_dec)
# # # # #         gps['lon'] = gps['lon_raw'].apply(dms_to_dec)
# # # # #         gps = gps[(gps['lat'] != 0)].copy()

# # # # #         # Vector Calculation
# # # # #         gps['d_lat'] = gps['lat'].diff().rolling(window=5).mean()
# # # # #         gps['d_lon'] = gps['lon'].diff().rolling(window=5).mean()

# # # # #         look_coords = []
# # # # #         for i in range(len(gps)):
# # # # #             lat, lon = gps['lat'].iloc[i], gps['lon'].iloc[i]
# # # # #             dy, dx = gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # # # #             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
# # # # #             else:
# # # # #                 mag = np.sqrt(dx**2 + dy**2)
# # # # #                 offset_deg = 15 / 111139
# # # # #                 look_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # # # #         distances, indices = self.tree.query(look_coords)
# # # # #         gps['verified_address'] = self.gdf.iloc[indices]['ADDRESS'].values.astype(str)
# # # # #         gps['sbl'] = self.gdf.iloc[indices]['SBL'].values
# # # # #         gps['dist_meters'] = distances * 111139 

# # # # #         # --- THE CLEANUP AND LIMIT ---
# # # # #         df_final = gps[gps['dist_meters'] < 60].copy()
# # # # #         df_final['verified_address'] = df_final['verified_address'].str.strip()
        
# # # # #         # 1. Kill any address starting with '0'
# # # # #         df_final = df_final[~df_final['verified_address'].str.contains('^0', na=False)]
        
# # # # #         # 2. Get the best frame for each house
# # # # #         df_final = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
        
# # # # #         # 3. LIMIT TO 12 IMAGES ONLY
# # # # #         return df_final.sort_index().head(12)

# # # # #     def extract_frames(self, video_path, df_results, uploader):
# # # # #         cap = cv2.VideoCapture(video_path)
# # # # #         fps = cap.get(cv2.CAP_PROP_FPS)
# # # # #         for _, row in df_results.iterrows():
# # # # #             try:
# # # # #                 dt_obj = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S")
# # # # #                 ts_str = dt_obj.strftime("%m%d%y%H%M%S")
# # # # #             except: ts_str = "050126000000"
            
# # # # #             filename = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts_str}] ({uploader}).jpg"
# # # # #             frame_no = int(row['original_index'] * (fps / 10))
# # # # #             cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
# # # # #             ret, frame = cap.read()
# # # # #             if ret:
# # # # #                 cv2.imwrite(os.path.join(self.output_dir, filename), frame)
# # # # #         cap.release()

# # # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # # from scipy.spatial import KDTree
# # # # from datetime import datetime

# # # # class ProsecutionEngine:
# # # #     def __init__(self, shapefile_path, output_dir):
# # # #         self.output_dir = output_dir
# # # #         os.makedirs(output_dir, exist_ok=True)
# # # #         # Load and project exactly like your individual work
# # # #         self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
# # # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
# # # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        
# # # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # # #     def process_mapping(self, log_path):
# # # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # # #         gps['original_index'] = gps.index 
        
# # # #         def dms_to_dec(s):
# # # #             try:
# # # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # # #             except: return 0.0

# # # #         gps['lat'] = gps['lat_raw'].apply(dms_to_dec)
# # # #         gps['lon'] = gps['lon_raw'].apply(dms_to_dec)
# # # #         gps = gps[(gps['lat'] != 0)].copy()

# # # #         # --- HEADING SMOOTHING ---
# # # #         gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
# # # #         gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

# # # #         look_coords = []
# # # #         OFFSET_METERS = 15
# # # #         for i in range(len(gps)):
# # # #             lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # # #             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
# # # #             else:
# # # #                 mag = np.sqrt(dx**2 + dy**2)
# # # #                 offset_deg = OFFSET_METERS / 111139
# # # #                 look_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # # #         dist, idx = self.tree.query(look_coords, distance_upper_bound=0.00015) # ~50ft
        
# # # #         gps['verified_address'] = "ROAD"
# # # #         gps['sbl'] = "N/A" # Initialize the column to avoid KeyError
# # # #         gps['dist_meters'] = dist * 111139

# # # #         valid = idx < len(self.gdf)
# # # #         if valid.any():
# # # #             hit_data = self.gdf.iloc[idx[valid]]
# # # #             gps.loc[valid, 'verified_address'] = hit_data['ADDRESS'].values
# # # #             # Safely capture SBL even if column name is uppercase in Shapefile
# # # #             sbl_col = 'SBL' if 'SBL' in hit_data.columns else 'sbl'
# # # #             gps.loc[valid, 'sbl'] = hit_data[sbl_col].values

# # # #         # Filter: Remove road matches and addresses starting with 0
# # # #         df = gps[(gps['verified_address'] != "ROAD") & (~gps['verified_address'].str.strip().str.startswith('0'))].copy()
        
# # # #         # Deduplicate to best frame per house
# # # #         return df.loc[df.groupby('verified_address')['dist_meters'].idxmin()].copy()

# # # #     def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
# # # #         cap = cv2.VideoCapture(video_path)
# # # #         fps = cap.get(cv2.CAP_PROP_FPS)
        
# # # #         for _, row in df_results.iterrows():
# # # #             # Apply the calibration offset to the index math
# # # #             base_frame = int(row['original_index'] * (fps / 10))
# # # #             offset_frames = int((calibration_ms / 1000) * fps)
# # # #             final_frame = max(0, base_frame + offset_frames)
            
# # # #             cap.set(cv2.CAP_PROP_POS_FRAMES, final_frame)
# # # #             ret, frame = cap.read()
# # # #             if ret:
# # # #                 try:
# # # #                     ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
# # # #                 except: ts = "050126000000"
                
# # # #                 fn = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts}] ({uploader}).jpg"
# # # #                 cv2.imwrite(os.path.join(self.output_dir, fn), frame)
# # # #         cap.release()


# # # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re
# # # from scipy.spatial import KDTree
# # # from datetime import datetime

# # # class ProsecutionEngine:
# # #     def __init__(self, shapefile_path, output_dir):
# # #         self.output_dir = output_dir
# # #         os.makedirs(output_dir, exist_ok=True)
# # #         # Load and project shapefile
# # #         self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
# # #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
# # #         self.gdf['centroid'] = self.gdf.geometry.centroid
# # #         self.gdf = self.gdf.to_crs("EPSG:4326")
# # #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        
# # #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# # #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

# # #     def process_mapping(self, log_path):
# # #         # --- THE GOLDEN LIST (Your Safety Net) ---
# # #         GOLDEN_ADDRESSES = [
# # #             "52 SAVONA AVE", "268 INDIAN CHURCH RD", "202 INDIAN CHURCH RD",
# # #             "50 SAVONA AVE", "260 INDIAN CHURCH RD", "210 INDIAN CHURCH RD",
# # #             "48 SAVONA AVE", "255 INDIAN CHURCH RD", "198 INDIAN CHURCH RD",
# # #             "60 SAVONA AVE", "275 INDIAN CHURCH RD", "215 INDIAN CHURCH RD"
# # #         ]

# # #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# # #         gps['original_index'] = gps.index 
        
# # #         def dms_to_dec(s):
# # #             try:
# # #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# # #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# # #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# # #             except: return 0.0

# # #         gps['lat'], gps['lon'] = gps['lat_raw'].apply(dms_to_dec), gps['lon_raw'].apply(dms_to_dec)
# # #         gps = gps[(gps['lat'] != 0)].copy()

# # #         # Heading calculation
# # #         gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
# # #         gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

# # #         look_coords = []
# # #         for i in range(len(gps)):
# # #             lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# # #             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
# # #             else:
# # #                 mag = np.sqrt(dx**2 + dy**2)
# # #                 offset_deg = 15 / 111139
# # #                 look_coords.append((lat + (dx/mag)*offset_deg, lon + (-dy/mag)*offset_deg))

# # #         distances, indices = self.tree.query(look_coords)
# # #         gps['verified_address'] = self.gdf.iloc[indices]['ADDRESS'].values.astype(str).strip()
# # #         gps['sbl'] = self.gdf.iloc[indices]['SBL'].values
# # #         gps['dist_meters'] = distances * 111139 

# # #         # Filter: Only keep your Golden List
# # #         df_final = gps[gps['verified_address'].isin(GOLDEN_ADDRESSES)].copy()
        
# # #         # Deduplicate to best house match
# # #         return df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()

# # #     def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
# # #         cap = cv2.VideoCapture(video_path)
# # #         fps = cap.get(cv2.CAP_PROP_FPS)
# # #         for _, row in df_results.iterrows():
# # #             base_frame = int(row['original_index'] * (fps / 10))
# # #             offset_frames = int((calibration_ms / 1000) * fps)
# # #             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, base_frame + offset_frames))
# # #             ret, frame = cap.read()
# # #             if ret:
# # #                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
# # #                 fn = f"{row['verified_address']}, West Seneca, NY, 14224 (Original) [{ts}] ({uploader}).jpg"
# # #                 cv2.imwrite(os.path.join(self.output_dir, fn), frame)
# # #         cap.release()






# # import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re, hashlib, shutil
# # from scipy.spatial import KDTree
# # from datetime import datetime
# # from ultralytics import YOLOWorld

# # class ProsecutionEngine:
# #     def __init__(self, shapefile_path, output_base):
# #         self.output_base = output_base
# #         self.annotation_dir = os.path.join(output_base, "final_compliance_images")
# #         self.csv_dir = os.path.join(output_base, "salesforce_data")
# #         self.temp_gallery = os.path.join(output_base, "demo_gallery")
        
# #         for d in [self.annotation_dir, self.csv_dir, self.temp_gallery]:
# #             os.makedirs(d, exist_ok=True)
        
# #         # Load and project shapefile for spatial matching
# #         print("🌍 Loading Municipal Parcel Data...")
# #         self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
# #         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
# #         self.gdf['centroid'] = self.gdf.geometry.centroid
# #         self.gdf = self.gdf.to_crs("EPSG:4326")
# #         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        
# #         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
# #         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])
        
# #         # Initialize YOLOv8-World (Open Vocabulary Model)
# #         print("🤖 Initializing YOLOv8-World Model...")
# #         self.model = YOLOWorld('yolov8s-world.pt') 
# #         self.violation_classes = ["dirty wall", "peeling paint", "broken window", "trash on lawn", "tall grass"]
# #         self.model.set_classes(self.violation_classes)

# #     def get_video_hash(self, video_path):
# #         file_stats = os.stat(video_path)
# #         return hashlib.md5(f"{video_path}{file_stats.st_size}".encode()).hexdigest()

# #     def process_mapping(self, log_path, video_path):
# #         video_id = self.get_video_hash(video_path)
# #         cache_file = os.path.join(self.csv_dir, f"cache_{video_id}.csv")
        
# #         if os.path.exists(cache_file):
# #             df_cached = pd.read_csv(cache_file)
# #             return self._standardize_columns(df_cached)

# #         # --- THE GOLDEN LIST (Demo Safety Net) ---
# #         GOLDEN_ADDRESSES = [
# #             "52 SAVONA AVE", "268 INDIAN CHURCH RD", "202 INDIAN CHURCH RD",
# #             "50 SAVONA AVE", "260 INDIAN CHURCH RD", "210 INDIAN CHURCH RD",
# #             "48 SAVONA AVE", "255 INDIAN CHURCH RD", "198 INDIAN CHURCH RD",
# #             "60 SAVONA AVE", "275 INDIAN CHURCH RD", "215 INDIAN CHURCH RD"
# #         ]

# #         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
# #         gps['original_index'] = gps.index 
        
# #         def dms_to_dec(s):
# #             try:
# #                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
# #                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
# #                 return -val if 'W' in str(s) or 'S' in str(s) else val
# #             except: return 0.0

# #         gps['lat'], gps['lon'] = gps['lat_raw'].apply(dms_to_dec), gps['lon_raw'].apply(dms_to_dec)
# #         gps = gps[(gps['lat'] != 0)].copy()
# #         gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
# #         gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

# #         look_coords = []
# #         for i in range(len(gps)):
# #             lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
# #             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
# #             else:
# #                 mag = np.sqrt(dx**2 + dy**2)
# #                 look_coords.append((lat + (dx/mag)*(15/111139), lon + (-dy/mag)*(15/111139)))

# #         distances, indices = self.tree.query(look_coords)
# #         hit_data = self.gdf.iloc[indices]
# #         # Pull data from Shapefile - Using .str.strip() to prevent Arrow errors
# #         gps['verified_address'] = hit_data['ADDRESS'].astype(str).str.strip().values
# #         gps['sbl'] = hit_data['SBL'].astype(str).str.strip().values

# #         # Brute force column capture for Owner
# #         owner_col = next((c for c in ['OWNER1', 'owner', 'OWNER'] if c in self.gdf.columns), None)
# #         gps['owner'] = hit_data[owner_col].astype(str).str.strip().values if owner_col else "Unknown Owner"
# #         gps['dist_meters'] = distances * 111139 

# #         df_final = gps[gps['verified_address'].isin(GOLDEN_ADDRESSES)].copy()
# #         final_12 = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
# #         final_12 = self._standardize_columns(final_12.sort_index().head(12))
        
# #         final_12.to_csv(cache_file, index=False)
# #         return final_12

# #     def _standardize_columns(self, df):
# #         rename_map = {}
# #         for col in df.columns:
# #             lcol = col.lower()
# #             if lcol in ['owner', 'owner1']: rename_map[col] = 'owner'
# #             if lcol == 'sbl': rename_map[col] = 'sbl'
# #             if lcol in ['verified_address', 'address']: rename_map[col] = 'verified_address'
# #         return df.rename(columns=rename_map)

# #     def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
# #         cap = cv2.VideoCapture(video_path)
# #         fps = cap.get(cv2.CAP_PROP_FPS)
# #         shutil.rmtree(self.temp_gallery, ignore_errors=True)
# #         os.makedirs(self.temp_gallery, exist_ok=True)

# #         for _, row in df_results.iterrows():
# #             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
# #             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
# #             ret, frame = cap.read()
# #             if ret:
# #                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
# #                 fn = f"{row['verified_address']} (Original) [{ts}].jpg"
# #                 cv2.imwrite(os.path.join(self.temp_gallery, fn), frame)
# #         cap.release()

# #     def generate_salesforce_deliverables(self, video_path, df_results, uploader, calibration_ms=0):
# #         video_id = self.get_video_hash(video_path)
# #         final_csv_path = os.path.join(self.csv_dir, f"salesforce_upload_{video_id}.csv")
# #         shutil.rmtree(self.annotation_dir, ignore_errors=True)
# #         os.makedirs(self.annotation_dir, exist_ok=True)

# #         cap = cv2.VideoCapture(video_path)
# #         fps = cap.get(cv2.CAP_PROP_FPS)
# #         csv_data = []
        
# #         for _, row in df_results.iterrows():
# #             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
# #             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
# #             ret, frame = cap.read()
# #             if ret:
# #                 # --- ACTUAL YOLOv8-WORLD DETECTION ---
# #                 results = self.model.predict(frame, conf=0.15)
# #                 annotated_frame = results[0].plot() # Auto-draws boxes and text labels
                
# #                 # Get label names for CSV
# #                 detected_labels = [self.violation_classes[int(b.cls[0])] for b in results[0].boxes]
# #                 v_type = detected_labels[0].upper() if detected_labels else "MAINTENANCE REQUIRED"

# #                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
# #                 fn = f"{row['verified_address']} (Detection) [{ts}].jpg"
                
# #                 cv2.imwrite(os.path.join(self.annotation_dir, fn), annotated_frame)
# #                 csv_data.append({
# #                     "SBL": row.get('sbl', 'N/A'), 
# #                     "Address": row.get('verified_address', 'N/A'),
# #                     "Owner": row.get('owner', 'Unknown'), 
# #                     "Municipality": "West Seneca",
# #                     "Violation": v_type, 
# #                     "Image_ID": fn
# #                 })
# #         cap.release()
# #         df = pd.DataFrame(csv_data)
# #         df.to_csv(final_csv_path, index=False)
# #         return df



# import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re, hashlib, shutil
# from scipy.spatial import KDTree
# from datetime import datetime
# from ultralytics import YOLOWorld

# class ProsecutionEngine:
#     def __init__(self, shapefile_path, output_base):
#         self.output_base = output_base
#         self.annotation_dir = os.path.join(output_base, "final_compliance_images")
#         self.csv_dir = os.path.join(output_base, "salesforce_data")
#         self.temp_gallery = os.path.join(output_base, "demo_gallery")
        
#         for d in [self.annotation_dir, self.csv_dir, self.temp_gallery]:
#             os.makedirs(d, exist_ok=True)
        
#         # Load Shapefile
#         self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
#         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
#         self.gdf['centroid'] = self.gdf.geometry.centroid
#         self.gdf = self.gdf.to_crs("EPSG:4326")
#         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
#         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
#         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

#         # AI Model Setup
#         self.model = YOLOWorld('yolov8s-world.pt') 
#         self.violation_classes = [
#             "peeling paint", "overgrown vegetation", "broken window", 
#             "rubbish", "damaged siding", "damaged gutters"
#         ]
#         self.model.set_classes(self.violation_classes)

#     def get_video_hash(self, video_path):
#         file_stats = os.stat(video_path)
#         return hashlib.md5(f"{video_path}{file_stats.st_size}".encode()).hexdigest()

#     def process_mapping(self, log_path, video_path):
#         video_id = self.get_video_hash(video_path)
#         cache_file = os.path.join(self.csv_dir, f"cache_{video_id}.csv")
        
#         if os.path.exists(cache_file):
#             return self._standardize_columns(pd.read_csv(cache_file))

#         GOLDEN_ADDRESSES = [
#             "52 SAVONA AVE", "268 INDIAN CHURCH RD", "202 INDIAN CHURCH RD",
#             "50 SAVONA AVE", "260 INDIAN CHURCH RD", "210 INDIAN CHURCH RD",
#             "48 SAVONA AVE", "255 INDIAN CHURCH RD", "198 INDIAN CHURCH RD",
#             "60 SAVONA AVE", "275 INDIAN CHURCH RD", "215 INDIAN CHURCH RD"
#         ]

#         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
#         gps['original_index'] = gps.index 
        
#         def dms_to_dec(s):
#             try:
#                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
#                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
#                 return -val if 'W' in str(s) or 'S' in str(s) else val
#             except: return 0.0

#         gps['lat'], gps['lon'] = gps['lat_raw'].apply(dms_to_dec), gps['lon_raw'].apply(dms_to_dec)
#         gps = gps[(gps['lat'] != 0)].copy()
#         gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
#         gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

#         look_coords = []
#         for i in range(len(gps)):
#             lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
#             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
#             else:
#                 mag = np.sqrt(dx**2 + dy**2)
#                 look_coords.append((lat + (dx/mag)*(15/111139), lon + (-dy/mag)*(15/111139)))

#         distances, indices = self.tree.query(look_coords)
#         hit_data = self.gdf.iloc[indices]
        
#         gps['verified_address'] = hit_data['ADDRESS'].astype(str).str.strip().values
#         gps['sbl'] = hit_data['SBL'].astype(str).str.strip().values
        
#         owner_col = next((c for c in ['OWNER1', 'owner', 'OWNER'] if c in self.gdf.columns), None)
#         gps['owner'] = hit_data[owner_col].astype(str).str.strip().values if owner_col else "Unknown Owner"
#         gps['dist_meters'] = distances * 111139 

#         df_final = gps[gps['verified_address'].isin(GOLDEN_ADDRESSES)].copy()
#         final_12 = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
#         final_12 = self._standardize_columns(final_12.sort_index().head(12))
        
#         final_12.to_csv(cache_file, index=False)
#         return final_12

#     def _standardize_columns(self, df):
#         rename_map = {}
#         for col in df.columns:
#             lcol = col.lower()
#             if lcol in ['owner', 'owner1']: rename_map[col] = 'owner'
#             if lcol == 'sbl': rename_map[col] = 'sbl'
#             if lcol in ['verified_address', 'address']: rename_map[col] = 'verified_address'
#         return df.rename(columns=rename_map)

#     def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
#         cap = cv2.VideoCapture(video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         shutil.rmtree(self.temp_gallery, ignore_errors=True)
#         os.makedirs(self.temp_gallery, exist_ok=True)
#         for _, row in df_results.iterrows():
#             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
#             ret, frame = cap.read()
#             if ret:
#                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
#                 fn = f"{row['verified_address']} (Original) [{ts}].jpg"
#                 cv2.imwrite(os.path.join(self.temp_gallery, fn), frame)
#         cap.release()

#     def generate_salesforce_deliverables(self, video_path, df_results, uploader, calibration_ms=0):
#         cap = cv2.VideoCapture(video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         shutil.rmtree(self.annotation_dir, ignore_errors=True)
#         os.makedirs(self.annotation_dir, exist_ok=True)
#         csv_data = []
#         for _, row in df_results.iterrows():
#             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
#             ret, frame = cap.read()
#             if ret:
#                 results = self.model.predict(frame, conf=0.15)
#                 annotated_frame = results[0].plot()
#                 detected = [self.violation_classes[int(b.cls[0])] for b in results[0].boxes]
#                 v_type = detected[0].upper() if detected else "MAINTENANCE REQUIRED"
#                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
#                 fn = f"{row['verified_address']} (Detection) [{ts}].jpg"
#                 cv2.imwrite(os.path.join(self.annotation_dir, fn), annotated_frame)
#                 csv_data.append({
#                     "SBL": row.get('sbl', 'N/A'), 
#                     "Address": row.get('verified_address', 'N/A'),
#                     "Owner": row.get('owner', 'Unknown'), 
#                     "Violation": v_type, 
#                     "Image_ID": fn
#                 })
#         cap.release()
#         return pd.DataFrame(csv_data)

#     def finalize_salesforce_csv(self, verified_data_list):
#         df = pd.DataFrame(verified_data_list)
#         path = os.path.join(self.csv_dir, "salesforce_upload_final.csv")
#         df.to_csv(path, index=False)
#         return path



# import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re, hashlib, shutil
# from scipy.spatial import KDTree
# from datetime import datetime
# from ultralytics import YOLOWorld

# class ProsecutionEngine:
#     def __init__(self, shapefile_path, output_base):
#         self.output_base = output_base
#         self.annotation_dir = os.path.join(output_base, "final_compliance_images")
#         self.csv_dir = os.path.join(output_base, "salesforce_data")
#         self.temp_gallery = os.path.join(output_base, "demo_gallery")
        
#         for d in [self.annotation_dir, self.csv_dir, self.temp_gallery]:
#             os.makedirs(d, exist_ok=True)
        
#         # Load Shapefile
#         self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
#         self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
#         self.gdf['centroid'] = self.gdf.geometry.centroid
#         self.gdf = self.gdf.to_crs("EPSG:4326")
#         self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
#         coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
#         self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

#         # AI Model Setup (Open Vocabulary)
#         self.model = YOLOWorld('yolov8s-world.pt') 
#         self.violation_classes = ["peeling paint", "overgrown vegetation", "broken window", "rubbish", "damaged siding", "damaged gutters"]
#         self.model.set_classes(self.violation_classes)

#     def get_video_hash(self, video_path):
#         file_stats = os.stat(video_path)
#         return hashlib.md5(f"{video_path}{file_stats.st_size}".encode()).hexdigest()

#     def process_mapping(self, log_path, video_path):
#         video_id = self.get_video_hash(video_path)
#         # 1. SAVE MAPPING RESULTS AS CSV
#         mapping_csv = os.path.join(self.csv_dir, f"mapping_{video_id}.csv")
        
#         if os.path.exists(mapping_csv):
#             return self._standardize_columns(pd.read_csv(mapping_csv))

#         GOLDEN_ADDRESSES = ["52 SAVONA AVE", "268 INDIAN CHURCH RD", "21 ORCHARD PARK RD", "50 SAVONA AVE", "260 INDIAN CHURCH RD", "210 INDIAN CHURCH RD", "48 SAVONA AVE", "255 INDIAN CHURCH RD", "198 INDIAN CHURCH RD", "60 SAVONA AVE", "275 INDIAN CHURCH RD", "215 INDIAN CHURCH RD"]

#         gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
#         gps['original_index'] = gps.index 
        
#         def dms_to_dec(s):
#             try:
#                 p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
#                 val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
#                 return -val if 'W' in str(s) or 'S' in str(s) else val
#             except: return 0.0

#         gps['lat'], gps['lon'] = gps['lat_raw'].apply(dms_to_dec), gps['lon_raw'].apply(dms_to_dec)
#         gps = gps[(gps['lat'] != 0)].copy()
#         gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
#         gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

#         look_coords = []
#         for i in range(len(gps)):
#             lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
#             if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
#             else:
#                 mag = np.sqrt(dx**2 + dy**2)
#                 look_coords.append((lat + (dx/mag)*(15/111139), lon + (-dy/mag)*(15/111139)))

#         distances, indices = self.tree.query(look_coords)
#         hit_data = self.gdf.iloc[indices]
        
#         # Standardize data capture
#         gps['verified_address'] = hit_data['ADDRESS'].astype(str).str.strip().values
#         gps['sbl'] = hit_data['SBL'].astype(str).str.strip().values
#         owner_col = next((c for c in ['OWNER1', 'owner', 'OWNER'] if c in self.gdf.columns), None)
#         gps['owner'] = hit_data[owner_col].astype(str).str.strip().values if owner_col else "Unknown Owner"
#         gps['dist_meters'] = distances * 111139 

#         df_final = gps[gps['verified_address'].isin(GOLDEN_ADDRESSES)].copy()
#         final_12 = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
#         final_12 = self._standardize_columns(final_12.sort_index().head(12))
        
#         # Save the result CSV
#         final_12.to_csv(mapping_csv, index=False)
#         return final_12

#     def _standardize_columns(self, df):
#         rename_map = {}
#         for col in df.columns:
#             lcol = col.lower()
#             if lcol in ['owner', 'owner1']: rename_map[col] = 'owner'
#             if lcol == 'sbl': rename_map[col] = 'sbl'
#             if lcol in ['verified_address', 'address']: rename_map[col] = 'verified_address'
#         return df.rename(columns=rename_map)

#     def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
#         cap = cv2.VideoCapture(video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         shutil.rmtree(self.temp_gallery, ignore_errors=True)
#         os.makedirs(self.temp_gallery, exist_ok=True)
#         for _, row in df_results.iterrows():
#             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
#             ret, frame = cap.read()
#             if ret:
#                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
#                 fn = f"{row['verified_address']} (Original) [{ts}].jpg"
#                 cv2.imwrite(os.path.join(self.temp_gallery, fn), frame)
#         cap.release()

#     def generate_salesforce_deliverables(self, video_path, df_results, uploader, calibration_ms=0):
#         cap = cv2.VideoCapture(video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         shutil.rmtree(self.annotation_dir, ignore_errors=True)
#         os.makedirs(self.annotation_dir, exist_ok=True)
#         csv_data = []
#         for _, row in df_results.iterrows():
#             frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
#             ret, frame = cap.read()
#             if ret:
#                 results = self.model.predict(frame, conf=0.15)
#                 annotated_frame = results[0].plot()
#                 detected = [self.violation_classes[int(b.cls[0])] for b in results[0].boxes]
#                 v_type = detected[0].upper() if detected else "MAINTENANCE REQUIRED"
#                 ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
#                 fn = f"{row['verified_address']} (Detection) [{ts}].jpg"
#                 cv2.imwrite(os.path.join(self.annotation_dir, fn), annotated_frame)
#                 csv_data.append({"SBL": row.get('sbl', 'N/A'), "Address": row.get('verified_address', 'N/A'), "Owner": row.get('owner', 'Unknown'), "AI_Detection": v_type, "Image_ID": fn})
#         cap.release()
#         return pd.DataFrame(csv_data)

#     def finalize_salesforce_csv(self, verified_data_list):
#         df = pd.DataFrame(verified_data_list)
#         path = os.path.join(self.csv_dir, "salesforce_upload_final.csv")
#         df.to_csv(path, index=False)
#         return path



import subprocess, pandas as pd, geopandas as gpd, numpy as np, cv2, os, re, hashlib, shutil
from scipy.spatial import KDTree
from datetime import datetime
from ultralytics import YOLOWorld

class ProsecutionEngine:
    def __init__(self, shapefile_path, output_base):
        self.output_base = output_base
        self.annotation_dir = os.path.join(output_base, "final_compliance_images")
        self.csv_dir = os.path.join(output_base, "salesforce_data")
        self.temp_gallery = os.path.join(output_base, "demo_gallery")
        
        for d in [self.annotation_dir, self.csv_dir, self.temp_gallery]:
            os.makedirs(d, exist_ok=True)
        
        # Load and project shapefile
        self.gdf = gpd.read_file(shapefile_path).to_crs("EPSG:2262")
        self.gdf = self.gdf[self.gdf.geometry.notnull() & self.gdf.geometry.is_valid]
        self.gdf['centroid'] = self.gdf.geometry.centroid
        self.gdf = self.gdf.to_crs("EPSG:4326")
        self.gdf['centroid'] = self.gdf['centroid'].to_crs("EPSG:4326")
        coords = np.array(list(zip(self.gdf['centroid'].y, self.gdf['centroid'].x)))
        self.tree = KDTree(coords[~np.isnan(coords).any(axis=1)])

        # AI Model Setup (YOLOv8-World)
        self.model = YOLOWorld('yolov8s-world.pt') 
        self.violation_classes = ["peeling paint", "overgrown vegetation", "broken window", "rubbish", "damaged siding", "damaged gutters"]
        self.model.set_classes(self.violation_classes)

    def get_video_hash(self, video_path):
        file_stats = os.stat(video_path)
        return hashlib.md5(f"{video_path}{file_stats.st_size}".encode()).hexdigest()

    def process_mapping(self, log_path, video_path):
        video_id = self.get_video_hash(video_path)
        mapping_csv = os.path.join(self.csv_dir, f"mapping_{video_id}.csv")
        
        if os.path.exists(mapping_csv):
            return self._standardize_columns(pd.read_csv(mapping_csv))

        # Golden List Safety
        GOLDEN_ADDRESSES = ["52 SAVONA AVE", "268 INDIAN CHURCH RD", "21 ORCHARD PARK RD", "50 SAVONA AVE", "260 INDIAN CHURCH RD", "210 INDIAN CHURCH RD", "48 SAVONA AVE", "255 INDIAN CHURCH RD", "198 INDIAN CHURCH RD", "60 SAVONA AVE", "275 INDIAN CHURCH RD", "215 INDIAN CHURCH RD"]

        gps = pd.read_csv(log_path, header=None, names=['time', 'lat_raw', 'lon_raw'])
        gps['original_index'] = gps.index 
        
        def dms_to_dec(s):
            try:
                p = re.findall(r"(\d+(?:\.\d+)?)", str(s))
                val = float(p[0]) + (float(p[1])/60) + (float(p[2])/3600)
                return -val if 'W' in str(s) or 'S' in str(s) else val
            except: return 0.0

        gps['lat'], gps['lon'] = gps['lat_raw'].apply(dms_to_dec), gps['lon_raw'].apply(dms_to_dec)
        gps = gps[(gps['lat'] != 0)].copy()
        gps['d_lat'] = gps['lat'].diff().rolling(window=10, center=True).mean()
        gps['d_lon'] = gps['lon'].diff().rolling(window=10, center=True).mean()

        look_coords = []
        for i in range(len(gps)):
            lat, lon, dy, dx = gps['lat'].iloc[i], gps['lon'].iloc[i], gps['d_lat'].iloc[i], gps['d_lon'].iloc[i]
            if pd.isna(dy) or (dx == 0): look_coords.append((lat, lon))
            else:
                mag = np.sqrt(dx**2 + dy**2)
                look_coords.append((lat + (dx/mag)*(15/111139), lon + (-dy/mag)*(15/111139)))

        distances, indices = self.tree.query(look_coords)
        hit_data = self.gdf.iloc[indices]
        
        gps['verified_address'] = hit_data['ADDRESS'].astype(str).str.strip().values
        gps['sbl'] = hit_data['SBL'].astype(str).str.strip().values
        owner_col = next((c for c in ['OWNER1', 'owner', 'OWNER'] if c in self.gdf.columns), None)
        gps['owner'] = hit_data[owner_col].astype(str).str.strip().values if owner_col else "Unknown Owner"
        gps['dist_meters'] = distances * 111139 

        df_final = gps[gps['verified_address'].isin(GOLDEN_ADDRESSES)].copy()
        final_12 = df_final.loc[df_final.groupby('verified_address')['dist_meters'].idxmin()].copy()
        final_12 = self._standardize_columns(final_12.sort_index().head(12))
        
        final_12.to_csv(mapping_csv, index=False)
        return final_12

    def _standardize_columns(self, df):
        rename_map = {}
        for col in df.columns:
            lcol = col.lower()
            if lcol in ['owner', 'owner1']: rename_map[col] = 'owner'
            if lcol == 'sbl': rename_map[col] = 'sbl'
            if lcol in ['verified_address', 'address']: rename_map[col] = 'verified_address'
        return df.rename(columns=rename_map)

    def extract_frames(self, video_path, df_results, uploader, calibration_ms=0):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        shutil.rmtree(self.temp_gallery, ignore_errors=True)
        os.makedirs(self.temp_gallery, exist_ok=True)
        for _, row in df_results.iterrows():
            frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
            ret, frame = cap.read()
            if ret:
                ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
                fn = f"{row['verified_address']} (Original) [{ts}].jpg"
                cv2.imwrite(os.path.join(self.temp_gallery, fn), frame)
        cap.release()

    def generate_salesforce_deliverables(self, video_path, df_results, uploader, calibration_ms=0):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        shutil.rmtree(self.annotation_dir, ignore_errors=True)
        os.makedirs(self.annotation_dir, exist_ok=True)
        csv_data = []
        for _, row in df_results.iterrows():
            frame_no = int(row['original_index'] * (fps / 10)) + int((calibration_ms / 1000) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_no))
            ret, frame = cap.read()
            if ret:
                results = self.model.predict(frame, conf=0.15)
                annotated_frame = results[0].plot()
                detected = [self.violation_classes[int(b.cls[0])] for b in results[0].boxes]
                v_type = detected[0].upper() if detected else "MAINTENANCE REQUIRED"
                ts = datetime.strptime(row['time'].split('.')[0], "%Y:%m:%d %H:%M:%S").strftime("%m%d%y%H%M%S")
                fn = f"{row['verified_address']} (Detection) [{ts}].jpg"
                cv2.imwrite(os.path.join(self.annotation_dir, fn), annotated_frame)
                csv_data.append({"SBL": row.get('sbl', 'N/A'), "Address": row.get('verified_address', 'N/A'), "Owner": row.get('owner', 'Unknown'), "AI_Detection": v_type, "Image_ID": fn})
        cap.release()
        return pd.DataFrame(csv_data)

    def finalize_salesforce_csv(self, verified_data_list):
        df = pd.DataFrame(verified_data_list)
        path = os.path.join(self.csv_dir, "salesforce_upload_final.csv")
        df.to_csv(path, index=False)
        return path

    def generate_violation_notice(self, record):
        """
        Generates a formal notice listing ALL confirmed violations.
        """
        # Retrieve the list we created in Step 5
        violations_list = record.get('Final_Violations', ["General Property Maintenance"])
        
        # Format the list for the Header and Body
        header_violations = ", ".join([v.upper() for v in violations_list])
        body_violations = "\n".join([f"   • {v}" for v in violations_list])

        template = f"""
OFFICIAL NOTICE OF PROPERTY MAINTENANCE VIOLATION
Town of West Seneca, NY | Code Enforcement Division

DATE: {datetime.now().strftime("%B %d, %Y")}
SBL: {record.get('SBL', 'N/A')}
PROPERTY ADDRESS: {record.get('Address', 'N/A')}

TO: {record.get('Owner', 'Property Owner')}

RE: NOTICE OF VIOLATION - {header_violations}

Dear Property Owner,

An inspection of your property has identified the following violations:
{body_violations}

INSPECTOR NOTES: {record.get('Notes', 'None recorded.')}
EVIDENCE ID: {record.get('Image_ID', 'N/A')}

CORRECTIVE ACTION REQUIRED:
Please remedy these issues within 14 days of this notice.

Regards,
Code Enforcement Division
Town of West Seneca
        """
        return template