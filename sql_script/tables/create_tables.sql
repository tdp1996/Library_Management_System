CREATE DATABASE IF NOT EXISTS LibraryDB;

USE LibraryDB;

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    ISBN VARCHAR(20) UNIQUE,
    Book_Title VARCHAR(100) NOT NULL,
    Book_Author VARCHAR(50),
    Year_Of_Publication INT,
    Publisher VARCHAR(50), 
    Genre VARCHAR(50),
    Amount INT,
    Available INT, 
    Image_URL_S VARCHAR(255),
    Image_URL_M VARCHAR(255),
    Image_URL_L VARCHAR(255)
);

CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    Member_Name VARCHAR(100) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Member_Address VARCHAR(50) NOT NULL,
    JoinDate DATE NOT NULL
);


CREATE TABLE Loans (
    LoanID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    LoanDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    Loan_Status VARCHAR(20) DEFAULT 'On Loan',
    Fine DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);
