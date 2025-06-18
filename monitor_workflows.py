#!/usr/bin/env python3
"""
GitHub Workflows Monitor Script

This script helps monitor GitHub workflows for the ThreePaneWindows project.
It provides various utilities to check workflow status, view logs, and get notifications.
"""

import subprocess
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import webbrowser


class WorkflowMonitor:
    """Monitor GitHub workflows for ThreePaneWindows project."""
    
    def __init__(self):
        self.repo = "stntg/ThreePaneWindows"
        self.workflows = {
            "ci": "ci.yml",
            "docs": "docs.yml", 
            "release": "release.yml",
            "test-release": "test-release.yml"
        }
        self.base_url = f"https://github.com/{self.repo}"
    
    def check_gh_cli(self) -> bool:
        """Check if GitHub CLI is installed."""
        try:
            result = subprocess.run(["gh", "--version"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_git_info(self) -> Dict[str, str]:
        """Get current git information."""
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True
            )
            current_branch = branch_result.stdout.strip()
            
            # Get latest commit
            commit_result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True, text=True
            )
            latest_commit = commit_result.stdout.strip()
            
            # Get remote URL
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True, text=True
            )
            remote_url = remote_result.stdout.strip()
            
            return {
                "branch": current_branch,
                "commit": latest_commit,
                "remote": remote_url
            }
        except Exception as e:
            return {"error": str(e)}
    
    def open_actions_page(self, workflow: Optional[str] = None):
        """Open GitHub Actions page in browser."""
        if workflow and workflow in self.workflows:
            url = f"{self.base_url}/actions/workflows/{self.workflows[workflow]}"
        else:
            url = f"{self.base_url}/actions"
        
        print(f"Opening: {url}")
        webbrowser.open(url)
    
    def get_workflow_runs(self, workflow: str, limit: int = 5) -> List[Dict]:
        """Get recent workflow runs using GitHub CLI."""
        if not self.check_gh_cli():
            print("❌ GitHub CLI not installed. Install from: https://cli.github.com/")
            return []
        
        try:
            cmd = ["gh", "run", "list", "--repo", self.repo, 
                   "--workflow", self.workflows.get(workflow, workflow),
                   "--limit", str(limit), "--json", 
                   "status,conclusion,createdAt,headBranch,headSha,url"]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"❌ Error getting workflow runs: {result.stderr}")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def watch_workflow(self, run_id: str):
        """Watch a specific workflow run."""
        if not self.check_gh_cli():
            print("❌ GitHub CLI not installed")
            return
        
        try:
            subprocess.run(["gh", "run", "watch", run_id, "--repo", self.repo])
        except KeyboardInterrupt:
            print("\n⏹️  Stopped watching workflow")
        except Exception as e:
            print(f"❌ Error watching workflow: {e}")
    
    def trigger_workflow(self, workflow: str, inputs: Optional[Dict] = None):
        """Trigger a workflow manually (for workflow_dispatch workflows)."""
        if not self.check_gh_cli():
            print("❌ GitHub CLI not installed")
            return
        
        if workflow not in ["test-release"]:
            print(f"❌ Workflow '{workflow}' cannot be triggered manually")
            return
        
        try:
            cmd = ["gh", "workflow", "run", self.workflows[workflow], 
                   "--repo", self.repo]
            
            if inputs:
                for key, value in inputs.items():
                    cmd.extend(["-f", f"{key}={value}"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Triggered {workflow} workflow")
            else:
                print(f"❌ Error triggering workflow: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_status(self):
        """Show current status of all workflows."""
        print("🔍 GitHub Workflows Status")
        print("=" * 50)
        
        # Show git info
        git_info = self.get_git_info()
        if "error" not in git_info:
            print(f"📍 Current Branch: {git_info['branch']}")
            print(f"📝 Latest Commit: {git_info['commit']}")
            print()
        
        # Show workflow status
        for workflow_name, workflow_file in self.workflows.items():
            print(f"🔧 {workflow_name.upper()} Workflow:")
            runs = self.get_workflow_runs(workflow_name, 3)
            
            if runs:
                for run in runs:
                    status_icon = self._get_status_icon(run['status'], run['conclusion'])
                    created_at = datetime.fromisoformat(
                        run['createdAt'].replace('Z', '+00:00')
                    ).strftime('%Y-%m-%d %H:%M')
                    
                    print(f"  {status_icon} {created_at} - {run['headBranch']} - {run['headSha'][:7]}")
            else:
                print("  ❓ No recent runs found")
            print()
    
    def _get_status_icon(self, status: str, conclusion: Optional[str]) -> str:
        """Get status icon for workflow run."""
        if status == "completed":
            if conclusion == "success":
                return "✅"
            elif conclusion == "failure":
                return "❌"
            elif conclusion == "cancelled":
                return "⏹️"
            else:
                return "❓"
        elif status == "in_progress":
            return "🟡"
        elif status == "queued":
            return "⚪"
        else:
            return "❓"
    
    def run_local_tests(self):
        """Run local tests to predict CI results."""
        print("🧪 Running Local Tests")
        print("=" * 30)
        
        tests = [
            ("pytest", ["python", "-m", "pytest", "tests/", "-v"]),
            ("flake8", ["flake8", "threepanewindows/"]),
            ("mypy", ["mypy", "threepanewindows/", "--ignore-missing-imports"]),
            ("bandit", ["bandit", "-r", "threepanewindows/"])
        ]
        
        results = {}
        for test_name, cmd in tests:
            print(f"Running {test_name}...")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                results[test_name] = {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr
                }
                status = "✅" if result.returncode == 0 else "❌"
                print(f"{status} {test_name}")
            except subprocess.TimeoutExpired:
                results[test_name] = {"success": False, "error": "Timeout"}
                print(f"⏰ {test_name} - Timeout")
            except FileNotFoundError:
                results[test_name] = {"success": False, "error": "Command not found"}
                print(f"❓ {test_name} - Command not found")
        
        return results


def main():
    """Main CLI interface."""
    monitor = WorkflowMonitor()
    
    if len(sys.argv) < 2:
        print("GitHub Workflows Monitor")
        print("=" * 30)
        print("Usage: python monitor_workflows.py <command> [args]")
        print()
        print("Commands:")
        print("  status              - Show workflow status")
        print("  open [workflow]     - Open Actions page in browser")
        print("  runs <workflow>     - Show recent runs for workflow")
        print("  watch <run_id>      - Watch specific workflow run")
        print("  trigger <workflow>  - Trigger workflow manually")
        print("  test                - Run local tests")
        print("  git                 - Show git information")
        print()
        print("Workflows: ci, docs, release, test-release")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        monitor.show_status()
    
    elif command == "open":
        workflow = sys.argv[2] if len(sys.argv) > 2 else None
        monitor.open_actions_page(workflow)
    
    elif command == "runs":
        if len(sys.argv) < 3:
            print("❌ Please specify workflow name")
            return
        workflow = sys.argv[2]
        runs = monitor.get_workflow_runs(workflow)
        if runs:
            for run in runs:
                status_icon = monitor._get_status_icon(run['status'], run['conclusion'])
                print(f"{status_icon} {run['createdAt']} - {run['headBranch']} - {run['url']}")
    
    elif command == "watch":
        if len(sys.argv) < 3:
            print("❌ Please specify run ID")
            return
        run_id = sys.argv[2]
        monitor.watch_workflow(run_id)
    
    elif command == "trigger":
        if len(sys.argv) < 3:
            print("❌ Please specify workflow name")
            return
        workflow = sys.argv[2]
        if workflow == "test-release":
            version = input("Enter version (e.g., 0.1.0-test1): ")
            test_only = input("Test PyPI only? (y/n): ").lower() == 'y'
            inputs = {"version": version, "test_pypi_only": str(test_only).lower()}
            monitor.trigger_workflow(workflow, inputs)
        else:
            monitor.trigger_workflow(workflow)
    
    elif command == "test":
        results = monitor.run_local_tests()
        print("\n📊 Test Results Summary:")
        for test, result in results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {test}")
    
    elif command == "git":
        git_info = monitor.get_git_info()
        print("📍 Git Information:")
        for key, value in git_info.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()