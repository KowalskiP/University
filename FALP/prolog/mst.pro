mst(Graph, Result) :- find_mst(Graph, [], Result).

find_mst(Distances, Exist, Result) :- 
    ( pick_minimum_edge(Distances, Exist, Edge) -> 
      find_mst(Distances, [Edge | Exist], Res), Result = [Edge | Res];
       Result = [] ).

pick_minimum_edge(Distances, Exist, Edge) :- pick_wo_cycle(Distances, Exist, [], Edge), \+ (Edge = []).

pick_wo_cycle([], _, ToCompare, ToCompare).
pick_wo_cycle([Edge|L], Exist, ToCompare, Result) :-  (
    ( less_edge(Edge, ToCompare), no_cycle(Edge, Exist) ) -> 
        pick_wo_cycle(L, Exist, Edge, Result)      ;
        pick_wo_cycle(L, Exist, ToCompare, Result) ).

less_edge(edge(_X1, _Y1, Z1), edge(_X2, _Y2, Z2)) :- Z1 < Z2.
less_edge(edge(_X1, _Y1, _Z1), []).

no_cycle(edge(X, Y, _), Exist) :- \+ (search(X, Y, Exist, [])).

search(X, Y, Edges,_):- member(edge(X,Y,_), Edges).
search(X, Y, Edges,_):- member(edge(Y,X,_), Edges).
search(X, Y, Edges, PassedVertices):- member(edge(X,Z, _),Edges), 
        \+ (member(Z, PassedVertices)), search(Z,Y,Edges,[Z|PassedVertices]).
search(X, Y, Edges, PassedVertices):- member(edge(Z,X, _),Edges), 
        \+ (member(Z, PassedVertices)), search(Z,Y,Edges,[Z|PassedVertices]).

get_graph(List):-	open('test4.txt', read, In), read_edges(In, List), close(In).

read_edges(In,[]):-at_end_of_stream(In).
read_edges(In,[X|L]):- \+ at_end_of_stream(In), read(In, X), assertz(X), read_edges(In,L).

get_cost([],0) :- !.
get_cost([Head|List],NewCost) :- get_cost(List,Cost), member( edge(X,Y,C), [Head] ),NewCost is Cost + C.

adj(A,B) :- edge(A,B,_);edge(B,A,_).
not_connected(Graph) :- adj(A,_),adj(B,_),A\=B, \+ ( search(A,B,Graph,[]) ).
is_connected(Graph) :- \+ ( not_connected(Graph) ).

:-initialization(main).
main:- get_graph(List) -> (is_connected(List) ->
     (mst(List,Res), write(Res), nl, get_cost(Res,Cost) ,write(Cost));
     write('No')).