import pandas as pd


class Sensor(object):

    def __init__(self, id_):

        self.id = id_
        self.df = pd.read_excel(r"U:\StephenJ\Python\Seismometer_Status\GCF_Python\Branch\calvals_merged.xlsx", index_col="id")
        self.calval = self.df.loc[id_, "calval"]
        self.gain = self.df.loc[id_, "gain"]
        self.decimation_factor = self.df.loc[id_, "decimation_factor"]
        self.displacement_factor = self.df.loc[id_, "displacement_factor"]
        self.easting = self.df.loc[id_, "easting"]
        self.northing = self.df.loc[id_, "northing"]
        self.local_factor = self.df.loc[id_, "alpha"]
        self.theta = self.df.loc[id_, "theta"]

    def _update_value(self, column, value):
        """
        Changes a specific value in the data frame, use with care

        :param column:
        :return:
        """

        self.df.loc[self.id, column] = value

        return 0


if __name__ == "__main__":

    s1 = Sensor("Rad1z2")
    print(s1.id)
    print(s1.df)
    print(s1.calval)
