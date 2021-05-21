from sys import maxsize
from git import Repo
from graphviz import Digraph
from graphviz import Graph
import time

from git.objects.commit import Commit

repo = Repo("../ai_engine")
commits = repo.iter_commits('master')

all_commits = []
plugin_config = []
plugin_integration = []
plugin_lifecycle = []
# plugin_deploy = []
sdk_manage = []
client_manage = []
# framework_cap = []
task_sche = []
cli_server_comm = []
ai_data_trans = []

for commit in commits:
    
    touched = False
    for file in commit.stats.files:
        if "common/protocol/plugin_config/" in file:
            touched = True
            if commit not in plugin_config:
                plugin_config.append(commit)
        
        if "server/plugin/" in file:
            touched = True
            if commit not in plugin_integration:
                plugin_integration.append(commit)

        if "server/plugin_manager/" in file:
            touched = True
            if commit not in plugin_lifecycle:
                plugin_lifecycle.append(commit)

        if ("interfaces/kits" in file) or ("services/client/algorithm_sdk" in file):
            touched = True
            if commit not in sdk_manage:
                sdk_manage.append(commit)

        if "services/client/client_executor" in file:
            touched = True
            if commit not in client_manage:
                client_manage.append(commit)

        if "services/server/server_executor" in file:
            touched = True
            if commit not in task_sche:
                task_sche.append(commit)

        if "common/platform/os_wrapper" in file or "server/plugin/" in file or "utils/encdec" in file:
            touched = True
            if commit not in ai_data_trans:
                ai_data_trans.append(commit)

        if "client/communication_adapter" in file or "server/communication_adapter" in file:
            touched = True
            if commit not in cli_server_comm:
                cli_server_comm.append(commit)
    all_commits.append(commit)


graph = Graph(comment='Semantic History Commit Slicing')
graph.attr(rankdir='RL')
graph.attr('node', shape='circle')
for commit in all_commits:
    with graph.subgraph() as s:
        s.attr(rank='same')
        s.node("all_"+str(all_commits.index(commit)), commit.hexsha[:7])
        if commit in plugin_config:
            s.node("plugin_config_"+str(plugin_config.index(commit)), commit.hexsha[:7])
        if commit in plugin_integration:
            s.node("plugin_integration_"+str(plugin_integration.index(commit)), commit.hexsha[:7])
        if commit in plugin_lifecycle:
            s.node("plugin_lifecycle_"+str(plugin_lifecycle.index(commit)), commit.hexsha[:7])
        if commit in sdk_manage:
            s.node("sdk_manage_"+str(sdk_manage.index(commit)), commit.hexsha[:7])
        if commit in client_manage:
            s.node("client_manage_"+str(client_manage.index(commit)), commit.hexsha[:7])
        if commit in task_sche:
            s.node("task_sche_"+str(task_sche.index(commit)), commit.hexsha[:7])
        if commit in ai_data_trans:
            s.node("ai_data_trans_"+str(ai_data_trans.index(commit)), commit.hexsha[:7])
        if commit in cli_server_comm:
            s.node("cli_server_comm_"+str(cli_server_comm.index(commit)), commit.hexsha[:7])

for i in range(0, len(all_commits)-1):
    graph.edge("all_"+str(i), "all_"+str(i+1))

for i in range(0, len(plugin_config)-1):
    graph.edge("plugin_config_"+str(i), "plugin_config_"+str(i+1))

for i in range(0, len(plugin_integration)-1):
    graph.edge("plugin_integration_"+str(i), "plugin_integration_"+str(i+1))

for i in range(0, len(plugin_lifecycle)-1):
    graph.edge("plugin_lifecycle_"+str(i), "plugin_lifecycle_"+str(i+1))

for i in range(0, len(sdk_manage)-1):
    graph.edge("sdk_manage_"+str(i), "sdk_manage_"+str(i+1))

for i in range(0, len(client_manage)-1):
    graph.edge("client_manage_"+str(i), "client_manage_"+str(i+1))

for i in range(0, len(task_sche)-1):
    graph.edge("task_sche_"+str(i), "task_sche_"+str(i+1))

for i in range(0, len(ai_data_trans)-1):
    graph.edge("ai_data_trans_"+str(i), "ai_data_trans_"+str(i+1))

for i in range(0, len(cli_server_comm)-1):
    graph.edge("cli_server_comm_"+str(i), "cli_server_comm_"+str(i+1))


graph.render("default.gv", view=True)
