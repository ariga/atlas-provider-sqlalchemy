-- atlas:pos user_account[type=table] [ABS_PATH]/tests/tables/tables.py:5
-- atlas:pos address[type=table] [ABS_PATH]/tests/tables/tables.py:13

CREATE TABLE user_account (id INTEGER NOT NULL AUTO_INCREMENT, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address (id INTEGER NOT NULL AUTO_INCREMENT, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account (id));

