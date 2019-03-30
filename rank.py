mat = [
	[1,1,2,3,3],
	[1,2,3,4,5],
	[2,2,2,2,2],
	[3,4,4,5,5],
	[1,2,2,2,2],
	[1,2,2,3,3],
	[1,2,2,2,3],
	[1,2,3,3,3],
	[1,1,1,2,2],
	[1,1,1,1,2],
	[1,1,2,2,2],
	[3,3,3,4,4],
	[1,2,3,3,4],
	[1,2,3,4,4]
]

rank = []
i = 0

while(i < 14):

	j = 0
	rline = []
	r = 1

	while (j < 4):	#col - 1

		if(mat[i][j] != mat[i][j + 1]):
			rline.append(r)
			r = r + 1
			j = j + 1
			if(j == 4):
				rline.append(r)
				continue
			else:
				continue
		
		else:	#repetitions exist
			count = 2
			k = j	

			while( j < 3):
				if( mat[i][j + 1] == mat[i][j + 2]):	#col - 2	
					count = count + 1
					j = j + 1
					continue
				else:
					break
			
			l = 0
			while(l < count):
				rline.append(r/float(count))
				l = l + 1
			r = r + 1
			j = k + count 


		if(len(rline) == 4):
			rline.append(r)

	rank.append(rline)
	i = i + 1

i = 0
while(i < 14):
	print("------#" + str(i + 1) + "---------" + str(rank[i]))
	i = i + 1
