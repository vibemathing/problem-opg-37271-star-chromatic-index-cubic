"""Bounded positive palette audit; no trusted mathematical receipt.
Palette masks are deliberate overapproximations of real graph boundaries.
"""
import itertools
import json
import platform
import resource
import signal
from pathlib import Path


def require(p, text):
    if not p:
        raise ValueError(text)


def first(mask):
    require(mask != 0, 'empty choice')
    return mask & -mask


def arms(k, absent=True):
    C = (1 << k) - 1
    result = [(0, 0)] if absent else []
    for i in range(k):
        p = 1 << i
        result += [(p, A) for A in range(1, C + 1)
                   if A & p and A.bit_count() <= 3]
    return result


def triangle_choice(p, a, A, b, B):
    C = 63
    T = C & ~(A | p | b)
    S = C & ~(B | p | a)
    require(T and S, 'triangle lacks candidate')
    for t in (1 << i for i in range(6) if T >> i & 1):
        if S & ~t:
            return t, first(S & ~t), False
    # The only failure of choosing distinct colors is T=S={r}.
    require(T == S and T.bit_count() == 1, 'bad fallback condition')
    require(a and b and a != b and not (A & (p | b))
            and not (B & (p | a)), 'fallback premises absent')
    return b, first(S), True


def main():
    signal.alarm(15)
    resource.setrlimit(resource.RLIMIT_CPU, (15, 16))
    resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
    six = arms(6)
    triangle_count = fallback_count = 0
    for p in (1 << i for i in range(6)):
        boundary = [(a, A) for a, A in six if a != p]
        for a, A in boundary:
            for b, B in boundary:
                t, s, fallback = triangle_choice(p, a, A, b, B)
                require(not(t & (A | p)) and not(s & (B | p)) and t != s,
                        'triangle properness or outward path failure')
                require((not b or t != b or not B & p)
                        and (not a or s != a or not A & p), 'chord path failure')
                require(not(a and b and s == a and t == b), 'cross path/cycle failure')
                triangle_count += 1
                fallback_count += int(fallback)
    five = arms(5, absent=False)
    chain_count = 0
    for p, A in five:
        for q, B in five:
            t = first(31 & ~(A | q))
            s = first(31 & ~(B | t))
            require(t != s and not(t & A) and not(s & B) and t != q,
                    'three-degree-two path failure')
            chain_count += 1
    claw_count = 0
    for p1, A1 in six:
        for p2, A2 in six:
            for p3, A3 in six:
                t1 = first(63 & ~(A1 | p2 | p3))
                t2 = first(63 & ~(A2 | t1 | p3))
                t3 = first(63 & ~(A3 | t1 | t2))
                require(len({t1, t2, t3}) == 3 and not(t1 & A1)
                        and not(t2 & A2) and not(t3 & A3), 'claw validity failure')
                require(t1 != p2 and t1 != p3 and t2 != p3, 'cross-arm swap')
                claw_count += 1
    # Witness to why arbitrary greedy distinct triangle choices need correction.
    p, a, b = 1, 2, 4
    A, B = 2 | 8 | 16, 4 | 8 | 16
    t, s, fallback = triangle_choice(p, a, A, b, B)
    require(fallback and (t, s) == (4, 32), 'fallback fixture failed')
    result = {
        'verdict': 'candidate_only', 'runtime': platform.python_version(),
        'triangle_boundaries_checked': triangle_count,
        'triangle_fallbacks_checked': fallback_count,
        'five_color_chain_boundaries_checked': chain_count,
        'six_color_low_neighbor_triples_checked': claw_count,
        'six_color_arm_options': len(six),
        'fallback_fixture': {'p': 1, 'a': 2, 'b': 3, 'A': [2,4,5],
                             'B': [3,4,5], 'chosen_xz': 3, 'chosen_xw': 6},
        'limits': {'wall_seconds': 15, 'cpu_seconds': 15, 'memory_mib': 256, 'threads': 1},
        'scope': 'Positive sufficient-choice checks on all abstract palettes; graph path proof is separate.',
        'trusted_receipt': False}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    Path(__file__).with_name('opg37271-c15-palette-result.json').write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
