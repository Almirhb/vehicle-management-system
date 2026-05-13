CREATE TABLE users_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    national_id VARCHAR(20) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL DEFAULT '',
    address VARCHAR(255) NOT NULL DEFAULT '',
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE vehicles_vehicle (
    id BIGSERIAL PRIMARY KEY, owner_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    plate_number VARCHAR(20) NOT NULL UNIQUE, vin VARCHAR(50) NOT NULL UNIQUE, make VARCHAR(80) NOT NULL, model VARCHAR(80) NOT NULL,
    year INTEGER NOT NULL, color VARCHAR(50) NOT NULL DEFAULT '', registration_date DATE NOT NULL, inspection_expiry DATE NULL, insurance_expiry DATE NULL,
    engine_number VARCHAR(50) NOT NULL DEFAULT '', status VARCHAR(30) NOT NULL DEFAULT 'active', market_value NUMERIC(12,2) NOT NULL DEFAULT 0, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_vehicle_owner_status ON vehicles_vehicle(owner_id, status);
CREATE INDEX idx_vehicle_inspection_expiry ON vehicles_vehicle(inspection_expiry);
CREATE INDEX idx_vehicle_insurance_expiry ON vehicles_vehicle(insurance_expiry);
CREATE TABLE obligations_obligation (
    id BIGSERIAL PRIMARY KEY, vehicle_id BIGINT NOT NULL REFERENCES vehicles_vehicle(id) ON DELETE CASCADE, obligation_type VARCHAR(30) NOT NULL,
    title VARCHAR(120) NOT NULL, description TEXT NOT NULL DEFAULT '', due_date DATE NOT NULL, amount NUMERIC(10,2) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'pending',
    external_reference VARCHAR(100) NOT NULL DEFAULT '', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_obligation_vehicle_status ON obligations_obligation(vehicle_id, status);
CREATE INDEX idx_obligation_due_status ON obligations_obligation(due_date, status);
CREATE TABLE payments_payment (
    id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE, obligation_id BIGINT NOT NULL REFERENCES obligations_obligation(id) ON DELETE CASCADE,
    transaction_reference VARCHAR(80) NOT NULL UNIQUE, amount NUMERIC(10,2) NOT NULL, method VARCHAR(30) NOT NULL DEFAULT 'card', provider_reference VARCHAR(120) NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'initiated', paid_at TIMESTAMPTZ NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_payment_user_status ON payments_payment(user_id, status);
CREATE INDEX idx_payment_created_at ON payments_payment(created_at);
CREATE TABLE transactions_transaction (
    id BIGSERIAL PRIMARY KEY, vehicle_id BIGINT NOT NULL REFERENCES vehicles_vehicle(id) ON DELETE CASCADE, initiated_by_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    target_user_id BIGINT NULL REFERENCES users_user(id) ON DELETE SET NULL, transaction_type VARCHAR(30) NOT NULL, reference_code VARCHAR(80) NOT NULL UNIQUE,
    amount NUMERIC(10,2) NOT NULL DEFAULT 0, notes TEXT NOT NULL DEFAULT '', status VARCHAR(20) NOT NULL DEFAULT 'pending', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), approved_at TIMESTAMPTZ NULL
);
CREATE INDEX idx_transaction_vehicle_status ON transactions_transaction(vehicle_id, status);
CREATE INDEX idx_transaction_type_status ON transactions_transaction(transaction_type, status);
CREATE TABLE documents_document (
    id BIGSERIAL PRIMARY KEY, vehicle_id BIGINT NOT NULL REFERENCES vehicles_vehicle(id) ON DELETE CASCADE, uploaded_by_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    document_type VARCHAR(30) NOT NULL, title VARCHAR(120) NOT NULL, file VARCHAR(255) NOT NULL, expires_at DATE NULL, verified BOOLEAN NOT NULL DEFAULT FALSE, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_document_vehicle_type ON documents_document(vehicle_id, document_type);
CREATE INDEX idx_document_expires_at ON documents_document(expires_at);
CREATE TABLE notifications_notification (
    id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE, category VARCHAR(30) NOT NULL DEFAULT 'system',
    title VARCHAR(120) NOT NULL, message TEXT NOT NULL, is_read BOOLEAN NOT NULL DEFAULT FALSE, action_url VARCHAR(255) NOT NULL DEFAULT '', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_notification_user_read ON notifications_notification(user_id, is_read);
CREATE INDEX idx_notification_created_at ON notifications_notification(created_at);
