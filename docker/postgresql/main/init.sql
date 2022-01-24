CREATE EXTENSION postgres_fdw;

-- Create SERVER and USER MAPPING for SHARD#1
CREATE SERVER books_shard1
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS( host 'postgresql_shard1', port '5432', dbname 'hsa_l19' );

CREATE USER MAPPING FOR hsa_user
SERVER books_shard1
OPTIONS (user 'hsa_user', password 'aV4h5bRsgc8MB8c3');

-- Create SERVER and USER MAPPING for SHARD#2
CREATE SERVER books_shard2
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS( host 'postgresql_shard2', port '5432', dbname 'hsa_l19' );

CREATE USER MAPPING FOR hsa_user
    SERVER books_shard2
    OPTIONS (user 'hsa_user', password 'aV4h5bRsgc8MB8c3');

-- Create tables

CREATE TABLE books (
    id bigint NOT NULL,
    category_id int NOT NULL,
    author character varying NOT NULL,
    title character varying NOT NULL,
    year int NOT NULL
) PARTITION BY RANGE (year);

CREATE FOREIGN TABLE books_1
    PARTITION OF books
        FOR VALUES FROM (MINVALUE) TO (2010)
    SERVER books_shard1;

CREATE FOREIGN TABLE books_2
    PARTITION OF books
        FOR VALUES FROM (2010) TO (MAXVALUE)
    SERVER books_shard2;
