# What is it?

Yet another API wrapper for [rottentomatoes](www.rottentomatoes.com).

# Installation

```python
pip install git+git://github.com/myedibleenso/snappytomato
```

# A walkthrough example

```python
from snappytomato import *
# pass your developer key to the api
snappy = RT("my key here")
# alternatively, use the convenience function for loading key from file:
# snappy = RT(load_from_key("path/to/rt/key"))
#
# search by title
lion_king = snappy.movies.movie_by_title("the lion king")
# lion_king.title
# lion_king.mpaa_rating
# lion_king.year # what year was it released?
# lion_king.cast # json dict from rottentomatoes
# lion_king.alternate_ids # imdb, etc
# lion_king.synopsis # might contain a description
# lion_king.audience_score
# lion_king.critics_score
#
# check reviews
for review in lion_king.reviews:
  print(review)
  # review.critic
  # review.quote # a quote from the review
  # review.freshness # rt.score
  # review.source # the url for the original review, but the value of this might be None :(
  # review.publication
  # review.original_score # non-normalized score
  # review.date
# find similar movies (according to rottentomatoes)
similar_movie = next(lion_king.similar)
# Counter of freshness labels across reviews
lion_king.freshness
# Find movies with the substring "snoop" (case-insensitive) in the title
movies = snappy.movies.search("snoop")
# Other calls (see http://developer.rottentomatoes.com/io-docs for options)
# Find movies ordered by current box office sales
current_box_office_hits = snappy.movies.box_office()
# Find movies currently in theaters
movies_in_theaters = snappy.movies.in_theaters()
# Find upcoming movies
upcoming_movies = snappy.movies.upcoming()
# Finding movies opening (this week?) at the box office
opening = snappy.movies.opening()
```
