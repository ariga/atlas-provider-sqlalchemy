-- Create "address" table
CREATE TABLE `address` (
  `id` Int32,
  `email_address` FixedString(30),
  `user_id` Int32
) ENGINE = MergeTree
PRIMARY KEY (`id`) ORDER BY (`id`) SETTINGS index_granularity = 8192;
-- Create "user_account" table
CREATE TABLE `user_account` (
  `id` Int32,
  `name` FixedString(30),
  `fullname` FixedString(30)
) ENGINE = MergeTree
PRIMARY KEY (`id`) ORDER BY (`id`) SETTINGS index_granularity = 8192;
