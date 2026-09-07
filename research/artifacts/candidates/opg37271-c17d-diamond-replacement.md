# C17D: an existentially sound diamond replacement

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; admitted target: `obligation:opg37271-leaf-extension`.
Root: `obligation:opg37271-root`, still open.
Base: `adb8fde9b329be300ce16385385bfcab5e7c048c`.

## 1. Quantifiers and replacement lemma

Let H be any finite simple subcubic graph with a star edge coloring c using C={1,...,6}, and let ab be an edge. Delete ab. Introduce four NEW, pairwise distinct vertices p,q,r,s and edges ap,bq,pr,ps,qr,qs,rs. No other edges incident with these new vertices are introduced. The resulting simple subcubic graph is G.

Claim D. EVERY such coloring c extends on H-ab to a star six-edge-coloring of G. In particular both ap and bq may receive c(ab). All five internal diamond edges are freely chosen; they are not a prescribed old coloring that must be preserved or permuted as a whole.

This is an edge-to-diamond replacement, not the original arbitrary-fixed-coloring leaf-extension statement. Its use in minimal-counterexample reasoning is valid because the reduced graph is smaller and ANY coloring supplied by minimality can be lifted.

## 2. Explicit palette choices

Put alpha=c(ab), A=c_H(a)-{alpha}, B=c_H(b)-{alpha}. Both have size at most two and avoid alpha. Define U=C-({alpha} union A) and V=C-({alpha} union B). Each has at least three elements inside the five-element set C-{alpha}, so U intersection V is nonempty.

Choose, in order:

    h in U intersection V;
    i in U-{h};
    j in V-{h,i};
    k in C-{alpha,h,i,j}.

Each choice exists. The five symbols alpha,h,i,j,k are pairwise distinct. Set

    ap=bq=alpha,
    pr=qs=h, ps=i, qr=j, rs=k.

The inside palettes at p and q are {h,i} and {h,j}, respectively. They are disjoint from A and B. No internal diamond edge has color alpha.

## 3. Complete star check by two-color components

A proper edge coloring of a finite simple graph is star precisely when every nontrivial two-color component is a path with at most three edges. Properness bounds the degree of such a component by two. An even cycle has at least four edges and is forbidden directly or contains a forbidden four-edge path; a path with four or more edges is also forbidden.

The new coloring is proper at every vertex. The internally colored diamond is star: only h occurs twice; its pairs with i,j,k give paths of length at most three. Pairs not containing h have at most two edges. Thus there is no internal four-edge path or four-cycle.

Pairs not containing alpha have no crossing edge between the diamond and the old graph. Their components are valid in the old graph or in the diamond separately.

For a pair {alpha,t}, examine its old component containing ab. This was a path of at most three edges. Deleting ab leaves separate endpoint arms at a and b, each of length at most two. In particular these arms cannot be joined by another old {alpha,t}-path: together with ab that would have been a forbidden two-color cycle. The arm at a is nonempty exactly when t is in A, and similarly at b.

In the diamond, since alpha is absent internally, the {alpha,t} continuation beyond ap contains at most one internal edge. If present, its color t is in {h,i}, hence not in A, so the old arm at a is empty. If the old arm is nonempty, the internal continuation is absent. Therefore the entire component through ap has at most 1+max(2,1)=3 edges. The identical argument applies at bq. The two components cannot connect inside: the internal t-edges form a matching, and pq is not an edge. They cannot connect outside by the preceding old-component argument. Thus no new two-color cycle or longer path is omitted.

This proves Claim D. The component argument also covers identifications among old neighbors; it does not assume an induced old path after replacing a new endpoint by b or a.

## 4. Consequence for a vertex-minimal root counterexample

Suppose G is a minimum-order counterexample to the root. Let p,q,r,s induce a diamond with edges pr,ps,qr,qs,rs, where p,q are its degree-two vertices inside the diamond. By the degree-two triangle reduction C15L-T, p and q must each have an external neighbor, say a and b.

If a and b are distinct and nonadjacent, H=G-{p,q,r,s}+ab is finite, simple, subcubic and has four fewer vertices. Minimality supplies a star six-coloring of H. Claim D lifts it, contradiction. Hence this configuration is reducible. No arbitrary coloring of the larger shore is fixed.

A common external neighbor a=b is also excluded, using the already derived C14B non-pendant-bridge reduction. The five-vertex piece consists of the diamond and a adjacent to p,q. If a has an external edge at, this is its only connection to the rest. When the other shore has at least two vertices it is a non-pendant bridge, already excluded. Otherwise the whole connected graph is the five-vertex piece or that piece plus the leaf t. Both have explicit colorings:

    pr,ps,qr,qs,rs,ap,aq = 1,2,3,1,4,5,6,

and, when present, at=2. Direct two-color checking gives the star property in each case. Thus common external neighbors cause no unproved exceptional family here.

If two triangles share an edge and their other vertices are adjacent, maximum degree three makes the connected component K4. Giving its six edges different colors suffices. Consequently the remaining overlapping-triangle case in a minimum-order counterexample is an induced diamond whose two external neighbors are DISTINCT AND ADJACENT. This last case is explicitly OPEN in this artifact. It is not legitimate to add a second copy of their existing edge and invoke a simple-graph theorem.

## 5. Finite positive boundary certificate

The companion standard-library program checks all six choices of alpha and all ordered A,B subsets of C-{alpha} of size at most two: 6*(1+5+10)^2=1536 cases. It checks properness, complete two-color components of the new seven-edge piece, absence of alpha internally, and the two disjointness conditions. All cases pass. This is a positive superset audit; no unrealizable abstract negative profile is used.

The result stores all 256 normalized alpha=1 recipes as zlib-compressed JSON in base64, with explicit edge order and decompressed SHA-256. Renaming colors covers the other cap choices; all 1536 were additionally checked directly. The script also checks the two small common-neighbor colorings and rejects three mutation fixtures: an alternating four-edge path, an alternating four-cycle, and adjacent equal colors.

Observed local runtime: CPython 3.13.5, standard library, one thread; per invocation wall alarm 15 seconds, CPU soft/hard limits 15/16 seconds, address-space limit 512 MiB. Output is bounded below 1 MiB. These are generator-side checks, not a trusted verifier, repository-script execution, or a change to the channel's command_execution setting. Replay writes its result beside the script; use a disposable copy.

The general proof in Sections 2-3 is the essential external-boundary argument; checking the isolated diamond alone would not prove Claim D. The computational certificate does not replace that argument.

## 6. Dependencies, source comparison and checkpoint

Definitions and axioms: frozen contract; finite-graph-basic and finite-combinatorics. Minimal-counterexample consequences use C15L-T and C14B's bridge reduction. No external theorem or novelty assertion is required. C15/C16 fixed-shore obstructions motivated allowing free internal recoloring; they are not counterexamples to the present edge-replacement rule. A bounded search for star-edge-coloring diamond reductions did not return an exact primary-source match; unrelated vertex-coloring, circular-coloring and gemology hits were not used.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open. State: nonterminal.
Next action: attack the remaining adjacent-external-neighbor diamond by a six-vertex collar replacement. Its far endpoints may coincide or already be adjacent, so those cases must be tracked rather than silently converted to a simple edge.
