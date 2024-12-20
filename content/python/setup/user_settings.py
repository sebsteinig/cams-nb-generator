# Data directory where files will be stored
DATA_DIR = './data'

# Get yesterday and today dates for default forecast times
today = datetime.now()
yesterday = today - timedelta(days=1)

# Forecast base time (when the forecast starts from)
# Default: Yesterday, but can be changed to any date in the past (YYYY-MM-DD)
FORECAST_BASE_TIME = yesterday.strftime('%Y-%m-%d')

# Forecast valid time (the time we want to forecast for)
# Default: Today, but can be changed to any date within 5 days of the forecast base time (YYYY-MM-DD)
FORECAST_VALID_TIME = today.strftime('%Y-%m-%d')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)