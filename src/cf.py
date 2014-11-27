from math import sqrt

# config 
datapath = "../data/ml-1m/"

prefs = {}

def loadDataset(path=""):	
	''' 
		To load the dataSet
		Parameter: The folder where the data files are stored
		Return: the dictionary with the data
	'''
	#Recover the titles of the books
	movies = {}
	for line in open(path+"movies.dat"):
		# line = line.replace('"', "")
		(id, title) = line.split("::") [0:2]
		movies[id] = title
	
	#Load the data
	count = 0
	for line in open(path+"ratings.dat"):
		# line = line.replace('"', "")
		# line = line.replace("\\","")
		(user, movieid, rating) = line.split("::")[0:3]
		user = int(user)
		try:
			if float(rating) > 0.0:
				prefs.setdefault(user,{})
				prefs[user][movieid] = float(rating)
		except ValueError:
			count += 1
			# print "value error found! " + user + bookid + rating
		except KeyError:
			count +=1
			# print "key error found! " + user + " " + bookid
	return prefs

#Returns a distance-base similarity score for person1 and person2
def sim_distance(person1, person2):
	#Get the list of shared_items
	si = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item] = 1
	#if they have no rating in common, return 0
	if len(si) == 0: 
		return 0
	#Add up the squares of all differences
	sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
	return 1 / (1 + sum_of_squares)

#Returns the Pearson correlation coefficient for p1 and p2 
def sim_pearson(p1,p2):
	#Get the list of mutually rated items
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]: 
			si[item] = 1
	#if they are no rating in common, return 0
	if len(si) == 0:
		return 0
	#sum calculations
	n = len(si)
	#sum of all preferences
	sum1 = sum([prefs[p1][it] for it in si])
	sum2 = sum([prefs[p2][it] for it in si])
	#Sum of the squares
	sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
	#Sum of the products
	pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
	#Calculate r (Pearson score)
	num = pSum - (sum1 * sum2/n)
	den = sqrt((sum1Sq - pow(sum1,2)/n) * (sum2Sq - pow(sum2,2)/n))
	if den == 0:
		return 0
	r = num/den
	return r

#Returns the best matches for person from the prefs dictionary
#Number of the results and similiraty function are optional params.
def topMatches(person,n=5,similarity=sim_pearson):
	scores = [(similarity(person,other),other)
				for other in prefs if other != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

#Gets recommendations for a person by using a weighted average
#of every other user's rankings
def getRecommendations(person,n=5,similarity=sim_pearson):
	totals = {}
	simSums = {}
	for other in prefs:
		#don't compare me to myself
		if other == person:
			continue
		sim = similarity(person,other)
		#ignore scores of zero or lower
		if sim <= 0: 
			continue
		for item in prefs[other]:
			#only score books i haven't seen yet
			if item not in prefs[person] or prefs[person][item] == 0:
				#Similarity * score
				totals.setdefault(item,0)
				totals[item] += prefs[other][item] * sim
				#Sum of similarities
				simSums.setdefault(item,0)
				simSums[item] += sim
	#Create the normalized list
	rankings = [(total/simSums[item],item) for item,total in totals.items()]
#	return rankings
	#Return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings[0:int (n)]

#Function to transform Person, item - > Item, person
def transformPrefs():
	results = {}
	for person in prefs:
		for item in prefs[person]:
			results.setdefault(item,{})
			#Flip item and person
			results[item][person] = prefs[person][item]
	return results

import matplotlib.pyplot as plt
import numpy as np

def doplot():
	users = []
	ratings = []
	movies = []
	count = 0
	with open("../data/ml-1m/"+"ratings.dat") as file:
		for line in file:
			if count<100000000:
				(user, movieid, rating) = [int(n) for n in line.split("::")[0:3]]
				users.append(user)
				movies.append (movieid)
				ratings.append(rating)
				count  = count+1
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	x = users
	y = movies
	color = ratings
	rgb = plt.get_cmap('hot')([x2 / 5 for x2 in color])
	ax.scatter(x, y, color = rgb , s = 1,edgecolors='none')
	fig.set_size_inches(18.5,10.5)
	plt.xlabel('Users')
	plt.ylabel('Movies')
	fig.savefig('test2png.png',dpi=300)
	plt.savefig('out.png')    # to save the figure to a file
	plt.show()
	# fig.suptitle('Data Visualised')
	return 0


# Load dataset
data = loadDataset(datapath)
print "Data read."
print "An example:"
print data['394'], "\n"
rec = getRecommendations(598)
doplot()
#print rec


users = []
ratings = []
movies = []
rec = []
for i in range (1,6040):
	rec.append(getRecommendations(i))



# def main():
# 	data = loadDataset("./Webscope_R4/")
# # 	# print data.keys()[0]
# # 	# print data.keys()[1]
# # 	# print sim_distance(data,'5988','5989')
# # 	print getRecommendations(data,'5988')
# if __name__ == '__main__':
# 	main()