##################################################
### GLOBAL VARIABLES
##################################################
COLUMN_NAMES = [
    'activity',
    'acc-x-axis',
    'acc-y-axis',
    'acc-z-axis',
    'gyro-x-axis',
    'gyro-y-axis',
    'gyro-z-axis',
    'mag-x-axis',
    'mag-y-axis',
    'mag-z-axis'
]

LABELS_NAMES = [
    'Pushup',
    'Squat',
    'Situp',
    'Jumping',
    'Lunge'
]

# Data
DATA_DIR = 'data/'
DATA_TEMP_DIR = 'data_temp/'
DATA_PATH = 'data/data.pckl'

# Model
MODEL_PATH = 'model/model.h5'
MODEL_PATH_DIR = 'model/'

# Tensorflow only
MODEL_META_PATH = 'model/model.ckpt.meta'


##################################################
### MODEL
##################################################
RANDOM_SEED = 13

# Model
N_CLASSES = len(LABELS_NAMES)
N_FEATURES = 3  # acc, gyro, magnetometer

# Hyperparameters
N_LSTM_LAYERS = 2
N_EPOCHS = 20
L2_LOSS = 0.0015
LEARNING_RATE = 0.0025
N_HIDDEN_NEURONS = 30
BATCH_SIZE = 10
DROPOUT_RATE = 0.5

##################################################
### DATA COLLECTION/PREPROCESSING
##################################################
IMU_MAC_ADDRESS = "FF:3C:8F:22:C9:C8"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"
BLE_HANDLE = "0x0011"

# Data type sent from the device
DATA_TYPE = 'h' # Short integer
DATA_SIZE_BYTES = 2 # Size of short

# How many times to collect samples
DATA_COLLECTION_TIME = 200
SCALE_FACTOR = 100

# Data preprocessing
TIME_STEP = 20
SEGMENT_TIME_SIZE = 40

# Train/test proportion
TEST_SIZE = 0.3

##################################################
### VISUALIZE
##################################################
plotRange_x = 50
plotRange_y = 20
