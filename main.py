from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from datetime import datetime

import os 
TOKEN = os.getenv("GITHUB_TOKEN")


# GitHub headers
headers = {
    "Authorization": "token " + TOKEN
}

leaderboard = []
cache = {}
# Create app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

positive_words = ["fix", "improve", "optimize", "resolve"]


# -----------------------------
# FUNCTION: Check Night Time
# -----------------------------
def is_night_time(timestamp):
    time_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    hour = time_obj.hour

    if hour >= 22 or hour < 6:
        return True
    else:
        return False


# -----------------------------
# FUNCTION: Check Complexity
# -----------------------------
def is_complex_commit(message):

    message_lower = message.lower()

    strong_keywords = [
        "refactor", "optimize", "implement",
        "architecture", "performance", "security",
        "scalable", "algorithm", "improve"
    ]

    weak_keywords = [
        "fix", "update", "change", "minor"
    ]

    strong_match = False
    weak_match = False

    for word in strong_keywords:
        if word in message_lower:
            strong_match = True

    for word in weak_keywords:
        if word in message_lower:
            weak_match = True

    # Strict logic
    if strong_match and len(message) > 40:
        return True

    return False
# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/score")
def get_score(username: str):
    if username in cache:
        return cache[username]
    ai_score = 0

    repos_url = "https://api.github.com/users/" + username + "/repos"

    repos_response = requests.get(repos_url, headers=headers)
    if repos_response.status_code != 200:
        return {"error": "GitHub API failed"}

    active_days = set()
    total_commits = 0
    night_commits = 0
    complex_commits = 0
    pr_count = 0
    merged_pr_count = 0
    total_merge_time = 0
    merged_prs_for_time = 0
    total_changes = 0

    if repos_response.status_code == 200:

        repos = repos_response.json()

        # LIMIT to 3 repos to avoid API limit
        for repo in repos[:5]:

            repo_name = repo["name"]

            commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=100"

            commits_response = requests.get(commits_url, headers=headers)

            if commits_response.status_code == 200:

                commits = commits_response.json()

                for commit in commits[:10]:
                    try:
                        timestamp = commit["commit"]["author"]["date"]
                        message = commit["commit"]["message"]
                        message_lower = message.lower()
                        
                        for word in positive_words:
                            if word in message_lower:
                                ai_score += 2
                        date_only = timestamp[:10]
                        active_days.add(date_only)

                        total_commits += 1

                        # Night check
                        if is_night_time(timestamp):
                            night_commits += 1

                        # Complexity check
                        # 🔥 REAL complexity check using lines changed
                        commit_url = commit["url"]
                        commit_detail = requests.get(commit_url, headers=headers)

                        if commit_detail.status_code == 200:
                            stats = commit_detail.json().get("stats", {})
                            additions = stats.get("additions", 0)
                            deletions = stats.get("deletions", 0)

                            changes = additions + deletions
                            total_changes += changes

                            if changes > 50:
                                complex_commits += 1

                        if total_commits > 0:
                            if night_commits > total_commits * 0.6:
                                burnout = "High burnout risk"
                            elif night_commits > total_commits * 0.3:
                                burnout = "Moderate burnout risk"
                            elif night_commits > total_commits * 0.1:
                                burnout = "Healthy work pattern"
                            else:
                                burnout = "No activity data"
                    except:
                        pass



            # Fetch Pull Requests
            pulls_url = f"https://api.github.com/repos/{username}/{repo_name}/pulls?state=closed&per_page=100"

            pulls_response = requests.get(pulls_url, headers=headers)

            if pulls_response.status_code == 200:

                pulls = pulls_response.json()

                for pr in pulls:
                    try:
                        
                        pr_count += 1
                        created_at = pr.get("created_at")
                        merged_at = pr.get("merged_at")

        # Count merged PR
                        if merged_at is not None and created_at is not None:
                            merged_pr_count += 1

            # Convert to datetime
                            created_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                            merged_time = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")

            # Calculate difference
                            time_diff = merged_time - created_time

            # Convert to hours
                            hours = time_diff.total_seconds() / 3600

                            total_merge_time += hours
                            merged_prs_for_time += 1

                    except Exception as e:
                        print("Merge Speed Error:", e)

 
            # -----------------------------

    avg_commit_size = total_changes / total_commits if total_commits > 0 else 0
# MERGE SPEED CALCULATION
# -----------------------------
    if merged_prs_for_time > 0:
        avg_merge_time = total_merge_time / merged_prs_for_time
    else:
        avg_merge_time = 0
    # 🔥 UPDATED SCORE
    # -----------------------------
