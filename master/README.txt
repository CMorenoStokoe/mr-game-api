# API in dev for game to elicit annotations for MR EvE

Databases use sample data which can display edges, annotations and add/delete an annotation
End-points and transactions (use postman file with pre-populated fields and requests):

```/edges```
- GET all
returns all edges in db, along with annotations

```/edges/<int:ref>```
- GET specific
/edges/1 returns ONE edge with that ref, along with annotations (ref = unique identifier for each edge, range=~1-6)

```/annotation```
- GET all
returns all annotations in db, without the edges they belong to

```/annotation/<int:ref>```
- GET annotation
/annotate/1 returns annotations for the edge with that ref, without the edge they belong to
- DEL annotation
deletes an annotation with that ref
- POST annotation  
can be fed data (to update SQLite db for annotations) in JSON form with format:
	{
		'ref':<int, range=~1-6>
		'username':<string>
		'judgement':<int, 1/0>
		'comment':<string>
	}