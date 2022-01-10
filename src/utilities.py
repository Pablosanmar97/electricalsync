import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as scp


#-------------------------------------FILTERS--------------------------------------#



def highpass_filter(data, cutoff_freq, sampling_rate, order = 5 , type = 'high'):	
	#Get filter coefficients to check frequency response
	nyq = 0.5 * sampling_rate
	normal_cutoff = cutoff_freq / nyq 
	b, a = butter(order, normal_cutoff, btype = type, analog = False)

	#Apply the filter
	return filtfilt(b ,a ,data)



def lowpass_filter(data, cutoff_freq, sampling_rate, order = 5 , type = 'low'):
	#Get filter coefficients to check frequency response
	nyq = 0.5 * sampling_rate
	normal_cutoff = cutoff_freq / nyq 
	b, a = butter(order, normal_cutoff, btype = type, analog = False)

	#Apply the filter
	return filtfilt(b ,a ,data)



def threshold_filter(data, threshold, remove = 'above'):
	if remove == 'above':
		for i in range(len(data)):
			if data[i] < threshold:
				data[i] = threshold
		return
	if remove == 'over':
		for i in range(len(data)):
			if data[i] > threshold:
				data[i] = threshold
		return



def downsample(data):
	print("2")
	


#-------------------------------------ANALYSIS--------------------------------------#



def relocate_spikes(discard, spike_gap, data_1_beg, data_1_end, data_1_max, data_1_mid, data_2_beg, data_2_end, data_2_max, data_2_mid):

	data_1 = data_1_beg
	data_2 = data_2_beg
	# TAKE THE LONGEST DATASET TO ITERATE AS MANY TIMES AS THE LENGTH OF IT
	if (len(data_1) > len(data_2)):
		max_dataset = data_1
		min_dataset = data_2
	elif (len(data_2) > len(data_1)):
		max_dataset = data_2
		min_dataset = data_1
	elif (len(data_2) == len(data_1)):
		max_dataset = data_2
		min_dataset = data_1
		return;

	# for i in range (len(max_dataset)-1):
	# 	diff = data_1[i] - data_2[i]
	# 	cc = []	
	# 	cc.append(diff)
	# mean = abs(sum(cc) / len(cc) * 2)

	# ITERATE FOR THE LENGTH OF THE LONGEST DATASET AND IF THE
	# DIFFERENCE BETWEEN SPIKES IS BIGGER THAN THE GAP INSERT 0
	# IN THE NEURON WHOSE SPIKE IS BEFORE (MISSING)

	length = len(min_dataset)
	i = 0
	while i < length:
		if(data_1[i] == None):
			data_1.insert(i, 0)
		elif(data_2[i] == None):
			data_2.insert(i, 0)
		else:
			diff = data_1[i] - data_2[i]
			# print(data_1[i], data_2[i], diff)
			if(abs(diff) > spike_gap):
				if(np.sign(diff) < 0):
					data_2.insert(i, 0)
					data_2_end.insert(i, 0)
					data_2_max.insert(i, 0)
					data_2_mid.insert(i, 0)
					if(discard):
						data_1.pop(i)
						data_1_end.pop(i)
						data_1_max.pop(i)
						data_1_mid.pop(i)
						data_2.pop(i)
						data_2_end.pop(i)
						data_2_max.pop(i)
						data_2_mid.pop(i)
				elif(np.sign(diff) > 0):
					data_1.insert(i, 0)
					data_1_end.insert(i, 0)
					data_1_max.insert(i, 0)
					data_1_mid.insert(i, 0)
					if(discard):
						data_1.pop(i)
						data_1_end.pop(i)
						data_1_max.pop(i)
						data_1_mid.pop(i)
						data_2.pop(i)
						data_2_end.pop(i)
						data_2_max.pop(i)
						data_2_mid.pop(i)
		i += 1
		length = len(min_dataset)

	return data_1_beg, data_1_end, data_1_max, data_1_mid, data_2_beg, data_2_end, data_2_max, data_2_mid



def get_spikes_max(recording_data, begs, ends):
	spike_max = []
	for i in range(len(begs)):
		spike_range = recording_data[begs[i]:ends[i]]
		maximum = max(spike_range)
		max_index = spike_range.tolist().index(maximum)
		spike_max.append(begs[i] + max_index)
	return spike_max



def get_spikes_middle(begs, ends):
	spike_middle = []
	for i in range(len(begs)):
		middle = int((begs[i]+ends[i])/2)
		spike_middle.append(middle)
	return spike_middle



def skip_iterations_loop(data, intraspike_milisecs, threshold):
	i = 0
	return_array = []
	while i < len(data):
		if data[i] >= threshold:
			maximum = get_spikes_max(data, i, int(i+(intraspike_milisecs*10)))
			return_array.append(i)
			i+= int(intraspike_milisecs*10)
		else:
			i+=1
	return return_array



def detect_single(data_neuron, data_time, thresh_high, thresh_low):
	low_sw = 0
	high_sw = 0
	spike_beg = []
	spike_end = []
	for i in range(len(data_neuron)):
		if data_neuron[i] > float(thresh_high):
			if(high_sw == 0):
				high_sw = 1
				spike_beg.append(i)

		if data_neuron[i] < float(thresh_high):
			if(high_sw == 1):
				high_sw = 0
				spike_end.append(i)
	return spike_beg, spike_end



# WITH LOW THRESHOLD AND LOW SWITCHER
def detect_single_low(data_neuron, data_time, thresh_high, thresh_low):
	spike_timing = []
	for i in range(len(data_neuron)):
		if data_neuron[i] > float(thresh_high):
			if(high_sw == 0):
				if(low_sw == 0):
					high_sw = 1
					low_sw = 1				
					spike_timing.append(data_time[i])

		if data_neuron[i] < float(thresh_high):
			if(high_sw == 1):
				high_sw = 0
				spike_timing.append(data_time[i])
			elif(high_sw == 0):
				if data_neuron[i] < float(thresh_low):
					low_sw = 0



def detect_burst_number(spikes1, spikes2):
	burst_number_array = []
	increment = 1
	for i in range(len(spikes1)):
		if i < len(spikes1) - 1:
			if abs(spikes1[i] - spikes1[i+1]) < 1000:
				burst_number_array.append(increment)
			else:	
				if abs(spikes2[i] - spikes2[i+1]) > 1000:
					burst_number_array.append(increment)
					increment += 1
				else:
					burst_number_array.append(increment)

		else:
			burst_number_array.append(increment)
	return burst_number_array



def detect_spike_number(bursts):
	spike_number_array = []
	current_burst = 1
	prev_spike = 1
	for i in range(len(bursts)):
		# print(bursts[i])
		# print(current_burst)
		# print(prev_spike)
		if bursts[i] == current_burst:
			spike_number_array.append(prev_spike)
			prev_spike += 1
			
		else:
			current_burst += 1
			prev_spike = 1
			spike_number_array.append(prev_spike)
			prev_spike += 1
	return spike_number_array




#--------------------------------------PLOTS----------------------------------------#



def raster_plot(spike_number, spikes_detect):
	to_subtract = 0
	raster_list = []
	sub_array=[]
	for i in range(len(spike_number)):
		if spike_number[i] == 1:
			if sub_array:
				raster_list.append(sub_array)
			sub_array = []
			to_subtract = spikes_detect[i]
			sub_array.append(spikes_detect[i] - to_subtract)
		else:
			sub_array.append(spikes_detect[i] - to_subtract)

	return raster_list
