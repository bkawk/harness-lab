#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MEMORY_DIR="${BIG_BANG_MEMORY_DIR:-$REPO_DIR/artifacts/memory}"
LOG_DIR="${BIG_BANG_LOG_DIR:-$REPO_DIR/artifacts/logs}"
PID_FILE="${BIG_BANG_PID_FILE:-$MEMORY_DIR/big_bang.pid}"
CTL_FILE="${BIG_BANG_CTL_FILE:-$MEMORY_DIR/big_bang_ctl.json}"
STATE_FILE="${BIG_BANG_STATE_FILE:-$MEMORY_DIR/big_bang_state.json}"
LOG_FILE="${BIG_BANG_LOG_FILE:-$LOG_DIR/big_bang.log}"
PYTHON_BIN="${BIG_BANG_PYTHON:-python3}"
DEFAULT_INTERVAL="${BIG_BANG_INTERVAL_SECONDS:-30}"
SCIENCE_TIME_BUDGET_SECONDS="${BIG_BANG_SCIENCE_TIME_BUDGET_SECONDS:-600}"
SCIENCE_EVAL_RESERVE_SECONDS="${BIG_BANG_SCIENCE_EVAL_RESERVE_SECONDS:-120}"
RUNNER_STALE_SECONDS="${BIG_BANG_RUNNER_STALE_SECONDS:-750}"

mkdir -p "$MEMORY_DIR" "$LOG_DIR"

usage() {
  cat <<'EOF'
Usage:
  scripts/big_bang_ctl.sh start [big-bang args...]
  scripts/big_bang_ctl.sh status
  scripts/big_bang_ctl.sh stop
  scripts/big_bang_ctl.sh restart [big-bang args...]

Notes:
  - `start` defaults to endless mode with `--cycles 0`.
  - extra args passed to `start`/`restart` are forwarded to `scripts/big_bang.py`.
  - status combines PID health with `artifacts/memory/big_bang_state.json` freshness.
EOF
}

pid_from_file() {
  if [[ -f "$PID_FILE" ]]; then
    tr -d '[:space:]' < "$PID_FILE"
  fi
}

