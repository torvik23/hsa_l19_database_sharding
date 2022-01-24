CREATE TABLE books_2 (
    id bigint NOT NULL,
    category_id int NOT NULL,
    author character varying NOT NULL,
    title character varying NOT NULL,
    year int NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX idx_books_2_year ON books (year);