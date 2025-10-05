-- =====================================================
-- MAINTAINER DASHBOARD DUMMY DATA
-- Mimics GitHub API & Ecosyste.ms data structures
-- =====================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS burnout_risk_scores CASCADE;
DROP TABLE IF EXISTS sentiment_analysis CASCADE;
DROP TABLE IF EXISTS pr_review_comments CASCADE;
DROP TABLE IF EXISTS pr_reviews CASCADE;
DROP TABLE IF EXISTS issue_timeline_events CASCADE;
DROP TABLE IF EXISTS issue_comments CASCADE;
DROP TABLE IF EXISTS discussion_comments CASCADE;
DROP TABLE IF EXISTS discussions CASCADE;
DROP TABLE IF EXISTS pull_requests CASCADE;
DROP TABLE IF EXISTS issues CASCADE;
DROP TABLE IF EXISTS commits CASCADE;
DROP TABLE IF EXISTS repositories CASCADE;
DROP TABLE IF EXISTS maintainers CASCADE;

-- =====================================================
-- TABLE SCHEMAS
-- =====================================================

-- Maintainers Table
CREATE TABLE maintainers (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    company VARCHAR(255),
    location VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    public_repos INT DEFAULT 0,
    followers INT DEFAULT 0,
    following INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Repositories Table
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(500) NOT NULL,
    owner_id INT REFERENCES maintainers(id),
    description TEXT,
    stars INT DEFAULT 0,
    forks INT DEFAULT 0,
    watchers INT DEFAULT 0,
    open_issues INT DEFAULT 0,
    language VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    pushed_at TIMESTAMP,
    size_kb INT DEFAULT 0,
    default_branch VARCHAR(100) DEFAULT 'main'
);

-- Issues Table
CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    repository_id INT REFERENCES repositories(id),
    number INT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    state VARCHAR(50) NOT NULL, -- open, closed
    created_by INT REFERENCES maintainers(id),
    assigned_to INT REFERENCES maintainers(id),
    closed_by INT REFERENCES maintainers(id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    comments_count INT DEFAULT 0,
    labels JSONB DEFAULT '[]'::jsonb,
    is_pull_request BOOLEAN DEFAULT FALSE
);

-- Pull Requests Table
CREATE TABLE pull_requests (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    repository_id INT REFERENCES repositories(id),
    number INT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    state VARCHAR(50) NOT NULL, -- open, closed, merged
    created_by INT REFERENCES maintainers(id),
    merged_by INT REFERENCES maintainers(id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    merged_at TIMESTAMP,
    commits_count INT DEFAULT 0,
    additions INT DEFAULT 0,
    deletions INT DEFAULT 0,
    changed_files INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    review_comments_count INT DEFAULT 0,
    base_branch VARCHAR(255),
    head_branch VARCHAR(255),
    mergeable BOOLEAN DEFAULT TRUE,
    draft BOOLEAN DEFAULT FALSE
);

-- PR Reviews Table
CREATE TABLE pr_reviews (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    pull_request_id INT REFERENCES pull_requests(id),
    reviewer_id INT REFERENCES maintainers(id),
    state VARCHAR(50) NOT NULL, -- APPROVED, CHANGES_REQUESTED, COMMENTED, DISMISSED, PENDING
    body TEXT,
    submitted_at TIMESTAMP NOT NULL,
    commit_id VARCHAR(40),
    review_depth_score DECIMAL(5,2) DEFAULT 0.0, -- Custom score for depth of review
    lines_reviewed INT DEFAULT 0
);

-- PR Review Comments Table
CREATE TABLE pr_review_comments (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    review_id INT REFERENCES pr_reviews(id),
    pull_request_id INT REFERENCES pull_requests(id),
    commenter_id INT REFERENCES maintainers(id),
    body TEXT NOT NULL,
    path VARCHAR(500), -- file path
    position INT, -- position in diff
    line INT, -- line number
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    in_reply_to_id INT REFERENCES pr_review_comments(id)
);

-- Issue Comments Table
CREATE TABLE issue_comments (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    issue_id INT REFERENCES issues(id),
    commenter_id INT REFERENCES maintainers(id),
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    reactions JSONB DEFAULT '{}'::jsonb -- {"+1": 5, "heart": 2, etc}
);

-- Issue Timeline Events Table (for triage tracking)
CREATE TABLE issue_timeline_events (
    id SERIAL PRIMARY KEY,
    github_id VARCHAR(100) UNIQUE NOT NULL,
    issue_id INT REFERENCES issues(id),
    event_type VARCHAR(100) NOT NULL, -- labeled, unlabeled, assigned, unassigned, closed, reopened, etc
    actor_id INT REFERENCES maintainers(id),
    created_at TIMESTAMP NOT NULL,
    label_name VARCHAR(255),
    assignee_id INT REFERENCES maintainers(id),
    milestone_title VARCHAR(255),
    old_value TEXT,
    new_value TEXT
);

-- GitHub Discussions Table
CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    repository_id INT REFERENCES repositories(id),
    number INT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    category VARCHAR(255),
    created_by INT REFERENCES maintainers(id),
    answered_by INT REFERENCES maintainers(id),
    is_answered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    comments_count INT DEFAULT 0,
    upvotes INT DEFAULT 0
);

-- Discussion Comments Table
CREATE TABLE discussion_comments (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    discussion_id INT REFERENCES discussions(id),
    commenter_id INT REFERENCES maintainers(id),
    parent_comment_id INT REFERENCES discussion_comments(id),
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    upvotes INT DEFAULT 0,
    is_answer BOOLEAN DEFAULT FALSE
);

-- Commits Table (for documentation and code changes)
CREATE TABLE commits (
    id SERIAL PRIMARY KEY,
    sha VARCHAR(40) UNIQUE NOT NULL,
    repository_id INT REFERENCES repositories(id),
    author_id INT REFERENCES maintainers(id),
    committer_id INT REFERENCES maintainers(id),
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    additions INT DEFAULT 0,
    deletions INT DEFAULT 0,
    changed_files INT DEFAULT 0,
    is_docs_related BOOLEAN DEFAULT FALSE -- Custom flag for doc changes
);

-- Sentiment Analysis Table
CREATE TABLE sentiment_analysis (
    id SERIAL PRIMARY KEY,
    maintainer_id INT REFERENCES maintainers(id),
    content_type VARCHAR(50) NOT NULL, -- pr_review, issue_comment, discussion_comment
    content_id INT NOT NULL, -- references the specific comment/review
    sentiment_score DECIMAL(5,4) NOT NULL, -- -1.0 to 1.0
    tone VARCHAR(50), -- constructive, neutral, harsh, supportive
    analysis_date TIMESTAMP NOT NULL,
    text_analyzed TEXT NOT NULL
);

-- Burnout Risk Scores Table
CREATE TABLE burnout_risk_scores (
    id SERIAL PRIMARY KEY,
    maintainer_id INT REFERENCES maintainers(id),
    calculation_date TIMESTAMP NOT NULL,
    overall_risk_score DECIMAL(5,2) NOT NULL, -- 0-100
    response_time_score DECIMAL(5,2), -- degradation indicator
    activity_level_score DECIMAL(5,2), -- decline indicator
    sentiment_score DECIMAL(5,2), -- deterioration indicator
    isolation_score DECIMAL(5,2), -- working alone indicator
    workload_score DECIMAL(5,2), -- hours worked indicator
    community_support_score DECIMAL(5,2) -- recognition received
);

-- =====================================================
-- DUMMY DATA INSERTION
-- =====================================================

-- Insert Maintainers (5 maintainers with varying activity patterns)
INSERT INTO maintainers (github_id, username, name, email, avatar_url, bio, company, location, created_at, updated_at, public_repos, followers, following, is_active) VALUES
(12345001, 'sarah_maintainer', 'Sarah Johnson', 'sarah@example.com', 'https://avatars.githubusercontent.com/u/12345001', 'Senior OSS Maintainer | Loves Python and Rust', 'TechCorp', 'San Francisco, CA', '2018-01-15 10:00:00', '2025-10-01 14:30:00', 45, 1250, 180, TRUE),
(12345002, 'alex_dev', 'Alex Chen', 'alex@example.com', 'https://avatars.githubusercontent.com/u/12345002', 'Full-stack developer | Open source enthusiast', 'StartupXYZ', 'New York, NY', '2019-03-20 09:00:00', '2025-09-28 16:45:00', 32, 890, 145, TRUE),
(12345003, 'morgan_code', 'Morgan Lee', 'morgan@example.com', 'https://avatars.githubusercontent.com/u/12345003', 'Backend specialist | Contributor to major projects', 'Freelance', 'Austin, TX', '2017-06-10 11:30:00', '2025-10-03 10:15:00', 67, 2100, 220, TRUE),
(12345004, 'jamie_oss', 'Jamie Rivera', 'jamie@example.com', 'https://avatars.githubusercontent.com/u/12345004', 'DevOps engineer | Documentation lover', 'CloudCo', 'Seattle, WA', '2020-02-05 08:00:00', '2025-09-25 13:20:00', 28, 650, 95, TRUE),
(12345005, 'riley_contrib', 'Riley Taylor', 'riley@example.com', 'https://avatars.githubusercontent.com/u/12345005', 'Junior developer | Learning in public', 'University', 'Boston, MA', '2022-08-12 15:00:00', '2025-10-04 09:00:00', 15, 180, 210, TRUE);

-- Insert Repositories (3 major projects)
INSERT INTO repositories (github_id, name, full_name, owner_id, description, stars, forks, watchers, open_issues, language, created_at, updated_at, pushed_at, size_kb, default_branch) VALUES
(98765001, 'awesome-framework', 'sarah_maintainer/awesome-framework', 1, 'A powerful web framework for modern applications', 15420, 2340, 890, 156, 'Python', '2019-05-10 10:00:00', '2025-10-04 11:30:00', '2025-10-04 11:30:00', 45678, 'main'),
(98765002, 'data-processor', 'alex_dev/data-processor', 2, 'High-performance data processing library', 8920, 1120, 450, 89, 'Rust', '2020-07-15 14:20:00', '2025-10-03 16:45:00', '2025-10-03 16:45:00', 23456, 'main'),
(98765003, 'cli-toolbox', 'morgan_code/cli-toolbox', 3, 'Essential command-line utilities for developers', 6780, 890, 320, 67, 'Go', '2021-03-22 09:15:00', '2025-10-02 10:20:00', '2025-10-02 10:20:00', 12345, 'main');

