mismo_lugar(X,Y):-
    X\=Y,
    encuentra(X,Z),
    encuentra(Y,Z).

misma_arma(X,Y):-
    X\=Y,
    armado(X,Z),
    armado(Y,Z).

misma_dificultad(X,Y,Z):-
    dificultad(X,Z),
    dificultad(Y,Z),
    X\=Y.
