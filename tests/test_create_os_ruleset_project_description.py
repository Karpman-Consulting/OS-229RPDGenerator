import sys
import unittest
import subprocess
import os
import glob
from pathlib import Path


class BaseTestCreateOSRulesetProjectDescription(unittest.TestCase):
    def setUp(self):

        self.script_path = os.path.join(
            os.path.dirname(__file__), "..", "createOSRulesetProjectDescription.py"
        )
        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = os.pathsep.join([self.env.get("PYTHONPATH", ""), os.path.dirname(self.script_path)])

        self.tests_dir = os.path.dirname(__file__)

        self.openstudio_model_path = ""
        self.filled_csv_file_path = ""

        self.weather_file_name = "USA_CO_Denver.Intl.AP.725650_TMY3.epw"
        self.convert_input_format_exe_path = (
            "C:/EnergyPlusV24-2-0/ConvertInputFormat.exe"
        )

        # Check if convert_input_format_exe_path exists
        if not os.path.exists(self.convert_input_format_exe_path):
            raise FileNotFoundError(
                f"ConvertInputFormat executable not found at {self.convert_input_format_exe_path}"
            )

    def create_cp_csv(self):
        result = subprocess.run(
            [
                sys.executable,
                self.script_path,
                "create_cp_csv",
                "--openstudio_model_path",
                self.openstudio_model_path,
                "--weather_file_name",
                self.weather_file_name,
                "--convert_input_format_exe_path",
                self.convert_input_format_exe_path,
            ],
            capture_output=True,
            text=True,
            cwd=self.tests_dir,
            env=self.env
        )

        if result.returncode != 0:
            print("create cp csv failed")
            print(result.stderr)

        self.assertEqual(
            result.returncode, 0, f"Script failed with error: {result.stderr}"
        )

    def create_rpd(self):
        result = subprocess.run(
            [
                sys.executable,
                self.script_path,
                "create_rpd",
                "--openstudio_model_path",
                self.openstudio_model_path,
                "--weather_file_name",
                self.weather_file_name,
                "--csv_file_path",
                self.filled_csv_file_path,
            ],
            capture_output=True,
            text=True,
            cwd=self.tests_dir,
            env=self.env
        )

        if result.returncode != 0:
            print("create rpd failed")
            print(result.stderr)

        self.assertEqual(
            result.returncode, 0, f"Script failed with error: {result.stderr}"
        )

    def tearDown(self):
        # Perform cleanup tasks
        osw_files = glob.glob(os.path.join(self.tests_dir, "*.osw"))
        for osw_file in osw_files:
            os.remove(osw_file)
            print(f"Removed file: {osw_file}")


class TestCreateOSRulesetProjectDescriptionE1(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_E1.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_E1-filled.csv"
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionE2(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_E2.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_E2-filled.csv"
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionE3(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_E3.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_E3-filled.csv"
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF100(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F100.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F100-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF110(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F110.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F110-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF120(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F120.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F120-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF130(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F130.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F130-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF140(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F140.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F140-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF150(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F150.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F150-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF160(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F160.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F160-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF170(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F170.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F170-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF180(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F180.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F180-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF190(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F190.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F190-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF200(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F200.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F200-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF210(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F210.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F210-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF220(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F220.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F220-filled.csv",
        )
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF230(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F230.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F230-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF240(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = os.path.join(
            os.path.dirname(__file__), "Test_F240.osm"
        )
        self.filled_csv_file_path = os.path.join(
            os.path.dirname(__file__),
            "Test_F240-filled.csv",
        )

        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


if __name__ == "__main__":
    unittest.main()
