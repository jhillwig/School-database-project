-- phpMyAdmin SQL Dump
-- version 5.2.3-1.el10_2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 10, 2026 at 01:28 AM
-- Server version: 10.11.15-MariaDB
-- PHP Version: 8.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jhillwig`
--

DELIMITER $$
--
-- Procedures
--

-- addInstructor
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `addInstructor` (
    IN `p_ID` VARCHAR(5),
    IN `p_name` VARCHAR(20), 
    IN `p_dept_name` VARCHAR(20), 
    IN `p_salary` DECIMAL(8,2)
)   
BEGIN
    INSERT INTO Instructor(i_ID, name, dept_name, salary)
    VALUES (p_ID, p_name, p_dept_name, p_salary);
END$$

-- addSection
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `addSection` (
    IN `p_sec_ID` VARCHAR(8), 
    IN `p_course_ID` VARCHAR(8), 
    IN `p_semester` VARCHAR(6), 
    IN `p_year` DECIMAL(4,0), 
    IN `p_time_slot_ID` VARCHAR(4), 
    IN `p_building` VARCHAR(15), 
    IN `p_room_number` VARCHAR(4)
)   
BEGIN
    INSERT INTO Section(sec_ID, course_ID, semester, year, time_slot_ID, building, room_number) 
    VALUES (p_sec_ID, p_course_ID, p_semester, p_year, p_time_slot_ID, p_building, p_room_number);
END$$

-- addStudent
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `addStudent` (
    IN `p_ID` VARCHAR(5), 
    IN `p_name` VARCHAR(20), 
    IN `p_dept` VARCHAR(20), 
    IN `p_tot_cred` DECIMAL(3,0)
)   
BEGIN
    INSERT INTO Student (s_ID, name, dept_name, tot_cred) 
    VALUES (p_ID, p_name, p_dept, p_tot_cred);
END$$

-- assignGrade
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `assignGrade` (
    IN `p_s_ID` VARCHAR(5), 
    IN `p_sec_ID` VARCHAR(8), 
    IN `p_grade` VARCHAR(2)
)   
BEGIN
    UPDATE Takes SET grade = p_grade WHERE s_ID = p_s_ID AND sec_ID = p_sec_ID;
END$$

-- assignInstructor
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `assignInstructor` (
    IN `p_i_ID` VARCHAR(5), 
    IN `p_course_ID` VARCHAR(8), 
    IN `p_sec_ID` VARCHAR(8), 
    IN `p_semester` VARCHAR(6)
)   
BEGIN
    INSERT INTO Teaches(i_ID, course_ID, sec_ID, semester) 
    VALUES (p_i_ID, p_course_ID, p_sec_ID, p_semester);
END$$

-- countDeptInstructor
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `countDeptInstructor` (
    IN `p_dept` VARCHAR(20), 
    OUT `p_count` INT
)   
BEGIN
    SELECT count(i_ID) INTO p_count
    FROM Instructor WHERE dept_name = p_dept;
END$$

-- countDeptStudent
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `countDeptStudent` (
    IN `p_dept` VARCHAR(20), 
    OUT `p_count` INT
)   
BEGIN
    SELECT COUNT(*) INTO p_count 
    FROM Student 
    WHERE dept_name = p_dept; 
END$$

-- dropInstructor
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `dropInstructor` (
    IN `p_i_ID` VARCHAR(5), 
    IN `p_sec_ID` VARCHAR(8)
)   
BEGIN
    DELETE FROM Teaches WHERE i_ID = p_i_ID AND sec_ID = p_sec_ID;
END$$

-- dropStudent
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `dropStudent` (
    IN `p_s_ID` VARCHAR(5), 
    IN `p_sec_ID` VARCHAR(8)
)   
BEGIN
    DELETE FROM Takes WHERE s_ID = p_s_ID AND sec_ID = p_sec_ID;
END$$

-- enrollStudent
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `enrollStudent` (
    IN `p_s_ID` VARCHAR(5), 
    IN `p_course_ID` VARCHAR(8), 
    IN `p_sec_ID` VARCHAR(8), 
    IN `p_semester` VARCHAR(6)
)   
BEGIN
    INSERT INTO Takes(s_ID, course_ID, sec_ID, semester) 
    VALUES (p_s_ID, p_course_ID, p_sec_ID, p_semester);
END$$


-- ============= Instructor Lookup =============
-- lookInstructorAll
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorAll` ()   
BEGIN
    SELECT * FROM Instructor;
