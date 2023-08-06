import os.path, time, json

def read_file(filename):
	with open(filename, encoding='utf-8') as f:
		return f.read()

def write_file(filename, s):
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(s)

def get_time_str(fmt='%c'):
	return time.strftime(fmt)

def get_yyyymmdd_time_str():
	return get_time_str('%Y-%m-%d %H-%M-%S')

def json_dump(filename, a):
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(a, f, ensure_ascii=False, indent='\t')

def load_json(filename):
	with open(filename, encoding='utf-8') as f:
		return json.load(f)

def pack_dict(self, lst):
	return { i: self.__dict__[i] for i in lst.split() }

def load_helper(self, lst, loadfx):
	for i in lst.split(): self.__dict__[i] = loadfx(i)

def current_path():
	return os.path.basename(os.getcwd())

def next_version(version_file='version.txt'):
	# style: 'x.x.x', without suffixes like 'b1', 'a2'
	version = read_file(version_file).strip().split('.')
	if len(version) != 3:
		raise TypeError(version)
	version = [ int(i) for i in version ]
	version[2] += 1
	new_version_str = '.'.join(map(str, version))
	write_file(version_file, new_version_str)
	return new_version_str