import os
import sys
import unittest
import time

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

import pingo

class AnyBoardTest(unittest.TestCase):

    def setUp(self):
        self.board = pingo.detect.MyBoard()

    def tearDown(self):
        self.board.cleanup()


class AnyBoardBasics(AnyBoardTest):

    def test_list_pins(self):
        vdd_pin = self.board.pins[2]
        self.assertIsInstance(vdd_pin, pingo.VddPin)

        pin = self.board.pins[13]
        self.assertIsInstance(pin, pingo.DigitalPin)

        #self.assertEqual(len(self.board.pins), 26)

    def test_led(self):
        pin = self.board.pins[13]
        pin.mode = pingo.OUT
        pin.on()

class AnyBoardDigitalInput(AnyBoardTest):

    def test_button(self):
        pin = self.board.pins[8]
        pin.mode = pingo.IN
        output = pingo.LOW
        t0 = time.time()
        delay = 5

        while output == pingo.LOW:
            output = pin.state
            if time.time() - t0 > delay:
                break

        msg = 'The button must be pressed in %ss for this test to pass' % delay
        self.assertEqual(output, pingo.HIGH, msg)


class AnyBoardExceptions(AnyBoardTest):

    @unittest.skip("Not every board needs this test")
    def test_disabled_pin(self):
        pin = self.board.pins[13]
        with self.assertRaises(pingo.DisabledPin) as cm:
            pin.on()

    def test_wrong_pin_mode_in(self):
        pin = self.board.pins[7]
        pin.mode = pingo.IN
        with self.assertRaises(pingo.WrongPinMode) as cm:
            pin.on()

    @unittest.skip("Discuss about this case")
    def test_wrong_pin_mode_out(self):
        pin = self.board.pins[13]
        pin.mode = pingo.OUT
        with self.assertRaises(pingo.WrongPinMode) as cm:
            pin.state


if __name__ == '__main__':
    unittest.main()