END$$

-- lookInstructorDept
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorDept` (
    IN `p_dept` VARCHAR(20)
)   
BEGIN
    SELECT * FROM Instructor WHERE dept_name = p_dept;

END$$

-- lookInstructorID
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorID` (
    IN `p_ID` VARCHAR(5)
)   
BEGIN
    SELECT * FROM Instructor WHERE i_ID = p_ID;
END$$

-- lookInstructorName
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorName` (
    IN `p_name` VARCHAR(20)
)   
BEGIN
    SELECT * FROM Instructor WHERE name LIKE CONCAT('%',p_name,'%');
END$$

-- lookInstructorSections
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorSections` (
    IN p_i_ID VARCHAR(5)
)
BEGIN
    SELECT * FROM Teaches WHERE i_ID = p_i_ID;
END$$

-- lookAllDepartments
CREATE PROCEDURE `lookAllDepartments`()
BEGIN
    SELECT dept_name FROM Department ORDER BY dept_name;
END$$

-- lookAllDepartmentsFull
CREATE PROCEDURE `lookAllDepartmentsFull`()
BEGIN
    SELECT * FROM Department ORDER BY dept_name;
END$$

-- lookAllCourses
CREATE PROCEDURE `lookAllCourses`()
BEGIN
    SELECT * FROM Course ORDER BY course_ID;
END$$

-- lookAllSectionsAdmin
CREATE PROCEDURE `lookAllSectionsAdmin`()
BEGIN
    SELECT s.*, c.title, c.dept_name
    FROM Section s
    LEFT JOIN Course c ON c.course_ID = s.course_ID
    ORDER BY s.year DESC, s.semester;
END$$


-- lookAllTimeSlots
CREATE PROCEDURE `lookAllTimeSlots`()
BEGIN
    SELECT * FROM Time_Slot ORDER BY time_slot_ID;
END$$

-- lookAllTeaches
CREATE PROCEDURE `lookAllTeaches`()
BEGIN
    SELECT t.*, i.name AS instructor_name, c.title
    FROM Teaches t
    LEFT JOIN Instructor i ON i.i_ID = t.i_ID
    LEFT JOIN Course c ON c.course_ID = t.course_ID
    ORDER BY t.sec_ID;
END$$

-- lookSectionRoster
CREATE PROCEDURE `lookSectionRoster`(IN p_sec_ID VARCHAR(8))
BEGIN
    SELECT st.s_ID, st.name, st.dept_name, tk.grade
    FROM Takes tk
    JOIN Student st ON st.s_ID = tk.s_ID
    WHERE tk.sec_ID = p_sec_ID
    ORDER BY st.name;
END$$

-- lookSectionsBySemester
CREATE PROCEDURE `lookSectionsBySemester`(
    IN p_semester VARCHAR(6),
    IN p_year DECIMAL(4,0)
)
BEGIN
    SELECT s.sec_ID, s.course_ID, s.semester, s.year,
           s.building, s.room_number,
           c.title, c.credits, c.dept_name,
           ts.day, ts.start_hr, ts.end_hr
    FROM Section s
    LEFT JOIN Course c ON c.course_ID = s.course_ID
    LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
    WHERE s.semester = p_semester AND s.year = p_year
    ORDER BY s.course_ID;
END$$

-- lookStudent
CREATE PROCEDURE `lookStudent`(IN p_ID VARCHAR(5))
BEGIN
    SELECT * FROM Student WHERE s_ID = p_ID;
