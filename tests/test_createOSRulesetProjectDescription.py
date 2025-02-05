import unittest
import os
import glob
from pathlib import Path

from openstudio229.createOSRulesetProjectDescription import handle_create_csv, handle_create_rpd, setup_analysis_directory


class BaseTestCreateOSRulesetProjectDescription(unittest.TestCase):
    def setUp(self):
        self.tests_dir = Path(__file__).parent
        self.script_path = self.tests_dir.parent / "createOSRulesetProjectDescription.py"
        self.weather_file_path = self.tests_dir.parent / "weather" / "USA_CO_Denver.Intl.AP.725650_TMY3.epw"

        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = os.pathsep.join([self.env.get("PYTHONPATH", ""), str(self.script_path.parent)])

        # Set up paths which are required, but do not set a default to ensure they are set by the test
        self.openstudio_model_path: Path = None
        self.filled_csv_file_path: Path = None

        self.convert_input_format_exe_path = Path(
            "C:/EnergyPlusV24-2-0/ConvertInputFormat.exe"
        )

        # Check if convert_input_format_exe_path exists
        if not os.path.exists(self.convert_input_format_exe_path):
            raise FileNotFoundError(
                f"ConvertInputFormat executable not found at {self.convert_input_format_exe_path}"
            )

    def create_comp_param_csv(self):
        analysis_path = Path(self.openstudio_model_path).parent / Path(self.openstudio_model_path).stem
        try:
            handle_create_csv(self.convert_input_format_exe_path, self.openstudio_model_path, self.weather_file_path, analysis_path)

        except Exception as e:
            self.fail(f"Test Error in create_cp_csv: {e}")

    def create_rpd(self):
        analysis_path = Path(self.openstudio_model_path).parent / Path(self.openstudio_model_path).stem
        try:
            handle_create_rpd(analysis_path, self.filled_csv_file_path)

        except Exception as e:
            self.fail(f"Test Error in create_rpd: {e}")

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
        self.openstudio_model_path = self.tests_dir / "Test_E1.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_E1-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionE2(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_E2.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_E2-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionE3(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_E3.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_E3-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF100(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F100.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F100-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF110(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F110.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F110-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF120(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F120.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F120-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF130(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F130.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F130-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF140(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F140.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F140-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF150(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F150.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F150-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF160(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F160.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F160-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF170(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F170.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F170-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF180(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F180.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F180-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF190(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F190.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F190-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF200(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F200.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F200-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF210(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F210.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F210-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF220(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F220.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F220-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF230(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F230.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F230-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescriptionF240(
    BaseTestCreateOSRulesetProjectDescription
):
    def setUp(self):
        super().setUp()
        self.openstudio_model_path = self.tests_dir / "Test_F240.osm"
        self.filled_csv_file_path = self.tests_dir / "Test_F240-filled.csv"
        setup_analysis_directory(self.openstudio_model_path)
        print(f"Using openstudio model at: {self.openstudio_model_path}")

    def test_create_cp_csv(self):
        print(
            f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}"
        )
        self.create_comp_param_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


if __name__ == "__main__":
    unittest.main()
