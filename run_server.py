import subprocess
import time
import re

def main():
    run_server_command = ['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar']

    server_start_time = time.time()
    server_stdout = subprocess.check_output(run_server_command)
    server_end_time = time.time()
    server_up_time = str(server_end_time - server_start_time)
    
    server_stdout = server_stdout.decode('utf-8')
    players = re.findall('\w+ joined the game', server_stdout)
   
    for player in players:
        player = player.replace(" joined the game", "")
    
    players_s = ",".join(players)

    print("\nServer closed")
    msg = "{} player on ther server ran for {}".format(players_s, server_up_time))
    
    if('help' in server_stdout):
        print("help in server_stdout")

    git = {'add':['git', 'add', '--all'], 'commit':build_git_commit(server_up_time), 'push':['git', 'push']}

    #subprocess.check_call(git_add)
    #subprocess.check_call(build_git_commit(msg))
    #subprocess.check_call(git_push)


def build_git_commit(msg):
    return ['git', 'commit', '-m', '\"', str(msg), '\"']
    
if __name__ == '__main__':
    main()