END$$

-- lookStudentClasses
CREATE PROCEDURE `lookStudentClasses`(IN p_s_ID VARCHAR(5))
BEGIN
    SELECT tk.s_ID, tk.sec_ID, tk.course_ID, tk.semester, tk.grade,
           s.year, s.building, s.room_number, c.title, c.credits,
           ts.day, ts.start_hr, ts.end_hr
    FROM Takes tk
    LEFT JOIN Section s ON s.sec_ID = tk.sec_ID
    LEFT JOIN Course c ON c.course_ID = tk.course_ID
    LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
    WHERE tk.s_ID = p_s_ID
    ORDER BY s.year DESC, tk.semester;
END$$

-- lookStudentAdvisor
CREATE PROCEDURE `lookStudentAdvisor`(IN p_s_ID VARCHAR(5))
BEGIN
    SELECT i.i_ID, i.name, i.dept_name
    FROM Advises a
    JOIN Instructor i ON i.i_ID = a.i_ID
    WHERE a.s_ID = p_s_ID
    LIMIT 1;
END$$

-- addAdvisor
CREATE PROCEDURE `addAdvisor`(
    IN p_i_ID VARCHAR(5),
    IN p_s_ID VARCHAR(5)
)
BEGIN
    INSERT IGNORE INTO Advises(i_ID, s_ID) VALUES(p_i_ID, p_s_ID);
END$$

-- removeAdvisor
CREATE PROCEDURE `removeAdvisor`(
    IN p_i_ID VARCHAR(5),
    IN p_s_ID VARCHAR(5)
)
BEGIN
    DELETE FROM Advises WHERE i_ID = p_i_ID AND s_ID = p_s_ID;
END$$

-- updateInstructor
CREATE PROCEDURE `updateInstructor`(
    IN p_ID VARCHAR(5),
    IN p_name VARCHAR(20),
    IN p_dept VARCHAR(20),
    IN p_salary DECIMAL(8,2)
)
BEGIN
    UPDATE Instructor SET name=p_name, dept_name=p_dept, salary=p_salary
    WHERE i_ID = p_ID;
END$$

-- updateStudent
CREATE PROCEDURE `updateStudent`(
    IN p_ID VARCHAR(5),
    IN p_name VARCHAR(20),
    IN p_dept VARCHAR(20),
    IN p_credits DECIMAL(3,0)
)
BEGIN
    UPDATE Student SET name=p_name, dept_name=p_dept, tot_cred=p_credits
    WHERE s_ID = p_ID;
END$$

-- insertCourse
CREATE PROCEDURE `insertCourse`(
    IN p_course_ID VARCHAR(8),
    IN p_title VARCHAR(50),
    IN p_dept VARCHAR(20),
    IN p_credits DECIMAL(2,0)
)
BEGIN
    INSERT INTO Course(course_ID, title, dept_name, credits)
    VALUES(p_course_ID, p_title, p_dept, p_credits);
END$$

-- updateCourse
CREATE PROCEDURE `updateCourse`(
    IN p_course_ID VARCHAR(8),
    IN p_title VARCHAR(50),
    IN p_dept VARCHAR(20),
    IN p_credits DECIMAL(2,0)
)
BEGIN
    UPDATE Course SET title=p_title, dept_name=p_dept, credits=p_credits
    WHERE course_ID = p_course_ID;
END$$

-- removeCourse
CREATE PROCEDURE `removeCourse`(IN p_course_ID VARCHAR(8))
BEGIN
    DELETE FROM Course WHERE course_ID = p_course_ID;
END$$

-- insertTimeSlot
CREATE PROCEDURE `insertTimeSlot`(
    IN p_ts_ID VARCHAR(4),
    IN p_day VARCHAR(1),
    IN p_start DECIMAL(2,0),
    IN p_end DECIMAL(2,0)
)
BEGIN
    INSERT INTO Time_Slot(time_slot_ID, day, start_hr, end_hr)
    VALUES(p_ts_ID, p_day, p_start, p_end);
