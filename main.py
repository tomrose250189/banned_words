from __future__ import print_function
import sys
import re


def one_pass_censor(censor_words_file_location, text_file_location, lines_per_iteration):
	"""This function creates a list of censor words from the censor word file. It then reads 'lines_per_iteration' lines of the text file, 
	substituting all letters of a censor word with a '*'. The resultant lines are printed out to stdout. This process finishes when the end 
	of the text file is reached."""
	with open(censor_words_file_location, 'r') as cwf:
		censor_words = []
		while True:
			cw = cwf.readline().rstrip() # Remove newline and trailing whitespace
			if cw == '':
				break # Keep reading until the end of the censor word file
			censor_words.append((cw, len(cw))) # Include the length in a tuple so it doesn't need to keep be recalculated
	with open(text_file_location, 'r') as tf:
		repl_lines = True # Initial condition required to enter while loop to start reading text file
		while repl_lines: # Keep reading whilst there are replacement lines to search for censor words in
			repl_lines = []
			for _ in range(lines_per_iteration): # Ensure that repl_lines.size() <= lines_per_iteration
				line = tf.readline()
				if line == '':
					break # Stop reading at eof
				repl_lines.append(line)
			repl_lines = "".join(repl_lines) # Transform list of lines back into multi-line string
			if repl_lines == "": # Return if end of text file is reached
				return
			for cw, lcw in censor_words: # for each censor word read from the censor word file
				repl_cw = '*'*lcw
				# Find and replace censor word (case insensitive) with appropriate number of *s when it occurs at the 
				# start of a line.
				repl_lines = re.sub(r'^'+cw+r'(?=\W)', repl_cw, repl_lines, flags=re.IGNORECASE)
				# Replace censor word "" "". Lookahead and lookbehind regexs are required to avoid overlapping matches, 
				# meaning not all occurrences of censor words are removed from a line.
				repl_lines = re.sub(r'(?<=\W)'+cw+r'(?=\W)', repl_cw, repl_lines, flags=re.IGNORECASE) 
			print(repl_lines, end='')

def censor(censor_words_file_location, text_file_location, lines_per_iteration, censor_words_one_pass=False):
	"""This function reads 'lines_per_iteration' lines of the text file at a time. If 'censor_words_one_pass' is true,
	all censor words are read once and put into a list, otherwise if false they are read one at a time, saving memory but
	requiring multiple re-reads of the same word for different groups of text file lines.
	The groups of text file lines then have every character of a contained censor word replaced with '*' using the re.sub 
	function. After all censor words have been substituted in the group of text file lines, they are printed to stdout."""
	if censor_words_one_pass:
		return one_pass_censor(censor_words_file_location, text_file_location, lines_per_iteration)
	with open(text_file_location, 'r') as tf, open(censor_words_file_location, 'r') as cwf:
		repl_lines = True # Initial condition required to enter while loop to start reading text file
		while repl_lines: # Keep reading whilst there are replacement lines to search for censor words in
			repl_lines = []
			for _ in range(lines_per_iteration): # Ensure that repl_lines.size() <= lines_per_iteration
				line = tf.readline()
				if line == '':
					break # Stop reading at eof
				repl_lines.append(line)
			repl_lines = "".join(repl_lines) # Transform list of lines back into multi-line string
			while repl_lines:
				cw = cwf.readline().rstrip() # Remove newline and trailing whitespace
				if cw == '':
					break # Keep reading until the end of the censor word file
				repl_cw = '*'*len(cw)
				# Find and replace censor word (case insensitive) with appropriate number of *s when it occurs at the 
				# start of a line.
				repl_lines = re.sub(r'^'+cw+r'(?=\W)', repl_cw, repl_lines, flags=re.IGNORECASE)
				# Replace censor word "" "". Lookahead and lookbehind regexs are required to avoid overlapping matches, 
				# meaning not all occurrences of censor words are removed from a line.
				repl_lines = re.sub(r'(?<=\W)'+cw+r'(?=\W)', repl_cw, repl_lines, flags=re.IGNORECASE)
			print(repl_lines, end='')
			# Go back to the top of the censor words file after the end is reached, so that it can be read again for the next group of text
			# file lines			
			cwf.seek(0) 
		
if __name__ == "__main__":
	# Command line input count test
	if len(sys.argv) != 3:
		print("Incorrect number of command line inputs. USAGE: Requires a censor words file location & a text file location.")
		exit()
	# Get input file locations and create a corresponding output file location
	censor_words_file_location = sys.argv[1]
	text_file_location = sys.argv[2]
	# Main censor functionality
	censor(censor_words_file_location, text_file_location, lines_per_iteration=200, censor_words_one_pass=False)