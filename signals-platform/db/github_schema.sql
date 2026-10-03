-- db/github_schema.sql
CREATE TABLE IF NOT EXISTS github.commit_activity (
    repo_name VARCHAR(100),
    week_starting DATE,
    commit_count INT,
    PRIMARY KEY (repo_name, week_starting)
);

CREATE INDEX IF NOT EXISTS idx_github_date ON github.commit_activity(week_starting);