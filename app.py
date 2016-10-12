#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

seats = [
    {
        'id': 1,
        'title': u'A1',
        'seat_type': u'Balcony',
        'done': False
   },
    {
        'id': 2,
        'title': u'K5',
        'seat_type': u'Platinum',
        'done': False
    },
    {
        'id':3,
        'title': u'C3',
        'seat_type': u'Gold',
        'done': False
    }

]

@app.route('/')
def index():
    return "Hello,World"


#GET requests
@app.route('/api/v1.0/seats', methods=['GET'])
def get_seats():
    return jsonify({'seats': [ make_public_seat(seat) for seat in seats] })

@app.route('/api/v1.0/seats/<int:seat_id>', methods=['GET'])
def get_seat(seat_id):
    seat = [seat for seat in seats if seat['id'] == seat_id]
    if len(seat) == 0:
        abort(404)
    return jsonify({'seats': seat[0]})

#POST request
@app.route('/api/v1.0/seats', methods=['POST'])
def create_seat():
    if not request.json or not 'title' in request.json:
        abort(400)
    seat = {
        'id': seats[-1]['id'] + 1,
        'title': request.json['title'],
        'seat_type': request.json.get('seat_type',""),
        'done': False
        }
    seats.append(seat)
    return jsonify({'seat': seat}), 201

#PUT request
@app.route('/api/v1.0/seats/<int:seat_id>', methods=['PUT'])
def update_seat(seat_id):
    seat = [seat for seat in seats if seat['id'] == seat_id]
    if len(seat) == 0:
        abort(404)
    if not request.json:
        abort(400)
#It's to note that since we are using python3, we are using 'str' here, in case of python2, 'str' needs to replace with 'unicode'
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'seat_type' in request.json and type(request.json['seat_type']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    seat[0]['title'] = request.json.get('title', seat[0]['title'])
    seat[0]['seat_type'] = request.json.get('seat_type', seat[0]['seat_type'])
    seat[0]['done'] = request.json.get('done', seat[0]['done'])
    return jsonify({'seat': seat[0]})

#DELETE request
@app.route('/api/v1.0/seats/<int:seat_id>', methods=['DELETE'])
def delete_seat(seat_id):
    seat = [seat for seat in seats if seat['id'] == seat_id]
    if len(seat) == 0:
        abort(404)
    seats.remove(seat[0])
    return jsonify({'result': True})

#For returning json in place of HTML, if encounter 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def make_public_seat(seat):
    new_seat = {}
    for field in seat:
        if field == 'id':
            new_seat['uri'] = url_for('get_seat', seat_id=seat['id'], _external=True)
        else:
            new_seat[field] = seat[field]
    return new_seat

if __name__ == '__main__':
    app.run(debug=True)

