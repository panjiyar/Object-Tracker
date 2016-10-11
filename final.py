from pic import reader


a = ""
ims = []
tmp = 7
prev_center = [180, 26]
prev_length = 42
prev_width = 18

for i in range(1, 253):
	a= ""
	a= str(i)
	while len(a) != 8:
		a = '0'+a
	a = a+".jpg"
	ims.append(a)
	a = ""

i = 0

for img in ims:
	i+=1
	if i <= 200:
		[left_end,right_end,top_end,bottom_end] = reader(img, 7, prev_center, prev_length, prev_width)
	else:
		[left_end,right_end,top_end,bottom_end] = reader(img, 5, prev_center, prev_length, prev_width)
	
	prev_center = [(bottom_end + top_end)/2, (right_end + left_end)/2]
	prev_width = bottom_end - top_end
	prev_length = right_end - left_end
	# print prev_center[1]
  