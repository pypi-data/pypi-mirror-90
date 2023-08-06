from github import Github
from github import InputFileContent
from gitlab import gitlab

def create_repo(repo_name, token=None, provider='github'):
  if not token:
    print('Token required')
  if 'github' in provider:
    g = Github(token)
    user = g.get_user()
    repo = user.create_repo(repo_name, private=True)
    return repo

def create_gist(gist_name, content, token=None, provider='github'):
  if not token:
    print('Token required')
  if 'github' in provider:
    g = Github(token)
    user = g.get_user()
    gist = user.create_gist(public=False, files={gist_name: InputFileContent(content)}, description="my description")
    return gist

def delete_repo(repo_name, token=None, provider='github'):
  if not token:
    print('Token required')
  if 'github' in provider:
    g = Github(token)

    repo = g.get_repo(f"{g.get_user().login}/{repo_name}")
    repo.delete()
    print(f"Repo {repo_name} deleted")


# def transfer_repo(repo_name, group=None, token=None, provider='github'):
#   if not token:
#     print('Token required')
#   if 'github' in provider:
#     g = Github(token)
#     user = g.get_user()
#     repo = user.create_repo(repo_name, private=True)
#     return repo

# def dev():
#   # if not token:
#   #   print('Token required')
#   gl = gitlab.Gitlab()
