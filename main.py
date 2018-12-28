import sys
import re


def censor(censor_words_file_location, text_file_location, censor_text_file_location, censor_words_per_iteration=20):
	"""Looks up a user specified number of censor words from the censor word file and creates an output text file of the
	original text file with these words removed. This repeats until all the censor words from the censor word file have
	been removed in the output text file. Selecting the number of censor words to be stored in memory at a time allows
	for a memory vs time trade-off decision to be made."""
	with open(censor_words_file_location, 'r') as cwf, open(censor_text_file_location, 'w+') as ctf, open(text_file_location, 'r') as tf:
		first_iteration = True
		# print("Creating: " + censor_text_file_location + ", a censored version of " + text_file_location + ", with words listed in " + censor_words_file_location + " removed.")
		while True:
			if first_iteration:
				read_file = tf # initially the source text file is read from.
			else:
				read_file = ctf # further iterations the output file is updated in read-write mode, so no temp files are created.
			censor_words = []
			for _ in range(censor_words_per_iteration):
				cw = cwf.readline().rstrip() # remove newline and trailing whitespace
				if cw == '':
					break # Keep reading until the end of the censor word file
				censor_words.append(cw)
			if censor_words == [] and not first_iteration:
				ctf.seek(0)
				print(ctf.read()) # Print entire output file to stdout.
				print()
				break # Function breaks and exits once there are no more censor words to remove (but after the first iteration, to allow an output file to be produced, even when the censor word file is empty).
			read_file.seek(0) # reset read and write heads
			ctf.seek(0)
			while True:
				pos_i = read_file.tell() # read a line and note the read head position before and after
				repl_line = read_file.readline()
				pos_f = read_file.tell()
				if repl_line == '':
					break # stop reading the read_file at eof
				for cw in censor_words: # for each censor word read from the censor word file
					repl_cw = '*'*len(cw)
					repl_line = re.sub(r'^'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE) # find and replace censor word (case insensitive) with appropriate number of *s when it occurs at the start of a line.
					repl_line = re.sub(r'(?<=\W)'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE) # replace censor word "" "". Lookahead and lookbehind regexs are required to avoid overlapping matches, meaning not all occurrences of censor words are removed from a line.
				ctf.seek(pos_i) # write to the appropriate position in the output text file and reset write head (required for read-write mode).
				ctf.write(repl_line)
				ctf.seek(pos_f)
			first_iteration = False
		# print("Finished.")


def test_1(censor_words_file_location, text_file_location, censor_text_file_location, verbose=False):
	"""For each censor word found in the censor word file, this test tests to see whether that word occurs in the source
	text and if so, whether all occurrences of it have been removed in the output text. This test fails if a censor word
	 is found in the output text file."""
	with open(censor_words_file_location, 'r') as cwf, open(censor_text_file_location, 'r') as ctf, open(text_file_location, 'r') as tf:
		print("Running test_1.")
		for cw in cwf:
			cw = cw.rstrip()
			tf.seek(0)
			ctf.seek(0)
			tf_count = len(re.findall(r'(^|[^\w\d]+)'+cw+r'([^\w\d]+|$)', tf.read(), flags=re.IGNORECASE))
			ctf_count = len(re.findall(r'(^|[^\w\d]+)'+cw+r'([^\w\d]+|$)', ctf.read(),flags=re.IGNORECASE))
			if verbose:
				print("Censor word: " + cw + "   Number of occurrences in text file: " + str(tf_count) + "   Number of occurences in censored text file: " + str(ctf_count) + ".")
			if ctf_count != 0: # Early fail.
				print("test_1 failed.")
				return False
		print("test_1 passed")
		return True


def test_2(text_file_location, censor_text_file_location, verbose=False):
	"""For each line in the source text file, this checks that the corresponding (stepping sequentially from the start)
	output text file line has the same number of characters. If the number of characters agree, this gives some
	confidence that the correct number of *s have been used to censor a word if a censor word is present in the line and
	also the line has been correctly copied otherwise. This test fails if there's a character count mismatch for 2
	corresponding lines."""
	with open(censor_text_file_location, 'r') as ctf, open(text_file_location, 'r') as tf:
		print("running test_2")
		line_number = 1
		for line in ctf:
			line_len = len(line)
			censor_line_len = len(tf.readline())
			if verbose:
				print("Line number: " + str(line_number) + ". Line length in text file is: " + str(line_len) + ". Line length in censor file is: " + str(censor_line_len) + ".")
			if line_len != censor_line_len:
				print("test_2 failed.")
				return False
		print("test_2 passed")
		return True
		
		
if __name__ == "__main__":
	# Command line input parsing
	if len(sys.argv) == 4 and sys.argv[3] == '-t':
		tests = True
	elif len(sys.argv) == 3:
		tests = False
	else:
		print("Incorrect number of command line inputs. USAGE: Requires a censor words file location & a text file location. For an additional quality testing of the output, use the additional switch -t after the file names.")
		exit()

	# Get input file locations and create a corresponding output file location
	censor_words_file_location = sys.argv[1]
	text_file_location = sys.argv[2]
	censor_text_file_location = re.sub(r'(\.txt$)', r'_censored\1', text_file_location)
	# Main censor functionality
	censor(censor_words_file_location, text_file_location, censor_text_file_location, censor_words_per_iteration=67)
	# Automated tests performed if selected. Modular design for ease of addition and deletion.
	if tests:
		all_tests_pass = True
		all_tests_pass = all_tests_pass and test_1(censor_words_file_location, text_file_location, censor_text_file_location, verbose=False)
		all_tests_pass = all_tests_pass and test_2(text_file_location, censor_text_file_location, verbose=False)
		
		if all_tests_pass:
			print("All tests have passed.")
		else:
			print("One or more tests have failed.")
