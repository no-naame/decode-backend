## ✅ *AVAILABLE FROM GITHUB API* (Direct Data)

### 1. *maintainers* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ username ⁠, ⁠ name ⁠, ⁠ email ⁠, ⁠ bio ⁠, ⁠ company ⁠, ⁠ location ⁠
•⁠  ⁠⁠ public_repos ⁠, ⁠ followers ⁠, ⁠ following ⁠, ⁠ created_at ⁠, ⁠ updated_at ⁠
•⁠  ⁠⁠ avatar_url ⁠, ⁠ html_url ⁠, ⁠ blog ⁠, ⁠ hireable ⁠

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ is_active ⁠ - You'll need to determine based on recent activity
•⁠  ⁠⁠ last_activity_date ⁠ - Calculate from recent commits/PRs/issues

### 2. *repositories* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ name ⁠, ⁠ description ⁠, ⁠ language ⁠, ⁠ html_url ⁠
•⁠  ⁠⁠ stars ⁠, ⁠ forks ⁠, ⁠ watchers ⁠, ⁠ open_issues ⁠, ⁠ created_at ⁠, ⁠ updated_at ⁠
•⁠  ⁠⁠ default_branch ⁠, ⁠ archived ⁠, ⁠ disabled ⁠, ⁠ private ⁠

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ owner_id ⁠ - Map to your maintainers table
•⁠  ⁠⁠ is_active ⁠ - Determine based on recent activity

### 3. *issues* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ number ⁠, ⁠ title ⁠, ⁠ body ⁠, ⁠ state ⁠, ⁠ created_at ⁠, ⁠ updated_at ⁠
•⁠  ⁠⁠ closed_at ⁠, ⁠ comments_count ⁠, ⁠ created_by ⁠ (user.login)
•⁠  ⁠⁠ labels ⁠ (as JSON array), ⁠ assignee ⁠ (user.login)

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ assigned_to ⁠, ⁠ closed_by ⁠ - Map to maintainers table
•⁠  ⁠⁠ priority_score ⁠ - Your custom calculation

### 4. *pull_requests* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ number ⁠, ⁠ title ⁠, ⁠ body ⁠, ⁠ state ⁠, ⁠ created_at ⁠, ⁠ updated_at ⁠
•⁠  ⁠⁠ merged_at ⁠, ⁠ closed_at ⁠, ⁠ created_by ⁠ (user.login)
•⁠  ⁠⁠ commits_count ⁠, ⁠ additions ⁠, ⁠ deletions ⁠, ⁠ changed_files ⁠
•⁠  ⁠⁠ review_comments_count ⁠, ⁠ comments_count ⁠, ⁠ draft ⁠

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ merged_by ⁠ - Map to maintainers table
•⁠  ⁠⁠ complexity_score ⁠ - Your custom calculation

### 5. *pr_reviews* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ state ⁠, ⁠ body ⁠, ⁠ submitted_at ⁠, ⁠ reviewer_id ⁠ (user.login)
•⁠  ⁠⁠ commit_id ⁠, ⁠ pull_request_id ⁠

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ review_depth_score ⁠ - *CRITICAL*: Calculate based on:
  - Length of review body
  - Number of inline comments
  - Specificity of feedback
  - Time spent (inferred from timestamps)
•⁠  ⁠⁠ lines_reviewed ⁠ - Estimate from file changes in PR

### 6. *pr_review_comments* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ body ⁠, ⁠ path ⁠, ⁠ position ⁠, ⁠ line ⁠, ⁠ created_at ⁠
•⁠  ⁠⁠ in_reply_to_id ⁠, ⁠ commenter_id ⁠ (user.login)

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ review_id ⁠ - Map to your pr_reviews table
•⁠  ⁠⁠ is_mentorship ⁠ - Determine if comment provides guidance/teaching

### 7. *issue_comments* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ body ⁠, ⁠ created_at ⁠, ⁠ commenter_id ⁠ (user.login)
•⁠  ⁠⁠ reactions ⁠ (as JSON object with counts)

### 8. *issue_timeline_events* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ event_type ⁠, ⁠ created_at ⁠, ⁠ actor_id ⁠ (user.login)
•⁠  ⁠⁠ label_name ⁠, ⁠ assignee_id ⁠ (user.login)

### 9. *discussions* table
*✅ Available from GitHub (GraphQL only):*
•⁠  ⁠⁠ github_id ⁠, ⁠ title ⁠, ⁠ body ⁠, ⁠ category ⁠, ⁠ created_at ⁠, ⁠ updated_at ⁠
•⁠  ⁠⁠ author_id ⁠ (user.login), ⁠ is_answered ⁠, ⁠ answered_by ⁠ (user.login)

### 10. *discussion_comments* table
*✅ Available from GitHub (GraphQL only):*
•⁠  ⁠⁠ github_id ⁠, ⁠ body ⁠, ⁠ created_at ⁠, ⁠ commenter_id ⁠ (user.login)
•⁠  ⁠⁠ parent_comment_id ⁠, ⁠ is_answer ⁠, ⁠ upvotes ⁠

### 11. *commits* table
*✅ Available from GitHub:*
•⁠  ⁠⁠ github_id ⁠, ⁠ message ⁠, ⁠ author_name ⁠, ⁠ author_email ⁠, ⁠ created_at ⁠
•⁠  ⁠⁠ additions ⁠, ⁠ deletions ⁠, ⁠ changed_files ⁠, ⁠ author_id ⁠ (user.login)

*❌ NOT Available (Need to calculate):*
•⁠  ⁠⁠ is_docs_related ⁠ - Analyze commit message and file changes

## ❌ *NOT AVAILABLE FROM GITHUB API* (Must Calculate)

### 1. *sentiment_analysis* table
*❌ Completely custom - you must calculate:*
•⁠  ⁠⁠ sentiment_score ⁠ (-1.0 to 1.0)
•⁠  ⁠⁠ tone ⁠ (constructive, neutral, harsh, supportive)
•⁠  ⁠⁠ text_analyzed ⁠ (the actual text)
•⁠  ⁠⁠ analysis_date ⁠

### 2. *burnout_risk_scores* table
*❌ Completely custom - you must calculate:*
•⁠  ⁠⁠ overall_risk_score ⁠ (0-100)
•⁠  ⁠⁠ response_time_score ⁠, ⁠ activity_level_score ⁠
•⁠  ⁠⁠ sentiment_score ⁠, ⁠ isolation_score ⁠
•⁠  ⁠⁠ workload_score ⁠, ⁠ community_support_score ⁠
