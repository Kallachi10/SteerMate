================================================================================
                    STEERMATE BACKEND - COMPLETE EXPLANATION
================================================================================

================================================================================
HOW THE BACKEND WORKS - SIMPLE OVERVIEW
================================================================================

SteerMate is a Driver Assistance System. The backend is the "brain" that stores
data and handles communication between the mobile app and the database.

WHAT IT DOES (In Simple Terms):
-------------------------------
1. STORES USER ACCOUNTS - People register/login to track their driving
2. STORES TRIP DATA - Every drive is saved with GPS, speed, events
3. DETECTS UNSAFE DRIVING - Tracks hard braking, speeding, harsh turns
4. RECOGNIZES TRAFFIC SIGNS - Uses AI to identify speed limits, warnings
5. PROVIDES ANALYTICS - Gives drivers insights on how to improve

THE FLOW (How Data Moves):
--------------------------

   [Mobile App] -----> [Backend API] -----> [PostgreSQL Database]
                            |
                     [ML/AI Module]
                  (Traffic Sign Detection)

   Step 1: User opens app, registers/logs in
           └──> Backend creates account, returns JWT token (like a password)

   Step 2: User starts a driving trip
           └──> App collects GPS, speed, accelerometer data locally
           └──> App's camera captures road signs (optional)

   Step 3: User ends trip
           └──> App sends all trip data to backend
           └──> Backend stores trip, events, sign detections

   Step 4: User views history/analytics
           └──> App requests data from backend
           └──> Backend returns trips, stats, recommendations

MAIN TECHNOLOGIES:
------------------
• FastAPI (Python) - The web framework that handles all HTTP requests
• PostgreSQL - Database that stores all the data permanently
• SQLAlchemy - Talks to the database using Python code (ORM)
• JWT Tokens - Secure way to know which user is making requests
• TensorFlow Lite - Runs AI model for traffic sign detection
• YOLOv8 - The AI model trained to detect 43 types of traffic signs

