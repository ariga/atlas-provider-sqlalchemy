-- atlas:pos user_account[type=table] [ABS_PATH]/tests/testdata/multi_path/models1/models.py:9
-- atlas:pos address[type=table] [ABS_PATH]/tests/testdata/multi_path/models1/models.py:18
-- atlas:pos user_account2[type=table] [ABS_PATH]/tests/testdata/multi_path/models2/models.py:9
-- atlas:pos address2[type=table] [ABS_PATH]/tests/testdata/multi_path/models2/models.py:19

CREATE TABLE user_account (id SERIAL NOT NULL, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address (id SERIAL NOT NULL, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account (id));

CREATE TABLE user_account2 (id SERIAL NOT NULL, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address2 (id SERIAL NOT NULL, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account2 (id));

