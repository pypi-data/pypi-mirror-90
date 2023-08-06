from .binary_metric import BinaryMetric
from tensorflow.keras.backend import epsilon

class Recall(BinaryMetric):
    def _custom_metric(self):
        return self.tp / (self.tp + self.fn + epsilon())