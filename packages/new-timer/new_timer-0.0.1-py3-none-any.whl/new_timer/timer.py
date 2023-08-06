import time
import math
import logging
import numpy as np
from datetime import datetime

# Set logging config.
FORMAT = '[%(levelname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT)


class ManualTimer(object):
    """
    This class is manual timer.

    Attributes:
    ------
    max: Save maximum elpased time value.

    min: Save minimum elpased time value.

    mean: Save mean elpased time value.


    ## Example:
        from timer import ManualTimer

        timer1 = ManualTimer(string="Print 0 ~ 9999", decimal=2)

        for i in range(10):
            timer1.start()
            for i in range(99999):
                print(i)
            timer1.stop()
    """

    def __init__(self, string="Program", decimal=12, show=True, show_others=False):
        """
        Args:
        -----
        string: Define your timer name.

        decimal: Display to a certain number of decimal places

        show: Show the elapsed time.
        """

        self.__string = string
        self.__decimal = decimal
        self.__show = show
        self.__show_others = show_others

        self.__elapsed_seconds = 0.0
        self.max = None
        self.min = None
        self.mean = None
        self.__time_records = np.array([])


    def start(self):
        """
        Start the timer.
        """
        self.__start_time = time.time()


    def stop(self):
        """
        Stop the timer.

        returns:
        --------
        hours: elapsed hours.

        minutes: elapsed minutes.

        seconds: elapsed seconds.
        """

        self.__elapsed_seconds = time.time() - self.__start_time

        # Get each time elapsed.
        self.__time_records = np.append(self.__time_records, self.__elapsed_seconds)
        logging.debug("self.__time_records: {}".format(self.__time_records))

        hours, minutes, seconds = self.__calc_time(self.__elapsed_seconds)
        self.__calc_3_values()
        
        if self.__show == True:
            logging.info("{} cost time {} hours {} mins {} secs.".format(self.__string, 
                                                                         hours, 
                                                                         minutes,
                                                                         np.round(seconds, self.__decimal)))
        if self.__show_others == True:
            logging.info("{} cost time max: {} hours {} mins {} secs.".format(self.__string, 
                                                                              self.max[0], 
                                                                              self.max[1],
                                                                              np.round(self.max[2], self.__decimal)))
            logging.info("{} cost time min: {} hours {} mins {} secs.".format(self.__string, 
                                                                              self.min[0], 
                                                                              self.min[1],
                                                                              np.round(self.min[2], self.__decimal)))
            logging.info("{} cost time mean: {} hours {} mins {} secs.".format(self.__string, 
                                                                              self.mean[0], 
                                                                              self.mean[1],
                                                                              np.round(self.mean[2], self.__decimal)))
        
        return (hours, minutes, seconds)


    def __calc_time(self, seconds):
        """
        Transfer unit from seconds to hours、minutes and seconds.

        Args:
        -----
        seconds: Input elpased seconds time.
        """
        hours = 0
        minutes = 0

        if seconds < 60:
            pass
        elif seconds/60 >= 1 and seconds/3600 < 1:
            minutes = math.floor(seconds/60 )
            seconds = seconds - minutes*60
        else:
            hours = math.floor(seconds/3600)
            minutes = math.floor((seconds - hours*3600) / 60)
            seconds = seconds - hours*3600 - minutes*60

        return (hours, minutes, seconds)
        
    
    def __calc_3_values(self):
        """
        Calculate maximum、minimum and mean of multiple time records, and transfer unit from seconds to hours、minutes and seconds.
        """

        self.max = self.__calc_time(self.__time_records.max())
        self.min = self.__calc_time(self.__time_records.min())
        self.mean = self.__calc_time(self.__time_records.mean())


class AutoTimer(object):
    """
    This class is automatic timer.

    ## Example:
        from timer import AutoTimer

        a = 0
        with AutoTimer("Pring 0 ~ 9999999", decimal=2)
            for i in range(9999999):
                a += i
                print(a)
    """

    def __init__(self, string="Program", decimal=12, show=True):
        """
        Args:
        -----
        string: Define your timer name.

        decimal: Display to a certain number of decimal places

        show: Show the elapsed time.
        """

        self.__string = string
        self.__decimal = decimal
        self.__show = show
        self.__hours = 0
        self.__minutes = 0
        self.__seconds = 0.0

    def __enter__(self):
        """
        Start the timer.
        """
        self.__start = time.time()

    def __exit__(self, *args):
        """
        Stop the timer.

        return:
        -------
        hours: elapsed hours.

        minutes: elapsed minutes.

        seconds: elapsed seconds.
        """

        self.__seconds = time.time() - self.__start
        
        if self.__seconds < 60:
            pass
        elif self.__seconds/60 >= 1 and self.__seconds/3600 < 1:
            self.__minutes = math.floor(self.__seconds/60 )
            self.__seconds = self.__seconds - self.__minutes*60
        elif self.__seconds/3600 >= 1 :
            self.__hours = math.floor(self.__seconds/3600)
            self.__minutes = math.floor((self.__seconds - self.__hours*3600) / 60)
            self.__seconds = self.__seconds - self.__hours*3600 - self.__minutes*60

        if self.__show == True:
            logging.info("{} cost time {} hours {} mins {} secs.".format(self.__string, 
                                                                         self.__hours, 
                                                                         self.__minutes,
                                                                         np.round(self.__seconds, self.__decimal)))


def get_now_time(format="%Y-%m-%d %H:%M:%S", show=True):
    """
    Gets current time.
    """
    now = datetime.now()
    now = now.strftime(format)
    
    if show == True:
        logging.info("Current time: {}".format(now))
    
    return now


if __name__ == "__main__":
    def circle_area(radius):
        area = radius ** 2 * 3.14
        return area

    timer1 = ManualTimer(decimal=2)
    
    # for i in range(5):
    #     timer1.start()
    #     for i in range(9999):
    #         print(i)
    #     timer1.stop()


    with AutoTimer():
        for i in range(9999):
            print(i)