END$$

-- updateTimeSlot
CREATE PROCEDURE `updateTimeSlot`(
    IN p_ts_ID VARCHAR(4),
    IN p_day VARCHAR(1),
    IN p_start DECIMAL(2,0),
    IN p_end DECIMAL(2,0)
)
BEGIN
    UPDATE Time_Slot SET day=p_day, start_hr=p_start, end_hr=p_end
    WHERE time_slot_ID = p_ts_ID;
END$$

-- removeTimeSlot
CREATE PROCEDURE `removeTimeSlot`(IN p_ts_ID VARCHAR(4))
BEGIN
    DELETE FROM Time_Slot WHERE time_slot_ID = p_ts_ID;
END$$

-- insertDepartment
CREATE PROCEDURE `insertDepartment`(
    IN p_dept VARCHAR(20),
    IN p_building VARCHAR(15),
    IN p_budget DECIMAL(12,2)
)
BEGIN
    INSERT INTO Department(dept_name, building, budget)
    VALUES(p_dept, p_building, p_budget);
END$$

-- updateDepartment
CREATE PROCEDURE `updateDepartment`(
    IN p_dept VARCHAR(20),
    IN p_building VARCHAR(15),
    IN p_budget DECIMAL(12,2)
)
BEGIN
    UPDATE Department SET building=p_building, budget=p_budget
    WHERE dept_name = p_dept;
END$$

-- removeDepartment
CREATE PROCEDURE `removeDepartment`(IN p_dept VARCHAR(20))
BEGIN
    DELETE FROM Department WHERE dept_name = p_dept;
END$$

-- insertPrereq
CREATE PROCEDURE `insertPrereq`(
    IN p_course_ID VARCHAR(8),
    IN p_prereq_ID VARCHAR(8)
)
BEGIN
    INSERT INTO Prereq(course_ID, prereq_id) VALUES(p_course_ID, p_prereq_ID);
END$$

-- removePrereq
CREATE PROCEDURE `removePrereq`(
    IN p_course_ID VARCHAR(8),
    IN p_prereq_ID VARCHAR(8)
)
BEGIN
    DELETE FROM Prereq WHERE course_ID=p_course_ID AND prereq_id=p_prereq_ID;
END$$


-- ============= Course Lookup =============
-- lookSectionCourse
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookSectionCourse` (
    IN `p_course_ID` VARCHAR(8)
)   
BEGIN
    SELECT * FROM Section WHERE course_ID = p_course_ID;
END$$

-- lookSectionSemester
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookSectionSemester` (
    IN `p_semester` VARCHAR(6), 
    IN `p_year` DECIMAL(4,0)
)   
BEGIN
    SELECT s.sec_ID, s.course_ID, s.semester, s.year,
           s.building, s.room_number,
           c.title, c.credits, c.dept_name,
           ts.day, ts.start_hr, ts.end_hr
    FROM Section s
    LEFT JOIN Course c ON c.course_ID = s.course_ID
    LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
    WHERE s.semester = p_semester AND s.year = p_year
    ORDER BY s.course_ID;
END$$

CREATE PROCEDURE `lookAllSections`()
BEGIN
    SELECT s.sec_ID, s.course_ID, s.semester, s.year,
           s.building, s.room_number,
           c.title, c.credits, c.dept_name,
           ts.day, ts.start_hr, ts.end_hr
    FROM Section s
    LEFT JOIN Course c ON c.course_ID = s.course_ID
    LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
    ORDER BY s.year DESC, s.semester;
END$$

CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookInstructorAdvisees` (
    IN p_i_ID VARCHAR(5)
)
BEGIN
    SELECT s.*
    FROM Advises a
    JOIN Student s ON a.s_ID = s.s_ID
    WHERE a.i_ID = p_i_ID;
END$$

-- ============= Student Lookup =============
-- lookStudentAll
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookStudentAll` ()   
BEGIN
    SELECT * FROM Student;
