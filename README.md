ref. https://gigacover.atlassian.net/browse/GC-1677

Compare PostgresDB:

 - cd to postgres-diff folder
 - type `./postgrediff.sh postgresql://username:password@host:port/db_name1 postgresql://username:password@host:port/db_name2`

Output is if not matching:

    
    TABLES: additional in "db_name1"
        table..

     TABLES: not matching
        table..
        table..

     VIEWS: not matching
        view..
     

Definition Tables to compare:
    `
    COLUMNS
    INDEXES
    CHECK CONSTRAINTS
    FOREIGN-KEY CONSTRAINTS
    REFERENCED BY
    `

Difference files will be stored in `diff`
