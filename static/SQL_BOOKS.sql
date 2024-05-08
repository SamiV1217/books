-- Drop existing tables to start fresh every time this SQL is run
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Publisher;
--Make the Book table
CREATE TABLE "Book" (
	"book_id"	INTEGER NOT NULL,
	"book_name"	TEXT NOT NULL,
	"author" TEXT NOT NULL,
	"owner"	TEXT NOT NULL,
	"holder"	TEXT NOT NULL,
	PRIMARY KEY("book_id")
);

--Insert books into book table
INSERT INTO Book (book_name, author, owner, holder)
VALUES("Knowing God's Will", "Blaine Smith", "Sami", "Sami");
INSERT INTO Book (book_name, author, owner, holder)
VALUES("Members of One Another", "Dennis McCallum", "Sami", "Sami");
INSERT INTO Book (book_name, author, owner, holder)
VALUES("Loving One Another", "Dennis McCallum", "Sami", "Sami");
INSERT INTO Book (book_name, author, owner, holder)
VALUES("Deeper", "Dane Ortlund", "Sami", "Sami");
