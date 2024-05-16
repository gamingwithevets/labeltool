import re
import sys
import logging

def load_labels(f, start):
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
					if curr_func is None:
						logging.error('No function label before local label')
						return
					addr = curr_func + int(data[0][3:], 16) - start
					if addr in labels: logging.warning(f'Duplicate local label {curr_func:05X}+{int(data[0][3:], 16):03X}, skipping')
					else: labels[addr] = [data[1], False, curr_func, []]
				elif data[0].startswith('d_'):
					addr = int(data[0][2:], 16)
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
						if '.' in data[0]:
							s = data[0].split('.')
							if s[0] in data_labels.values() and s[1].isnumeric():
								if 0 <= int(s[1]) <= 7:
									if data[0] in data_bit_labels: logging.warning(f'Duplicate bit data label {data[0]}, skipping')
									else: data_bit_labels[data[0]] = data[1]
								else: logging.warning(f'Invalid bit data label {data[0]}, skipping')
							else: logging.warning(f'Invalid label {data[0]}, skipping')
						else: logging.warning(f'Invalid label {data[0]}, skipping')
			except Exception as e:
				logging.error(f'Exception occured: {str(e)} [{type(e).__name__}]')
				return

	return labels, data_labels, data_bit_labels

def save_labels(f, start, labels_, data_labels, data_bit_labels):
	labels = {}
	for k, v in labels_.items():
		addr = k + start
		if not v[1]:
			if v[0].startswith('.l_') and addr == v[2] + int(v[0][3:], 16): continue
			v[2] += start
		labels[addr] = v

	labels = dict(sorted(labels.items()))
	data_labels = dict(sorted(data_labels.items()))
	data_bit_labels = dict(sorted(data_bit_labels.items()))

	content = '# Function + local labels\n'
	content += '\n'.join([f'{format(k, "05X") if v[1] else ".l_"+format(k-v[2], "03X")}\t\t{v[0]}' for k, v in labels.items()]) + '\n\n# Data labels\n'
	content += '\n'.join([f'd_{k:05X}\t\t{v}' for k, v in data_labels.items()]) + '\n\n# Bit data labels\n'
	content += '\n'.join([f'{k}\t\t{v}' for k, v in data_bit_labels.items()]) + '\n'

	f.write(content)

if __name__ == '__main__':
	print('Command line interface coming soon!')
	sys.exit()
