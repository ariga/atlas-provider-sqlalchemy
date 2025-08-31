-- atlas:pos user_account[type=table] /home/noam/src/atlas-provider-sqlalchemy/tests/testdata/multi_path/models1/models.py:9
-- atlas:pos blabla[type=table] /home/noam/src/atlas-provider-sqlalchemy/tests/testdata/multi_path/models1/models.py:19
-- atlas:pos address[type=table] /home/noam/src/atlas-provider-sqlalchemy/tests/testdata/multi_path/models1/models.py:29

CREATE TABLE user_account (id INTEGER NOT NULL AUTO_INCREMENT, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE blabla (id INTEGER NOT NULL AUTO_INCREMENT, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address (id INTEGER NOT NULL AUTO_INCREMENT, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account (id));

-- atlas:pos user_account2[type=table] /home/noam/src/atlas-provider-sqlalchemy/tests/testdata/multi_path/models2/models.py:9
-- atlas:pos address2[type=table] /home/noam/src/atlas-provider-sqlalchemy/tests/testdata/multi_path/models2/models.py:19

CREATE TABLE user_account2 (id INTEGER NOT NULL AUTO_INCREMENT, name VARCHAR(30) NOT NULL, fullname VARCHAR(30), PRIMARY KEY (id));

CREATE TABLE address2 (id INTEGER NOT NULL AUTO_INCREMENT, email_address VARCHAR(30) NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES user_account2 (id));

