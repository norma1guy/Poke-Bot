

R = {
    "NONE": 0,
    "ROUTE_101": 1,
    "ROUTE_102": 2,
    "ROUTE_103": 3,
    "ROUTE_104": 4,
    "ROUTE_105": 5,
    "ROUTE_106": 6,
    "ROUTE_107": 7,
    "ROUTE_108": 8,
    "ROUTE_109": 9,
    "ROUTE_110": 10,
    "ROUTE_111": 11,
    "ROUTE_112": 12,
    "ROUTE_113": 13,
    "ROUTE_114": 14,
    "ROUTE_115": 15,
    "ROUTE_116": 16,
    "ROUTE_117": 17,
    "ROUTE_118": 18,
    "ROUTE_119": 19,
    "ROUTE_120": 20,
    "ROUTE_121": 21,
    "ROUTE_122": 22,
    "ROUTE_123": 23,
    "ROUTE_124": 24,
    "ROUTE_125": 25,
    "ROUTE_126": 26,
    "ROUTE_127": 27,
    "ROUTE_128": 28,
    "ROUTE_129": 29,
    "ROUTE_130": 30,
    "ROUTE_131": 31,
    "ROUTE_132": 32,
    "ROUTE_133": 33,
    "ROUTE_134": 34,

    "LITTLEROOT_TOWN": 40,
    "OLDALE_TOWN": 41,
    "PETALBURG_CITY": 42,
    "RUSTBORO_CITY": 43,
    "DEWFORD_TOWN": 44,
    "SLATEPORT_CITY": 45,
    "MAUVILLE_CITY": 46,
    "VERDANTURF_TOWN": 47,
    "LAVARIDGE_TOWN": 48,
    "FALLARBOR_TOWN": 49,
    "FORTREE_CITY": 50,
    "LILYCOVE_CITY": 51,
    "MOSSDEEP_CITY": 52,
    "SOOTOPOLIS_CITY": 53,
    "EVER_GRANDE_CITY": 54,
    "PACIFIDLOG_TOWN": 55,

    "MT_CHIMNEY": 60,
    "SAFARI_ZONE": 61,
    "BATTLE_FRONTIER": 62,
    "SOUTHERN_ISLAND": 63,
}


region_layout = [
    [R["NONE"], R["ROUTE_114"], R["ROUTE_114"], R["FALLARBOR_TOWN"], R["ROUTE_113"], R["ROUTE_113"], R["ROUTE_113"], R["ROUTE_113"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["FORTREE_CITY"], R["ROUTE_120"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["NONE"], R["ROUTE_114"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["MT_CHIMNEY"], R["MT_CHIMNEY"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["NONE"], R["ROUTE_120"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["ROUTE_115"], R["ROUTE_114"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["MT_CHIMNEY"], R["MT_CHIMNEY"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["NONE"], R["ROUTE_120"], R["NONE"], R["NONE"], R["SAFARI_ZONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["ROUTE_115"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["LAVARIDGE_TOWN"], R["ROUTE_112"], R["ROUTE_112"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["NONE"], R["ROUTE_120"], R["ROUTE_121"], R["ROUTE_121"], R["ROUTE_121"], R["ROUTE_121"], R["LILYCOVE_CITY"], R["LILYCOVE_CITY"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_125"], R["ROUTE_125"], R["NONE"], R["NONE"]],
    [R["ROUTE_115"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_122"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_125"], R["ROUTE_125"], R["NONE"], R["NONE"]],
    [R["RUSTBORO_CITY"], R["ROUTE_116"], R["ROUTE_116"], R["ROUTE_116"], R["ROUTE_116"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_111"], R["NONE"], R["NONE"], R["ROUTE_119"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_122"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["ROUTE_124"], R["MOSSDEEP_CITY"], R["MOSSDEEP_CITY"], R["NONE"], R["NONE"]],
    [R["RUSTBORO_CITY"], R["NONE"], R["NONE"], R["NONE"], R["VERDANTURF_TOWN"], R["ROUTE_117"], R["ROUTE_117"], R["ROUTE_117"], R["MAUVILLE_CITY"], R["MAUVILLE_CITY"], R["ROUTE_118"], R["ROUTE_118"], R["ROUTE_123"], R["ROUTE_123"], R["ROUTE_123"], R["ROUTE_123"], R["ROUTE_123"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_126"], R["ROUTE_126"], R["ROUTE_126"], R["ROUTE_127"], R["ROUTE_127"], R["ROUTE_127"], R["NONE"], R["NONE"]],
    [R["ROUTE_104"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_110"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_126"], R["SOOTOPOLIS_CITY"], R["ROUTE_126"], R["ROUTE_127"], R["ROUTE_127"], R["ROUTE_127"], R["NONE"], R["NONE"]],
    [R["ROUTE_104"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_103"], R["ROUTE_103"], R["ROUTE_103"], R["ROUTE_103"], R["ROUTE_110"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_126"], R["ROUTE_126"], R["ROUTE_126"], R["ROUTE_127"], R["ROUTE_127"], R["ROUTE_127"], R["NONE"], R["EVER_GRANDE_CITY"]],
    [R["ROUTE_104"], R["PETALBURG_CITY"], R["ROUTE_102"], R["ROUTE_102"], R["OLDALE_TOWN"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_110"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_128"], R["ROUTE_128"], R["ROUTE_128"], R["ROUTE_128"], R["EVER_GRANDE_CITY"]],
    [R["ROUTE_105"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_101"], R["NONE"], R["NONE"], R["NONE"], R["SLATEPORT_CITY"], R["ROUTE_134"], R["ROUTE_134"], R["ROUTE_134"], R["ROUTE_133"], R["ROUTE_133"], R["ROUTE_133"], R["ROUTE_132"], R["ROUTE_132"], R["PACIFIDLOG_TOWN"], R["ROUTE_131"], R["ROUTE_131"], R["ROUTE_131"], R["ROUTE_130"], R["ROUTE_130"], R["ROUTE_130"], R["ROUTE_129"], R["ROUTE_129"], R["NONE"], R["NONE"]],
    [R["ROUTE_105"], R["NONE"], R["NONE"], R["NONE"], R["LITTLEROOT_TOWN"], R["NONE"], R["NONE"], R["NONE"], R["SLATEPORT_CITY"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["ROUTE_105"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_109"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["BATTLE_FRONTIER"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["ROUTE_106"], R["ROUTE_106"], R["ROUTE_106"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["ROUTE_109"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
    [R["NONE"], R["NONE"], R["DEWFORD_TOWN"], R["ROUTE_107"], R["ROUTE_107"], R["ROUTE_107"], R["ROUTE_108"], R["ROUTE_108"], R["ROUTE_109"], R["NONE"], R["NONE"], R["NONE"], R["SOUTHERN_ISLAND"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"], R["NONE"]],
]

from collections import defaultdict

def build_graph(layout):
    h, w = len(layout), len(layout[0])
    graph = defaultdict(set)

    for y in range(h):
        for x in range(w):
            a = layout[y][x]
            if a == 0:
                continue

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h:
                    b = layout[ny][nx]
                    if b != 0 and b != a:
                        graph[a].add(b)

    return graph

map = build_graph(region_layout)