END$$

-- lookStudentDept
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookStudentDept` (
    IN `p_dept` VARCHAR(20)
)   
BEGIN
    SELECT * FROM Student WHERE dept_name = p_dept;
END$$

-- lookStudentID
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookStudentID` (
    IN `p_ID` VARCHAR(5)
)   
BEGIN
    SELECT * FROM Student WHERE s_ID = p_ID;
END$$

-- lookStudentName
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `lookStudentName` (
    IN `p_name` VARCHAR(20)
)
BEGIN
    SELECT * FROM Student WHERE name LIKE CONCAT('%',p_name,'%');
END$$


-- ============= Removal =============
-- removeInstructor
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `removeInstructor` (
    IN `p_ID` VARCHAR(5)
)   
BEGIN
    DELETE FROM Instructor WHERE i_ID = p_ID;
END$$

-- removeSection
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `removeSection` (
    IN `p_sec_ID` VARCHAR(8)
)   
BEGIN
    DELETE FROM Section WHERE sec_ID = p_sec_ID;
END$$

-- removeStudent
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `removeStudent` (
    IN `p_ID` VARCHAR(5)
)   
BEGIN
    DELETE FROM Student WHERE s_ID = p_ID;
END$$

-- ============= Updates =============
-- updateInstructorSalary
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `updateInstructorSalary` (
    IN `p_ID` VARCHAR(5), 
    IN `p_updatedSalary` DECIMAL(8,2)
)   
BEGIN
    UPDATE Instructor 
    SET salary = p_updatedSalary WHERE i_ID = p_ID;
END$$

-- updateSectionRoom
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `updateSectionRoom` (
    IN `p_sec_ID` VARCHAR(8), 
    IN `p_build` VARCHAR(15), 
    IN `p_room` VARCHAR(4)
)   
BEGIN
    UPDATE Section 
    SET building = p_build, room_number = p_room WHERE sec_ID = p_sec_ID;
END$$

-- updateStudentCredits
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `updateStudentCredits` (
    IN `p_ID` VARCHAR(5), 
    IN `p_updatedCredits` DECIMAL(3,0)
)   
BEGIN
    UPDATE Student 
    SET tot_cred = p_updatedCredits WHERE s_ID = p_ID;
END$$

-- Grades
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `deptAvgGrade` (
IN p_deptName VARCHAR(20)
)   
BEGIN
	SELECT 
	dept_name,
	AVG(CASE
		WHEN grade = 'A' THEN 4.0
		WHEN grade = 'A-' THEN 3.7
		WHEN grade = 'B+' THEN 3.3
		WHEN grade = 'B' THEN 3
		WHEN grade = 'B-' THEN 2.7
		WHEN grade = 'C+' THEN 2.3
		WHEN grade = 'C' THEN 2
		WHEN grade = 'C-' THEN 1.7
		WHEN grade = 'D+' THEN 1.3
		WHEN grade = 'D' THEN 1
		WHEN grade = 'D-' THEN 0.7
		WHEN grade = 'F' THEN 0
		ELSE NULL
		END
		) AS avg_gpa
	FROM Student
	JOIN Takes ON Student.s_ID = Takes.s_ID
	WHERE Student.dept_name = p_deptName
	AND Takes.grade IS NOT NULL
	GROUP BY Student.dept_name;
END$$ 


