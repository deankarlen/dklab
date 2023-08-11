# A RadioactiveSource has a known activity (a calibration source)

class RadioactiveSource:
    def __init__(self, activity):
        self.activity = None
        self.max_calibration_source_activity = 30.
        self.set_activity(activity)

    def set_activity(self, activity):
        if activity < 0.:
            print('Error: calibration source activity must not be negative! Its activity is set to zero.')
            self.activity = 0.
        else:
            self.activity = activity
            if activity > self.max_calibration_source_activity:
                print('Warning: the activity specified is higher than the most active source available.')
                print('The activity of the source is set to', self.max_calibration_source_activity, 'Bq.')
                self.activity = self.max_calibration_source_activity

