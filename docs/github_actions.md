# GitHub Actions

This document explains the GitHub Actions workflows used to automate repetitive tasks: code formatting and scheduled article extraction.

## Overview

The project uses **GitHub Actions** for continuous automation. All workflows are defined as YAML files in the `.github/workflows/` directory.

## Workflows

### 1. Format Workflow

**Purpose**: Automatically check and fix Python code style consistency.

**File**: [`.github/workflows/format.yml`](../.github/workflows/format.yml)

**Trigger Events**:

- Pull requests to `main` branch (with changes to `main.py` or `utils/`)
- Direct pushes to `main` branch (with changes to `main.py` or `utils/`)

**Scope**: Checks and formats `main.py` and all files in `utils/` folder

**Tool**: Ruff (Python code formatter)

**Steps**:

1. Check out code from repository
2. Set up Python 3.10
3. Install Ruff
4. Run Ruff formatter (`make format`)
5. Configure Git user (github-actions bot)
6. Auto-commit and push changes back to PR/branch (only if modifications were made)

**Key Benefit**: Ensures consistent code style without manual enforcement

---

### 2. Scheduled Extraction Workflow

**Purpose**: Automatically extract and store articles on a schedule.

**File**: [`.github/workflows/scheduled_extraction.yml`](../.github/workflows/scheduled_extraction.yml)

**Trigger Events**:

- **Schedule**: Every day at 6:00 AM UTC (configurable via cron expression)
- **Manual**: Anytime via GitHub UI "Run workflow" button

**Configuration**:

```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM UTC daily
  workflow_dispatch:     # Manual trigger
```

**Steps**:

1. Check out repository code
2. Set up Python 3.10
3. Install dependencies (upgrade pip and run `make install`)
4. Create `credentials.json` from GitHub secrets
5. Verify credentials file exists (safety check)
6. Run extraction script (`make run`) and capture output to timestamped log file
7. Clean up (delete temporary `credentials.json`)
8. Upload log file as GitHub Action artifact

**Environment Variables**:

- `SHEET_ID`: Set from GitHub secrets

**Artifacts**: Extraction logs are available in the Actions tab for review and debugging (named `extraction-log-YYYY-MM-DD.txt`)

**Key Benefit**: Fully automated, zero-downtime article collection

---

## Monitoring & Debugging

### Viewing Workflow Results

1. Navigate to your repository
2. Click **Actions** tab
3. Select a workflow run
4. View real-time logs or download artifacts

### Accessing Extraction Logs

1. Go to **Actions** → **Daily Extraction Schedule**
2. Click a workflow run
3. Scroll to **Artifacts** section
4. Download `extraction-log-YYYY-MM-DD.txt`
