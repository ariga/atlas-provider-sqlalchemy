-- atlas:pos user_account[type=table] [ABS_PATH]/tests/testdata/old_models/models.py:11
-- atlas:pos address[type=table] [ABS_PATH]/tests/testdata/old_models/models.py:23

CREATE TABLE user_account (id INTEGER, name FixedString(30), fullname FixedString(30)) ENGINE = MergeTree() ORDER BY id;

CREATE TABLE address (id INTEGER, email_address FixedString(30), user_id INTEGER) ENGINE = MergeTree() ORDER BY id;

