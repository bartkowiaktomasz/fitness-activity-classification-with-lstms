##################################################
### GLOBAL VARIABLES
##################################################
COLUMN_NAMES = [
    'activity',
    # 'timestamp',
    'acc-x-axis',
    'acc-y-axis',
    'acc-z-axis'
    'gyro-x-axis',
    'gyro-y-axis',
    'gyro-z-axis'
    'mag-x-axis',
    'mag-y-axis',
    'mag-z-axis'
]

LABELS_NAMES = [
    'Downstairs',
    'Upstairs',
    'Sitting',
    'Standing',
    'Staying',
    'Walking',
    'Jumping'
]

DATA_DIR = 'data/'
DATA_PATH = 'data/data.pckl'
MODEL_PATH = 'model/classificator.ckpt'
MODEL_META_PATH = 'model/classificator.ckpt.meta'
MODEL_CHECKPOINT_PATH = 'model/'



RANDOM_SEED = 13

# Data preprocessing
# For WSIDM TIME_STEP = 100, SEGMENT_TIME_SIZE = 180
TIME_STEP = 10
SEGMENT_TIME_SIZE = 10

# Model
N_CLASSES = 6
N_FEATURES = 3  # x-acceleration, y-acceleration, z-acceleration

# Hyperparameters
N_LSTM_LAYERS = 2
N_EPOCHS = 50
L2_LOSS = 0.0015
LEARNING_RATE = 0.0025
N_HIDDEN_NEURONS = 30
BATCH_SIZE = 1

##################################################
### DATA COLLECTION - GATT
##################################################
IMU_MAC_ADDRESS = "FF:3C:8F:22:C9:C8"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"

# Data type sent from the device
DATA_TYPE = 'h' # Short integer
DATA_SIZE_BYTES = 2

DATA_COLLECTION_ITERATIONS = 1

SCALE_FACTOR = 100

##################################################
### DATA TESTING
##################################################
TEST_SIZE = 0.3
