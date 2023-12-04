import re
import sys
import logging

def load_labels(f: open, start: int):
	label_data = []
	labels = f.readlines()
	f.close()
	labeldata = [re.split(r'\s+', label.strip().split('#')[0].strip()) for label in labels]
	label_data.extend(list(filter((['']).__ne__, labeldata)))

	labels = {}
	data_labels = {}
	data_bit_labels = {}

	curr_func = None
	for data in label_data:
		if len(data) > 1:
			try:
				if data[0].startswith('f_'):
					addr = int(data[0][2:], 16) - start
					if addr in labels: logging.warning(f'Duplicate function label {addr:05X}, skipping')
					else:
						labels[addr] = [data[1], True]
						curr_func = addr
				elif data[0].startswith('.l_'):
					addr = curr_func + int(data[0][3:], 16) - start
					if addr in labels: logging.warning(f'Duplicate local label {curr_func:05X}+{int(data[0][3:], 16):03X}, skipping')
					else: labels[addr] = [data[1], False, 0, []]
				elif data[0].startswith('d_'):
					addr = int(data[0][2:], 16) - start
					if addr in data_labels: logging.warning(f'Duplicate data label {addr:05X}, skipping')
					else: data_labels[addr] = data[1]
				else:
					try:
						addr = int(data[0], 16) - start
						if addr in labels: logging.warning(f'Duplicate function label {addr:05X}, skipping')
						else:
							labels[addr] = [data[1], True]
							curr_func = addr
					except ValueError:
						if data[0] in data_bit_labels: logging.warning(f'Duplicate bit data label {data[0]}, skipping')
						else: data_bit_labels[data[0]] = data[1]
			except Exception as e: logging.warning(f'Exception occured: {str(e)} [{type(e).__name__}]')

	return labels, data_labels, data_bit_labels

if __name__ == '__main__':
	print('Command line interface coming soon!')
	sys.exit()