-- Best and worst performing classes for a semester
CREATE PROCEDURE `bestWorstClasses`(
    IN p_semester VARCHAR(6),
    IN p_year DECIMAL(4,0)
)
BEGIN
    SELECT t.course_ID, c.title,
        AVG(CASE
            WHEN grade = 'A'  THEN 4.0 WHEN grade = 'A-' THEN 3.7
            WHEN grade = 'B+' THEN 3.3 WHEN grade = 'B'  THEN 3.0
            WHEN grade = 'B-' THEN 2.7 WHEN grade = 'C+' THEN 2.3
            WHEN grade = 'C'  THEN 2.0 WHEN grade = 'C-' THEN 1.7
            WHEN grade = 'D+' THEN 1.3 WHEN grade = 'D'  THEN 1.0
            WHEN grade = 'D-' THEN 0.7 WHEN grade = 'F'  THEN 0.0
            ELSE NULL END) AS avg_gpa,
        COUNT(t.s_ID) AS enrollment
    FROM Takes t
    JOIN Section s ON s.sec_ID = t.sec_ID
    JOIN Course c ON c.course_ID = t.course_ID
    WHERE s.semester = p_semester AND s.year = p_year
      AND t.grade IS NOT NULL
    GROUP BY t.course_ID, c.title
    ORDER BY avg_gpa DESC;
END$$

-- Currently enrolled students by department (in Takes with no grade yet = active)
CREATE PROCEDURE `enrolledStudentsByDept`(
    IN p_dept VARCHAR(20)
)
BEGIN
    SELECT s.dept_name, COUNT(DISTINCT t.s_ID) AS enrolled_count
    FROM Takes t
    JOIN Student s ON s.s_ID = t.s_ID
    WHERE s.dept_name = p_dept
      AND t.grade IS NULL
    GROUP BY s.dept_name;
END$$

-- ==========================================================
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `courseGradeAvg` (
    IN p_courseID VARCHAR(8),
    IN p_yearBegin DECIMAL(4,0),
    IN P_yearEnd DECIMAL(4,0)
)   
BEGIN
	SELECT 
	t.course_ID,
	AVG(CASE
		WHEN grade = 'A' THEN 4.0
		WHEN grade = 'B' THEN 3.0
		WHEN grade = 'C' THEN 2.0
		WHEN grade = 'D' THEN 1.0
		WHEN grade = 'F' THEN 0.0
		ELSE NULL
		END
		) AS avg_gpa
	FROM Takes t	
	JOIN Section s ON t.sec_ID = s.sec_ID
    WHERE t.course_ID = p_courseID
	    AND s.year BETWEEN p_yearBegin AND p_yearEnd
        AND t.grade IS NOT NULL
    GROUP BY t.course_ID;
END$$

-- ==========================================================
CREATE DEFINER=`jhillwig`@`%` PROCEDURE `getStudentsByDept` (
IN p_deptName VARCHAR(20)
)   
BEGIN
	SELECT 
	dept_name,
	COUNT(s_ID) as student_total
	FROM Student
	WHERE dept_name = p_deptName
	GROUP BY dept_name;
END$$

DELIMITER ; 

-- --------------------------------------------------------

--
-- Table structure for table `Department`
--

