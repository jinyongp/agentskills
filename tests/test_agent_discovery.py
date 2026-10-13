"""Keep real-agent discovery failures bounded and ensure noisy children can exit."""

import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from smoke_agents import JsonProcess


class AgentDiscoveryProcessTests(unittest.TestCase):
    def test_oversized_protocol_line_fails_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            client = JsonProcess([sys.executable, "-c",
                                  "import sys;sys.stdout.write('x'*(1024*1024+1)+'\\n');sys.stdout.flush()"],
                                 directory, os.environ)
            try:
                with self.assertRaisesRegex(RuntimeError, "exceeded 1 MiB") as error:
                    client.request({"id": 1}, lambda r: r.get("id") == 1)
                self.assertLess(len(str(error.exception)), 1000)
            finally:
                client.close()
            self.assertIsNotNone(client.process.poll())

    def test_large_stderr_is_drained_and_reported_with_omission_count(self):
        with tempfile.TemporaryDirectory() as directory:
            client = JsonProcess([sys.executable, "-c",
                                  "import sys;sys.stderr.write('x'*65536);sys.stderr.flush();"
                                  "sys.stdout.write('invalid json\\n');sys.stdout.flush()"],
                                 directory, os.environ)
            try:
                with self.assertRaisesRegex(RuntimeError, "invalid JSON") as error:
                    client.request({"id": 1}, lambda r: r.get("id") == 1)
                self.assertRegex(str(error.exception), r"\d+ bytes omitted")
                self.assertLess(len(str(error.exception)), 5000)
            finally:
                client.close()
            self.assertIsNotNone(client.process.poll())
            self.assertEqual(client.stderr_bytes, 65536)
            self.assertEqual(len(client.stderr), 4096)


if __name__ == "__main__":
    unittest.main()
