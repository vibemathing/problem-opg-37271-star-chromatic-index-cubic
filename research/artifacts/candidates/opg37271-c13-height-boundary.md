# C13H: sharp height boundary for one-old-edge repair on trees

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Target: `obligation:opg37271-leaf-extension`; root remains open.
Base revision: `b1af2ef058f5bca3e81fa2b19fe822f72a107763`.

## 1. Exact scope

Height means maximum distance from u, not diameter or distance from the deleted leaf. Let G be a finite simple subcubic TREE, let v be a leaf with neighbor u, and fix a star edge coloring of H=G-v in {1,...,6}. A repair counts changed OLD edges; assigning uv has cost zero. The final coloring, rather than each intermediate edit, defines the task.

Claim H3: if every vertex of H has distance at most three from u, a repair changes at most one old edge.
Claim H4: there is a height-four example on 28 vertices in G with exact repair cost two. This is a sharp height threshold for universal one-edit repair, not an order-minimality theorem or a root obstruction.

## 2. Height-three proof candidate

If the old coloring extends without edits, there is nothing to prove. Otherwise C01's exact forbidden-set equality forces, after relabeling, ux=1, uy=2, xa=3, xb=4, yc=5, yd=6, and an edge of color 1 continuing from each of a,b and color 2 from each of c,d. All these vertices are distinct. In a tree the support az of color 1 has its far endpoint z at distance three from u. Therefore z is a leaf under the height hypothesis. Vertex a has at most one other child w, also a leaf; call its color q when present. Properness gives q different from 1 and 3.

Delete az temporarily. The colors forbidding a pendant edge at a are contained in {3,q,4}, omitting q if w is absent. To verify this without a heuristic count, every simple three-edge path from a begins through x, since w is a leaf. Its only possibilities are a-x-u-y, whose first and third colors are 3 and 2, or a-x-b-t with t a child of b. The former is not an alternating witness; the latter forbids only its middle color 4, and only when bt has color 3. This exhausts the paths.

Choose delta in {2,5,6} excluding q, and recolor az to delta. At least two choices remain. The exact pendant criterion makes this a star coloring of H. Vertex a now has no incident color 1, while the two roots and the four differently colored spokes are unchanged. Hence color 3 is no longer forbidden at uv. Assign uv=3. Exactly one old edge was changed in the nonextendible case. No assumption about a specially chosen initial coloring was made.

## 3. Complete height-four witness

Start with ux=1, uy=2, xa=3, xb=4, yc=5, yd=6. For each i in {a,b,c,d}, add four private vertices zi,li,ri,wi and edges i-zi=A, zi-li=L, zi-ri=R, i-wi=B as follows:

| i | A | B | L | R |
|---|---:|---:|---:|---:|
| a | 1 | 2 | 5 | 6 |
| b | 1 | 3 | 3 | 5 |
| c | 2 | 1 | 3 | 4 |
| d | 2 | 5 | 5 | 3 |

Add wb-tb=2, wb-sb=6, wd-td=1, wd-sd=4, with four new leaves. Add v and the uncolored uv. All names are distinct, and there are no other edges. Thus H has 27 vertices and 26 edges, G has 28 vertices and 27 edges, maximum degree is three, and height from u is four. This replaces C11's length-two tails by forks and changes two support-leaf colors; it is not merely deletion from C11.

The old coloring is proper. The maximum component sizes in the fifteen two-color subgraphs are:

| pairs | maximum edges |
|---|---:|
| 1,2; 1,5; 1,6; 2,3; 2,4; 3,5; 3,6; 4,5 | 2 |
| 1,3; 1,4; 2,5; 2,6; 3,4; 5,6 | 3 |
| 4,6 | 1 |

Every such component is a path because the graph is a tree and the coloring is proper. The edge table permits direct checking of all entries. A separate path-enumeration check is supplied below.

## 4. All one-edit repairs excluded

