-- Create "user_account" table
CREATE TABLE [user_account] (
  [id] int IDENTITY (1, 1) NOT NULL,
  [name] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
  [fullname] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
  CONSTRAINT [PK_user_account] PRIMARY KEY CLUSTERED ([id] ASC)
);
-- Create "address" table
CREATE TABLE [address] (
  [id] int IDENTITY (1, 1) NOT NULL,
  [email_address] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
  [user_id] int NOT NULL,
  CONSTRAINT [PK_address] PRIMARY KEY CLUSTERED ([id] ASC),
 
  CONSTRAINT [FK__address__user_id__22CA2527] FOREIGN KEY ([user_id]) REFERENCES [user_account] ([id]) ON UPDATE NO ACTION ON DELETE NO ACTION
);
