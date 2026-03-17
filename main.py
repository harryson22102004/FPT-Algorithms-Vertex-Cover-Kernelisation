def crown_reduction(G, V):
    """Crown reduction rule for vertex cover kernelisation."""
    independent=set(V)
    for v in V:
        for u in G.get(v,[]):
            independent.discard(u)
    return independent
 
def kernelise_vertex_cover(G, k):
    """LP-based kernelisation: kernel size ≤ 2k."""
    V=set(G.keys())
 vc=set(); remaining_k=k
    while remaining_k>0:
        # High-degree rule: if deg(v) > k, must include v
        done=False
        for v in list(V):
            if len([u for u in G.get(v,[]) if u in V]) > remaining_k:
                vc.add(v); V.discard(v); remaining_k-=1; done=True; break
        if not done: break
    return vc, V, remaining_k
 
def bounded_search_tree(G, V, k):
    """FPT: 2^k * n algorithm for vertex cover."""
    # Find uncovered edge
    for v in V:
        for u in G.get(v,[]):
            if u in V:
                if k==0: return None
                # Branch: include v or u
                G1={x:[y for y in G.get(x,[]) if y!=v] for x in V-{v}}
                r1=bounded_search_tree(G1,V-{v},k-1)
                if r1 is not None: return r1|{v}
                G2={x:[y for y in G.get(x,[]) if y!=u] for x in V-{u}}
                r2=bounded_search_tree(G2,V-{u},k-1)
                if r2 is not None: return r2|{u}
                return None
    return set()
 
G={0:[1,2,3],1:[0,4],2:[0,4],3:[0],4:[1,2]}
V=set(G.keys())
vc,_,_=kernelise_vertex_cover(G,3)
bst=bounded_search_tree(G,V,3)
print(f"Kernelised VC seed: {vc}")
print(f"BST Vertex Cover (k=3): {bst}")
