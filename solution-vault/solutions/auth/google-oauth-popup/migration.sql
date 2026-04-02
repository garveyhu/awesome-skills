-- 用户表添加 google_id 字段
-- ADAPT: 替换表名和语法（MySQL/PostgreSQL/SQLite）

-- MySQL / PostgreSQL
ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE;
CREATE INDEX ix_users_google_id ON users (google_id);

-- SQLite (需要用 Alembic batch mode)
-- with op.batch_alter_table('users') as batch_op:
--     batch_op.add_column(sa.Column('google_id', sa.String(255), nullable=True))
--     batch_op.create_index('ix_users_google_id', ['google_id'], unique=True)