-- Insert Issues (20 issues across repositories)
INSERT INTO issues (github_id, repository_id, number, title, body, state, created_by, assigned_to, closed_by, created_at, updated_at, closed_at, comments_count, labels, is_pull_request) VALUES
-- awesome-framework issues
(19876001, 1, 1, 'Memory leak in WebSocket handler', 'Detailed description of memory leak...', 'closed', 5, 1, 1, '2025-09-15 10:30:00', '2025-09-20 16:45:00', '2025-09-20 16:45:00', 8, '["bug", "high-priority", "performance"]', FALSE),
(19876002, 1, 2, 'Add support for async middleware', 'Feature request for async middleware support...', 'open', 4, 2, NULL, '2025-09-18 14:20:00', '2025-10-03 11:15:00', NULL, 12, '["enhancement", "good-first-issue"]', FALSE),
(19876003, 1, 3, 'Documentation unclear for configuration', 'The configuration docs need better examples...', 'closed', 5, 1, 1, '2025-09-22 09:00:00', '2025-09-25 15:30:00', '2025-09-25 15:30:00', 5, '["documentation"]', FALSE),
(19876004, 1, 4, 'Security vulnerability in auth module', 'URGENT: Found security issue in authentication...', 'closed', 3, 1, 1, '2025-09-25 16:00:00', '2025-09-27 10:20:00', '2025-09-27 10:20:00', 15, '["security", "critical"]', FALSE),
(19876005, 1, 5, 'Performance regression in v3.2', 'Response times increased after upgrade...', 'open', 2, 1, NULL, '2025-09-28 11:45:00', '2025-10-04 09:30:00', NULL, 18, '["bug", "performance", "needs-investigation"]', FALSE),
(19876006, 1, 6, 'Add TypeScript definitions', 'Request to add TypeScript type definitions...', 'open', 5, 2, NULL, '2025-10-01 10:15:00', '2025-10-04 14:20:00', NULL, 7, '["enhancement", "typescript"]', FALSE),
(19876007, 1, 7, 'Error handling improvements', 'Better error messages needed throughout...', 'open', 4, NULL, NULL, '2025-10-02 13:30:00', '2025-10-03 16:45:00', NULL, 3, '["enhancement", "dx-improvement"]', FALSE),

-- data-processor issues
(19876008, 2, 1, 'Parallel processing not working on Windows', 'Issue with thread pool on Windows systems...', 'closed', 5, 2, 2, '2025-09-12 14:00:00', '2025-09-18 11:30:00', '2025-09-18 11:30:00', 10, '["bug", "platform-specific"]', FALSE),
(19876009, 2, 2, 'Add CSV export functionality', 'Users requesting CSV export feature...', 'open', 3, 2, NULL, '2025-09-20 10:30:00', '2025-10-02 15:20:00', NULL, 14, '["enhancement", "user-request"]', FALSE),
(19876010, 2, 3, 'Benchmark comparisons needed', 'Need benchmarks against similar tools...', 'open', 4, NULL, NULL, '2025-09-25 09:15:00', '2025-09-28 14:45:00', NULL, 6, '["documentation", "benchmarks"]', FALSE),
(19876011, 2, 4, 'Memory usage too high on large datasets', 'Processing 1GB+ files causes OOM errors...', 'open', 1, 2, NULL, '2025-09-29 16:20:00', '2025-10-04 10:15:00', NULL, 9, '["bug", "performance", "high-priority"]', FALSE),
(19876012, 2, 5, 'Installation fails on Ubuntu 22.04', 'Dependency conflict during installation...', 'closed', 5, 3, 2, '2025-10-01 11:00:00', '2025-10-03 13:45:00', '2025-10-03 13:45:00', 4, '["bug", "installation"]', FALSE),

-- cli-toolbox issues
(19876013, 3, 1, 'Command autocompletion not working', 'Shell completion scripts not loading...', 'closed', 4, 3, 3, '2025-09-14 15:30:00', '2025-09-22 10:00:00', '2025-09-22 10:00:00', 7, '["bug", "cli"]', FALSE),
(19876014, 3, 2, 'Add color theme customization', 'Allow users to customize output colors...', 'open', 5, 3, NULL, '2025-09-19 13:45:00', '2025-10-01 16:30:00', NULL, 11, '["enhancement", "ui"]', FALSE),
(19876015, 3, 3, 'Improve error messages', 'Error messages should be more helpful...', 'open', 2, NULL, NULL, '2025-09-24 10:00:00', '2025-09-30 14:15:00', NULL, 5, '["enhancement", "dx-improvement"]', FALSE),
(19876016, 3, 4, 'Config file validation', 'Add validation for config file format...', 'open', 1, 3, NULL, '2025-09-27 12:30:00', '2025-10-04 11:45:00', NULL, 8, '["enhancement", "validation"]', FALSE),
(19876017, 3, 5, 'Update documentation for v2.0', 'Docs need updating for new release...', 'open', 4, 3, NULL, '2025-09-30 09:20:00', '2025-10-03 15:00:00', NULL, 6, '["documentation", "release"]', FALSE),
(19876018, 3, 6, 'Plugin system architecture', 'Design proposal for plugin system...', 'open', 3, NULL, NULL, '2025-10-01 14:15:00', '2025-10-04 12:30:00', NULL, 13, '["discussion", "architecture"]', FALSE),
(19876019, 3, 7, 'Performance optimization for large outputs', 'Output buffering for large command results...', 'open', 2, 3, NULL, '2025-10-02 11:00:00', '2025-10-04 09:15:00', NULL, 4, '["enhancement", "performance"]', FALSE),
(19876020, 3, 8, 'Cross-platform testing CI', 'Setup CI for Windows, Mac, and Linux...', 'open', 5, NULL, NULL, '2025-10-03 16:45:00', '2025-10-04 10:30:00', NULL, 2, '["ci", "testing"]', FALSE);

-- Insert Pull Requests (25 PRs across repositories)
INSERT INTO pull_requests (github_id, repository_id, number, title, body, state, created_by, merged_by, created_at, updated_at, closed_at, merged_at, commits_count, additions, deletions, changed_files, comments_count, review_comments_count, base_branch, head_branch, mergeable, draft) VALUES
-- awesome-framework PRs
(29876001, 1, 100, 'Fix memory leak in WebSocket handler', 'Fixes issue #1 by properly closing connections...', 'merged', 5, 1, '2025-09-16 10:00:00', '2025-09-20 16:30:00', '2025-09-20 16:30:00', '2025-09-20 16:30:00', 3, 45, 12, 2, 5, 8, 'main', 'fix/websocket-leak', TRUE, FALSE),
(29876002, 1, 101, 'Add async middleware support', 'Implements async middleware as requested in #2...', 'open', 4, NULL, '2025-09-19 11:30:00', '2025-10-03 15:45:00', NULL, NULL, 8, 234, 67, 5, 12, 18, 'main', 'feature/async-middleware', TRUE, FALSE),
(29876003, 1, 102, 'Update configuration documentation', 'Improves config docs with examples...', 'merged', 1, 1, '2025-09-23 09:15:00', '2025-09-25 15:00:00', '2025-09-25 15:00:00', '2025-09-25 15:00:00', 2, 156, 34, 3, 3, 4, 'main', 'docs/config-examples', TRUE, FALSE),
(29876004, 1, 103, 'Security fix for auth module', 'SECURITY: Patches vulnerability in auth...', 'merged', 3, 1, '2025-09-25 16:30:00', '2025-09-27 10:00:00', '2025-09-27 10:00:00', '2025-09-27 10:00:00', 5, 78, 45, 4, 8, 12, 'main', 'security/auth-patch', TRUE, FALSE),
(29876005, 1, 104, 'Performance optimization for v3.2', 'Addresses performance regression in #5...', 'open', 2, NULL, '2025-09-29 10:00:00', '2025-10-04 11:30:00', NULL, NULL, 6, 189, 98, 7, 15, 22, 'main', 'perf/v3.2-optimization', TRUE, FALSE),
(29876006, 1, 105, 'Add TypeScript definitions', 'Initial TypeScript type definitions...', 'open', 5, NULL, '2025-10-01 14:45:00', '2025-10-04 16:20:00', NULL, NULL, 4, 312, 0, 8, 9, 14, 'main', 'feature/typescript-defs', TRUE, FALSE),
(29876007, 1, 106, 'Refactor error handling', 'Improves error handling across codebase...', 'open', 1, NULL, '2025-10-02 15:30:00', '2025-10-04 13:15:00', NULL, NULL, 7, 267, 134, 12, 6, 11, 'main', 'refactor/error-handling', TRUE, TRUE),
(29876008, 1, 107, 'Update dependencies', 'Bump dependencies to latest versions...', 'merged', 2, 2, '2025-10-03 09:00:00', '2025-10-03 17:45:00', '2025-10-03 17:45:00', '2025-10-03 17:45:00', 1, 23, 23, 1, 2, 2, 'main', 'chore/deps-update', TRUE, FALSE),

-- data-processor PRs
(29876009, 2, 50, 'Fix Windows thread pool issue', 'Resolves parallel processing bug on Windows...', 'merged', 4, 2, '2025-09-13 11:00:00', '2025-09-18 11:00:00', '2025-09-18 11:00:00', '2025-09-18 11:00:00', 4, 123, 56, 3, 7, 10, 'main', 'fix/windows-threads', TRUE, FALSE),
(29876010, 2, 51, 'Implement CSV export feature', 'Adds CSV export functionality as requested...', 'open', 3, NULL, '2025-09-21 10:15:00', '2025-10-02 16:30:00', NULL, NULL, 9, 456, 12, 6, 11, 17, 'main', 'feature/csv-export', TRUE, FALSE),
(29876011, 2, 52, 'Add benchmark documentation', 'Adds comprehensive benchmark comparisons...', 'open', 4, NULL, '2025-09-26 14:00:00', '2025-09-29 11:20:00', NULL, NULL, 3, 234, 8, 5, 5, 6, 'main', 'docs/benchmarks', TRUE, FALSE),
(29876012, 2, 53, 'Optimize memory usage', 'Reduces memory footprint for large datasets...', 'open', 2, NULL, '2025-09-30 13:30:00', '2025-10-04 14:45:00', NULL, NULL, 11, 378, 167, 9, 13, 20, 'main', 'perf/memory-optimization', TRUE, FALSE),
(29876013, 2, 54, 'Fix Ubuntu installation', 'Resolves dependency conflict on Ubuntu...', 'merged', 5, 2, '2025-10-01 15:20:00', '2025-10-03 13:30:00', '2025-10-03 13:30:00', '2025-10-03 13:30:00', 2, 34, 12, 2, 3, 3, 'main', 'fix/ubuntu-install', TRUE, FALSE),
(29876014, 2, 55, 'Refactor core processing engine', 'Major refactoring for better maintainability...', 'open', 1, NULL, '2025-10-02 10:45:00', '2025-10-04 15:00:00', NULL, NULL, 15, 689, 423, 18, 8, 15, 'main', 'refactor/core-engine', TRUE, TRUE),

