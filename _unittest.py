# Ignore warnings with
# python -W ignore _unittest

import unittest
import numpy as np
import random

from config import *
from preprocessing import *

def create_sample_dataframe():
    ax_readings = []
    ay_readings = []
    az_readings = []
    mx_readings = []
    my_readings = []
    mz_readings = []
    gx_readings = []
    gy_readings = []
    gz_readings = []
    activity_list = [LABELS_NAMES[0] for _ in range(SEGMENT_TIME_SIZE)]


    for _ in range(SEGMENT_TIME_SIZE):
        ax_readings.append(random.uniform(-10,10))
        ay_readings.append(random.uniform(-10,10))
        az_readings.append(random.uniform(-10,10))
        mx_readings.append(random.uniform(-10,10))
        my_readings.append(random.uniform(-10,10))
        mz_readings.append(random.uniform(-10,10))
        gx_readings.append(random.uniform(-10,10))
        gy_readings.append(random.uniform(-10,10))
        gz_readings.append(random.uniform(-10,10))

    data_dict = {
                COLUMN_NAMES[0]: activity_list, COLUMN_NAMES[1]: ax_readings,
                COLUMN_NAMES[2]: ay_readings, COLUMN_NAMES[3]: az_readings,
                COLUMN_NAMES[4]: gx_readings, COLUMN_NAMES[5]: gy_readings,
                COLUMN_NAMES[6]: gz_readings, COLUMN_NAMES[7]: mx_readings,
                COLUMN_NAMES[8]: my_readings, COLUMN_NAMES[9]: mz_readings
                }

    df = pd.DataFrame(data=data_dict)
    return df


class TestPreprocessing(unittest.TestCase):

    def test_label_position(self):
        existing_label = LABELS_NAMES[0]
        unexisting_label = "This label does not exist"

        self.assertGreaterEqual(label_position(existing_label), 0)
        with self.assertRaises(NameError):
            label_position(unexisting_label)

    def test_one_hot_encode(self):
        arr = np.zeros(N_CLASSES)
        arr[1] = 1
        label = [LABELS_NAMES[1]]
        np.testing.assert_array_equal(one_hot_encode(label)[0], arr)

    def test_get_convoluted_data(self):
        df = create_sample_dataframe()
        data_convoluted, labels = get_convoluted_data(df)
        self.assertEqual(data_convoluted.shape[0], 1)
        self.assertEqual(data_convoluted.shape[1], SEGMENT_TIME_SIZE)
        self.assertEqual(data_convoluted.shape[2], N_FEATURES)
        self.assertEqual(labels.shape[0], 1)
        self.assertEqual(labels.shape[1], N_CLASSES)


if __name__ == '__main__':
    unittest.main()
