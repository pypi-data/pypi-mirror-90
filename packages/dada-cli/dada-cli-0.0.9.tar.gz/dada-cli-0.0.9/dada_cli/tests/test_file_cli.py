import unittest

from click.testing import CliRunner

from dada_test import BaseTest
from dada_cli import dada_file_cli

cli_runner = CliRunner()


class DadaCliTest(BaseTest):
    def test_dada_file_cli(self):
        # https://click.palletsprojects.com/en/7.x/testing/#basic-testing
        fp = self.get_fixture("space-time-motion.mp3")
        result = cli_runner.invoke(dada_file_cli, ["put", fp, "--out"])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