-- cli-toolbox PRs
(29876015, 3, 30, 'Fix shell completion scripts', 'Fixes autocompletion loading issues...', 'merged', 5, 3, '2025-09-15 12:00:00', '2025-09-22 09:45:00', '2025-09-22 09:45:00', '2025-09-22 09:45:00', 3, 67, 23, 3, 5, 6, 'main', 'fix/completion-scripts', TRUE, FALSE),
(29876016, 3, 31, 'Add color theme customization', 'Implements user-customizable color themes...', 'open', 4, NULL, '2025-09-20 15:15:00', '2025-10-01 17:00:00', NULL, NULL, 7, 289, 45, 8, 9, 13, 'main', 'feature/color-themes', TRUE, FALSE),
(29876017, 3, 32, 'Improve CLI error messages', 'Makes error messages more user-friendly...', 'open', 2, NULL, '2025-09-25 11:45:00', '2025-09-30 15:30:00', NULL, NULL, 5, 134, 78, 6, 4, 7, 'main', 'improve/error-messages', TRUE, FALSE),
(29876018, 3, 33, 'Add config file validation', 'Validates config file format and values...', 'open', 1, NULL, '2025-09-28 14:20:00', '2025-10-04 12:15:00', NULL, NULL, 6, 178, 34, 4, 7, 10, 'main', 'feature/config-validation', TRUE, FALSE),
(29876019, 3, 34, 'Update documentation for v2.0', 'Comprehensive docs update for v2.0 release...', 'open', 3, NULL, '2025-10-01 10:30:00', '2025-10-03 16:45:00', NULL, NULL, 8, 567, 234, 15, 5, 8, 'main', 'docs/v2.0-update', TRUE, FALSE),
(29876020, 3, 35, 'Design plugin system', 'Initial implementation of plugin architecture...', 'open', 2, NULL, '2025-10-01 16:00:00', '2025-10-04 13:00:00', NULL, NULL, 12, 834, 123, 22, 11, 19, 'main', 'feature/plugin-system', TRUE, TRUE),
(29876021, 3, 36, 'Optimize output buffering', 'Improves performance for large outputs...', 'open', 5, NULL, '2025-10-02 13:15:00', '2025-10-04 10:45:00', NULL, NULL, 4, 156, 89, 5, 3, 5, 'main', 'perf/output-buffering', TRUE, FALSE),
(29876022, 3, 37, 'Setup cross-platform CI', 'Adds CI workflow for Windows, Mac, Linux...', 'open', 4, NULL, '2025-10-03 17:30:00', '2025-10-04 11:00:00', NULL, NULL, 3, 234, 12, 6, 2, 2, 'main', 'ci/cross-platform', TRUE, FALSE),
(29876023, 3, 38, 'Add integration tests', 'Comprehensive integration test suite...', 'open', 1, NULL, '2025-10-04 09:30:00', '2025-10-04 14:30:00', NULL, NULL, 6, 456, 23, 12, 4, 7, 'main', 'test/integration-suite', TRUE, FALSE);

-- Insert PR Reviews (60+ reviews showing various patterns)
INSERT INTO pr_reviews (github_id, pull_request_id, reviewer_id, state, body, submitted_at, commit_id, review_depth_score, lines_reviewed) VALUES
-- Reviews for awesome-framework PRs (showing Sarah as active reviewer with varying sentiments)
(39876001, 1, 1, 'APPROVED', 'Great fix! This properly addresses the memory leak. The connection cleanup logic looks solid.', '2025-09-19 14:30:00', 'abc123def', 8.5, 45),
(39876002, 1, 2, 'COMMENTED', 'Have you tested this with high concurrency? Would like to see some load test results.', '2025-09-18 11:00:00', 'abc123def', 6.0, 38),
(39876003, 1, 3, 'APPROVED', 'LGTM! Nice work on the tests.', '2025-09-19 16:15:00', 'abc123def', 5.5, 30),

(39876004, 2, 1, 'CHANGES_REQUESTED', 'The implementation looks good but we need comprehensive tests for edge cases. Also, please add error handling for timeout scenarios.', '2025-09-23 10:30:00', 'def456ghi', 9.2, 234),
(39876005, 2, 2, 'COMMENTED', 'This is a significant change. We should consider backwards compatibility implications.', '2025-09-25 14:45:00', 'def456ghi', 7.8, 189),
(39876006, 2, 3, 'CHANGES_REQUESTED', 'Missing documentation for the new async API. Users will need clear examples.', '2025-09-28 11:20:00', 'ghi789jkl', 8.0, 156),
(39876007, 2, 1, 'COMMENTED', 'Thanks for addressing my concerns. The timeout handling looks better. Still waiting on the documentation updates before approval.', '2025-10-02 09:15:00', 'jkl012mno', 7.5, 123),

(39876008, 3, 1, 'APPROVED', 'Excellent documentation improvements! The examples are very clear.', '2025-09-24 16:00:00', 'mno345pqr', 7.0, 120),
(39876009, 3, 4, 'APPROVED', 'Docs look great!', '2025-09-25 10:30:00', 'mno345pqr', 4.5, 85),

(39876010, 4, 1, 'APPROVED', 'Critical security fix. Thanks for the quick turnaround. The patch looks comprehensive.', '2025-09-26 18:00:00', 'pqr678stu', 9.5, 78),
(39876011, 4, 2, 'APPROVED', 'Security issue properly addressed. Good catch.', '2025-09-26 19:30:00', 'pqr678stu', 7.8, 67),
(39876012, 4, 3, 'COMMENTED', 'Should we add regression tests to prevent this from happening again?', '2025-09-27 08:15:00', 'pqr678stu', 6.5, 52),

(39876013, 5, 1, 'CHANGES_REQUESTED', 'The optimization approach is interesting but I''m seeing potential race conditions in the caching layer. Please review the mutex usage carefully.', '2025-10-01 14:00:00', 'stu901vwx', 9.0, 189),
(39876014, 5, 2, 'COMMENTED', 'Have you benchmarked this against the previous version? Would be good to see concrete numbers.', '2025-10-02 10:45:00', 'vwx234yz1', 7.2, 145),
(39876015, 5, 3, 'COMMENTED', 'The caching strategy makes sense but concerned about memory overhead.', '2025-10-03 15:20:00', 'vwx234yz1', 6.8, 132),
(39876016, 5, 1, 'COMMENTED', 'Thanks for addressing the race condition. The mutex fix looks good. Still need to see benchmark results before we can merge.', '2025-10-04 09:45:00', 'yz1345abc', 8.3, 156),

(39876017, 6, 1, 'CHANGES_REQUESTED', 'Good start on TypeScript definitions but several types are incomplete. See inline comments for specifics.', '2025-10-02 16:30:00', 'abc456def', 8.7, 234),
(39876018, 6, 2, 'COMMENTED', 'These types will really help our TypeScript users. Nice work!', '2025-10-03 11:00:00', 'def789ghi', 6.5, 187),
(39876019, 6, 4, 'CHANGES_REQUESTED', 'Missing generics for several key interfaces. This won''t be flexible enough for advanced use cases.', '2025-10-04 14:15:00', 'ghi012jkl', 7.9, 203),

(39876020, 7, 1, 'COMMENTED', 'This is a substantial refactoring. Let''s make sure we have test coverage before merging.', '2025-10-03 16:00:00', 'jkl345mno', 8.2, 267),
(39876021, 7, 3, 'COMMENTED', 'Looks good so far. Will do a full review once tests are added.', '2025-10-04 10:30:00', 'mno678pqr', 6.0, 189),

(39876022, 8, 2, 'APPROVED', 'Dependency updates look clean. All tests passing.', '2025-10-03 15:00:00', 'pqr901stu', 5.0, 23),

-- Reviews for data-processor PRs (showing Alex as lead reviewer)
(39876023, 9, 2, 'APPROVED', 'Excellent fix for the Windows issue. Platform-specific handling is well done.', '2025-09-16 15:30:00', 'stu234vwx', 8.8, 123),
(39876024, 9, 3, 'APPROVED', 'Windows threading finally works! Great job.', '2025-09-17 10:00:00', 'vwx567yz2', 6.2, 98),
(39876025, 9, 1, 'COMMENTED', 'Consider adding tests for Mac as well since threading can vary by platform.', '2025-09-17 14:20:00', 'vwx567yz2', 7.0, 87),

(39876026, 10, 2, 'CHANGES_REQUESTED', 'CSV implementation needs better error handling. What happens with malformed data?', '2025-09-26 11:45:00', 'yz2678abc', 8.5, 345),
(39876027, 10, 3, 'COMMENTED', 'Looking forward to this feature! The API design looks intuitive.', '2025-09-28 09:30:00', 'abc901def', 6.8, 267),
(39876028, 10, 1, 'CHANGES_REQUESTED', 'Need comprehensive tests for edge cases - empty files, huge files, special characters, etc.', '2025-09-30 16:00:00', 'def234ghi', 9.0, 312),
(39876029, 10, 2, 'COMMENTED', 'Thanks for the updates. Error handling is much better. Still want to see those edge case tests though.', '2025-10-02 13:45:00', 'ghi567jkl', 7.8, 289),

(39876030, 11, 2, 'COMMENTED', 'Benchmarks are helpful. Can you add comparisons with similar tools?', '2025-09-27 15:15:00', 'jkl890mno', 7.2, 178),
(39876031, 11, 4, 'APPROVED', 'Great benchmark documentation!', '2025-09-29 10:00:00', 'mno123pqr', 5.5, 145),

(39876032, 12, 2, 'CHANGES_REQUESTED', 'Memory optimization looks promising but I''m seeing potential issues with the buffer pool management. Let''s discuss the approach.', '2025-10-02 11:30:00', 'pqr456stu', 9.3, 378),
(39876033, 12, 3, 'COMMENTED', 'This is complex. Would benefit from detailed comments explaining the algorithm.', '2025-10-03 14:00:00', 'stu789vwx', 8.0, 312),
(39876034, 12, 1, 'COMMENTED', 'The buffer pool pattern is good but consider using an existing library instead of rolling our own.', '2025-10-04 10:15:00', 'vwx012yz3', 7.5, 267),

(39876035, 13, 2, 'APPROVED', 'Quick fix for the Ubuntu issue. Thanks!', '2025-10-02 18:00:00', 'yz3345abc', 6.0, 34),
(39876036, 13, 3, 'APPROVED', 'Installation works now. Great!', '2025-10-03 09:15:00', 'yz3345abc', 4.8, 28),

(39876037, 14, 2, 'COMMENTED', 'Major refactoring like this needs extensive testing. Let''s be cautious.', '2025-10-03 16:30:00', 'abc678def', 8.8, 456),
(39876038, 14, 1, 'COMMENTED', 'Good direction but this will take time to review properly. Breaking changes?', '2025-10-04 13:15:00', 'def901ghi', 7.0, 389),

