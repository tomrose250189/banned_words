import sys
import re
import multiprocessing
import sys
 

def replace_words(arg):
	repl_line = arg[0]
	censor_words = arg[1]
	for cw, lcw in censor_words: # for each censor word read from the censor word file
		repl_cw = '*'*lcw
		# find and replace censor word (case insensitive) with appropriate number of *s when it occurs at the 
		# start of a line.
		repl_line = re.sub(r'^'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE)
		# replace censor word "" "". Lookahead and lookbehind regexs are required to avoid overlapping matches, 
		# meaning not all occurrences of censor words are removed from a line.
		repl_line = re.sub(r'(?<=\W)'+cw+r'(?=\W)', repl_cw, repl_line, flags=re.IGNORECASE)
	return repl_line

def censor(censor_words_file_location, text_file_location, mp=True):
	"""This function creates a list of censor words from the censor word file. It then reads each line of the text file, 
	substituting any letters of a censor word found with a '*'. The resultant line is printed out to stdout. This process 
	finishes when the end of the end of the text file is reached."""
	with open(censor_words_file_location, 'r') as cwf:
		cores = multiprocessing.cpu_count() if mp else 1
		censor_words = [[] for _ in range(cores)]
		i = 0
		while True:
			cw = cwf.readline().rstrip() # remove newline and trailing whitespace
			if cw == '':
				break # Keep reading until the end of the censor word file
			censor_words[i].append((cw, len(cw)))
			i = (i + 1) % cores
	with open(text_file_location, 'r') as tf:
		pool = multiprocessing.Pool(cores)
		while True:
			repl_line = tf.readline()
			if repl_line == '':
				break # stop reading at eof
			if mp:
				res = pool.map(replace_words, [[repl_line, censor_words[i]] for i in range(cores)])
				repl_line = ''
				for i in xrange(len(res[0])):
					for j in range(cores):
						if(res[j][i] == '*'):
							repl_line += '*'
							break
					else:	
						repl_line += res[0][i]
			else:
				repl_line = replace_words([repl_line, censor_words[0]])
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
	censor(censor_words_file_location, text_file_location, mp=True)
