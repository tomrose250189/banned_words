import unittest
from main import censor
import sys
import os


class TestCensor(unittest.TestCase):
	"""Unit test class for censor function in main.py, containing all automated tests."""
	
	def test_slpi_cwro(self):
		"""This tests whether censor works as expected reading only one line of prose per iteration and only reading 
		the censor words into a list once."""
		with open("test_slpi_cwro.txt", "w") as test_slpi_cwro_output:
			sys.stdout = test_slpi_cwro_output # Redirect print in censor to temporary output file
			# Appropriate censor function call
			censor(censor_words_file_location, text_file_location, lines_per_iteration=1, censor_words_one_pass=True)
		with open("test_slpi_cwro.txt", "r") as test_slpi_cwro_output:
			while True:
				# Assert every output line in file matches the expected output
				line_output = test_slpi_cwro_output.readline()
				line_correct = cc_test_prose.readline()
				self.assertEqual(line_output, line_correct)
				if line_correct == '': # Stop reading expected output at eof
					break
		cc_test_prose.seek(0) # Reset read head in expected output file
		sys.stdout = sys.__stdout__ # Reset stdout redirection
		os.remove("test_slpi_cwro.txt") # Delete temporary output file if test is successful
					
	def test_slpi_cwrm(self):
		"""This tests whether censor works as expected reading only one line of prose per iteration but reading censor 
		words from file on multiple occassions to reduce memory overhead."""
		with open("test_slpi_cwrm.txt", "w") as test_slpi_cwrm_output:
			sys.stdout = test_slpi_cwrm_output
			censor(censor_words_file_location, text_file_location, lines_per_iteration=1, censor_words_one_pass=False)
		with open("test_slpi_cwrm.txt", "r") as test_slpi_cwrm_output:
			while True:
				line_output = test_slpi_cwrm_output.readline()
				line_correct = cc_test_prose.readline()
				self.assertEqual(line_output, line_correct)
				if line_correct == '':
					break
		cc_test_prose.seek(0)
		sys.stdout = sys.__stdout__
		os.remove("test_slpi_cwrm.txt")

	def test_mlpi_cwro(self):
		"""This tests whether censor works as expected reading multiple lines of prose per iteration and only reading 
		the censor words into a list once."""
		with open("test_mlpi_cwro.txt", "w") as test_mlpi_cwro_output:
			sys.stdout = test_mlpi_cwro_output
			censor(censor_words_file_location, text_file_location, lines_per_iteration=100, censor_words_one_pass=True)
		with open("test_mlpi_cwro.txt", "r") as test_mlpi_cwro_output:
			while True:
				line_output = test_mlpi_cwro_output.readline()
				line_correct = cc_test_prose.readline()
				self.assertEqual(line_output, line_correct)
				if line_correct == '':
					break
		cc_test_prose.seek(0)
		sys.stdout = sys.__stdout__
		os.remove("test_mlpi_cwro.txt")
	
	def test_mlpi_cwrm(self):
		"""This tests whether censor works as expected reading multiple lines of prose per iteration but reading censor 
		words from file on multiple occassions to reduce memory overhead."""
		with open("test_mlpi_cwrm.txt", "w") as test_mlpi_cwrm_output:
			sys.stdout = test_mlpi_cwrm_output
			censor(censor_words_file_location, text_file_location, lines_per_iteration=100, censor_words_one_pass=False)
		with open("test_mlpi_cwrm.txt", "r") as test_mlpi_cwrm_output:
			while True:
				line_output = test_mlpi_cwrm_output.readline()
				line_correct = cc_test_prose.readline()
				self.assertEqual(line_output, line_correct)
				if line_correct == '':
					break
		cc_test_prose.seek(0)
		sys.stdout = sys.__stdout__
		os.remove("test_mlpi_cwrm.txt")


if __name__ == "__main__":
	# Open file with correctly censored text, give file locations for text and censor word files and start unit tests
	with open("test_text_correctly_censored.txt", "r") as cc_test_prose:
		censor_words_file_location = "test_censor_words.txt"
		text_file_location = "test_text.txt"
		unittest.main()
	