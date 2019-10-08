import unittest
import obspy

# import the functions to test
from _helpers import _calibrate

class TestCalibration(unittest.TestCase):

    def setUp(self):
        self.gcf_path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical"
                         r"\5.1 Monitoring Campaign\381-190109-4013\2019-10-01\6v70z2\20190926_1800.gcf")

        self.test_stream = obspy.read(self.gcf_path)


    def test_calibrate_calibration(self):
        """
        Test that the calibration values (calval/gain) are applied correctly
        :return:
        """
        test_stream1 = self.test_stream.copy()
        test_stream2 = self.test_stream.copy()

        test_output = _calibrate(test_stream1, 2, 1, 1)

        for trace in test_stream2:
            for datapoint in trace.data:
                datapoint = datapoint * 2

            trace.split()
            trace.detrend('linear')
            trace.decimate(1)


        # firstly test that the two streams have the same number of traces
        self.assertEqual(len(test_stream2), len(test_output))

        # test that all the traces are the same length
        for i in range(len(test_output)):
            self.assertEqual(len(test_stream2[i]), len(test_output[i]))

        # test that all the datapoints are the same
        for i in range(len(test_output)):
            for j in range(len(test_output[i].data)):
                self.assertEqual(test_stream2[i].data[j], test_output[i].data[j])


    def test_calibrate_decimation(self):
        """
        Test that the decimation is working correctly

        :param self:
        :return:
        """

        # divide all sampling rates by two
        initial_srs = [trace.stats.sampling_rate/2 for trace in self.test_stream]

        calibrated_stream = _calibrate(self.test_stream, 1, 1, 2)

        # check the same is achieved using the calibrate function
        test_srs = [trace.stats.sampling_rate for trace in calibrated_stream]

        self.assertEqual(initial_srs, test_srs)



if __name__ == '__main__':
    unittest.main()
