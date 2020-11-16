CREATE TABLE user_profile (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    pwd VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);

CREATE TABLE note (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    creation_date TIMESTAMP NOT NULL,
    edit_date TIMESTAMP NOT NULL,
    id_user INT NOT NULL,
    is_public BOOLEAN NOT NULL,
    uuid VARCHAR(255) NOT NULL,
    CONSTRAINT fk_note_user FOREIGN KEY(id_user) REFERENCES user_profile(id)
);

INSERT INTO TABLE user_profile (email, pwd, first_name, last_name) VALUES ('test@gmail.com', '1234', 'test', 'test');

