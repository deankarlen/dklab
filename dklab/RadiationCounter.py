# A RadiationCounter accepts a RadiationSource and counts the number of decays over a fixed period of time

import requests
from scipy import stats

from dklab.RadioactiveSource import RadioactiveSource


class RadiationCounter:
    def __init__(self, student_id=0):
        self.student_id = student_id
        self.counting_time = 10.
        self.source = None
        self.count = 0
        self.lab_source = RadioactiveSource(0., lab_source=True)
        print("Lab radiation counter built for student ID" + str(self.student_id) + \
              ". Default counting time is", self.counting_time, "seconds.")

    def set_counting_time(self, counting_time):
        if counting_time > 30.:
            print('Counting time not changed:', counting_time, 'seconds is too long to wait! (30 seconds max)')
        elif counting_time < 0.:
            print('Error: Counting time must not be negative')
        else:
            self.counting_time = counting_time

    def get_counting_time(self):
        return self.counting_time

    def insert_lab_source(self):
        self.source = self.lab_source

    def insert_known_source(self, source):
        self.source = source

    def remove_source(self):
        self.source = None

    def get_count(self):
        return self.count

    def start(self):
        success = True
        try:
            i_counting_time = int(self.counting_time * 1000000)
            if self.source.lab_source:
                i_activity = -1
            else:
                i_activity = int(self.source.activity * 1000000)
            command = 'get_counts/' + str(self.student_id) + '/' + str(i_counting_time) + '/' + str(i_activity)
            response = requests.get('http://dklab.ipypm.ca/' + command)
            self.count = int(response)
        except requests.exceptions.RequestException as error:
            print('Error retrieving data from the detector:')
            print()
            print(error)
            self.count = 0
            success = False

        return success


class SimulatedRadiationCounter(RadiationCounter):
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

    def insert_lab_source(self):
        print('Error: You cannot put the lab source into a simulated detector!')

    def insert_known_source(self, source):
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

    def start(self):
        print('To get data from the simulated detector, use the "get_data" method.')

    def get_data(self, reps=2):
        try:
            i_counting_time = int(self.counting_time * 1000000)
            i_activity = int(self.source.activity * 1000000)
            i_background = int(self.source.background * 1000000)
            i_efficiency = int(self.source.efficiency * 1000000)
            command = 'get_sim_counts/' + str(self.student_id) + '/' + str(i_counting_time) + '/' +\
                      str(i_activity) + '/' + str(i_background) + '/' + str(i_efficiency)
            response = requests.get('http://dklab.ipypm.ca/' + command)
            counts = response.json()['counts']
        except requests.exceptions.RequestException as error:
            print('Error retrieving data from the simulator:')
            print()
            print(error)
            counts = []
        return counts

    def get_likelihood(self, count):
        activity = 0
        if self.source is not None:
            activity = self.source.activity
        expected_value = activity * self.counting_time * self.efficiency + self.background * self.counting_time
        likelihood = stats.poisson.pmf(count, expected_value)

        return likelihood
