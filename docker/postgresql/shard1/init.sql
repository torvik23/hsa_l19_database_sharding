CREATE TABLE books_1 (
    id bigint NOT NULL,
    category_id int NOT NULL,
    author character varying NOT NULL,
    title character varying NOT NULL,
    year int NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX idx_books_1_year ON books (year);