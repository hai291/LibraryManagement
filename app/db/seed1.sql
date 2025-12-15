USE library_db;

INSERT INTO Authors (AuthorName) VALUES 
('J.K. Rowling'),
('George Orwell'),
('Nam Cao'),
('Nguyen Nhat Anh'),
('Haruki Murakami'),
('Agatha Christie'),
('Stephen King'),
('To Hoai'),
('Ernest Hemingway'),
('Arthur Conan Doyle');

INSERT INTO Books (BookTitle, AuthorID) VALUES 
('Harry Potter and the Sorcerers Stone', 1),
('Harry Potter and the Chamber of Secrets', 1),
('1984', 2),
('Animal Farm', 2),
('Chi Pheo', 3),
('Doi Thua', 3),
('Mat Biec', 4),
('Kinh Van Hoa', 4),
('Norwegian Wood', 5),
('Kafka on the Shore', 5),
('Murder on the Orient Express', 6),
('It', 7),
('De Men Phieu Luu Ky', 8),
('The Old Man and the Sea', 9),
('Sherlock Holmes: A Study in Scarlet', 10);

INSERT INTO Borrowers (BorrowerName) VALUES 
('Nguyen Van An'),
('Tran Thi Bich'),
('Le Van Cuong'),
('Pham Thi Dung'),
('Hoang Van Em'),
('Vu Thi Phuong'),
('Dang Van Giang'),
('Bui Thi Hang'),
('Ngo Van Hung'),
('Do Thi Kieu'),
('Ly Van Lam'),
('Trinh Thi Mai');

INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(1, 1, '2023-01-10', '2023-01-24', 'Returned'),
(2, 3, '2023-02-05', '2023-02-19', 'Returned'),
(3, 5, '2023-03-12', '2023-03-26', 'Returned'),
(4, 7, '2023-05-20', '2023-06-03', 'Returned'),
(5, 2, '2023-06-15', '2023-06-29', 'Returned'),
(1, 4, '2024-01-10', '2024-01-24', 'Returned'),
(2, 6, '2024-02-14', '2024-02-28', 'Returned'),
(6, 8, '2024-03-01', '2024-03-15', 'Returned'),
(7, 10, '2024-04-10', '2024-04-24', 'Returned'),
(8, 12, '2024-05-05', '2024-05-19', 'Returned'),
(9, 14, '2024-06-20', '2024-07-04', 'Returned'),
(10, 1, '2024-07-01', '2024-07-15', 'Returned'),
(11, 3, '2024-08-10', '2024-08-24', 'Returned'),
(12, 5, '2024-09-05', '2024-09-19', 'Returned'),
(1, 15, '2024-10-01', '2024-10-15', 'Returned');

INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(2, 1, '2024-11-01', '2024-11-15', 'Overdue'),
(3, 2, '2024-12-01', '2024-12-15', 'Overdue'),
(4, 4, '2025-01-10', '2025-01-24', 'Overdue'),
(5, 6, '2025-02-01', '2025-02-15', 'Overdue'),
(6, 9, '2025-03-05', '2025-03-19', 'Overdue'),
(7, 11, '2025-04-01', '2025-04-15', 'Overdue'),
(8, 13, '2025-05-10', '2025-05-24', 'Overdue'),
(1, 7, '2025-06-01', '2025-06-15', 'Borrowed');

INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(9, 15, '2025-12-01', '2025-12-15', 'Borrowed'),
(10, 14, '2025-12-05', '2025-12-19', 'Borrowed'),
(11, 12, '2025-12-10', '2025-12-24', 'Borrowed'),
(12, 10, '2025-12-11', '2025-12-25', 'Borrowed'),
(1, 8, '2025-12-12', '2025-12-26', 'Borrowed'),
(2, 5, '2025-12-12', '2025-12-26', 'Borrowed'),
(3, 3, '2025-12-13', '2025-12-27', 'Borrowed'),
(4, 1, '2025-12-14', '2025-12-28', 'Borrowed'),
(5, 11, '2025-12-14', '2025-12-28', 'Borrowed'),
(6, 13, '2025-12-15', '2025-12-29', 'Borrowed'),
(7, 2, '2025-12-15', '2025-12-29', 'Borrowed'),
(8, 4, '2025-12-15', '2025-12-29', 'Borrowed');