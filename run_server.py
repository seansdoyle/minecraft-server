import subprocess
import time
import re
import requests

def main():
    run_server_command = ['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar']
    
    _ip = requests.get("http://ifconfig.me")
    ip_addr = _ip.text

    print(f"Serving at: {ip_addr}")
    server_start_time = time.time()
    server_stdout = subprocess.check_output(run_server_command)
    server_end_time = time.time()
    server_up_time = server_end_time - server_start_time
    
    # stdout returned as byte stream, decode to utf-8 string
    server_stdout = server_stdout.decode('utf-8')

    # get list of players from stdout
    plrs = server_stdout_to_players(server_stdout)

    # build report based on players and uptime
    msg = build_report(plrs, server_up_time)
    print(msg)

    # Finally add server files to git
    add_server_to_git(build_git_commit, msg)

    return 0

def add_server_to_git(commit_msg_func, msg):
    '''Creates dictionary of git commands: add, commit, push - to add
    server files to git repository. Takes in commit msg and the function
    that builds the message.'''
    git = {'add':['git', 'add', '--all'], 'commit':commit_msg_func(msg), 'push':['git', 'push']}

    subprocess.check_call(git['add'])
    subprocess.check_call(git['commit'])
    subprocess.check_call(git['push'])

def server_stdout_to_players(stdout):
    '''Converts string type stdout to list of players on the server.'''
    players = re.findall("\w+ joined the game", stdout)
    unique_players = []

    for player in players:
        player = player.replace(" joined the game", "")
        if player not in return_players:
            unique_players.append(player)

    return unique_players

def build_git_commit(msg):
    '''Current function used to build commit command.'''
    return ['git', 'commit', '-m', '"' + msg + '"']

def build_report(players, server_up_time):
    '''Builds a report of the servers run. Returns string with players who
    played and the amount of time the server process ran for.'''
    minutes = int(server_up_time/60)
    seconds = server_up_time % 60
    
    players = ", ".join(players)

    return f"{players} played minecraft for {minutes}:{seconds}"

if __name__ == '__main__':
    main()