-- Reviews for cli-toolbox PRs (showing Morgan as active reviewer)
(39876039, 15, 3, 'APPROVED', 'Shell completion works perfectly now. Nice fix!', '2025-09-20 14:00:00', 'ghi234jkl', 7.5, 67),
(39876040, 15, 4, 'APPROVED', 'Completion scripts look good!', '2025-09-21 10:30:00', 'ghi234jkl', 5.2, 45),

(39876041, 16, 3, 'CHANGES_REQUESTED', 'Color customization is a great feature but the config format is inconsistent with our existing patterns. Let''s align this with the rest of the codebase.', '2025-09-28 11:00:00', 'jkl567mno', 8.9, 289),
(39876042, 16, 1, 'COMMENTED', 'Love the feature! Agree with Morgan about the config format though.', '2025-09-30 15:45:00', 'mno890pqr', 6.9, 234),
(39876043, 16, 4, 'COMMENTED', 'Will this support custom themes from files?', '2025-10-01 13:20:00', 'mno890pqr', 5.8, 198),

(39876044, 17, 3, 'APPROVED', 'Much better error messages! This will really help users.', '2025-09-29 16:30:00', 'pqr123stu', 7.8, 134),
(39876045, 17, 2, 'APPROVED', 'Error improvements look great.', '2025-09-30 11:00:00', 'pqr123stu', 6.0, 98),

(39876046, 18, 3, 'CHANGES_REQUESTED', 'Validation logic is good but error messages could be more specific. Help users understand exactly what''s wrong with their config.', '2025-10-02 10:00:00', 'stu456vwx', 8.6, 178),
(39876047, 18, 1, 'COMMENTED', 'Config validation is important. Consider adding validation for value ranges too.', '2025-10-03 14:30:00', 'vwx789yz4', 7.3, 145),
(39876048, 18, 4, 'COMMENTED', 'Can we provide suggestions for fixing invalid configs?', '2025-10-04 09:00:00', 'vwx789yz4', 6.5, 123),

(39876049, 19, 3, 'COMMENTED', 'Comprehensive docs update. This will take some time to review thoroughly.', '2025-10-02 16:00:00', 'yz4012abc', 8.2, 456),
(39876050, 19, 2, 'COMMENTED', 'Looking good so far. Will finish review by end of week.', '2025-10-03 11:30:00', 'abc345def', 6.8, 378),

(39876051, 20, 3, 'COMMENTED', 'Plugin architecture is ambitious! Let''s make sure the API is stable before committing to this design.', '2025-10-02 18:00:00', 'def678ghi', 9.0, 623),
(39876052, 20, 2, 'COMMENTED', 'This needs careful design review. Plugin systems are hard to change later.', '2025-10-03 13:00:00', 'ghi901jkl', 8.5, 556),
(39876053, 20, 1, 'COMMENTED', 'Exciting feature! Have you looked at how other tools handle plugins?', '2025-10-04 10:00:00', 'jkl234mno', 7.8, 489),

(39876054, 21, 3, 'APPROVED', 'Output buffering optimization works well. Good performance improvement.', '2025-10-03 15:30:00', 'mno567pqr', 7.6, 156),
(39876055, 21, 5, 'APPROVED', 'Performance is noticeably better!', '2025-10-04 09:30:00', 'mno567pqr', 5.5, 112),

(39876056, 22, 3, 'COMMENTED', 'CI setup looks comprehensive. Make sure all platforms are covered.', '2025-10-04 13:45:00', 'pqr890stu', 7.0, 178),
(39876057, 22, 4, 'APPROVED', 'CI configuration looks good!', '2025-10-04 14:30:00', 'pqr890stu', 6.2, 145),

(39876058, 23, 3, 'COMMENTED', 'Integration tests are crucial. This looks like a good start.', '2025-10-04 12:00:00', 'stu123vwx', 7.8, 345),
(39876059, 23, 1, 'COMMENTED', 'Great to see comprehensive tests! A few edge cases missing though.', '2025-10-04 15:00:00', 'vwx456yz5', 8.2, 312);

-- Insert PR Review Comments (detailed line-by-line comments showing mentorship)
INSERT INTO pr_review_comments (github_id, review_id, pull_request_id, commenter_id, body, path, position, line, created_at, updated_at, in_reply_to_id) VALUES
-- Comments showing mentorship for less experienced contributor (Riley)
(49876001, 1, 1, 1, 'Nice approach! One suggestion: consider using a context manager here for cleaner resource cleanup.', 'src/websocket/handler.py', 15, 45, '2025-09-19 14:15:00', '2025-09-19 14:15:00', NULL),
(49876002, 1, 1, 1, 'Good catch on the edge case. Have you considered what happens when the connection is already closed?', 'src/websocket/handler.py', 28, 67, '2025-09-19 14:20:00', '2025-09-19 14:20:00', NULL),
(49876003, 1, 1, 5, 'Thanks for the suggestion! I''ll add try-except for already closed connections.', 'src/websocket/handler.py', 28, 67, '2025-09-19 15:30:00', '2025-09-19 15:30:00', 49876002),
(49876004, 1, 1, 1, 'Perfect! That''ll make it more robust. Keep up the great work! 🎉', 'src/websocket/handler.py', 28, 67, '2025-09-19 16:00:00', '2025-09-19 16:00:00', 49876003),

-- Comments showing detailed technical review
(49876005, 4, 2, 1, 'This async implementation is solid, but let''s add timeout handling. Without it, async operations could hang indefinitely.', 'src/middleware/async_handler.py', 23, 89, '2025-09-23 10:15:00', '2025-09-23 10:15:00', NULL),
(49876006, 4, 2, 1, 'Consider extracting this into a separate validator function. It''ll make testing easier.', 'src/middleware/async_handler.py', 45, 123, '2025-09-23 10:20:00', '2025-09-23 10:20:00', NULL),
(49876007, 4, 2, 1, 'Documentation for this function should explain the timeout behavior and what exceptions callers should expect.', 'src/middleware/async_handler.py', 67, 167, '2025-09-23 10:25:00', '2025-09-23 10:25:00', NULL),
(49876008, 4, 2, 4, 'Good point about the timeout. I''ll add a configurable timeout parameter.', 'src/middleware/async_handler.py', 23, 89, '2025-09-24 09:00:00', '2025-09-24 09:00:00', 49876005),

-- Comments showing harsh but technically correct feedback (potential burnout indicator)
(49876009, 13, 5, 1, 'This caching implementation has race conditions. Did you even test this with concurrent requests? This won''t work in production.', 'src/cache/manager.py', 34, 112, '2025-10-01 14:00:00', '2025-10-01 14:00:00', NULL),
(49876010, 13, 5, 1, 'You''re missing mutex locks here. This is basic concurrency 101.', 'src/cache/manager.py', 56, 145, '2025-10-01 14:05:00', '2025-10-01 14:05:00', NULL),
(49876011, 13, 5, 2, 'Thanks for catching that. I''ll add proper locking.', 'src/cache/manager.py', 56, 145, '2025-10-01 16:30:00', '2025-10-01 16:30:00', 49876010),

-- Comments showing constructive feedback
(49876012, 17, 6, 1, 'The type definitions look good! A few suggestions to make them even better...', 'index.d.ts', 12, 34, '2025-10-02 16:15:00', '2025-10-02 16:15:00', NULL),
(49876013, 17, 6, 1, 'This interface should probably be generic to support different middleware types.', 'index.d.ts', 45, 78, '2025-10-02 16:20:00', '2025-10-02 16:20:00', NULL),
(49876014, 17, 6, 5, 'Great idea! How would you suggest structuring the generic?', 'index.d.ts', 45, 78, '2025-10-02 18:00:00', '2025-10-02 18:00:00', 49876013),
(49876015, 17, 6, 1, 'Something like: interface Middleware<T, R> { ... }. This way users can specify input and output types.', 'index.d.ts', 45, 78, '2025-10-03 09:00:00', '2025-10-03 09:00:00', 49876014),

-- Comments showing plugin system design discussion (mentorship through architecture)
(49876016, 51, 20, 3, 'For the plugin system, I''d recommend looking at how VSCode handles extensions. Their approach is battle-tested.', 'src/plugin/loader.py', 23, 67, '2025-10-02 18:00:00', '2025-10-02 18:00:00', NULL),
(49876017, 51, 20, 3, 'We should define a clear plugin lifecycle: init, load, activate, deactivate. This prevents plugins from leaving resources hanging.', 'src/plugin/manager.py', 34, 89, '2025-10-02 18:10:00', '2025-10-02 18:10:00', NULL),
(49876018, 51, 20, 2, 'Excellent point about lifecycle. I''ll research the VSCode extension model.', 'src/plugin/loader.py', 23, 67, '2025-10-03 10:00:00', '2025-10-03 10:00:00', 49876016),
(49876019, 51, 20, 3, 'Happy to pair program on this if you want. Plugin systems are tricky to get right.', 'src/plugin/loader.py', 23, 67, '2025-10-03 15:00:00', '2025-10-03 15:00:00', 49876018),

-- More comments showing various review patterns
(49876020, 26, 10, 2, 'Have you tested this with files containing non-UTF8 characters? CSV encoding can be tricky.', 'src/export/csv.py', 45, 123, '2025-09-26 11:30:00', '2025-09-26 11:30:00', NULL),
(49876021, 26, 10, 3, 'Not yet, good catch! I''ll add encoding tests.', 'src/export/csv.py', 45, 123, '2025-09-27 09:00:00', '2025-09-27 09:00:00', 49876020),

(49876022, 32, 12, 2, 'This buffer pool implementation is clever, but consider: what happens when the pool is exhausted? Need a fallback strategy.', 'src/memory/pool.rs', 67, 234, '2025-10-02 11:15:00', '2025-10-02 11:15:00', NULL),
(49876023, 32, 12, 2, 'Also, the buffer size should probably be configurable based on system memory.', 'src/memory/pool.rs', 89, 289, '2025-10-02 11:20:00', '2025-10-02 11:20:00', NULL),

(49876024, 41, 16, 3, 'Love the color theme feature! Minor nitpick: the theme names could be more descriptive.', 'src/ui/themes.go', 23, 78, '2025-09-28 11:00:00', '2025-09-28 11:00:00', NULL),
(49876025, 41, 16, 4, 'What would you suggest for naming? I was going for simplicity.', 'src/ui/themes.go', 23, 78, '2025-09-29 10:00:00', '2025-09-29 10:00:00', 49876024),
(49876026, 41, 16, 3, 'Maybe something like ''github-dark'', ''solarized-light'' instead of ''theme1'', ''theme2''? Makes it clearer to users.', 'src/ui/themes.go', 23, 78, '2025-09-29 14:00:00', '2025-09-29 14:00:00', 49876025),

