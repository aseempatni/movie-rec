from graphlab import SFrame
sf = graphlab.SFrame({'user_id': ["0", "0", "0", "1", "1", "2", "2", "2"],
                      'item_id': ["a", "b", "c", "a", "b", "b", "c", "d"],
                      'rating': [1, 3, 2, 5, 4, 1, 4, 3]})
m = graphlab.recommender.create(sf, target='rating')
recs = m.recommend()