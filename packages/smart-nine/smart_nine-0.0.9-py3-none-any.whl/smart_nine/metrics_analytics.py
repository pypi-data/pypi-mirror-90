from . import constants
from scipy.signal import find_peaks

class MetricsAnalytics():
    """
    Use to determine top nine images in set
    """
    def __init__(self):
        pass        
        
    def find_top_nine_peaks(self, ts_list, like_list, filename_list, username, year):
        """
        Returns subset of input lists based on top nine filtering
        """
        if len(like_list) < constants.MATRIX_SIZE:
            raise ValueError(f"Instagram account: @{username} doesn't have at least 9 photographs in year: {year}")

        distance = int(len(like_list) / constants.SPACING)
        if distance < constants.MIN_SPACING:
            distance = constants.MIN_SPACING

        peak_indices = (find_peaks(like_list, distance=distance)[0])

        if len(peak_indices) < constants.MATRIX_SIZE:
            print(f"Failed to find peaks, finding max points instead.")
            peak_indices = [i[0] for i in sorted(enumerate(like_list), key=lambda k: k[1], reverse=True)][0:9]

        ts_peak = [ts_list[peak_index] for peak_index in peak_indices]
        like_peak = [like_list[peak_index] for peak_index in peak_indices]
        filename_peak = [filename_list[peak_index] for peak_index in peak_indices]

        return ts_peak, like_peak, filename_peak