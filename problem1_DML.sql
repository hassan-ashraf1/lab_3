USE company;

INSERT INTO DEPARTMENT
(Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES
(1, 'IT', NULL, '2026-01-01'),
(2, 'HR', NULL, '2026-02-01'),
(3, 'Sales', NULL, '2026-03-01');

INSERT INTO EMPLOYEE
(ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES
('111111111', 'Ahmed', 'Ali', '2000-05-10', 'Alexandria', 'M', 8000.00, 1),
('222222222', 'Sara', 'Hassan', '2001-03-15', 'Cairo', 'F', 7500.00, 2),
('333333333', 'Omar', 'Khaled', '1999-07-20', 'Alexandria', 'M', 9000.00, 3);

UPDATE DEPARTMENT
SET mgr_ssn = '111111111'
WHERE Dnumber = 1;

UPDATE DEPARTMENT
SET mgr_ssn = '222222222'
WHERE Dnumber = 2;

UPDATE DEPARTMENT
SET mgr_ssn = '333333333'
WHERE Dnumber = 3;

INSERT INTO PROJECT
(Pnumber, Pname, Plocation, Dno)
VALUES
(101, 'Website', 'Alexandria', 1),
(102, 'Recruitment', 'Cairo', 2),
(103, 'Marketing', 'Alexandria', 3);