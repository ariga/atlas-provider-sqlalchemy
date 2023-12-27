CREATE TABLE user_account (id SERIAL NOT NULL, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address (id SERIAL NOT NULL, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account (id));

