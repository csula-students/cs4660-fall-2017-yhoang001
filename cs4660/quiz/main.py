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
    c = 0
    while (q.qsize() > 0):
        i = q.get()
        for room in get_state(i[0]['id'])['neighbors']:
            if room not in nodes:
                c += 1
                if room['id'] == finish['id']:
                    if q.empty():
                        return False
                    print("\nBFS founded after", c)
                    N = i
                q.put_nowait((room, i))
                nodes.append(room)
    while (N[1] is not None):
        moves.append(transition_state(N[1][0]['id'], (N[0])['id']))
        N = N[1]
    moves.reverse()
    t_state = transition_state(moves[len(moves) - 1]['id'], finish['id'])
    moves.append(t_state)
    return moves

def dijkstra(start, finish):
    distance = {}
    parent = {}
    edges = {}
    # print(distance_of[start['id']])
    distance[start['id']] = 0
    q = PriorityQueue()
    q.put((0, start['id']))
    visited = []
    c = 0
    while (q.qsize() > 0):
        u = get_state(q.get()[1])
        U = u['id']
        visited.append(u['id'])
        for i in u['neighbors']:
            I = i['id']
            edge = transition_state(U, I)
            weight = distance[U] + edge['event']['effect']
            if i['id'] not in visited and (I not in distance or weight > distance[I]):
                c += 1
                q.put((-weight, I))
                distance[I] = weight
                parent[I] = U
                edges[I] = edge
    moves = []
    print("\nDijksta founded after", c)
    while finish['id'] in parent:
        moves.append(edges[finish['id']])
        finish['id'] = parent[finish['id']]
    moves.reverse()
    return moves

if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dest_room = get_state('f1f131f647621a4be7c71292e79613f9')
    # print(empty_room,"check")
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    bfs_action = bfs(empty_room, dest_room)
    hp_bfs = 0
    last_bfs = 0
    print(empty_room['location']['name'], empty_room['id'])
    for i in  bfs_action:
        hp_bfs += i['event']['effect']
        # print(move)
        # move = get_state(bfs_action[i]['id'])
        # last = empty_room
        # next = bfs_action[i]['id']
        print(i['action'], i['id'])
        # print(i['action'],i['id'])
        # last = next
    print('\nHP: ', hp_bfs)

    dij = dijkstra(empty_room, dest_room)
    hp_dij = 0
    for i in dij:
        hp_dij += i['event']['effect']
        print(i['action'], i['id'])
    print('\nHP: ', hp_dij)
    print('\n')
    # dijkstra_result = dijkstra(empty_room, dest_room)
    # d_hp = 0
    # for u in dijkstra_result:
    #     d_hp += u['event']['effect']
    #     print(u)
    # print('HP: ', d_hp)
    # actions = dijkstra(empty_room, dest_room)
    # actions = dijkstra('7f3dc077574c013d98b2de8f735058b4', 'f1f131f647621a4be7c71292e79613f9')
    # for u in actions:
    #     print(u)
    # print("\nDijkstra Path:")
    # print_actions(actions, '7f3dc077574c013d98b2de8f735058b4')
    # print(actions)

