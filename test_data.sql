-- Sample Employer data
INSERT INTO employer (username, password, email) VALUES
    ('employer1', 'password1', 'employer1@example.com'),
    ('employer2', 'password2', 'employer2@example.com'),
    ('employer3', 'password3', 'employer3@example.com'),
    ('employer4', 'password4', 'employer4@example.com'),
    ('employer5', 'password5', 'employer5@example.com');

-- Sample Candidate data
INSERT INTO candidate (username, password, email) VALUES
    ('candidate1', 'password1', 'candidate1@example.com'),
    ('candidate2', 'password2', 'candidate2@example.com'),
    ('candidate3', 'password3', 'candidate3@example.com'),
    ('candidate4', 'password4', 'candidate4@example.com'),
    ('candidate5', 'password5', 'candidate5@example.com');

-- Sample CV data
INSERT INTO cv (candidate_id, full_name, sector, address, experience, skills, "references", contact_number, gcse_passes, education_level, past_experience) VALUES
    (1, 'John Doe', 'Technology', '123 Main St, City', 5, 'Python, SQL', 'Reference 1', '123-456-7890', 10, 2, 'Previous experience in web development'),
    (2, 'Jane Smith', 'Finance', '456 Elm St, Town', 8, 'Accounting, Financial Analysis', NULL, '987-654-3210', 8, 3, 'Worked in a financial institution for 5 years'),
    (3, 'Michael Johnson', 'Marketing', '789 Oak St, Village', 3, 'Digital Marketing, Social Media Management', 'Reference 2', '555-123-4567', 12, 2, NULL),
    (4, 'Emily Davis', 'Healthcare', '321 Pine St, City', 2, 'Medical Coding, Patient Care', NULL, '444-555-6666', 5, 4, 'Volunteered at a local hospital'),
    (5, 'David Wilson', 'Education', '678 Walnut St, Town', 6, 'Curriculum Development, Classroom Management', 'Reference 3', '111-222-3333', 12, 3, 'Taught in a high school for 3 years');
