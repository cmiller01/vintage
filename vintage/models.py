from typing import Tuple, List


class ReceiverIO:
    """ ReceiverIO describes the input/output specs """

    def __init__(self, io_type: str, sensitivity: int, is_input: bool):
        """ 
        io_type is the IO type: mic, line, mm/mc, etc.
        sensitivity is in millivolts
        """
        self.io_type = io_type
        self.sensitivity = sensitivity
        self.is_input = is_input


class Receiver:
    """ Receiver is a stereo receiver"""

    def __init__(
        self,
        brand: str,
        model: str,
        watts: int,
        weight: float,
        distortion: float,
        frequency_response: Tuple[int, int],
        year: int,
        dimensions: Tuple[int, int, int],
        damping_factor: int,
        io: List[ReceiverIO],
    ):
        """ unique on brand - model """
        self.brand = brand
        self.model = model
        self.watts = watts
        self.weight = weight
        self.distortion = distorion
        self.frequency_response = frequency_response
        self.year = year
        self.dimensions = dimensions
        self.damping_factor = damping_factor
        self.io = io


class ReceiverItem:
    """ ReceiverItem is a specific instance of a Receiver"""

    def __init__(self, receiver: Receiver, condition: str):
        self.receiver = receiver
        self.condition = consition
