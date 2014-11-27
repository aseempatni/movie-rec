import graphlab as gl
url = '../data/training_data.csv'
data = gl.SFrame.read_csv(url, column_type_hints={"rating":int})
data.show()
model = gl.recommender.create(data, user_id="user", item_id="movie", target="rating")
results = model.recommend(users=None, k=5)


'''
def get_movies():
	# CSV file of Moives will be used here
	movies = {}
	# movies will be the dictionary to be returned
	with open('movie_db_yoda.csv', mode='r') as infile:
		reader = csv.reader(infile)
		movies = {int(rows[0]):rows[1] for rows in reader}
		return movies

sf = gl.SFrame.read_csv(url='ydata-ymovies-user-movie-ratings-train-v1_0.csv',header=True,column_type_hints=[int,long,int,int]) #,nrows=200
m = gl.ranking_factorization_recommender.create(sf,user_id='user_id', item_id='movie_id',target='rated') #Mostly for column number 3 which is reating from 1 to 5
recs = m.recommend()
print recs

movies = get_movies()
print len(movies)
#print movies.keys()
#print movies
for i in recs:
	if i['user_id']==1:
#print i
#print i['movie_id'] in movies.keys()
if(i['movie_id'] in movies.keys()):
	print movies[i['movie_id']]
else:
	print 'Hugga!'


#def query_user(user):
'''