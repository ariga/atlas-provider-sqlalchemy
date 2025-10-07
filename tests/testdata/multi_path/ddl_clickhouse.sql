-- atlas:pos user_account[type=table] [ABS_PATH]/tests/testdata/multi_path/models1/models.py:10
-- atlas:pos address[type=table] [ABS_PATH]/tests/testdata/multi_path/models1/models.py:21
-- atlas:pos user_account2[type=table] [ABS_PATH]/tests/testdata/multi_path/models2/models.py:10
-- atlas:pos address2[type=table] [ABS_PATH]/tests/testdata/multi_path/models2/models.py:22

CREATE TABLE user_account (id INTEGER, name FixedString(30), fullname FixedString(30)) ENGINE = MergeTree() ORDER BY id;

CREATE TABLE address (id INTEGER, email_address FixedString(30), user_id INTEGER) ENGINE = MergeTree() ORDER BY id;

CREATE TABLE user_account2 (id INTEGER, name FixedString(30), fullname FixedString(30)) ENGINE = MergeTree() ORDER BY id;

CREATE TABLE address2 (id INTEGER, email_address FixedString(30), user_id INTEGER) ENGINE = MergeTree() ORDER BY id;

