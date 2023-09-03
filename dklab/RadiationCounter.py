# A RadiationCounter accepts a RadioactiveSource and counts the number of decays over a fixed period of time

import requests
from scipy import stats


class RadiationCounter:
    def __init__(self, student_id=0):
        self.student_id = int(student_id)
        self.counting_time = 10.
        self.source = None  # will be a radioactive source if one is inserted into the counter
        self.lab_source = False  # specifies whether the lab source is inside the counter (only one source at a time)
        self.count = -1
        self.success = False  # specifies whether the last measurement was successful

        print("Lab radiation counter built for student ID: " + str(self.student_id) +
              ". Default counting time is", self.counting_time, "seconds.")

    def set_counting_time(self, counting_time):
        if counting_time > 30.:  # If this is changed, also update text below and dklab-server
            print('Counting time not changed:', counting_time, 'seconds is too long to wait! (30 seconds max)')
        elif counting_time < 0.:
            print('Error: Counting time must not be negative. Counting time is not changed.')
        else:
            self.counting_time = counting_time

    def get_counting_time(self):
        return self.counting_time

    def insert_lab_source(self):
        if self.source is not None:
            print('The calibration source has been removed from the counter.')
            self.source = None  # only one source is allowed at a time
        if self.lab_source:
            print('The lab source is already in the counter.')
        else:
            print('The lab source has been inserted into the counter.')
        self.lab_source = True

    def insert_calibration_source(self, source):
        if self.lab_source:
            print('The lab source has been removed from the counter.')
            self.lab_source = False  # only one source is allowed at a time
        if self.source is None:
            print('The calibration source has been inserted into the counter')
        elif self.source == source:
            print('The calibration source is already in the counter.')
        else:
            print('The calibration source in the counter has been replaced by the new source.')
        self.source = source

    def remove_source(self):
        self.source = None
        self.lab_source = False

    def get_count(self):
        return self.count

    def get_success(self):
        return self.success

    def start(self):
        print('Measurement has begun. Please wait',self.counting_time,'seconds.')
        self.success = True

        i_counting_time = int(self.counting_time * 1000000)
        if self.source is not None:
            i_activity = int(self.source.activity * 1000000)
        elif self.lab_source:
            i_activity = -1
        else:
            i_activity = 0

        try:
            command = 'get_counts/' + str(self.student_id) + '/' + str(i_counting_time) + '/' + str(i_activity)
            response = requests.get('http://dklab.ipypm.ca/' + command)
            self.count = response.json()['counts']
        except requests.exceptions.RequestException as error:
            print('Error retrieving data from the detector:')
            print()
            print(error)
            self.count = -1
            self.success = False

        if self.success:
            print('Number of counts observed in', self.counting_time, 'seconds was',self.count)


class SimulatedRadiationCounter:
    def __init__(self, efficiency=1., background=0.):
        self.counting_time = 10.
        self.source = None
        self.efficiency = efficiency
        self.background = background
        print("Simulated detector built. Counting time =", self.counting_time,
              "Efficiency =", efficiency, "Background rate=", background, "(Hz)")

    def set_counting_time(self, counting_time):
        if counting_time < 0.:
            print('Error: Counting time must not be negative')
        else:
            self.counting_time = counting_time

    def get_counting_time(self):
        return self.counting_time

    def insert_calibration_source(self, source):
        self.source = source

    def set_efficiency(self, efficiency):
        if 0. <= efficiency <= 1.:
            self.efficiency = efficiency
        else:
            print('Error: Efficiency must be between 0. and 1.')

    def set_background(self, background):
        if background >= 0.:
            self.background = background
        else:
            print('Error: Background rate cannot be negative')

    def get_data(self, reps=2):
        activity = 0
        if self.source is not None:
            activity = self.source.activity
        expected_value = activity * self.counting_time * self.efficiency + self.background * self.counting_time
        return stats.poisson.rvs(expected_value, size=reps)

    def get_likelihood(self, count):
        activity = 0
        if self.source is not None:
            activity = self.source.activity
        expected_value = activity * self.counting_time * self.efficiency + self.background * self.counting_time
        likelihood = stats.poisson.pmf(count, expected_value)

        return likelihood
