INSERT INTO users_user (id, password, username, first_name, last_name, email, is_staff, is_active, role, national_id, phone, address, email_verified, date_joined, created_at)
VALUES
(1, 'pbkdf2_sha256$870000$adminsalt12$puutiUPeK7iePvLENd6IJCQIYvk8rYUMRQBaqAsO764=', 'admin', 'System', 'Admin', 'admin@example.com', TRUE, TRUE, 'admin', 'A0001', '+355680000001', 'Tirana', TRUE, NOW(), NOW()),
(2, 'pbkdf2_sha256$870000$usersalt12$/4TjkXdytw6szPsgSX68Hil/KT7VsX7pdL2bgv2WWn4=', 'antuela', 'Antuela', 'Demo', 'antuela@example.com', FALSE, TRUE, 'user', 'U0002', '+355680000002', 'Berat', TRUE, NOW(), NOW());

INSERT INTO vehicles_vehicle (id, owner_id, plate_number, vin, make, model, year, color, registration_date, inspection_expiry, insurance_expiry, engine_number, status, market_value, created_at)
VALUES
(1, 2, 'AB123CD', 'VIN00000000000001', 'Volkswagen', 'Golf', 2020, 'Blue', '2023-03-10', '2026-09-01', '2026-08-15', 'ENG-1001', 'active', 11000.00, NOW()),
(2, 2, 'AA222BB', 'VIN00000000000002', 'Mercedes-Benz', 'C220', 2019, 'Black', '2022-05-05', '2026-07-20', '2026-07-18', 'ENG-1002', 'active', 18500.00, NOW());

INSERT INTO obligations_obligation (id, vehicle_id, obligation_type, title, description, due_date, amount, status, external_reference, created_at)
VALUES
(1, 1, 'tax', 'Annual Vehicle Tax', 'Annual road tax for 2026', '2026-05-20', 150.00, 'pending', 'EA-TAX-001', NOW()),
(2, 1, 'inspection', 'Technical Inspection', 'Mandatory technical control', '2026-06-10', 35.00, 'pending', 'DPSH-INSP-001', NOW()),
(3, 2, 'insurance', 'Insurance Renewal', 'TPL renewal due', '2026-05-01', 220.00, 'pending', 'INS-2026-001', NOW());

INSERT INTO payments_payment (id, user_id, obligation_id, transaction_reference, amount, method, provider_reference, status, paid_at, created_at)
VALUES
(1, 2, 1, 'PAY-202604010001', 150.00, 'e_albania', 'EA-MOCK-0001', 'successful', NOW(), NOW()),
(2, 2, 2, 'PAY-202604010002', 35.00, 'card', '', 'initiated', NULL, NOW());

UPDATE obligations_obligation SET status='paid' WHERE id=1;

INSERT INTO transactions_transaction (id, vehicle_id, initiated_by_id, target_user_id, transaction_type, reference_code, amount, notes, status, created_at, approved_at)
VALUES
(1, 1, 2, 1, 'sale', 'TRX-202604010001', 11200.00, 'Vehicle sale request for manual approval', 'pending', NOW(), NULL),
(2, 2, 2, NULL, 'inspection', 'TRX-202604010002', 35.00, 'Inspection booking created by user', 'approved', NOW(), NOW());

INSERT INTO documents_document (id, vehicle_id, uploaded_by_id, document_type, title, file, expires_at, verified, created_at)
VALUES
(1, 1, 2, 'registration', 'Registration Certificate', 'documents/registration_ab123cd.pdf', '2027-03-10', TRUE, NOW()),
(2, 2, 2, 'insurance', 'Insurance Policy', 'documents/insurance_aa222bb.pdf', '2026-07-18', TRUE, NOW());

INSERT INTO notifications_notification (id, user_id, category, title, message, is_read, action_url, created_at)
VALUES
(1, 2, 'payment', 'Payment completed', 'Annual tax payment completed successfully.', FALSE, '/payments', NOW()),
(2, 2, 'obligation', 'Inspection due soon', 'Your vehicle AB123CD needs inspection before 2026-06-10.', FALSE, '/dashboard', NOW()),
(3, 1, 'transaction', 'Sale approval required', 'A sale request is waiting for admin review.', FALSE, '/admin', NOW());
