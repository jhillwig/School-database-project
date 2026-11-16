# Insert new instructor
DELIMITER //

CREATE PROCEDURE insertInstructor (
    IN p_ID VARCHAR(5),
    IN p_name VARCHAR(20),
    IN p_dept_name VARCHAR(20),
    IN p_salary DECIMAL(8,2)
)
BEGIN
    INSERT INTO instructor (ID, name, dept_name, salary)
    VALUES (p_ID, p_name, p_dept_name, p_salary);
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE insertStudent (
    IN p_ID VARCHAR(5),
    IN p_name VARCHAR(20),
    IN p_dept_name VARCHAR(20),
    IN p_tot_cred DECIMAL(3,0)
)
BEGIN
    INSERT INTO student (ID, name, dept_name, tot_cred)
    VALUES (p_ID, p_name, p_dept_name, p_tot_cred);
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE lookAllInstructors ()
BEGIN
    select * from instructor;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookAllStudents ()
BEGIN
    select * from student;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookInstructorsDept (
    IN pDept_name VARCHAR(20)
)
BEGIN
    select *  from instructors
    where instructor.dept_name = pDept_name;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookInstructor (
    IN pID VARCHAR(5)
)
BEGIN
    select * from instructor
    where instructor.ID = pID;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE studentFilterYear (
    IN pID VARCHAR(5),
    IN pYear decimal(4,0)
)
BEGIN
    select * from takes
    where takes.ID = pID AND takes.year = pYear;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookStudent (
    IN pID VARCHAR(5)
)
BEGIN
    select * from student
    where student.ID LIKE CONCAT('%', pID, '%');

    
END //

DELIMITER ;

DELIMITER //


CREATE PROCEDURE lookStudentName (
    IN pName VARCHAR(20)
)
BEGIN
    select * from student
    where student.name LIKE CONCAT('%', pName, '%');
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookInstructorName (
    IN pName VARCHAR(20)
)
BEGIN
    select * from instructor
    where instructor.name LIKE CONCAT('%', pName, '%');
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE removeInstructor (
    IN pID VARCHAR(5)
)
BEGIN
    delete from instructor
    where instructor.ID = pID;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE removeStudent (
    IN pID VARCHAR(5)
)
BEGIN
    delete from student
    where student.ID = pID;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE lookAllDepartments()
BEGIN
    select dept_name 
    from department;
    
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE scheduleStudent(
    IN pID varchar(5)
)
BEGIN   
    select * from takes
    where takes.ID = pID;
END //


CREATE PROCEDURE scheduleYearFilter(
    IN pYear decimal(4,0),
    IN pID varchar(5)

)
BEGIN   
    select * from takes
    where takes.year = pYear AND takes.ID = pID;

END //


CREATE PROCEDURE lookInstructorName (
    IN pName VARCHAR(20)
)
BEGIN
    select * from instructor
    where instructor.name LIKE CONCAT('%', pName, '%');
    
END //


DELIMITER //
CREATE PROCEDURE countDeptFaculty(
    IN pDept_name VARCHAR(20)
)
BEGIN
    select count(instructor.ID)
    from instructor
    where instructor.dept_name = pDept_name;
    
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE countDeptFaculty(
    IN pDept_name VARCHAR(20),
    OUT oCount INT
)
BEGIN
    select count(instructor.ID) into oCount
    from instructor
    where instructor.dept_name = pDept_name;
    
END //

DELIMITER ;

