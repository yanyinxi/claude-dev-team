-- =====================================================
-- Autonomous Evolution System Database Schema
-- 自主进化系统数据库架构
-- =====================================================

-- =====================================================
-- Tasks Table - 任务队列
-- =====================================================
-- 存储所有自动生成的任务
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,  -- time_based, event_based, metric_based, llm_driven
    description TEXT NOT NULL,
    priority INTEGER NOT NULL,  -- 1-10, 10 is highest
    status TEXT NOT NULL,  -- pending, running, completed, failed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSON,  -- Additional task-specific data

    -- Indexes for common queries
    CHECK (priority >= 1 AND priority <= 10),
    CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_scheduled_at ON tasks(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(type);

-- =====================================================
-- Execution History Table - 执行历史
-- =====================================================
-- 记录所有任务的执行结果
CREATE TABLE IF NOT EXISTS execution_history (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    status TEXT NOT NULL,  -- success, failure, timeout, cancelled
    result JSON,  -- Execution result data
    error TEXT,  -- Error message if failed
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_seconds REAL,  -- Execution duration

    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    CHECK (status IN ('success', 'failure', 'timeout', 'cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_execution_history_task_id ON execution_history(task_id);
CREATE INDEX IF NOT EXISTS idx_execution_history_status ON execution_history(status);
CREATE INDEX IF NOT EXISTS idx_execution_history_started_at ON execution_history(started_at DESC);

-- =====================================================
-- Metrics Table - 系统指标
-- =====================================================
-- 存储系统运行指标，用于触发 metric-based 任务
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,  -- error_rate, response_time_ms, test_coverage, etc.
    metric_value REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,  -- Additional metric context

    CHECK (metric_value >= 0)
);

CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON metrics(metric_name, timestamp DESC);

-- =====================================================
-- Audit Log Table - 审计日志
-- =====================================================
-- 记录所有系统操作，用于安全审计和回溯
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,  -- task_created, task_executed, approval_required, rollback_triggered, etc.
    description TEXT NOT NULL,
    user TEXT,  -- User who triggered the event (if applicable)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,  -- Additional event context

    CHECK (event_type IN (
        'task_created', 'task_executed', 'task_failed', 'task_cancelled',
        'approval_required', 'approval_granted', 'approval_denied',
        'rollback_triggered', 'rollback_completed',
        'rate_limit_exceeded', 'conflict_detected',
        'system_started', 'system_stopped'
    ))
);

CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user);

-- =====================================================
-- Views for Common Queries
-- 常用查询视图
-- =====================================================

-- Active tasks view
CREATE VIEW IF NOT EXISTS v_active_tasks AS
SELECT
    id,
    type,
    description,
    priority,
    status,
    created_at,
    scheduled_at,
    CASE
        WHEN scheduled_at IS NULL THEN 0
        WHEN scheduled_at <= CURRENT_TIMESTAMP THEN 1
        ELSE 0
    END AS is_ready
FROM tasks
WHERE status IN ('pending', 'running')
ORDER BY priority DESC, scheduled_at ASC;

-- Task execution statistics view
CREATE VIEW IF NOT EXISTS v_task_statistics AS
SELECT
    t.type,
    COUNT(*) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    SUM(CASE WHEN t.status = 'failed' THEN 1 ELSE 0 END) AS failed_tasks,
    AVG(CASE WHEN eh.duration_seconds IS NOT NULL THEN eh.duration_seconds ELSE NULL END) AS avg_duration_seconds,
    MAX(t.created_at) AS last_task_created_at
FROM tasks t
LEFT JOIN execution_history eh ON t.id = eh.task_id
GROUP BY t.type;

-- Recent metrics view
CREATE VIEW IF NOT EXISTS v_recent_metrics AS
SELECT
    metric_name,
    metric_value,
    timestamp,
    ROW_NUMBER() OVER (PARTITION BY metric_name ORDER BY timestamp DESC) AS rn
FROM metrics
WHERE timestamp >= datetime('now', '-7 days');

-- System health view
CREATE VIEW IF NOT EXISTS v_system_health AS
SELECT
    (SELECT COUNT(*) FROM tasks WHERE status = 'pending') AS pending_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'running') AS running_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'failed' AND created_at >= datetime('now', '-1 day')) AS failed_tasks_24h,
    (SELECT AVG(duration_seconds) FROM execution_history WHERE started_at >= datetime('now', '-1 hour')) AS avg_execution_time_1h,
    (SELECT COUNT(*) FROM audit_log WHERE event_type = 'rate_limit_exceeded' AND timestamp >= datetime('now', '-1 hour')) AS rate_limit_hits_1h;
