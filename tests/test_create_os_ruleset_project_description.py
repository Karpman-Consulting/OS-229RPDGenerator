import unittest
import subprocess
import os
import shutil
import glob
from pathlib import Path

class BaseTestCreateOSRulesetProjectDescription(unittest.TestCase):


    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), '..', 'createOSRulesetProjectDescription.py')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E1.osm')
        self.weather_file_name = 'USA_CO_Denver.Intl.AP.725650_TMY3.epw'
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.filled_csv_file_path = ""
        self.weather_file_name = 'USA_CO_Denver.Intl.AP.725650_TMY3.epw'
        self.convert_input_format_exe_path = 'C:/EnergyPlusV24-2-0/ConvertInputFormat.exe'
        self.tests_dir = os.path.dirname(__file__)

        # Check if convert_input_format_exe_path exists
        if not os.path.exists(self.convert_input_format_exe_path):
            raise FileNotFoundError(f"ConvertInputFormat executable not found at {self.convert_input_format_exe_path}")

    def create_cp_csv(self):
        result = subprocess.run([
            'python', self.script_path, 'create_cp_csv',
            '--openstudio_model_path', self.openstudio_model_path,
            '--weather_file_name', self.weather_file_name,
            '--convert_input_format_exe_path', self.convert_input_format_exe_path
        ], capture_output=True, text=True, cwd=self.tests_dir)

        if result.returncode != 0:
            print('create cp csv failed')
            print(result.stderr)

        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")
        # Add more assertions here based on the expected output of the script
        # For example, you can check if the CSV file was created or if specific output is present in stdout
        print(f'Copying {self.initial_filed_csv_file_path} to {self.filled_csv_file_path}')
        shutil.copy(self.initial_filed_csv_file_path, self.filled_csv_file_path)

    def create_rpd(self):

        result = subprocess.run([
            'python', self.script_path, 'create_rpd',
            '--openstudio_model_path', self.openstudio_model_path,
            '--weather_file_name', self.weather_file_name,
            '--csv_file_path', self.filled_csv_file_path
        ], capture_output=True, text=True, cwd=self.tests_dir)

        
        if result.returncode != 0:
            print('create rpd failed')
            print(result.stderr)

        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")

    def tearDown(self):
        # Perform cleanup tasks
        osw_files = glob.glob(os.path.join(self.tests_dir, '*.osw'))
        for osw_file in osw_files:
            os.remove(osw_file)
            print(f"Removed file: {osw_file}")


class TestCreateOSRulesetProjectDescription_E1(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E1.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E1', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_E2(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E2.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E2', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    
    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

class TestCreateOSRulesetProjectDescription_E3(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E3.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E3', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F100(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F100_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F100_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F110(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F110_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F110_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F120(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F120_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F120_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F130(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F130_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F130_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F140(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F140_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F140_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F150(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F150_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F150_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

class TestCreateOSRulesetProjectDescription_F160(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_160_autosized2.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_160_autosized2', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F170(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_170_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_170_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F180(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_180_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_180_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

class TestCreateOSRulesetProjectDescription_F190(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_190_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_190_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F200(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_200_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_200_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_200_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_220_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F210(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_210_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_210_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_210_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_210_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

class TestCreateOSRulesetProjectDescription_F220(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_220_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_220_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_220_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_220_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

class TestCreateOSRulesetProjectDescription_F230(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_230_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_230_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_F240(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_F_240_autosized.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_F_240_autosized', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        print(f"Testing create_cp_csv for model {Path(self.openstudio_model_path).stem}")
        self.create_cp_csv()

    def test_create_rpd(self):
        print(f"Testing create_rpd for model {Path(self.openstudio_model_path).stem}")
        self.create_rpd()

if __name__ == '__main__':
    unittest.main()