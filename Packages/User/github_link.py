import os
import sublime, sublime_plugin

# creates a github link to the line of the cursor location, on the working git branch

REPOS = ["airbnb", "restore", "chef", "milestones", "deployboard", "tungsten-support", "rails", "tungsten"]
BASE_URL = "https://git.musta.ch/airbnb/"

class GithubLinkCommand(sublime_plugin.TextCommand):
  def run(self, edit, branch_override = None):
    file_name = self.view.file_name()
    dir_path = "/".join(file_name.split("/")[:-1])

    repo_directory_cmd = "cd %s; git rev-parse --show-toplevel" % dir_path
    branch_cmd = "cd %s; git rev-parse --abbrev-ref HEAD" % dir_path

    repo_directory = os.popen(repo_directory_cmd).read()[:-1]

    print(repo_directory)


    branch_name = branch_override or os.popen(branch_cmd).read()[:-1]
    repo_name = self._get_repo_name(repo_directory)

    print(repo_name)
    print(file_name)
    print(file_name.startswith(repo_directory))


    if repo_name is None:
      return

    # if not file_name.startswith(repo_directory):
    #   return

    github_link = BASE_URL + "%(repo_name)s/blob/%(branch_name)s%(file_name_path)s%(line_number)s" % {
      "repo_name": repo_name,
      "branch_name": branch_name,
      "file_name_path": file_name[len(repo_directory):],
      "line_number": self._get_line_number_anchor(self.view)
    }
    sublime.status_message(github_link + " copied to clipboard")
    os.system("echo '%s' | pbcopy" % github_link)
    return

  def _get_repo_name(self, repo_directory):
    found_repos = [r for r in REPOS if r in repo_directory]
    if len(found_repos) == 1:
      return found_repos[0]
    else:
      return None

  def _get_line_number(self, view):
    sel = view.sel()
    if len(sel) == 1:
      line, _ = view.rowcol(sel[0].a)
      return line + 1
    else:
      return 0

  def _get_line_number_anchor(self, view):
    line_number = self._get_line_number(view)
    if line_number > 0:
      return "#L%(line_number)s" % { "line_number": line_number }
    else:
      return ""
