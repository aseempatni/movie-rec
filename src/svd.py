from recsys.algorithm.factorize import SVD
import recsys.algorithm
import csv


# config 
datapath = "../data/ml-1m/"

recsys.algorithm.VERBOSE = True
k = 100
svd = SVD()
movies = {}

svd.load_data(filename=datapath + 'ratings.dat', sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})
svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile='/tmp/movielens')

# Loading already computed SVD model
svd2 = SVD(filename='/tmp/movielens') 

def get_movies():
	# CSV file of Moives will be used here
	# movies will be the dictionary to be returned
	with open(datapath + 'movies.csv', mode='r') as infile:
		reader = csv.reader(infile)
		movies = {int(rows[0]):rows for rows in reader}
	return movies

def query(user_id):
	for i in svd.recommend(user_id,only_unknowns=True,is_row=False):
		if(i[0] in movies.keys()):
			print i
			print movies[i[0]][1]
			#print movies[i['movie_id']][10]
			#print movies[i['movie_id']][11]
		else:
			print 'Hugga!'

prefs = {}
def loadDataset():	
	""" To load the dataSet"
		Parameter: The folder where the data files are stored
		Return: the dictionary with the data
	"""
	#Recover the titles of the books
	movies = {}
	for line in open(datapath + "movies.dat"):
		# line = line.replace('"', "")
		(id, title) = line.split("::") [0:2]
		movies[id] = title
	
	#Load the data
	count = 0
	for line in open(datapath + "ratings.dat"):
		# line = line.replace('"', "")
		# line = line.replace("\\","")
		(user, movieid, rating) = line.split("::")[0:3]
		try:
			if float(rating) > 0.0:
				prefs.setdefault(user,{})
				prefs[user][movies[movieid]] = float(rating)
		except ValueError:
			count += 1
			# print "value error found! " + user + bookid + rating
		except KeyError:
			count +=1
			# print "key error found! " + user + " " + bookid
	return prefs

user_pref = {}
def get_user_movies(user_id):
	for i in  prefs[user_id]:
		print i