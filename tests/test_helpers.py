import unittest
import obspy

# import the functions to test
from _helpers import _calibrate

class TestHelpers(unittest.TestCase):
    """
    Testing the helper function _helpers._calibration
    """
    def setUp(self):
        self.gcf_path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical"
                         r"\5.1 Monitoring Campaign\381-190109-4013\2019-10-01\6v70z2\20190926_1800.gcf")

        self.test_stream = obspy.read(self.gcf_path)


    def test_calibrate_calibration(self):
        """
        Test that the calibration values (calval/gain) are applied correctly
        :return:
        """

        # set up the two streams to test against each other
        testing_stream = self.test_stream.copy()
        constructing_stream = self.test_stream.copy()

        # This is what the function does
        test_output = _calibrate(testing_stream, 2, 1, 1)

        # satisfy the other conditions in the same way as the function so that we only test the calibration part
        for trace in constructing_stream:

            trace.split()
            trace.detrend('linear')
            trace.decimate(1)

        # test that all the data points are the same (note the *2 since that's the calibration factor we are testing
        for i in range(len(test_output)):
            for j in range(len(test_output[i].data)):
                self.assertEqual(constructing_stream[i].data[j]*2, test_output[i].data[j])


    def test_calibrate_decimation(self):
        """
        Testing that the obspy decimation function reduces the sample rate by the correct factor
        (this is the only test I can think of for this)

        :return:
        """

        # divide all sampling rates by two
        constructed_sample_rates = [trace.stats.sampling_rate/2 for trace in self.test_stream]
        # apply the calibration function to the test stream
        calibrated_stream = _calibrate(self.test_stream, 1, 1, 2)
        # check the same sampler rates are obtained as the constructed_sample_rates
        testing_sample_rates = [trace.stats.sampling_rate for trace in calibrated_stream]

        self.assertEqual(constructed_sample_rates, testing_sample_rates)


    def test_select_channel(self):
        """
        The Fortis, and the radians require different channels to be selected.
        Test that the correct channel is selected

        :return:
        """




if __name__ == '__main__':
    unittest.main()