Let D consist of ux,uy, all four spokes, and the four supports i-zi. Colors 1,2 on uv fail properness. Each spoke color P is blocked by v-u-parent-i-zi, colored P,A,P,A. These six original obstructions involve only D and uv.

Every edge of D is individually frozen in H. The symmetry swaps x/y, a/c, b/d, corresponding private vertices, and colors 1/2, 3/5, 4/6, so the following left-side cases suffice:

- ux: alternatives 2,3,4 are improper; 5,6 create x-u-y-c-zc or x-u-y-d-zd.
- xa: 1,2,4 are improper; 5,6 create u-x-a-za-la or u-x-a-za-ra.
- xb: 1,3 are improper; 5 creates u-x-b-zb-rb; 2,6 create a-x-b-wb-tb or a-x-b-wb-sb.
- a-za: 2,3,5,6 are improper; 4 creates za-a-x-b-wb.
- b-zb: 3,4,5 are improper; 2,6 create lb-zb-b-wb-tb or lb-zb-b-wb-sb.

In each listed four-edge path the colors alternate after the proposed edit. The symmetry supplies the other five edges and all fifty alternatives. A single edit inside D cannot even preserve H's star property. A single edit outside D preserves all six original obstructions. Thus no simultaneous assignment of uv and at most one old-edge edit works.

## 5. Two edits suffice

Change b-wb from 3 to 5. The other endpoint palettes are {4,1} and {2,6}, which are disjoint, so a new alternating path cannot use the changed edge internally. Endpoint paths into wb terminate after one more edge; those through b-x cannot continue with 5; those through b-zb with next color 1 reach a leaf after the next 5-edge. Hence this edit is star-preserving.

Change a-za from 1 to 4. Its other endpoint palettes {3,2} and {5,6} are disjoint. Endpoint paths through za or wa terminate at leaves. The only possible alternating continuation through x is za-a-x-b with colors 4,3,4, but b now has no color 3. Hence this edit is also star-preserving. Finally assign uv=3 by C01's exact forbidden-set criterion. The old-edge repair cost is exactly two.

## 6. Frozen finite certificate and observed check

`opg37271-c13-height-certificate.json` gives the old edge list, fifty frozen-edge witnesses, six original leaf obstructions, and the full final coloring. Edge indices refer to that list; uv is appended as edge 26. Its SHA-256 is `6d0f528f957107f25767678bbd5020074fa2e387e58d4bf4897a7f78494b9cc0`.

`opg37271-c13-height-check.py` reconstructs the tree, checks its domain/height, enumerates every incident pair and every simple four-edge path, checks all fifty witnesses, tests all 786 zero-or-one-edit assignments, and checks the explicit two-edit coloring. It also rejects a mutation assigning uv=1 in the repaired coloring. Cycles are absent by the connected n-1-edge tree check; it is not a general-graph checker.

Observed local run: CPython 3.13.5, standard library only, one thread, ten-second wall alarm and CPU soft limit, 256 MiB address-space cap. All reported checks passed. Output is saved in `opg37271-c13-height-result.json`. This is generator-side computation, not an admitted adapter run, kernel execution, or trusted mathematical receipt. Repository command-execution capabilities and control files were not changed. The script writes its certificate and result beside itself; replay in a disposable copy when preserving immutable artifacts.

## 7. Scope and checkpoint

C12R already supplies a different Q2 obstruction candidate; no Q2 search is repeated here. H3/H4 identify a genuine boundary for a one-edit invariant, not a claim that all deeper trees have cost at least two. Sources are the frozen definitions, C01's forbidden-set derivation, and C11's witness as an explicitly changed construction. No novelty assertion or uninspected external theorem is needed.

Best verified result: none. Best verified candidate: none.
Both admitted obligations remain open. Next action: derive bridge gluing and cubic completion for the existential root, then audit reducible degree-two and separator configurations without fixing a deleted graph's coloring.
