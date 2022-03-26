# Github Autofollow

This repo is a dead simple script that automatically follows people. I have this configured so that it follows back people that follow you, and follows people that star or contribute to repos you specify.

## Setup

#### Github Token

You need to create a github token for yourself that has `user:follow` permissions. Drop this token in a file called `TOKEN`.

#### Configuration

Everything is driven from a configuration file called `config.json`. Its structure is:

```yaml
{
  # My username
  "me": "wabscale",
  
  # Repos that will be inspected for stargazers and contributors
  "repos": ["AnubisLMS/Anubis"],
  
  # Really cool people that will have their followers followed
  "cool_people": ["synoet"]
}
```

## Running

I have this running in a cronjob on one of my severs. 

```text
0 0 * * * python3.10 /path/to/autofollow.py
```