(49876027, 46, 18, 3, 'For validation errors, providing the line number where the error occurred would be super helpful for users.', 'src/config/validator.go', 34, 145, '2025-10-02 10:00:00', '2025-10-02 10:00:00', NULL),
(49876028, 46, 18, 1, 'And maybe suggest the correct format or value? Like ''Expected string, got integer at line 23''', 'src/config/validator.go', 45, 167, '2025-10-03 14:15:00', '2025-10-03 14:15:00', NULL);

-- Insert Issue Comments (showing triage and community engagement)
INSERT INTO issue_comments (github_id, issue_id, commenter_id, body, created_at, updated_at, reactions) VALUES
-- Memory leak issue - showing triage process
(59876001, 1, 1, 'Thanks for reporting this! Can you provide more details about your environment? What version are you running and approximately how many concurrent connections?', '2025-09-15 11:00:00', '2025-09-15 11:00:00', '{"heart": 2, "+1": 3}'),
(59876002, 1, 5, 'I''m on v3.1.2 with around 500-1000 concurrent WebSocket connections. Memory grows steadily over 24 hours until the process crashes.', '2025-09-15 14:30:00', '2025-09-15 14:30:00', '{}'),
(59876003, 1, 1, 'Perfect, that helps! I''ve been able to reproduce the issue. It looks like connection cleanup isn''t happening properly. I''ll have a fix ready soon.', '2025-09-16 09:00:00', '2025-09-16 09:00:00', '{"+1": 5, "rocket": 2}'),
(59876004, 1, 2, 'Is this related to #87? That also mentioned memory issues with WebSockets.', '2025-09-16 11:30:00', '2025-09-16 11:30:00', '{}'),
(59876005, 1, 1, 'Good catch Alex! Yes, it''s the same root cause. I''ll link the issues.', '2025-09-16 12:00:00', '2025-09-16 12:00:00', '{"heart": 1}'),
(59876006, 1, 1, 'Fix is ready in PR #100. Would appreciate if you could test @riley_contrib before we merge.', '2025-09-18 15:00:00', '2025-09-18 15:00:00', '{}'),
(59876007, 1, 5, 'Tested the fix - working perfectly! Memory usage is now stable over 48 hours. Thanks so much! 🎉', '2025-09-19 17:00:00', '2025-09-19 17:00:00', '{"+1": 8, "heart": 4, "hooray": 2}'),
(59876008, 1, 1, 'Excellent! Merged and will be in the next release. Thanks for the detailed report!', '2025-09-20 16:45:00', '2025-09-20 16:45:00', '{"rocket": 3}'),

-- Feature request showing mentorship
(59876009, 2, 1, 'Thanks for the feature request! This would be a great first contribution if you''re interested @jamie_oss. The middleware system is well-documented and I can guide you through the implementation.', '2025-09-18 15:30:00', '2025-09-18 15:30:00', '{"heart": 3}'),
(59876010, 2, 4, 'I''d love to take this on! Where should I start?', '2025-09-18 16:00:00', '2025-09-18 16:00:00', '{}'),
(59876011, 2, 1, 'Great! Start by reading docs/ARCHITECTURE.md to understand the middleware chain. Then look at the existing sync middleware in src/middleware/. I''d recommend creating the async version alongside it. Feel free to ping me with questions!', '2025-09-19 09:00:00', '2025-09-19 09:00:00', '{"+1": 5, "rocket": 1}'),
(59876012, 2, 4, 'Working on it! Quick question: should async middleware support both sync and async next() calls?', '2025-09-20 14:00:00', '2025-09-20 14:00:00', '{}'),
(59876013, 2, 1, 'Good question! Yes, for backward compatibility we should support both. You can check if next() returns a coroutine and handle accordingly.', '2025-09-20 15:30:00', '2025-09-20 15:30:00', '{"heart": 2}'),
(59876014, 2, 4, 'Makes sense! I''ll have a draft PR ready by tomorrow.', '2025-09-20 16:00:00', '2025-09-20 16:00:00', '{}'),
(59876015, 2, 1, 'Awesome! Looking forward to reviewing it. Don''t worry about making it perfect - we can iterate together.', '2025-09-20 16:15:00', '2025-09-20 16:15:00', '{"heart": 4}'),
(59876016, 2, 2, 'This is a much-needed feature. Thanks for working on it @jamie_oss!', '2025-09-22 10:00:00', '2025-09-22 10:00:00', '{"+1": 6}'),
(59876017, 2, 3, 'Keep in mind we''ll need extensive tests for edge cases with async/await.', '2025-09-23 11:30:00', '2025-09-23 11:30:00', '{"+1": 3}'),
(59876018, 2, 4, 'Good point Morgan! I''m including tests for timeout scenarios, error propagation, and concurrent execution.', '2025-09-24 09:00:00', '2025-09-24 09:00:00', '{"rocket": 2}'),
(59876019, 2, 1, 'That''s the spirit! Thorough testing is what makes good software great.', '2025-09-24 10:00:00', '2025-09-24 10:00:00', '{"heart": 3}'),
(59876020, 2, 5, 'Really excited about this feature! Will make our API so much faster.', '2025-09-28 13:00:00', '2025-09-28 13:00:00', '{"+1": 4}'),
(59876021, 2, 1, '@jamie_oss How''s the PR coming along? Any blockers?', '2025-10-02 10:00:00', '2025-10-02 10:00:00', '{}'),

-- Documentation issue showing quick triage
(59876022, 3, 1, 'You''re absolutely right! I''ll improve the configuration docs with real-world examples.', '2025-09-22 10:00:00', '2025-09-22 10:00:00', '{"+1": 4}'),
(59876023, 3, 5, 'Would be great to have examples for common use cases like API rate limiting and caching.', '2025-09-22 14:00:00', '2025-09-22 14:00:00', '{"heart": 2}'),
(59876024, 3, 1, 'Good suggestions! Adding those examples now. PR #102 incoming.', '2025-09-23 09:00:00', '2025-09-23 09:00:00', '{"rocket": 2}'),
(59876025, 3, 4, 'The new docs look much better! Thanks @sarah_maintainer', '2025-09-25 16:00:00', '2025-09-25 16:00:00', '{"heart": 3}'),

-- Security issue showing urgent handling
(59876026, 4, 1, 'Thanks for reporting this responsibly! I''m investigating immediately. For others: please avoid posting details publicly until we have a patch.', '2025-09-25 16:30:00', '2025-09-25 16:30:00', '{"heart": 5, "eyes": 3}'),
(59876027, 4, 3, 'I can help review the security patch if needed.', '2025-09-25 17:00:00', '2025-09-25 17:00:00', '{"+1": 4}'),
(59876028, 4, 1, 'Thanks Morgan! I''ll have a patch ready in a few hours. Will tag you for review.', '2025-09-25 17:15:00', '2025-09-25 17:15:00', '{}'),
(59876029, 4, 1, 'Patch is ready in PR #103. @morgan_code can you review ASAP?', '2025-09-25 18:30:00', '2025-09-25 18:30:00', '{}'),
(59876030, 4, 3, 'On it!', '2025-09-25 18:45:00', '2025-09-25 18:45:00', '{}'),
(59876031, 4, 2, 'Should we notify users to upgrade immediately?', '2025-09-26 09:00:00', '2025-09-26 09:00:00', '{}'),
(59876032, 4, 1, 'Yes, preparing security advisory now. Will publish once PR merges.', '2025-09-26 09:30:00', '2025-09-26 09:30:00', '{}'),
(59876033, 4, 1, 'Security fix is now merged and released as v3.2.1. Please upgrade immediately! Details in SECURITY.md', '2025-09-27 10:20:00', '2025-09-27 10:20:00', '{"rocket": 8, "heart": 6}'),
(59876034, 4, 3, 'Great quick turnaround on the fix! Well done team.', '2025-09-27 11:00:00', '2025-09-27 11:00:00', '{"+1": 7}'),
(59876035, 4, 5, 'Upgraded successfully. Thanks for the fast response! 🙏', '2025-09-27 14:00:00', '2025-09-27 14:00:00', '{"heart": 4}'),

-- Performance issue showing burnout patterns (short, frustrated responses)
(59876036, 5, 1, 'Need more details. What exactly is slow? Which endpoints?', '2025-09-28 12:00:00', '2025-09-28 12:00:00', '{}'),
(59876037, 5, 2, 'All endpoints seem affected. Response times went from ~50ms to ~300ms after upgrading from v3.1 to v3.2', '2025-09-28 14:30:00', '2025-09-28 14:30:00', '{}'),
(59876038, 5, 1, 'Can''t reproduce. Need your configuration.', '2025-09-29 09:00:00', '2025-09-29 09:00:00', '{}'),
(59876039, 5, 3, '@sarah_maintainer I can help investigate this. @alex_dev can you share your config and a minimal repro?', '2025-09-29 10:30:00', '2025-09-29 10:30:00', '{"heart": 4}'),
(59876040, 5, 2, 'Sure! Here''s my config: [config details]. I can create a minimal repo to reproduce.', '2025-09-29 12:00:00', '2025-09-29 12:00:00', '{}'),
(59876041, 5, 3, 'Thanks! I''ll take a look. Might be related to the caching changes in v3.2.', '2025-09-30 09:00:00', '2025-09-30 09:00:00', '{}'),
(59876042, 5, 2, 'Created reproduction repo: github.com/alex_dev/framework-perf-issue', '2025-09-30 14:00:00', '2025-09-30 14:00:00', '{"+1": 3}'),
(59876043, 5, 3, 'Confirmed! The issue is in the new cache key generation. Working on a fix.', '2025-10-01 11:00:00', '2025-10-01 11:00:00', '{"rocket": 5}'),
(59876044, 5, 1, 'Thanks Morgan for jumping in. I''ve been swamped this week.', '2025-10-01 14:00:00', '2025-10-01 14:00:00', '{"heart": 3}'),
(59876045, 5, 3, 'No worries! PR #105 has the optimization. @alex_dev can you test?', '2025-10-02 15:00:00', '2025-10-02 15:00:00', '{}'),
(59876046, 5, 2, 'Testing now...', '2025-10-02 16:30:00', '2025-10-02 16:30:00', '{}'),
(59876047, 5, 2, 'Performance is back to normal! Response times even better than v3.1 now. Great work! 🎉', '2025-10-03 09:00:00', '2025-10-03 09:00:00', '{"rocket": 6, "heart": 4}'),

