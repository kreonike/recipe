
\c skillbox_db

CREATE TABLE coffee (
    id SERIAL NOT NULL,
    title VARCHAR(200) NOT NULL,
    origin VARCHAR(200),
    intensifier VARCHAR(100),
    notes VARCHAR[],
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id SERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50),
    patronomic VARCHAR(50),
    has_sale BOOLEAN,
    address JSON,
    coffee_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(coffee_id) REFERENCES coffee (id)
);

GRANT ALL PRIVILEGES ON DATABASE skillbox_db TO "user";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "user";