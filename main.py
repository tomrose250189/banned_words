import sys
import re

def censor(censor_words_file_location, text_file_location):
	"""This function creates a list of censor words from the censor word file. It then reads each line of the text file, 
	substituting any letters of a censor word found with a '*'. The resultant line is printed out to stdout. This process 
	finishes when the end of the end of the text file is reached."""
	with open(censor_words_file_location, 'r') as cwf:
		censor_words = []
		while True:
			cw = cwf.readline().rstrip() # remove newline and trailing whitespace
			if cw == '':
				break # Keep reading until the end of the censor word file
			censor_words.append((cw, len(cw)))
	with open(text_file_location, 'r') as tf:
		while True:
			repl_line = tf.readline()
			if repl_line == '':
				break # stop reading at eof
			for cw, lcw in censor_words: # for each censor word read from the censor word file
				repl_cw = '*'*lcw
				# find and replace censor word (case insensitive) with appropriate number of *s when it occurs at the 
				# start of a line.
				repl_line = re.sub(r'^'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE)
				# replace censor word "" "". Lookahead and lookbehind regexs are required to avoid overlapping matches, 
				# meaning not all occurrences of censor words are removed from a line.
				repl_line = re.sub(r'(?<=\W)'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE) 
			print(repl_line)
		
if __name__ == "__main__":
	# Command line input count test
	if len(sys.argv) != 3:
		print("Incorrect number of command line inputs. USAGE: Requires a censor words file location & a text file location.")
		exit()
	# Get input file locations and create a corresponding output file location
	censor_words_file_location = sys.argv[1]
	text_file_location = sys.argv[2]
	# Main censor functionality
	censor(censor_words_file_location, text_file_location)