CREATE TABLE `Department` (
  `dept_name` varchar(20) NOT NULL,
  `building` varchar(15) DEFAULT NULL,
  `budget` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`dept_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Department`
--

INSERT INTO `Department` (`dept_name`, `building`, `budget`) VALUES
('Architecture', 'Enviro. Design', 240000.00),
('Buisness', 'Crawford Hall', 100000.00),
('Communications', 'Taylor Hall', 100000.00),
('Computer Science', 'MSB', 150000.00),
('Digital Media', 'Lincoln Hall', 120000.00),
('Earth Science', 'Williams Hall', 100000.00),
('Education', 'Ritchie Hall', 150000.00),
('English', 'McGilvrey Hall', 100000.00),
('Fashion', 'Fashion Hall', 250000.00),
('History', 'Merrill Hall', 80000.00),
('Mathematics', 'MSB', 100000.00),
('Music', 'Cartwright Hall', 60000.00);


-- --------------------------------------------------------

--
-- Table structure for table `Time_Slot`
--

CREATE TABLE `Time_Slot` (
  `time_slot_ID` varchar(4) NOT NULL,
  `day` varchar(1) DEFAULT NULL,
  `start_hr` decimal(2,0) DEFAULT NULL,
  `end_hr` decimal(2,0) DEFAULT NULL,
  PRIMARY KEY (`time_slot_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `Course` (
  `course_ID` varchar(8) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `credits` decimal(2,0) DEFAULT NULL,
  PRIMARY KEY (`course_ID`),
  KEY `dept_name` (`dept_name`),
  CONSTRAINT `Course_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `Department` (`dept_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Course`
--

INSERT INTO `Course` (`course_ID`, `title`, `dept_name`, `credits`) VALUES
('12345', 'CS1A', 'Computer Science', 3),
('12346', 'CS1B', 'Computer Science', 3),
('13456', 'CS2', 'Computer Science', 3);


-- --------------------------------------------------------

--
-- Table structure for table `Instructor`
--

CREATE TABLE `Instructor` (
  `i_ID` varchar(5) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `password` varchar(20) Default NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `salary` decimal(8,2) DEFAULT NULL,
  Primary Key(`i_ID`),
  KEY `dept_name` (`dept_name`),
  CONSTRAINT `Instructor_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `Department` (`dept_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Instructor`
--

INSERT INTO `Instructor` (`i_ID`, `name`, `password`, `dept_name`, `salary`) VALUES
('03495', 'Hough', '55723', 'Earth Science', 70000.00),
('12001', 'Giovanni', '14581', 'Computer Science', 30000.00),
('12002', 'Meldin', '57295', 'Computer Science', 100000.00),
('12003', 'Maletic', '57234','Computer Science', 250000.00),
('12004', 'Khan', '98634', 'History', 80000.00),
('12058', 'Harris', '14651', 'Communications', 67000.00),
('18394', 'Butler', '57294', 'Fashion', 180000.00),
('34059', 'Kota', '47145', 'Buisness', 80000.00),
('39485', 'Moriarty', '58201', 'Education', 60000.00),
('65849', 'Mitchell', '58572', 'Mathematics', 100000.00),
('69503', 'Grindem', '52815', 'Communications', 65000.00),
('82953', 'Johnson', '58521', 'Digital Media', 200000.00),
('83948', 'Pringle', '52745', 'English', 65000.00),
('85939', 'Kaiser', '68201', 'History', 87000.00),
('85948', 'Ennis', '57294', 'Communications', 80000.00),
('94839', 'Lynch', '68201', 'Architecture', 110000.00),
('96785', 'Barthes', '68205', 'Fashion', 200000.00),
('98490', 'Phillips', '81752', 'Digital Media', 45000.00);


-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `s_ID` varchar(5) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `password` varchar(20) Default Null,
  `dept_name` varchar(20) DEFAULT NULL,
  `tot_cred` decimal(3,0) NOT NULL,
  Primary Key (`s_ID`),
  Key `dept_name` (`dept_name`),
  CONSTRAINT `Student_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `Department` (`dept_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Student`
--

INSERT INTO `Student` (`s_ID`, `name`, `password`, `dept_name`, `tot_cred`) VALUES
('19304', 'Day', '17319', 'Communications', 12),
('19305', 'Harford', '47104', 'Music', 39),
('19348', 'Seibel', '57193', 'Buisness', 24),
('19404', 'Schuster', '58014', 'Music', 54),
('19843', 'Marchetti', '68025', 'Architecture', 95),
('29304', 'Stanley', '67204', 'Buisness', 90),
('29348', 'Hillwig', '67201', 'Computer Science', 45),
('29383', 'Lutz', '76721', 'Fashion', 20),
('29384', 'Magill', '92856', 'Computer Science', 50),
('29408', 'Evans', '15349', 'Digital Media', 79),
('38921', 'Short', '48715', 'Mathematics', 70),
('39403', 'Unk', '68201', 'Buisness', 36),
('42004', 'Stone', '68201', 'Architecture', 67),
('49302', 'Bishko', '58914', 'Buisness', 80),
('57392', 'Maloberti', '18587', 'English', 12),
('57823', 'Johnson', '58105', 'Earth Science', 30),
('70904', 'Roddy', '68205', 'Computer Science', 76),
('95847', 'Farrell', '18757', 'Computer Science', 1);


-- --------------------------------------------------------
--
-- Table structure for table `Section`
--

CREATE TABLE `Section` (
  `sec_ID` varchar(8) NOT NULL,
  `course_ID` varchar(8) DEFAULT NULL,
  `semester` varchar(6) DEFAULT NULL,
  `year` decimal(4,0) DEFAULT NULL,
  `time_slot_ID` varchar(4) DEFAULT NULL,
  `building` varchar(15) DEFAULT NULL,
  `room_number` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`sec_ID`),
  Key `course_ID` (`course_ID`),
  CONSTRAINT `Section_ibfk_1` FOREIGN KEY (`course_ID`) REFERENCES `Course` (`course_ID`),
  CONSTRAINT `Section_ibfk_2` FOREIGN KEY (`time_slot_ID`) REFERENCES `Time_Slot` (`time_slot_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


-- --------------------------------------------------------
--
-- Table structure for table `Takes`
--

CREATE TABLE `Takes` (
  `s_ID` varchar(5) NOT NULL,
  `course_ID` varchar(8) DEFAULT NULL,
  `sec_ID` varchar(8) DEFAULT NULL,
  `semester` varchar(6) DEFAULT NULL,
  `grade` Varchar(2),
  PRIMARY Key (`s_ID`, `sec_ID`),
  Key `course_ID` (`course_ID`),
  CONSTRAINT `Takes_ibfk_1` FOREIGN KEY (`s_ID`) REFERENCES `Student` (`s_ID`),
  CONSTRAINT `Takes_ibfk_2` FOREIGN KEY (`sec_ID`) REFERENCES `Section` (`sec_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Teaches`
--

CREATE TABLE `Teaches` (
  `i_ID` varchar(5) NOT NULL,
  `course_ID` varchar(8) DEFAULT NULL,
  `sec_ID` varchar(8) DEFAULT NULL,
  `semester` varchar(6) DEFAULT NULL,
  KEY `sec_ID` (`sec_ID`),
  CONSTRAINT `Teaches_ibfk_1` FOREIGN KEY (`i_ID`) REFERENCES `Instructor` (`i_ID`),
  CONSTRAINT `Teaches_ibfk_2` FOREIGN KEY (`sec_ID`) REFERENCES `Section` (`sec_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;



-- -------------------------------------------------------
-- Advises table to lookInstructorAdvisees
CREATE TABLE Advises (
    i_ID VARCHAR(5),
    s_ID VARCHAR(5),
    PRIMARY KEY (`i_ID`, `s_ID`),
    CONSTRAINT `Advises_ibfk_1` FOREIGN KEY (`i_ID`) REFERENCES `Instructor` (`i_ID`),
    CONSTRAINT `Advises_ibfk_2` FOREIGN KEY (`s_ID`) REFERENCES `Student` (`s_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------
CREATE TABLE `Admin` (
    `a_ID` Varchar(5) Not Null,
    `name` Varchar(20) Default Null,
    `password` Varchar(20) Default Null,
    Primary Key (`a_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

INSERT INTO `Admin` (`a_ID`, `name`, `password`) VALUES
('admin1', 'Admin', 'adminLogin'),
('64925', 'Smith', '41345'),
('18475', 'Klien', '69657'),
('86732', 'Happy', '05581'),
('12834', 'Gray', '55323'),
('17591', 'Trey', '12121'),
('84173', 'Huff', '69696');

-- ----------------------------------------------------------------------
CREATE TABLE `Prereq` (
  `course_ID` varchar(8) NOT NULL,
  `prereq_id` varchar(8) NOT NULL,
  PRIMARY KEY (`course_ID`, `prereq_id`),
  CONSTRAINT `Prereq_ibfk_1` FOREIGN KEY (`course_ID`) REFERENCES `Course` (`course_ID`),
  CONSTRAINT `Prereq_ibfk_2` FOREIGN KEY (`prereq_id`) REFERENCES `Course` (`course_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


COMMIT;