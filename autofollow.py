import requests
import pickle
import yaml
import os

# cd to dir with script (for cron jobs)
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

##
#
# {
#   "me": "wabscale",
#   "repos": ["AnubisLMS/Anubis"],
#   "cool_people": ["synoet"]
# }
#
##
config = yaml.safe_load(open('config.json'))
me = config['me']
cool_people = config['cool_people']
config_repos = config['repos']

token = open('TOKEN').read()
s = requests.Session()
s.headers['accept'] = 'application/vnd.github.v3+json'
s.headers['Authorization'] = f'token {token}'

user_repos_url = 'https://api.github.com/users/{username}/repos'
stars_url = 'https://api.github.com/repos/{repo}/stargazers'
contributors_url = 'https://api.github.com/repos/{repo}/contributors'
follow_url = 'https://api.github.com/user/following/{username}'
following_url = 'https://api.github.com/users/{username}/followers'

users_to_follow: set[str] = set()
if os.path.exists('following.pickle'):
    following: set[str] = pickle.load(open('following.pickle'))
else:
    following: set[str] = set()

def follow(username: str):
    if username in following or username == me:
        return

    print(f'following {username}')
    s.put(follow_url.format(username=username))
    following.add(username)

def follow_all(usernames: list[str]):
    for username in usernames:
        follow(username)

def get_repo_usernames(repos: str) -> set[str]:
    usernames = set()
    for repo in repos:
        print('inspecting', repo)
        for user in s.get(stars_url.format(repo=repo)).json():
            usernames.add(user.get('login', me))
        for user in s.get(contributors_url.format(repo=repo)).json():
            usernames.add(user.get('login', me))
    return usernames

def get_user_followers(username: str) -> set[str]:
    users = s.get(following_url.format(username=username)).json()
    return {user.get('login', me) for user in users}

def get_user_repos(username: str) -> set[str]:
    return  {repo['full_name'] for repo in s.get(user_repos_url.format(username=username)).json()}

my_repos = get_user_repos(me)

u1 = get_repo_usernames(my_repos)
users_to_follow = users_to_follow.union(u1)
print('users from config repos ::', len(u1))

u2 = get_repo_usernames(config_repos)
users_to_follow = users_to_follow.union(u2)
print('users from my repos ::', len(u2))

my_followers = get_user_followers(me)
users_to_follow = users_to_follow.union(my_followers)
print(f'users from {me} followers ::', len(my_followers))

for cool_person in cool_people:
    cool_person_followers = get_user_followers(cool_person)
    users_to_follow = users_to_follow.union(cool_person_followers)
    print(f'users from {cool_person_followers} followers ::', len(cool_person_followers))

# Remove people that we are already following
users_to_follow = users_to_follow.difference(following)

follow_all(users_to_follow)

pickle.dump(following, open('following.pickle', 'wb'))