-- More issues showing various maintainer activities...
(59876048, 6, 5, 'TypeScript support would be amazing! Our team would love this.', '2025-10-01 11:00:00', '2025-10-01 11:00:00', '{"+1": 8}'),
(59876049, 6, 1, 'Agreed! This has been requested multiple times. I''ll prioritize this.', '2025-10-01 14:00:00', '2025-10-01 14:00:00', '{"heart": 6}'),
(59876050, 6, 5, 'I can work on this if you''d like! I have experience with TS definitions.', '2025-10-01 15:30:00', '2025-10-01 15:30:00', '{}'),
(59876051, 6, 1, 'That would be fantastic! Let me know if you need help with our internal types.', '2025-10-01 16:00:00', '2025-10-01 16:00:00', '{"heart": 4}'),
(59876052, 6, 5, 'Started working on PR #106. Should have something ready this week!', '2025-10-01 17:00:00', '2025-10-01 17:00:00', '{"rocket": 5}'),

(59876053, 7, 4, 'Better error handling would really improve the developer experience.', '2025-10-02 14:00:00', '2025-10-02 14:00:00', '{"+1": 5}'),
(59876054, 7, 2, 'I could take a look at this. Should be straightforward.', '2025-10-03 10:00:00', '2025-10-03 10:00:00', '{}'),
(59876055, 7, 1, 'Go for it @alex_dev! Check out how we handle errors in the auth module for consistency.', '2025-10-03 11:00:00', '2025-10-03 11:00:00', '{"heart": 2}');

-- Insert more issue comments for data-processor repository
INSERT INTO issue_comments (github_id, issue_id, commenter_id, body, created_at, updated_at, reactions) VALUES
(59876056, 8, 2, 'Thanks for the bug report! Windows threading is tricky. I''ll investigate.', '2025-09-12 15:00:00', '2025-09-12 15:00:00', '{"+1": 3}'),
(59876057, 8, 5, 'I can provide more debug logs if needed.', '2025-09-13 09:00:00', '2025-09-13 09:00:00', '{}'),
(59876058, 8, 2, 'Found the issue - it''s related to how Windows handles thread pools differently. Fix coming in PR #50.', '2025-09-14 11:00:00', '2025-09-14 11:00:00', '{"rocket": 4}'),
(59876059, 8, 4, 'Good catch! Should we add platform-specific tests?', '2025-09-14 14:00:00', '2025-09-14 14:00:00', '{"+1": 2}'),
(59876060, 8, 2, 'Absolutely. I''m adding Windows CI in the same PR.', '2025-09-14 15:00:00', '2025-09-14 15:00:00', '{"heart": 3}'),

(59876061, 9, 2, 'CSV export has been requested several times. I''ll add this to the roadmap.', '2025-09-20 11:00:00', '2025-09-20 11:00:00', '{"+1": 6}'),
(59876062, 9, 3, 'Happy to contribute if you want. I''ve implemented CSV export in other projects.', '2025-09-21 09:00:00', '2025-09-21 09:00:00', '{}'),
(59876063, 9, 2, 'That''d be great Morgan! Let''s chat about the API design first.', '2025-09-21 10:00:00', '2025-09-21 10:00:00', '{"heart": 2}'),
(59876064, 9, 1, 'Make sure to handle edge cases like special characters and huge files.', '2025-09-22 14:00:00', '2025-09-22 14:00:00', '{"+1": 4}'),

(59876065, 11, 2, 'This is a known limitation with large datasets. Working on memory optimization in PR #53.', '2025-09-29 17:00:00', '2025-09-29 17:00:00', '{}'),
(59876066, 11, 1, 'Have you considered streaming instead of loading everything into memory?', '2025-09-30 10:00:00', '2025-09-30 10:00:00', '{"+1": 5}'),
(59876067, 11, 2, 'That''s exactly what I''m implementing! Streaming with chunked processing.', '2025-09-30 11:30:00', '2025-09-30 11:30:00', '{"rocket": 6}'),
(59876068, 11, 3, 'Can''t wait to test this! Our production workloads need this badly.', '2025-10-01 09:00:00', '2025-10-01 09:00:00', '{}');

-- Insert Issue Timeline Events (showing triage activity)
INSERT INTO issue_timeline_events (github_id, issue_id, event_type, actor_id, created_at, label_name, assignee_id) VALUES
-- Issue #1 timeline
('evt_001', 1, 'labeled', 1, '2025-09-15 10:35:00', 'bug', NULL),
('evt_002', 1, 'labeled', 1, '2025-09-15 10:35:00', 'high-priority', NULL),
('evt_003', 1, 'assigned', 1, '2025-09-15 10:40:00', NULL, 1),
('evt_004', 1, 'labeled', 1, '2025-09-16 09:05:00', 'performance', NULL),
('evt_005', 1, 'closed', 1, '2025-09-20 16:45:00', NULL, NULL),

-- Issue #2 timeline
('evt_006', 2, 'labeled', 1, '2025-09-18 14:25:00', 'enhancement', NULL),
('evt_007', 2, 'labeled', 1, '2025-09-18 14:25:00', 'good-first-issue', NULL),
('evt_008', 2, 'assigned', 1, '2025-09-19 09:05:00', NULL, 2),

-- Issue #3 timeline
('evt_009', 3, 'labeled', 1, '2025-09-22 09:05:00', 'documentation', NULL),
('evt_010', 3, 'assigned', 1, '2025-09-22 10:05:00', NULL, 1),
('evt_011', 3, 'closed', 1, '2025-09-25 15:30:00', NULL, NULL),

-- Issue #4 timeline (security - fast triage)
('evt_012', 4, 'labeled', 1, '2025-09-25 16:05:00', 'security', NULL),
('evt_013', 4, 'labeled', 1, '2025-09-25 16:05:00', 'critical', NULL),
('evt_014', 4, 'assigned', 1, '2025-09-25 16:10:00', NULL, 1),
('evt_015', 4, 'closed', 1, '2025-09-27 10:20:00', NULL, NULL),

-- Issue #5 timeline
('evt_016', 5, 'labeled', 1, '2025-09-28 12:05:00', 'bug', NULL),
('evt_017', 5, 'labeled', 1, '2025-09-28 12:05:00', 'performance', NULL),
('evt_018', 5, 'assigned', 3, '2025-09-29 10:35:00', NULL, 1),
('evt_019', 5, 'labeled', 3, '2025-09-30 09:05:00', 'needs-investigation', NULL),

-- Issue #6 timeline
('evt_020', 6, 'labeled', 1, '2025-10-01 10:20:00', 'enhancement', NULL),
('evt_021', 6, 'labeled', 1, '2025-10-01 10:20:00', 'typescript', NULL),
('evt_022', 6, 'assigned', 1, '2025-10-01 16:05:00', NULL, 2),

-- Issue #7 timeline
('evt_023', 7, 'labeled', 1, '2025-10-02 13:35:00', 'enhancement', NULL),
('evt_024', 7, 'labeled', 2, '2025-10-03 10:05:00', 'dx-improvement', NULL),

-- Data processor issues timeline
('evt_025', 8, 'labeled', 2, '2025-09-12 14:05:00', 'bug', NULL),
('evt_026', 8, 'labeled', 2, '2025-09-12 14:05:00', 'platform-specific', NULL),
('evt_027', 8, 'assigned', 2, '2025-09-12 15:05:00', NULL, 2),
('evt_028', 8, 'closed', 2, '2025-09-18 11:30:00', NULL, NULL),

('evt_029', 9, 'labeled', 2, '2025-09-20 10:35:00', 'enhancement', NULL),
('evt_030', 9, 'labeled', 2, '2025-09-20 10:35:00', 'user-request', NULL),
('evt_031', 9, 'assigned', 2, '2025-09-21 10:05:00', NULL, 2),

('evt_032', 10, 'labeled', 2, '2025-09-25 09:20:00', 'documentation', NULL),
('evt_033', 10, 'labeled', 2, '2025-09-25 09:20:00', 'benchmarks', NULL),

('evt_034', 11, 'labeled', 2, '2025-09-29 16:25:00', 'bug', NULL),
('evt_035', 11, 'labeled', 2, '2025-09-29 16:25:00', 'performance', NULL),
('evt_036', 11, 'labeled', 2, '2025-09-29 16:25:00', 'high-priority', NULL),
('evt_037', 11, 'assigned', 2, '2025-09-29 17:05:00', NULL, 2),

('evt_038', 12, 'labeled', 2, '2025-10-01 11:05:00', 'bug', NULL),
('evt_039', 12, 'labeled', 2, '2025-10-01 11:05:00', 'installation', NULL),
('evt_040', 12, 'assigned', 2, '2025-10-01 15:25:00', NULL, 3),
('evt_041', 12, 'closed', 2, '2025-10-03 13:45:00', NULL, NULL),

-- CLI toolbox issues timeline
('evt_042', 13, 'labeled', 3, '2025-09-14 15:35:00', 'bug', NULL),
('evt_043', 13, 'labeled', 3, '2025-09-14 15:35:00', 'cli', NULL),
('evt_044', 13, 'assigned', 3, '2025-09-14 15:40:00', NULL, 3),
('evt_045', 13, 'closed', 3, '2025-09-22 10:00:00', NULL, NULL),

('evt_046', 14, 'labeled', 3, '2025-09-19 13:50:00', 'enhancement', NULL),
('evt_047', 14, 'labeled', 3, '2025-09-19 13:50:00', 'ui', NULL),
('evt_048', 14, 'assigned', 3, '2025-09-20 15:20:00', NULL, 3),

('evt_049', 15, 'labeled', 3, '2025-09-24 10:05:00', 'enhancement', NULL),
('evt_050', 15, 'labeled', 3, '2025-09-24 10:05:00', 'dx-improvement', NULL),

('evt_051', 16, 'labeled', 3, '2025-09-27 12:35:00', 'enhancement', NULL),
('evt_052', 16, 'labeled', 3, '2025-09-27 12:35:00', 'validation', NULL),
('evt_053', 16, 'assigned', 3, '2025-09-28 14:25:00', NULL, 3),

('evt_054', 17, 'labeled', 3, '2025-09-30 09:25:00', 'documentation', NULL),
('evt_055', 17, 'labeled', 3, '2025-09-30 09:25:00', 'release', NULL),
('evt_056', 17, 'assigned', 3, '2025-10-01 10:35:00', NULL, 3),

('evt_057', 18, 'labeled', 3, '2025-10-01 14:20:00', 'discussion', NULL),
('evt_058', 18, 'labeled', 3, '2025-10-01 14:20:00', 'architecture', NULL),

('evt_059', 19, 'labeled', 3, '2025-10-02 11:05:00', 'enhancement', NULL),
('evt_060', 19, 'labeled', 3, '2025-10-02 11:05:00', 'performance', NULL),
('evt_061', 19, 'assigned', 3, '2025-10-02 13:20:00', NULL, 3),

