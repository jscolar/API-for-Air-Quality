from flask import Flask, jsonify, json, request

with open('records.json') as f:
    all_records = json.load(f)

app = Flask(__name__)

@app.route('/')
def hello():
	return "<h1>Hola de nuevo Juanito</h1>"

@app.route('/records', methods=['GET'])
def get_all_records():
	return jsonify(all_records)

@app.route('/records/all_bands/', methods=['GET'])
def get_bands():
	response = [item['name'] for item in all_records]
	return jsonify(response)

@app.route('/records/albums_by_band/<bandname>/', methods=['GET'])
def get_album_by_band(bandname):
	response={bandname:'Not Found!'}
	for item in all_records:
		if item["name"]==bandname:
			response = [x["title"] for x in item["albums"]]
			break
	return jsonify(response)

@app.route('/records/<bandname>', methods=['GET'])
def get_albums_by_band(bandname):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404
    else:
        response = [album['title'] for album in albums[0]]
        return jsonify(response), 200

@app.route('/records/<bandname>', methods=['DELETE'])
def delete_a_band(bandname):
    matching_records = [band for band in all_records if band['name'] == bandname]
    if len(matching_records)==0:
        return jsonify({'error':'band name not found!'}), 404

    all_records.remove(matching_records[0])
    return jsonify({'success': True})

@app.route('/records/<bandname>/<albumtitle>', methods=['GET'])
def get_songs_by_band_and_album(bandname, albumtitle):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404
    else:
        songs = [album['songs'] for album in albums[0] if album['title'] == albumtitle]
        if len(songs)==0:
            return jsonify({'error':'album title not found!'}), 404
        else:
            return jsonify(songs[0]), 200

@app.route('/records', methods=['POST'])
def create_a_record():
    if not request.json or not 'name' in request.json:
        return jsonify({'error':'the new record needs to have a band name'}), 400
    new_record = {
        'name': request.json['name'],
        'albums': request.json.get('albums', '')
    }
    all_records.append(new_record)
    return jsonify({'message': 'created: /records/{}'.format(new_record['name'])}), 201

@app.route('/records/<bandname>', methods=['POST'])
def create_a_band():
    if not request.json or not 'albums' in request.json:
        return jsonify({'error':'the new band needs to have an album name'}), 400
    new_band = {
        'albums': request.json.get('albums', '')
    }
    all_records.append(new_band)
    return jsonify({'message': 'created: /records/<bandname>/{}'.format(new_band['name'])}), 201

if __name__ == '__main__':
	app.run(debug=True)
