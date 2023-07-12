# A RadioactiveSource contains unstable isotopes

class RadioactiveSource:
    def __init__(self, activity, lab_source=False):
        self.activity = None
        self.max_calibration_source_activity = 30.
        self.lab_source = lab_source
        if not lab_source:
            self.set_activity(activity)

    def set_activity(self, activity):
        if activity < 0.:
            print('Error: source activity must not be negative!')
        else:
            self.activity = activity
            if activity > self.max_calibration_source_activity:
                print('Warning: the activity specified is higher than the most active source available.')
                print('The activity of the source is set to', self.max_calibration_source_activity, 'Bq.')
                self.activity = self.max_calibration_source_activity

    def get_decays(self, recording_time):
        number = 0
        if recording_time >= 0.:
            expected_value = self.activity * recording_time
            number = stats.poisson.rvs(expected_value)
        else:
            print('Error: recording time must not be negative!')
        return number
