read_input(FilePath, X) :-
    see(FilePath), read(X), seen.

retrieve_all_literals_selection(KB, Lit) :-
    member(Clause, KB), 
    member(Lit, Clause).
retreive_negation_literals_selection(AllLiterals, NegLit) :-
    member(Lit, AllLiterals), 
    negate(Lit, NegLit), 
    \+ member(NegLit, AllLiterals).
exclude_pure_clauses_from_kb(KB, NewKB) :- 
    findall(Lit, retrieve_all_literals_selection(KB, Lit), AllLiterals),
    findall(NegLit, retreive_negation_literals_selection(AllLiterals, NegLit), NotFoundLiterals),
    exclude(is_pure_clause(NotFoundLiterals), KB, NewKB).
is_pure_clause(NotFoundLiterals, Clause) :-
    member(Lit, Clause), negate(Lit, NegLit), member(NegLit, NotFoundLiterals).

exclude_tautologies_from_kb(KB, NewKB) :- exclude(is_tautology, KB, NewKB).
is_tautology(Clause) :- member(Lit, Clause), negate(Lit, NegLit), member(NegLit, Clause).

exclude_subsumed_clauses_from_kb(KB, NewKB) :- exclude(is_subsummed(KB), KB, NewKB).
is_subsummed(KB, Clause) :- member(NewClause, KB), NewClause \= Clause, subset(NewClause, Clause).

negate(n(X), X) :- !.
negate(X, n(X)).

solve(FirstClause, SecondClause, Resultant) :-
    member(Lit, FirstClause),
    negate(Lit, NegLit),
    member(NegLit, SecondClause),
    select(Lit, FirstClause, RestOfFirstClause),
    select(NegLit, SecondClause, RestOfSecondClause),
    append(RestOfFirstClause, RestOfSecondClause, IntermediateResultant),
    sort(IntermediateResultant, Resultant),
    write('Resolving: '), write(FirstClause), write(' AND '), write(SecondClause), nl,
    write('Resultant: '), write(Resultant), nl.

resolve_kb(KB, NewKB) :-
    findall(Resultant,
        (member(FirstClause, KB),
         member(SecondClause, KB),
         FirstClause @< SecondClause,
         solve(FirstClause, SecondClause, Resultant),
         \+ member(Resultant, KB)),
    NewClauses),
    append(KB, NewClauses, TempKB),
    sort(TempKB, NewKB),
    write('New Clauses: '), write(NewClauses), nl.

apply_solve_resolution(KB) :-
    (member([], KB) -> write('UNSATISFIABLE'), nl, ! ; 
     resolve_kb(KB, NewKB),
     (KB == NewKB -> write('SATISFIABLE'), nl ; apply_solve_resolution(NewKB))).

resolution_fol(FilePath) :-
    read_input(FilePath, KB),
    write('Initial KB: '), write(KB), nl,
    apply_solve_resolution(KB).

resolution_propositional(FilePath) :-
    read_input(FilePath, KB),
    write('Initial KB: '), write(KB), nl,
    exclude_pure_clauses_from_kb(KB, FilteredPureClausesKB),
    write('Our KB after pure classes removal: '), write(FilteredPureClausesKB), nl,
    exclude_tautologies_from_kb(FilteredPureClausesKB, FilteredTautologiesClausesKB),
    write('Our KB after tautologies removal: '), write(FilteredTautologiesClausesKB), nl,
    exclude_subsumed_clauses_from_kb(FilteredTautologiesClausesKB, NewKB),
    write('Our KB after subsumed clauses removal: '), write(NewKB), nl,
    apply_solve_resolution(KB).

retreive_p_by_value(P, ValueOfP, NewP) :-
    (
        ValueOfP = true -> NewP = P
        ;
        ValueOfP = false -> negate(P, NegP), NewP = NegP
    ).