# SCORE CALCULATION
# -----------------------------

    consistency_score = len(active_days)
    score = (
        (night_commits * 1)
        + (total_commits * 2)
        + (complex_commits * 5)
        + (merged_pr_count * 6)
        + (consistency_score * 3)
    )
    score += ai_score

    if score > 400:
        score_msg = "Elite Night Developer"
    elif score > 250:
        score_msg = "Strong Contributor"
    else:
        score_msg = "Growing Developer"

    # -----------------------------
# MERGE SPEED ANALYSIS
# -----------------------------
    if avg_merge_time == 0:
        merge_msg = "No merged PR data"
    elif avg_merge_time < 24:
        merge_msg = "Fast PR resolution"
    elif avg_merge_time < 72:
        merge_msg = "Moderate PR resolution speed"
    else:
        merge_msg = "Slow PR resolution"

    # Badge logic
    if score > 500:
        badge = "Dark Knight Master"
    elif score > 200:
        badge = "Midnight Warrior"
    else:
        badge = "Night Beginner"

# Explanation logic
    if night_commits == 0:
        night_msg = "No night activity detected"
    elif night_commits > total_commits * 0.4:
        night_msg = "Strong night productivity"
    else:
        night_msg = "Moderate night activity"

    if complex_commits > total_commits * 0.3:
        complexity_msg = "High complexity work"
    else:
        complexity_msg = "Basic to moderate complexity work"
    
    if pr_count == 0:
        pr_msg = "Low collaborative via Pull Requests"
    elif merged_pr_count == 0:
        pr_msg = "PRs exist but rarely merged"
    else:
        pr_msg = "Active contributor via pull requests"

    final_summary = (
        "This developer shows " +
        night_msg.lower() + ", " +
        complexity_msg.lower() + ", and " +
        pr_msg.lower() + "."
    )

    if score > 400:
        level = "Elite Developer"
    elif score > 250:
        level = "Strong Contributor"
    else:
        level = "Growing Developer"

    if score > 400:
        decision = "Recommended for high-impact engineering roles"
    elif score > 250:
        decision = "Suitable for consistent development roles"
    else:
        decision = "Needs improvement for production-level work"

    # -----------------------------
# BASELINE DATASET (SIMULATED REAL USERS)
# -----------------------------
    baseline_scores = [u["score"] for u in leaderboard] + [score]

# Calculate percentile
    below_count = len([s for s in baseline_scores if s < score])
    percentile = int((below_count / len(baseline_scores)) * 100)

# Label
    if len(baseline_scores) < 5:
        benchmark_label = "Insufficient Data"
        percentile = 50
    else:
        if percentile >= 90:
            benchmark_label = "Top 10%"
        elif percentile >= 70:
            benchmark_label = "Top 30%"
        elif percentile >= 50:
            benchmark_label = "Above Average"
        else:
            benchmark_label = "Below Average"

    # -----------------------------
# SAVE TO LEADERBOARD
# -----------------------------
    import random

    import hashlib
    user_id = "User#" + hashlib.md5(username.encode()).hexdigest()[:6]
    proof_string = username + str(score)
    proof_hash = hashlib.sha256(proof_string.encode()).hexdigest()
    leaderboard.append({
        "user_id": user_id,
        "score": score
    })

# SORT LEADERBOARD (highest first)
    leaderboard_sorted = sorted(
        leaderboard,
        key=lambda x: x["score"],
        reverse=True
    )

# TAKE TOP 5 USERS
    top_users = leaderboard_sorted[:5]

    privacy_note = "User identity is anonymized. Data is processed temporarily and not stored."
    ai_note = "This system uses lightweight NLP to analyze commit messages and behavioral patterns."

    return {
        "user_id": user_id,
        "total_commits": total_commits,

        "night_commits": night_commits,
        "avg_commit_size": round(avg_commit_size, 2),
        "complex_commits": complex_commits,
        "pull_requests": pr_count,
        "merged_pull_requests": merged_pr_count,
        "pr_analysis": pr_msg,
        "level": level,
        "decision": decision,
        "dark_knight_score": score,
        "leaderboard": top_users,
        "consistency_days": consistency_score,
        "percentile": percentile,
        "benchmark_label": benchmark_label,
        "badge": badge,
        "night_analysis": night_msg,
        "complexity_analysis": complexity_msg,
        "average_merge_time_hours": round(avg_merge_time, 2),
        "merge_speed_analysis": merge_msg,
        "score_interpretation": score_msg,
        "privacy_note": privacy_note,
        "ai_note": ai_note,
        "proof": proof_hash,
        "burnout": burnout,
        "final_summary": final_summary,


    }