('evt_062', 20, 'labeled', 3, '2025-10-03 16:50:00', 'ci', NULL),
('evt_063', 20, 'labeled', 3, '2025-10-03 16:50:00', 'testing', NULL);

-- Insert GitHub Discussions
INSERT INTO discussions (github_id, repository_id, number, title, body, category, created_by, answered_by, is_answered, created_at, updated_at, comments_count, upvotes) VALUES
(69876001, 1, 1, 'Best practices for production deployment', 'What are the recommended practices for deploying this framework in production? Looking for advice on scaling, monitoring, and error handling...', 'Q&A', 5, 1, TRUE, '2025-09-10 14:00:00', '2025-09-15 16:30:00', 8, 15),
(69876002, 1, 2, 'Proposal: Plugin system for v4.0', 'I''d like to propose a plugin system for the next major release. This would allow the community to extend functionality without modifying core...', 'Ideas', 3, NULL, FALSE, '2025-09-18 11:00:00', '2025-10-03 14:45:00', 12, 24),
(69876003, 2, 1, 'Performance optimization strategies', 'Share your tips and tricks for optimizing data processing performance. What techniques have worked well for you?', 'Show and tell', 2, 2, TRUE, '2025-09-22 10:00:00', '2025-09-28 15:00:00', 6, 11),
(69876004, 3, 1, 'Building custom commands tutorial', 'Tutorial on building custom commands for the CLI. Walking through a complete example from start to finish...', 'Show and tell', 3, NULL, FALSE, '2025-09-25 13:00:00', '2025-10-02 11:30:00', 5, 9);

-- Insert Discussion Comments
INSERT INTO discussion_comments (github_id, discussion_id, commenter_id, parent_comment_id, body, created_at, updated_at, upvotes, is_answer) VALUES
-- Discussion #1 comments (deployment best practices - showing mentorship)
(79876001, 1, 1, NULL, 'Great question! Here''s what I recommend for production deployment:\n\n1. **Scaling**: Use a load balancer and run multiple instances\n2. **Monitoring**: Integrate with Prometheus and Grafana\n3. **Error handling**: Configure centralized logging with Sentry or similar\n\nI can provide more specific examples if you need them!', '2025-09-11 09:00:00', '2025-09-11 09:00:00', 12, TRUE),
(79876002, 1, 5, 79876001, 'Thanks so much! Do you have any config examples for Prometheus?', '2025-09-11 11:00:00', '2025-09-11 11:00:00', 3, FALSE),
(79876003, 1, 1, 79876002, 'Sure! Here''s a sample prometheus.yml config: [detailed config example]. Also check out our docs/monitoring/prometheus.md for more details.', '2025-09-11 14:00:00', '2025-09-11 14:00:00', 8, FALSE),
(79876004, 1, 2, NULL, 'Also recommend setting up health check endpoints for your load balancer. We use /health and /ready in our setup.', '2025-09-12 10:00:00', '2025-09-12 10:00:00', 6, FALSE),
(79876005, 1, 5, 79876004, 'Good point! Are those endpoints built into the framework?', '2025-09-12 14:00:00', '2025-09-12 14:00:00', 2, FALSE),
(79876006, 1, 2, 79876005, 'They''re available through the middleware. Check out the health check middleware in the docs.', '2025-09-13 09:00:00', '2025-09-13 09:00:00', 4, FALSE),
(79876007, 1, 4, NULL, 'Don''t forget about database connection pooling! That''s critical for scaling.', '2025-09-14 11:00:00', '2025-09-14 11:00:00', 7, FALSE),
(79876008, 1, 5, NULL, 'Thank you all! This is incredibly helpful. I''ll implement these suggestions.', '2025-09-15 16:30:00', '2025-09-15 16:30:00', 9, FALSE),

-- Discussion #2 comments (plugin system proposal - showing architecture discussion)
(79876009, 2, 1, NULL, 'Interesting proposal! A plugin system would definitely add flexibility. A few questions:\n- How would you handle plugin dependencies?\n- What about plugin security/sandboxing?\n- Should we support both sync and async plugins?', '2025-09-19 10:00:00', '2025-09-19 10:00:00', 15, FALSE),
(79876010, 2, 3, 79876009, 'Good questions! For dependencies, I''m thinking each plugin would declare its own deps similar to how npm packages work. For security, maybe we could use a capability-based system?', '2025-09-20 14:00:00', '2025-09-20 14:00:00', 8, FALSE),
(79876011, 2, 2, NULL, 'Have you looked at how VSCode handles extensions? Their approach might be worth studying.', '2025-09-21 11:00:00', '2025-09-21 11:00:00', 11, FALSE),
(79876012, 2, 3, 79876011, 'Great reference! VSCode''s extension API is excellent. I''ll analyze their approach.', '2025-09-22 09:00:00', '2025-09-22 09:00:00', 7, FALSE),
(79876013, 2, 4, NULL, 'Plugin discoverability will be important too. Should we have a registry?', '2025-09-24 10:00:00', '2025-09-24 10:00:00', 9, FALSE),
(79876014, 2, 3, 79876013, 'Absolutely! A community registry would make plugins easy to find and install.', '2025-09-25 15:00:00', '2025-09-25 15:00:00', 6, FALSE),
(79876015, 2, 1, NULL, 'This is getting interesting! Want to schedule a call to discuss the architecture in detail? We could use GitHub Discussions video.', '2025-09-28 11:00:00', '2025-09-28 11:00:00', 12, FALSE),
(79876016, 2, 3, 79876015, 'That would be great! I''ll send you my availability.', '2025-09-28 14:00:00', '2025-09-28 14:00:00', 5, FALSE),
(79876017, 2, 2, NULL, 'I''d love to join that call if possible. Plugin systems are my specialty.', '2025-09-29 10:00:00', '2025-09-29 10:00:00', 8, FALSE),
(79876018, 2, 5, NULL, 'This would be an amazing feature! Looking forward to seeing it in v4.0.', '2025-10-01 13:00:00', '2025-10-01 13:00:00', 10, FALSE),
(79876019, 2, 1, NULL, 'Let''s create a design document to formalize the proposal. @morgan_code want to collaborate on it?', '2025-10-02 16:00:00', '2025-10-02 16:00:00', 9, FALSE),
(79876020, 2, 3, 79876019, 'Definitely! I''ll start a draft in a new discussion.', '2025-10-03 14:45:00', '2025-10-03 14:45:00', 7, FALSE),

-- Discussion #3 comments (performance optimization)
(79876021, 3, 2, NULL, 'Here are some strategies that worked well for our use case:\n1. Batch processing instead of one-by-one\n2. Parallel execution where possible\n3. Caching frequently accessed data\n4. Using memory-mapped files for huge datasets', '2025-09-23 11:00:00', '2025-09-23 11:00:00', 9, TRUE),
(79876022, 3, 3, 79876021, 'Memory-mapped files are a game changer! Reduced our processing time by 60%.', '2025-09-24 10:00:00', '2025-09-24 10:00:00', 6, FALSE),
(79876023, 3, 1, NULL, 'Don''t forget about profiling! Use cargo-flamegraph to find bottlenecks.', '2025-09-25 14:00:00', '2025-09-25 14:00:00', 7, FALSE),
(79876024, 3, 4, NULL, 'For parallel processing, tokio is excellent if you''re using async Rust.', '2025-09-26 09:00:00', '2025-09-26 09:00:00', 5, FALSE),
(79876025, 3, 5, NULL, 'These tips are super helpful! Thank you everyone!', '2025-09-28 15:00:00', '2025-09-28 15:00:00', 4, FALSE),

-- Discussion #4 comments (custom commands tutorial)
(79876026, 4, 4, NULL, 'Great tutorial! One suggestion: add error handling examples.', '2025-09-26 14:00:00', '2025-09-26 14:00:00', 5, FALSE),
(79876027, 4, 3, 79876026, 'Good point! I''ll add a section on error handling and user-friendly error messages.', '2025-09-27 10:00:00', '2025-09-27 10:00:00', 4, FALSE),
(79876028, 4, 5, NULL, 'This is exactly what I needed! Thanks for sharing.', '2025-09-29 11:00:00', '2025-09-29 11:00:00', 6, FALSE),
(79876029, 4, 2, NULL, 'Nice work! Consider adding integration tests examples too.', '2025-10-01 10:00:00', '2025-10-01 10:00:00', 4, FALSE),
(79876030, 4, 3, 79876029, 'Will do! I''ll update the tutorial with testing examples.', '2025-10-02 11:30:00', '2025-10-02 11:30:00', 3, FALSE);

-- Insert Commits (documentation and code changes)
INSERT INTO commits (sha, repository_id, author_id, committer_id, message, created_at, additions, deletions, changed_files, is_docs_related) VALUES
-- Documentation commits (showing docs maintenance)
('doc001abc', 1, 1, 1, 'docs: Update configuration examples\n\nAdds comprehensive examples for common use cases including rate limiting and caching.', '2025-09-23 14:30:00', 156, 34, 3, TRUE),
('doc002def', 1, 1, 1, 'docs: Add production deployment guide', '2025-09-12 16:00:00', 234, 12, 2, TRUE),
('doc003ghi', 2, 2, 2, 'docs: Add benchmark comparisons', '2025-09-27 11:00:00', 189, 23, 4, TRUE),
('doc004jkl', 3, 3, 3, 'docs: Update v2.0 documentation', '2025-10-02 15:00:00', 567, 234, 15, TRUE),
('doc005mno', 1, 4, 4, 'docs: Fix typos in async middleware guide', '2025-09-26 10:00:00', 12, 8, 1, TRUE),

-- Code commits
('code001pqr', 1, 5, 1, 'fix: Close WebSocket connections properly', '2025-09-18 14:00:00', 45, 12, 2, FALSE),
('code002stu', 1, 3, 1, 'security: Patch auth vulnerability', '2025-09-26 17:00:00', 78, 45, 4, FALSE),
('code003vwx', 2, 4, 2, 'fix: Resolve Windows threading issue', '2025-09-15 16:00:00', 123, 56, 3, FALSE),
('code004yz1', 3, 5, 3, 'fix: Update shell completion scripts', '2025-09-20 13:00:00', 67, 23, 3, FALSE),
('code005abc', 1, 2, 2, 'chore: Update dependencies to latest versions', '2025-10-03 16:00:00', 23, 23, 1, FALSE);

-- =====================================================
-- SENTIMENT ANALYSIS DATA
-- =====================================================

