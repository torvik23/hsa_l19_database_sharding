CREATE TABLE books (
    id bigint NOT NULL PRIMARY KEY,
    category_id int NOT NULL,
    author character varying NOT NULL,
    title character varying NOT NULL,
    year int NOT NULL
);

CREATE INDEX idx_books_year ON books (year);