dot_operation([], _, _, []) :- !.
dot_operation([CurrentClause | RestClauses], P, ValueOfP, NewClauses) :-
    retreive_p_by_value(P, ValueOfP, NewP),
    (member(NewP, CurrentClause) -> 
        dot_operation(RestClauses, P, ValueOfP, NewClauses)
        ;
        negate(NewP, NegP), (member(NegP, CurrentClause) ->
            delete(CurrentClause, NegP, NewCurrentClause),
            (NewCurrentClause == [] -> fail ; true),
            dot_operation(RestClauses, P, ValueOfP, RecursiveNewClauses),

            NewClauses = [NewCurrentClause | RecursiveNewClauses]
            ;
            dot_operation(RestClauses, P, ValueOfP, RecursiveNewClauses),

            NewClauses = [CurrentClause | RecursiveNewClauses]
            )
        ).

choose_most_frequent_atom(KB, P) :-
    findall(Lit, retrieve_all_literals_selection(KB, Lit), AllLiterals),
    construct_frequency_list(AllLiterals, P).
% https://stackoverflow.com/questions/50437617/prolog-function-that-returns-the-most-frequent-element-in-a-list
construct_frequency_list(AllLiterals, P) :-
    sort(AllLiterals, UniqueLiterals),
    findall([Freq, X], (member(X, UniqueLiterals), include(=(X), AllLiterals, XX), length(XX, Freq)), Freqs),
    sort(Freqs, SFreqs),
    last(SFreqs, [Freq, P]).
apply_solve_davis_putnam_most_frequent([], []) :- !.
apply_solve_davis_putnam_most_frequent(KB, _) :- member([], KB), !, fail.
apply_solve_davis_putnam_most_frequent(KB, Solution) :-
    choose_most_frequent_atom(KB, P),
    (
        dot_operation(KB, P, true, NewKBTrue),
        write('Choosen Atom: '), write(P), write(' with value TRUE'), nl,
        write('Clauses after dot operation: '), write(NewKBTrue), nl,
        apply_solve_davis_putnam_most_frequent(NewKBTrue, RecursiveSolutions),

        Solution = [atom(P, true) | RecursiveSolutions]
        ;
        dot_operation(KB, P, false, NewKBFalse),
        write('Choosen Atom: '), write(P), write(' with value FALSE'), nl,
        write('Clauses after dot operation: '), write(NewKBFalse), nl,
        apply_solve_davis_putnam_most_frequent(NewKBFalse, RecursiveSolutions),

        Solution = [atom(P, false) | RecursiveSolutions]
        ).
davis_putnam_most_frequent(FilePath) :-
    read_input(FilePath, KB),
    write('Initial KB: '), write(KB), nl,
    (apply_solve_davis_putnam_most_frequent(KB, Solution) -> 
        write('YES'), nl, write('Solution: '), write(Solution)
        ;
        write('NO')
        ).

choose_shortest_clause_atom(KB, P) :-
    findall([Length, Clause], (member(Clause, KB), length(Clause, Length)), AllClauseLengths),
    sort(AllClauseLengths, SortedAllClauseLengths),
    SortedAllClauseLengths = [[_, ShortestClause] | _],
    member(P, ShortestClause).
apply_solve_davis_putnam_shortest_clause([], []) :- !.
apply_solve_davis_putnam_shortest_clause(KB, _) :- member([], KB), !, fail.
apply_solve_davis_putnam_shortest_clause(KB, Solution) :-
    choose_shortest_clause_atom(KB, P),
    (
        dot_operation(KB, P, true, NewKBTrue),
        write('Choosen Atom: '), write(P), write(' with value TRUE'), nl,
        write('Clauses after dot operation: '), write(NewKBTrue), nl,
        apply_solve_davis_putnam_most_frequent(NewKBTrue, RecursiveSolutions),

        Solution = [atom(P, true) | RecursiveSolutions]
        ;
        dot_operation(KB, P, false, NewKBFalse),
        write('Choosen Atom: '), write(P), write(' with value FALSE'), nl,
        write('Clauses after dot operation: '), write(NewKBFalse), nl,
        apply_solve_davis_putnam_most_frequent(NewKBFalse, RecursiveSolutions),

        Solution = [atom(P, false) | RecursiveSolutions]
        ).

davis_putnam_shortest_clause(FilePath) :-
    read_input(FilePath, KB),
    write('Initial KB: '), write(KB), nl,
    (apply_solve_davis_putnam_shortest_clause(KB, Solution) ->
        write('YES'), nl, write('Solution: '), write(Solution)
        ;
        write('NO')
        ).
