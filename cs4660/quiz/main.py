"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
from queue import *
# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def bfs(start, finish):
    nodes = []
    moves = []
    N = ((None, None))
    q = Queue()
    q.put((start, None))

    while (q.qsize() > 0):
        i = q.get()
        for room in get_state(i[0]['id'])['neighbors']:
            if room not in nodes:
                if room['id'] == finish['id']:
                    print("reached")
                    N = i

                q.put((room, i))
                nodes.append(room)

    while (N[1] is not None):
        moves.append(transition_state(N[1][0]['id'], (N[0])['id']))
        N = N[1]

    moves.reverse()
    moves.append(transition_state(moves[len(moves) - 1]['id'], finish['id']))

    return moves

if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dest_room = get_state('f1f131f647621a4be7c71292e79613f9')
    # print(empty_room,"check")
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    bfs_result = bfs(empty_room, dest_room)
    for move in bfs_result:
        print(move)