-- Insert Sentiment Analysis (showing various tones over time)
INSERT INTO sentiment_analysis (maintainer_id, content_type, content_id, sentiment_score, tone, analysis_date, text_analyzed) VALUES
-- Sarah's sentiment pattern (showing burnout progression)
(1, 'pr_review', 1, 0.8500, 'supportive', '2025-09-19 14:30:00', 'Great fix! This properly addresses the memory leak.'),
(1, 'pr_review', 4, 0.7200, 'constructive', '2025-09-23 10:30:00', 'The implementation looks good but we need comprehensive tests.'),
(1, 'pr_review', 8, 0.8200, 'supportive', '2025-09-24 16:00:00', 'Excellent documentation improvements!'),
(1, 'pr_review', 10, 0.9000, 'supportive', '2025-09-26 18:00:00', 'Critical security fix. Thanks for the quick turnaround.'),
(1, 'pr_review', 13, 0.3200, 'harsh', '2025-10-01 14:00:00', 'This caching implementation has race conditions. Did you even test this?'),
(1, 'pr_review', 13, 0.2800, 'harsh', '2025-10-01 14:05:00', 'You''re missing mutex locks here. This is basic concurrency 101.'),
(1, 'pr_review', 17, 0.6500, 'constructive', '2025-10-02 16:30:00', 'Good start on TypeScript definitions but several types are incomplete.'),
(1, 'issue_comment', 59876036, 0.3500, 'neutral', '2025-09-28 12:00:00', 'Need more details. What exactly is slow?'),
(1, 'issue_comment', 59876038, 0.3000, 'neutral', '2025-09-29 09:00:00', 'Can''t reproduce. Need your configuration.'),

-- Alex's sentiment (consistently constructive)
(2, 'pr_review', 2, 0.6800, 'constructive', '2025-09-18 11:00:00', 'Have you tested this with high concurrency?'),
(2, 'pr_review', 23, 0.8800, 'supportive', '2025-09-16 15:30:00', 'Excellent fix for the Windows issue.'),
(2, 'pr_review', 26, 0.7500, 'constructive', '2025-09-26 11:45:00', 'CSV implementation needs better error handling.'),
(2, 'pr_review', 32, 0.8000, 'constructive', '2025-10-02 11:30:00', 'Memory optimization looks promising but I''m seeing potential issues.'),
(2, 'issue_comment', 59876023, 0.7800, 'supportive', '2025-09-22 14:00:00', 'Would be great to have examples for common use cases.'),

-- Morgan's sentiment (helpful and detailed)
(3, 'pr_review', 3, 0.7500, 'supportive', '2025-09-19 16:15:00', 'LGTM! Nice work on the tests.'),
(3, 'pr_review', 25, 0.7200, 'supportive', '2025-09-17 10:00:00', 'Windows threading finally works! Great job.'),
(3, 'pr_review', 39, 0.8500, 'supportive', '2025-09-20 14:00:00', 'Shell completion works perfectly now.'),
(3, 'pr_review', 41, 0.7800, 'constructive', '2025-09-28 11:00:00', 'Color customization is a great feature but the config format is inconsistent.'),
(3, 'pr_review', 44, 0.8200, 'supportive', '2025-09-29 16:30:00', 'Much better error messages! This will really help users.'),
(3, 'pr_review', 51, 0.8500, 'supportive', '2025-10-02 18:00:00', 'For the plugin system, I''d recommend looking at how VSCode handles extensions.'),

-- Jamie's sentiment (learning and positive)
(4, 'pr_review', 9, 0.6500, 'supportive', '2025-09-25 10:30:00', 'Docs look great!'),
(4, 'pr_review', 31, 0.6200, 'constructive', '2025-09-29 10:00:00', 'Looking good so far. Will do a full review once tests are added.'),
(4, 'issue_comment', 59876010, 0.8500, 'supportive', '2025-09-18 16:00:00', 'I''d love to take this on! Where should I start?'),
(4, 'issue_comment', 59876018, 0.7800, 'supportive', '2025-09-24 09:00:00', 'I''m including tests for timeout scenarios, error propagation, and concurrent execution.'),

-- Riley's sentiment (enthusiastic learner)
(5, 'issue_comment', 59876007, 0.9200, 'supportive', '2025-09-19 17:00:00', 'Tested the fix - working perfectly! Memory usage is now stable over 48 hours.'),
(5, 'issue_comment', 59876048, 0.8800, 'supportive', '2025-10-01 11:00:00', 'TypeScript support would be amazing! Our team would love this.');

-- =====================================================
-- BURNOUT RISK SCORES
-- =====================================================

-- Insert Burnout Risk Scores (showing Sarah's increasing burnout over time)
INSERT INTO burnout_risk_scores (maintainer_id, calculation_date, overall_risk_score, response_time_score, activity_level_score, sentiment_score, isolation_score, workload_score, community_support_score) VALUES
-- Sarah's burnout progression
(1, '2025-09-15 00:00:00', 25.00, 15.00, 20.00, 85.00, 30.00, 35.00, 80.00),
(1, '2025-09-22 00:00:00', 32.00, 25.00, 28.00, 75.00, 35.00, 45.00, 75.00),
(1, '2025-09-29 00:00:00', 48.00, 40.00, 38.00, 58.00, 48.00, 58.00, 65.00),
(1, '2025-10-04 00:00:00', 62.00, 55.00, 52.00, 42.00, 58.00, 72.00, 55.00),

-- Alex's stable scores (healthy maintainer)
(2, '2025-09-15 00:00:00', 18.00, 12.00, 15.00, 88.00, 20.00, 25.00, 85.00),
(2, '2025-09-22 00:00:00', 20.00, 15.00, 18.00, 86.00, 22.00, 28.00, 82.00),
(2, '2025-09-29 00:00:00', 19.00, 14.00, 17.00, 87.00, 21.00, 26.00, 84.00),
(2, '2025-10-04 00:00:00', 21.00, 16.00, 19.00, 85.00, 23.00, 29.00, 83.00),

-- Morgan's excellent scores (thriving maintainer)
(3, '2025-09-15 00:00:00', 12.00, 8.00, 10.00, 92.00, 15.00, 18.00, 90.00),
(3, '2025-09-22 00:00:00', 14.00, 10.00, 12.00, 90.00, 16.00, 20.00, 88.00),
(3, '2025-09-29 00:00:00', 13.00, 9.00, 11.00, 91.00, 15.00, 19.00, 89.00),
(3, '2025-10-04 00:00:00', 15.00, 11.00, 13.00, 89.00, 17.00, 21.00, 87.00),

-- Jamie's improving scores (growing contributor)
(4, '2025-09-15 00:00:00', 35.00, 30.00, 32.00, 75.00, 40.00, 38.00, 70.00),
(4, '2025-09-22 00:00:00', 28.00, 24.00, 26.00, 80.00, 32.00, 30.00, 78.00),
(4, '2025-09-29 00:00:00', 24.00, 20.00, 22.00, 84.00, 28.00, 26.00, 82.00),
(4, '2025-10-04 00:00:00', 22.00, 18.00, 20.00, 86.00, 25.00, 24.00, 84.00),

-- Riley's enthusiastic but inexperienced scores
(5, '2025-09-15 00:00:00', 42.00, 45.00, 40.00, 88.00, 48.00, 35.00, 72.00),
(5, '2025-09-22 00:00:00', 38.00, 40.00, 36.00, 89.00, 42.00, 32.00, 75.00),
(5, '2025-09-29 00:00:00', 35.00, 38.00, 34.00, 90.00, 38.00, 30.00, 78.00),
(5, '2025-10-04 00:00:00', 33.00, 35.00, 32.00, 91.00, 35.00, 28.00, 80.00);

-- =====================================================
-- ANALYSIS SUMMARY
-- =====================================================

-- Create summary view for maintainer activity scores
CREATE OR REPLACE VIEW maintainer_activity_summary AS
SELECT 
    m.id,
    m.username,
    m.name,
    -- Review activity (30%)
    COUNT(DISTINCT pr.id) * 3.0 AS review_count_score,
    AVG(pr.review_depth_score) AS avg_review_depth,
    -- Issue triage (20%)
    COUNT(DISTINCT ite.id) * 2.0 AS triage_count_score,
    -- Community engagement (15%)
    COUNT(DISTINCT ic.id) + COUNT(DISTINCT dc.id) AS engagement_count,
    -- Documentation (10%)
    COUNT(DISTINCT CASE WHEN c.is_docs_related THEN c.id END) AS docs_contribution_count,
    -- Mentorship indicators (25%)
    COUNT(DISTINCT prc.id) FILTER (WHERE LENGTH(prc.body) > 200) AS detailed_review_comments,
    -- Overall activity
    COUNT(DISTINCT pr.id) + COUNT(DISTINCT ic.id) + COUNT(DISTINCT ite.id) AS total_activities
FROM maintainers m
LEFT JOIN pr_reviews pr ON pr.reviewer_id = m.id
LEFT JOIN issue_timeline_events ite ON ite.actor_id = m.id
LEFT JOIN issue_comments ic ON ic.commenter_id = m.id
LEFT JOIN discussion_comments dc ON dc.commenter_id = m.id
LEFT JOIN commits c ON c.author_id = m.id
LEFT JOIN pr_review_comments prc ON prc.commenter_id = m.id
WHERE m.is_active = TRUE
  AND pr.submitted_at >= NOW() - INTERVAL '30 days'
GROUP BY m.id, m.username, m.name;

-- Create indexes for performance
CREATE INDEX idx_pr_reviews_reviewer ON pr_reviews(reviewer_id);
CREATE INDEX idx_pr_reviews_submitted ON pr_reviews(submitted_at);
CREATE INDEX idx_issue_comments_commenter ON issue_comments(commenter_id);
CREATE INDEX idx_issue_comments_created ON issue_comments(created_at);
CREATE INDEX idx_timeline_events_actor ON issue_timeline_events(actor_id);
CREATE INDEX idx_timeline_events_created ON issue_timeline_events(created_at);
CREATE INDEX idx_sentiment_maintainer ON sentiment_analysis(maintainer_id);
CREATE INDEX idx_sentiment_date ON sentiment_analysis(analysis_date);
CREATE INDEX idx_burnout_maintainer ON burnout_risk_scores(maintainer_id);
CREATE INDEX idx_burnout_date ON burnout_risk_scores(calculation_date);

-- Analysis queries for testing
COMMENT ON TABLE maintainers IS 'Core maintainer/contributor profiles';
COMMENT ON TABLE pr_reviews IS 'Pull request reviews with depth scores for invisible labor tracking';
COMMENT ON TABLE issue_timeline_events IS 'Issue triage activities showing maintenance work';
COMMENT ON TABLE sentiment_analysis IS 'AI-powered sentiment analysis of maintainer interactions';
COMMENT ON TABLE burnout_risk_scores IS 'Burnout risk indicators calculated from multiple factors';

-- =====================================================
-- END OF DUMMY DATA
-- =====================================================
