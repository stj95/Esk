import pandas as pd
import obspy
import _helpers
import navigation


if __name__ == "__main__":

    download_folders_path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir"
                             r"\5 Technical\5.1 Monitoring Campaign\381-190109-4013")

    download_folders = ["2019-10-01"]
    sensors = ["6v70"]

    df = navigation.psd_download_folder(download_folders_path, download_folders, sensors)

    print(df)

