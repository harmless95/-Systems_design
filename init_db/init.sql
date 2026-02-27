CREATE TABLE IF NOT EXISTS telegram_data (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255),
    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_telegram_data_username ON telegram_data (username);