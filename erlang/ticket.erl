-module(ticket).
-export( [makeTicket/1, ticket/1] ).

makeTicket(N) -> spawn(fun() -> ticket(N) end).

ticket(N) ->
  receive
    _ -> 
        io:format("Next ticket is ~p~n", [N]),
        ticket(N+1)
  end.
  
