"""Prompt detection must follow the visible console, including redraws."""

import unittest

from windows_terminal import PromptScreen


class PromptScreenTests(unittest.TestCase):
    def test_prompt_drawn_out_of_order(self):
        screen = PromptScreen()
        output = b"\x1b[1;8H[y/N] \x1b[1;1HApply? "
        self.assertNotIn(b"Apply? [y/N]", output)
        for chunk in (output[:3], output[3:15], output[15:]):
            screen.feed(chunk)
        self.assertTrue(screen.contains(b"Apply? [y/N]"))
        screen.feed(b"\x1b[2J")
        self.assertFalse(screen.contains(b"Apply? [y/N]"))

    def test_split_utf8_prompt(self):
        screen = PromptScreen()
        output = "한글 Apply? [y/N]".encode()
        for byte in output:
            screen.feed(bytes([byte]))
        self.assertTrue(screen.contains(output))


if __name__ == "__main__":
    unittest.main()
