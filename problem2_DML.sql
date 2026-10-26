USE library;

INSERT INTO AUTHOR
(author_id, name, country)
VALUES
(1, 'Ahmed Khaled', 'Egypt'),
(2, 'John Smith', 'USA'),
(3, 'Sara Ali', 'Egypt');

INSERT INTO BOOK
(book_id, title, price, author_id)
VALUES
(1, 'Database Basics', 150.00, 1),
(2, 'Learning SQL', 200.00, 1),
(3, 'Python Programming', 250.00, 2),
(4, 'Web Development', 180.00, 2),
(5, 'Computer Networks', 220.00, 3),
(6, 'Data Structures', 190.00, 3);