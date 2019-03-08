from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

edges = [
	{
		'gene':'rs10857',
		'exposure':'smoking',
		'outcome':'lung_cancer',
		'annotations':[
			{
			'userID':101,
			'annotation':'smoking_is_good_for_you'
			}
		]
	}
]



#POST edges
@app.route('/edges',methods=['POST'])
def create_edge():
	request_data=request.get_json()
	new_edge={
		'gene': request_data['gene'],
		'exposure':request_data['exposure'],
		'outcome':request_data['outcome'],
		'annotations':[]
	}
	edges.append(new_edge)
	return jsonify(new_edge)

#GET edges by gene
@app.route('/edges/<string:gene>')
def get_edge_by_gene(gene):
	for edge in edges:
		if edge['gene'] == gene:
			return jsonify(edge)
	return jsonify({'message':'gene not found'})
	#iterate over edges
	#if the edges name matches, return it
	#if none mathes, return an error

#GET edges
@app.route('/edges')
def get_edges():
	return jsonify({'edges':edges})

#POST annotations
@app.route('/edges/<string:gene>/annotations',methods=['POST'])
def create_annotations_in_edges_by_gene(gene):
	request_data=request.get_json()
	for edge in edges:
		if edge['gene'] == gene:
			new_annotation={
				'annotation':request_data['annotation'],
				'userID':request_data['userID']
			}
			edge['annotations'].append(new.edge)
	return jsonify({'message':'gene not found'})

#GET annotations
@app.route('/edges/<string:gene>/annotations')
def get_annotations_in_edges_by_gene(gene):
	for edge in edges:
		if edge['gene'] == gene:
			return jsonify({'annotations':edge['annotations']})
	return jsonify({'message':'gene not found'})

app.run(port=5000)