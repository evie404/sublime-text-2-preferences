import os
import sublime, sublime_plugin

# creates a cgit link to the line of the cursor location, on the working git branch

repos = ("birdcage", "science", "peacock", "tfe", "stageit")

class CgitCommand(sublime_plugin.TextCommand):

  def _base(self, gitRepo):
    foundRepos = [r for r in repos if r in gitRepo]
    if len(foundRepos) == 1:
      return "https://cgit.twitter.biz/" + foundRepos[0] + "/tree"
    else:
      return None


  def run(self, edit):
    file = self.view.file_name()
    dir = "/".join(file.split("/")[:-1])
    gitRepo = os.popen('cd %s; git rev-parse --show-toplevel'%(dir)).read()[:-1]
    branch = os.popen('cd %s; git rev-parse --abbrev-ref HEAD'%(dir)).read()[:-1]
    link = self._base(gitRepo)
    if link is not None and file.startswith(gitRepo):
      relPath = file[len(gitRepo):]
      if "master" not in branch and len(branch)>0:
        branchParam = "?h="+branch
      else:
        branchParam = ""
      sel = self.view.sel()
      if len(sel)==1:
        line, _ = self.view.rowcol(sel[0].a)
        currentLine = "#n%s"%(line+1)
      else:
        currentLine = ""
      cgitLink = link+relPath+branchParam+currentLine
      sublime.status_message(cgitLink + " copied to clipboard")
      os.system("echo '%s' | pbcopy"%(cgitLink))

    pass