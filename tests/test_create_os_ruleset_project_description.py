import unittest
import subprocess
import os
import shutil
import glob

class BaseTestCreateOSRulesetProjectDescription(unittest.TestCase):

    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), '..', 'createOSRulesetProjectDescription.py')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E1.osm')
        self.weather_file_name = 'USA_CO_Denver.Intl.AP.725650_TMY3.epw'
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.filled_csv_file_path = ".flake8"
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

        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")
        # Add more assertions here based on the expected output of the script
        # For example, you can check if the CSV file was created or if specific output is present in stdout
        print(result.stdout, 'result stdout create_cp_csv')

        shutil.copy(self.initial_filed_csv_file_path, self.filled_csv_file_path)

    
    def create_rpd(self):

        result = subprocess.run([
            'python', self.script_path, 'create_rpd',
            '--openstudio_model_path', self.openstudio_model_path,
            '--weather_file_name', self.weather_file_name,
            '--csv_file_path', self.filled_csv_file_path
        ], capture_output=True, text=True, cwd=self.tests_dir)

        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")
        # Add more assertions here based on the expected output of the script
        # For example, you can check if the CSV file was created or if specific output is present in stdout
        #self.assertIn("Expected output", result.stdout)
        print(result.stdout, 'result stdout create_rpd')


    def tearDown(self):
        # Perform cleanup tasks
        osw_files = glob.glob(os.path.join(self.tests_dir, '*.osw'))
        for osw_file in osw_files:
            os.remove(osw_file)
            print(f"Removed file: {osw_file}")


# class TestCreateOSRulesetProjectDescription_E1(BaseTestCreateOSRulesetProjectDescription):

#     def setUp(self):
#         super().setUp()
#         self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
#         self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E1.osm')
#         self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E1', 'run','Test_E1_filled.csv' )

#         print(f'Using openstudio model at: {self.openstudio_model_path}')

#     def test_create_cp_csv(self):
#         self.create_cp_csv()

#     def test_create_rpd(self):
#         self.create_rpd()


class TestCreateOSRulesetProjectDescription_E2(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E2.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E2', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        self.create_cp_csv()

    def test_create_rpd(self):
        self.create_rpd()


class TestCreateOSRulesetProjectDescription_E3(BaseTestCreateOSRulesetProjectDescription):

    def setUp(self):
        super().setUp()
        self.initial_filed_csv_file_path = os.path.join(os.path.dirname(__file__),'Test_E1_filled.csv')
        self.openstudio_model_path = os.path.join(os.path.dirname(__file__), 'Test_E3.osm')
        self.filled_csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_E3', 'run','Test_E1_filled.csv' )

        print(f'Using openstudio model at: {self.openstudio_model_path}')

    def test_create_cp_csv(self):
        self.create_cp_csv()

    def test_create_rpd(self):
        self.create_rpd()



if __name__ == '__main__':
    unittest.main()

# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(TestCreateOSRulesetProjectDescription('test_create_cp_csv'))
#     suite.addTest(TestCreateOSRulesetProjectDescription('test_create_rpd'))

#     # Run the test suite
#     runner = unittest.TextTestRunner()
#     runner.run(suite)