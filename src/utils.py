import csv
import os

constants = {
	'max_lat':52.3,
	'min_lat':45.3,
	'max_lon':40.25,
	'min_lon':22.25,
	'data_address':'../data/FIRMS/modis-c6.1/'	
}

'''
FIRMS key
0 'latitude'
1 'longitude'
2 'brightness'
3 'scan'
4 'track'
5 'acq_date'
6 'acq_time'
7 'satellite'
8 'confidence'
9 'version'
10 'bright_t31'
11 'frp'
12 'daynight'
'''
def geo_fence(row):
	row_lon = float(row[0])
	row_lat = float(row[1])
	if constants['min_lon'] > row_lon:
		return False
	if row_lon > constants['max_lon']:
		return False
	if constants['min_lat'] > row_lat:
		return False
	if row_lat > constants['max_lat']:
		return False

	return True



def clean_data(region='Europe'):
	raw_data_files = get_data_files(region)
	for day in raw_data_files:
		result = process_day(day)
		print(result[0])
		print(result[1])
		print(
			result[0][0]/result[1][0],
			result[0][1]/result[1][1])
		print()


def process_day(day_address):
	with open(day_address, newline='') as csv_file:
		firm_data = csv.reader( csv_file )
		outties = 0
		innies = 0
		total_pow_out = 0
		total_pow_in = 0
		for row in firm_data:
			if row[0] == 'latitude':
				continue
			if float(row[8]) < 80:
				continue
			in_fence = geo_fence(row)
			if in_fence:
				innies+=1
				total_pow_in+= float(row[11])
			else:
				outties+=1
				total_pow_out+= float(row[11])

	return [
		[innies,total_pow_in/innies],
		[outties,total_pow_out/outties]
		]

def get_data_files(region='Europe'):
	prefix = os.path.join(constants['data_address'], region)
	files = os.listdir(prefix)
	return list(map(lambda x: os.path.join(prefix, x), files))

# boppo