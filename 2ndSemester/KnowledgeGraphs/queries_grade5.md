## 1. SELECT (at least 2 relations: ex:playsFor + ex:hasAgent)

PREFIX ex: <http://example.org/sportskg#>

SELECT ?playerName ?clubName ?agentName WHERE {
    ?player a ex:Player ;
            ex:name ?playerName ;
            ex:playsFor ?club ;
            ex:hasAgent ?agent .
    ?club  ex:name ?clubName .
    ?agent ex:name ?agentName .
}
ORDER BY ?clubName ?playerName

## 2. ASK

PREFIX ex: <http://example.org/sportskg#>

ASK {
    ?player a ex:Player ;
            ex:birthDate ?birthDate ;
            ex:hasContract ?contract .

    BIND(
        IRI(
            REPLACE(
                STR(?contract),
                "http://example.org/",
                "http://example.org/sportskg#"
            )
        ) AS ?fixedContract
    )

    ?fixedContract ex:salaryEUR ?salaryEUR .

    FILTER(?salaryEUR > 10000)
}

## 3. DESCRIBE

PREFIX data: <http://example.org/sportskg/data#>

DESCRIBE data:P007
## 4. CONSTRUCT

PREFIX ex: <http://example.org/sportskg#>

CONSTRUCT {
    ?process ex:transferInvolvesPlayer ?player .
    ?process ex:transferInvolvesAgent ?agent .
    ?process ex:transferFromClub ?fromClub .
    ?process ex:transferToClub ?toClub .
}
WHERE {
    ?process a ex:TransferProcess ;
             ex:involvesPlayer ?player ;
             ex:fromClub ?fromClub ;
             ex:toClub ?toClub .
    ?player ex:hasAgent ?agent .
}