pid_is_alive() {
  local pid="${1:-}"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

write_ctl_file() {
  local pid="$1"
  local interval="$2"
  local log_file="$3"
  shift 3
  local args_json
  args_json="$("$PYTHON_BIN" - "$@" <<'PY'
import json
import sys
print(json.dumps(sys.argv[1:]))
PY
)"
  "$PYTHON_BIN" - "$CTL_FILE" "$pid" "$interval" "$log_file" "$args_json" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
payload = {
    "pid": int(sys.argv[2]),
    "interval_seconds": int(sys.argv[3]),
    "log_file": sys.argv[4],
    "args": json.loads(sys.argv[5]),
    "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}

start_big_bang() {
  local existing_pid
  existing_pid="$(pid_from_file || true)"
  if pid_is_alive "$existing_pid"; then
    echo "big-bang already running (pid $existing_pid)"
    return 0
  fi

  rm -f "$PID_FILE"

  local args=("$@")
  if [[ ${#args[@]} -eq 0 ]]; then
    args=(
      --source-dataset-id abc_raw_v1
      --prepared-dataset-id abc_boundary512
      --cycles 0
      --runner-backend auto
      --interval-seconds "$DEFAULT_INTERVAL"
    )
  fi

  local interval="$DEFAULT_INTERVAL"
  local i=0
  while [[ $i -lt ${#args[@]} ]]; do
    if [[ "${args[$i]}" == "--interval-seconds" ]] && [[ $((i + 1)) -lt ${#args[@]} ]]; then
      interval="${args[$((i + 1))]}"
      break
    fi
    i=$((i + 1))
  done

  (
    cd "$REPO_DIR"
    nohup env PYTHONPATH=src HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS="$SCIENCE_TIME_BUDGET_SECONDS" HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS="$SCIENCE_EVAL_RESERVE_SECONDS" HARNESS_LAB_RUNNER_STALE_SECONDS="$RUNNER_STALE_SECONDS" "$PYTHON_BIN" scripts/big_bang.py "${args[@]}" >>"$LOG_FILE" 2>&1 &
    echo $! >"$PID_FILE"
  )

  local pid
  pid="$(pid_from_file || true)"
  if ! pid_is_alive "$pid"; then
    echo "failed to start big-bang" >&2
    return 1
  fi

  write_ctl_file "$pid" "$interval" "$LOG_FILE" "${args[@]}"
  echo "big-bang started"
  echo "pid: $pid"
  echo "log: $LOG_FILE"
}

stop_big_bang() {
  local pid
  pid="$(pid_from_file || true)"
  if ! pid_is_alive "$pid"; then
    rm -f "$PID_FILE"
    echo "big-bang is not running"
    return 0
  fi

  kill "$pid"
  local waited=0
  while pid_is_alive "$pid" && [[ $waited -lt 10 ]]; do
    sleep 1
    waited=$((waited + 1))
  done
  if pid_is_alive "$pid"; then
    kill -9 "$pid"
  fi
  rm -f "$PID_FILE"
  "$PYTHON_BIN" - "$STATE_FILE" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
payload = {}
if path.exists():
    payload = json.loads(path.read_text(encoding="utf-8"))
payload["status"] = "stopped"
payload["last_heartbeat"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
  echo "big-bang stopped"
}

status_big_bang() {
  "$PYTHON_BIN" - "$PID_FILE" "$CTL_FILE" "$STATE_FILE" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

pid_file = Path(sys.argv[1])
ctl_file = Path(sys.argv[2])
state_file = Path(sys.argv[3])

pid = None
if pid_file.exists():
    text = pid_file.read_text(encoding="utf-8").strip()
    if text:
        pid = int(text)

ctl = {}
if ctl_file.exists():
    ctl = json.loads(ctl_file.read_text(encoding="utf-8"))

state = {}
if state_file.exists():
    state = json.loads(state_file.read_text(encoding="utf-8"))

process_alive = False
if pid is not None:
    try:
        os.kill(pid, 0)
        process_alive = True
    except OSError:
        process_alive = False

interval = int(ctl.get("interval_seconds", 30) or 30)
fresh_window = max(120, interval * 3)

heartbeat = state.get("last_heartbeat", "")
heartbeat_age_seconds = None
heartbeat_fresh = False
if heartbeat:
    ts = datetime.fromisoformat(heartbeat.replace("Z", "+00:00"))
    heartbeat_age_seconds = int((datetime.now(timezone.utc) - ts).total_seconds())
    heartbeat_fresh = heartbeat_age_seconds <= fresh_window

control_plane = "running" if process_alive or heartbeat_fresh else "stopped"
dashboard_status = "fresh" if heartbeat_fresh else "stale"
state_status = str(state.get("status", "-") or "-")
if process_alive:
    control_plane = "running"
elif state_status == "stopped":
    control_plane = "stopped"
elif heartbeat_fresh:
    control_plane = "heartbeat_only"
else:
    control_plane = "stopped"

print(f"pid: {pid if pid is not None else 'none'}")
print(f"process_alive: {'yes' if process_alive else 'no'}")
print(f"control_plane: {control_plane}")
print(f"dashboard_status: {dashboard_status}")
print(f"heartbeat_age_seconds: {heartbeat_age_seconds if heartbeat_age_seconds is not None else 'unknown'}")
print(f"state_status: {state_status}")
print(f"cycles_completed: {state.get('cycles_completed', 0)}")
print(f"last_candidate: {state.get('last_candidate_id', '-') or '-'}")
print(f"last_cycle_mode: {state.get('last_cycle_mode', '-') or '-'}")
print(f"novelty_cycles_triggered: {state.get('novelty_cycles_triggered', 0)}")
print(f"last_commit: {state.get('last_commit_sha', '-') or '-'}")
print(f"log: {ctl.get('log_file', '-') if ctl else '-'}")
PY
}

command="${1:-}"
if [[ -z "$command" ]]; then
  usage
  exit 1
fi
shift || true

case "$command" in
  start)
    start_big_bang "$@"
    ;;
  stop)
    stop_big_bang
    ;;
  restart)
    stop_big_bang
    start_big_bang "$@"
    ;;
  status)
    status_big_bang
    ;;
  *)
    usage
    exit 1
    ;;
esac