API STRUCTURE (What URLs Do What):
----------------------------------
/auth/*       --> Registration and Login
/user/*       --> User profile management
/trips/*      --> Trip data (upload, view, reports)
/detection/*  --> Traffic sign detection features

================================================================================
DIRECTORY STRUCTURE
================================================================================

backend/
├── .env                        # Secret configuration (DB password, JWT key)
├── .env.example                # Template for .env file
├── .python-version             # Python version (3.12)
├── pyproject.toml              # Project metadata
├── requirements.txt            # Python packages to install
├── uv.lock                     # Package lock file
├── config.py                   # Settings loader
├── database.py                 # Database connection setup
├── main.py                     # App entry point (starts everything)
│
├── models/                     # DATABASE TABLES (what data looks like)
│   ├── __init__.py             # Exports all models
│   ├── user.py                 # User accounts table
│   └── trip.py                 # Trips, events, sign detections tables
│
├── schemas/                    # DATA VALIDATION (what requests/responses look like)
│   ├── __init__.py             # Exports all schemas
│   ├── user.py                 # User request/response formats
│   ├── profile.py              # Profile update format
│   ├── trip.py                 # Trip data formats
│   └── detection.py            # Detection API formats
│
├── routers/                    # API ENDPOINTS (the actual URLs)
│   ├── __init__.py             # Exports all routers
│   ├── auth.py                 # /auth/* - Login, Register
│   ├── user.py                 # /user/* - Profile
│   ├── trips.py                # /trips/* - Trip management
│   └── detection.py            # /detection/* - Sign detection
│
├── utils/                      # HELPER FUNCTIONS
│   ├── __init__.py             # Exports utilities
│   ├── security.py             # Password hashing, JWT tokens
│   └── dependencies.py         # User authentication check
│
├── ml/                         # MACHINE LEARNING (AI for sign detection)
│   ├── __init__.py             # Exports ML components
│   ├── sign_classes.py         # All 43 traffic sign types
│   ├── detector.py             # TFLite model wrapper
│   ├── driver_scoring.py       # Safety score calculation
│   └── models/                 # Trained model files
│       └── traffic_signs.tflite  # The AI model (12MB)
│
└── training/                   # MODEL TRAINING (how we built the AI)
    ├── README.md               # Training instructions
    ├── scripts/                # Training scripts
    │   ├── convert_gtsrb_to_yolo.py  # Dataset converter
    │   ├── train_yolov8.py           # Training script
    │   └── download_pretrained.py    # Model downloader
    ├── data/                   # Training dataset
    │   └── traffic_signs.yaml  # Dataset config
    └── models/                 # Training outputs
        └── traffic_signs_gtsrb/  # Trained model weights

================================================================================
ROOT-LEVEL FILES (Detailed)
================================================================================

### .env (SECRETS - Never share this file!)

Contains sensitive configuration that changes per environment:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/steermate
JWT_SECRET_KEY=your-super-secret-key-here
JWT_EXPIRY_DAYS=7
DEBUG=true
```

### .env.example

Safe template showing what variables are needed. Copy this to .env and fill in.

### config.py (28 lines)

Loads settings from .env file using Pydantic Settings.
```python
class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 7
    debug: bool = True
```

### database.py (45 lines)

Sets up connection to PostgreSQL database.
- Creates async engine and session factory
- Auto-creates all tables on startup
- Provides database sessions to API routes

### main.py (58 lines)

The entry point - starts the FastAPI application.
- Registers all API routers
- Configures CORS (allows mobile app to connect)
- Creates database tables on startup
- Defines root (/) and health check (/health) endpoints

================================================================================
models/ FOLDER - DATABASE TABLES
================================================================================

These files define what data is stored and how tables are structured.

### models/__init__.py
Exports: User, Trip, TripEvent, SignDetection

### models/user.py - User Accounts Table

Table name: "users"
Columns:
  • id (int) - Primary key, auto-increment
  • email (str) - Unique, indexed for fast lookup
  • password_hash (str) - Bcrypt hashed password (never store plain text!)
  • name (str|null) - Display name
  • created_at (datetime) - When account was created

### models/trip.py - Trip Data Tables

Contains 3 related tables:

1. TRIPS TABLE (Table: "trips")
   - id: Primary key
   - user_id: Which user owns this trip
   - start_time, end_time: When trip occurred
   - duration_seconds: Total trip length
   - distance_m: Distance traveled in meters
   - avg_speed_m_s, max_speed_m_s: Speed stats
   - unsafe_events: Count of dangerous events

2. TRIP EVENTS TABLE (Table: "trip_events")
   - id: Primary key
   - trip_id: Which trip this belongs to
   - event_type: 'hard_brake', 'overspeed', 'harsh_accel', 'unsafe_curve'
   - timestamp: When it happened
   - lat, lon: GPS coordinates
   - speed_m_s: Speed at that moment
   - accel_m_s2: Acceleration/deceleration value

3. SIGN DETECTIONS TABLE (Table: "sign_detections")
   - id: Primary key
   - trip_id: Which trip this belongs to
   - ts: Detection timestamp
   - sign_class: e.g., 'speed_limit_60', 'stop', 'yield'
   - confidence: AI confidence (0.0-1.0)
   - bbox: Bounding box coordinates in image

================================================================================
schemas/ FOLDER - DATA VALIDATION
================================================================================

These files define what data the API accepts and returns. They validate
incoming requests and format outgoing responses.

### schemas/user.py - User Data Formats

UserCreate: For registration
  { email, password, name }

UserLogin: For login (uses OAuth2 form)
  { username (email), password }

UserResponse: What's returned for user data
  { id, email, name, created_at }

Token: Login response
  { access_token, token_type: "bearer" }

### schemas/profile.py - Profile Updates

ProfileUpdate:
  { name (optional) }

### schemas/trip.py - Trip Data Formats

TripUpload: What the app sends after a trip
  { start_time, end_time, duration_seconds, distance_m,
    avg_speed_m_s, max_speed_m_s, events[], sign_detections[] }

TripResponse: Full trip data returned by API
  { id, all trip fields, events[], sign_detections[] }

TripSummary: Brief trip info for lists
  { id, start_time, end_time, distance_m, unsafe_events }

### schemas/detection.py - Detection API Formats

SignClassInfo: Traffic sign class details
  { id, name, category, speed_limit_value }

DetectionResult: Single detection
  { class_id, class_name, confidence, bbox }

================================================================================
routers/ FOLDER - API ENDPOINTS
================================================================================

These files define the actual URLs and what happens when you call them.

### routers/auth.py - Authentication (/auth/*)

POST /auth/register
  - Input: { email, password, name }
  - What it does: Creates new user, hashes password
  - Output: { id, email, name, created_at }

POST /auth/login
  - Input: Form with username (email), password
  - What it does: Verifies credentials, creates JWT token
  - Output: { access_token, token_type: "bearer" }

### routers/user.py - User Profile (/user/*)

🔒 All endpoints require JWT token in header

GET /user/profile
  - What it does: Returns current user's profile
  - Output: { id, email, name, created_at }

PUT /user/profile
  - Input: { name }
  - What it does: Updates user's name
  - Output: Updated user data

### routers/trips.py - Trip Management (/trips/*)

🔒 All endpoints require JWT token in header

POST /trips/upload
  - Input: Complete trip data with events and detections
  - What it does: Saves everything to database
  - Output: Saved trip with ID

GET /trips
  - What it does: Lists all trips for current user
  - Output: Array of trip summaries

GET /trips/{trip_id}
  - What it does: Gets full trip details
  - Output: Trip with all events and sign detections

GET /trips/{trip_id}/report
  - What it does: Generates analytics report
  - Output: Stats, event breakdown, driving recommendations

### routers/detection.py - Traffic Sign Detection (/detection/*)

GET /detection/classes
  - What it does: Returns all 43 traffic sign types
  - Output: Array of sign class info

GET /detection/classes/{class_id}
  - What it does: Gets details for one sign type
  - Output: Single sign class info

GET /detection/model/info
  - What it does: Returns ML model metadata
  - Output: { model_name, num_classes, input_size, is_available }

GET /detection/model/download
  - What it does: Downloads TFLite model file
  - Output: Binary file (traffic_signs.tflite)

POST /detection/detect
  - Input: Image file upload
  - What it does: Runs AI detection on image
  - Output: { detections[], detected_speed_limit }

GET /detection/speed-limits
  - What it does: Returns speed limit sign mappings
  - Output: { class_id: km_per_hour, ... }

================================================================================
utils/ FOLDER - HELPER FUNCTIONS
================================================================================

### utils/security.py - Password & Token Security

hash_password(password) -> hashed_string
  - Uses bcrypt with 12 rounds of salt
  - Never store plain passwords!

verify_password(plain, hashed) -> True/False
  - Checks if password matches hash

create_access_token(data) -> jwt_string
  - Creates JWT token with user_id and expiry
  - Signs with secret key

decode_access_token(token) -> data or None
  - Verifies and decodes JWT token
  - Returns None if invalid/expired

### utils/dependencies.py - Request Dependencies

get_db() -> DatabaseSession
  - Provides database connection to routes
  - Auto-handles commit/rollback

get_current_user(token, db) -> User
  - Extracts user from JWT token
  - Raises 401 Unauthorized if invalid
  - Used by all protected routes

================================================================================
ml/ FOLDER - MACHINE LEARNING MODULE
================================================================================

This is the AI brain that recognizes traffic signs!

### ml/sign_classes.py - Traffic Sign Definitions

GTSRB_CLASSES: Dictionary of all 43 German traffic sign types
  
  Speed Limits (Classes 0-8):
    0: Speed limit 20 km/h
    1: Speed limit 30 km/h
    2: Speed limit 50 km/h
    3: Speed limit 60 km/h
    4: Speed limit 70 km/h
    5: Speed limit 80 km/h
    6: End of 80 km/h limit
    7: Speed limit 100 km/h
    8: Speed limit 120 km/h
  
  Other Signs (Classes 9-42):
    9: No passing
    10: No passing for trucks
    11-12: Right of way signs
    13: Yield
    14: Stop
    15-17: Prohibition signs
    18-31: Warning signs (curves, road work, pedestrians, etc.)
    32: End of all limits
    33-42: Directional and mandatory signs

Helper functions:
  get_speed_limit_value(class_id) -> km/h or None
  get_class_name(class_id) -> string
  is_warning_sign(class_id) -> bool
  is_speed_limit_sign(class_id) -> bool

### ml/detector.py - AI Model Runner

SignDetector class:
  - Loads TFLite model into memory
  - Runs inference on images
  - Returns detected signs with confidence scores

Methods:
  load() -> bool: Load model file
  detect(image_bytes) -> list: Run detection
  is_available() -> bool: Check if model is ready

### ml/driver_scoring.py - Safety Score Algorithm

Calculates driving safety scores based on:
  - Number of hard braking events
  - Speeding incidents
  - Harsh acceleration
  - Unsafe curve handling

Returns:
  - Overall score (0-100)
  - Category scores
  - Improvement recommendations

### ml/models/traffic_signs.tflite (12MB)

The trained YOLOv8n model in TensorFlow Lite format.
- Trained on 35,000+ images
- 43 traffic sign classes
- 99.5% accuracy (mAP50)
- Optimized for mobile devices

================================================================================
training/ FOLDER - HOW THE AI MODEL WAS TRAINED
================================================================================

### training/README.md
Instructions for training the model.

### training/scripts/convert_gtsrb_to_yolo.py
Converts GTSRB dataset to YOLO format:
- Reads CSV annotations
- Normalizes bounding boxes
- Creates train/val/test splits
- Generates YAML config

### training/scripts/train_yolov8.py
Main training script:
- Loads YOLOv8n base model
- Fine-tunes on GTSRB dataset
- Exports to TFLite format

### training/scripts/download_pretrained.py
Downloads pre-trained models for quick start.

### training/data/traffic_signs.yaml
Dataset configuration for YOLO training.

### training/models/traffic_signs_gtsrb/
Contains trained model weights:
- best.pt: Best PyTorch weights (6.2MB)
- last.pt: Final epoch weights

================================================================================
COMPLETE API REFERENCE
================================================================================

AUTHENTICATION
  POST /auth/register      Create account
  POST /auth/login         Get JWT token

USER PROFILE (🔒 Protected)
  GET  /user/profile       Get my profile
  PUT  /user/profile       Update my profile

TRIPS (🔒 Protected)
  POST /trips/upload       Upload trip data
  GET  /trips              List my trips
  GET  /trips/{id}         Get trip details
  GET  /trips/{id}/report  Get trip analytics

DETECTION
  GET  /detection/classes           All 43 sign types
  GET  /detection/classes/{id}      One sign type
  GET  /detection/model/info        Model metadata
  GET  /detection/model/download    Download model file
  POST /detection/detect            Detect signs in image
  GET  /detection/speed-limits      Speed limit mappings

SYSTEM
  GET  /                   API info
  GET  /health             Health check

================================================================================
RUNNING THE BACKEND
================================================================================

PREREQUISITES:
  • Python 3.10+ installed
  • PostgreSQL database (or Docker)
  • pip or uv package manager

QUICK START:

1. Navigate to backend folder:
   cd backend/

2. Create environment file:
   cp .env.example .env
   # Edit .env with your database URL and secret key

3. Install dependencies:
   pip install -r requirements.txt
   # OR: uv sync

4. Start PostgreSQL (if using Docker):
   docker compose up -d

5. Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

ACCESS POINTS:
  • API Root: http://localhost:8000
  • API Docs: http://localhost:8000/docs
  • Health Check: http://localhost:8000/health

================================================================================
END OF EXPLANATION
================================================================================
