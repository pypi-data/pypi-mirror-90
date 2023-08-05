import sys

import typer
from terminaltables import AsciiTable

from savvihub import Context
from savvihub.common import kubectl
from savvihub.common.constants import WEB_HOST
from savvihub.common.git import GitRepository, InvalidGitRepository

cluster_app = typer.Typer()


@cluster_app.callback()
def main():
    """
    Manage custom clusters
    """


@cluster_app.command()
def register():
    """
    Register a new kubernetes cluster to SavviHub
    """
    context = Context(user_required=True)
    client = context.authorized_client

    kubectl_context_name = kubectl.get_current_context()
    default_workspace_name = None
    try:
        context.git_repo = GitRepository()
        context.project_config = context.load_project_config(context.git_repo.get_savvihub_config_file_path())
        project = context.get_project()
        if project is not None:
            default_workspace_name = project.workspace.name
    except InvalidGitRepository:
        pass

    workspace_name = typer.prompt('SavviHub workspace name', default=default_workspace_name)
    workspace = client.workspace_read(workspace_name)
    if workspace is None:
        typer.echo(f'Workspace \'{workspace_name}\' does not exist or is not accessible.')
        sys.exit(1)

    default_cluster_name = None
    cluster_list = client.cluster_list(workspace_name)
    for cluster in sorted(cluster_list, key=lambda x: x.created_dt, reverse=True):
        if cluster.status == 'pending':
            default_cluster_name = cluster.name
            break

    if default_cluster_name is None:
        typer.echo(f'There is no pending cluster in the workspace \'{workspace_name}\'.\n'
                   f'Please create one here: {WEB_HOST}/{workspace_name}/settings/clusters')
        sys.exit(1)

    cluster_name = typer.prompt('SavviHub cluster name', default=default_cluster_name)

    kubectl_context_confirm = typer.confirm(f'Current kubectl context is \'{kubectl_context_name}\'.\n'
                                            f'Do you want to register this Kubernetes cluster to SavviHub?', default=True)
    if not kubectl_context_confirm:
        typer.echo('Run \'kubectl config use-context\' to switch the context.')
        sys.exit(1)

    namespace = typer.prompt('Kubernetes namespace')

    master_endpoint, ssl_ca_cert_base64_encoded = kubectl.get_cluster_info(kubectl_context_name)
    sa_token = kubectl.get_service_account_token(namespace)

    cluster = client.cluster_register(workspace_name, cluster_name,
                                      master_endpoint, namespace, sa_token, ssl_ca_cert_base64_encoded)
    typer.echo(f'\n'
               f'Custom cluster \'{cluster.name}\' is successfully registered to workspace \'{workspace_name}\'.\n'
               f'{WEB_HOST}/{workspace_name}/settings/clusters')


@cluster_app.command()
def list():
    """
    List custom clusters registered to SavviHub
    """
    context = Context(user_required=True)
    client = context.authorized_client
    workspace_name = None
    try:
        context.git_repo = GitRepository()
        context.project_config = context.load_project_config(context.git_repo.get_savvihub_config_file_path())
        project = context.get_project()
        if project is not None:
            workspace_name = project.workspace.name
    except InvalidGitRepository:
        pass

    if workspace_name is None:
        typer.echo('Run \'sv project init\' not to see this prompt.')
        workspace_name = typer.prompt('SavviHub workspace name')

    clusters = client.cluster_list(workspace_name)
    rows = []
    for cluster in clusters:
        rows.append([
            cluster.name + ' (SavviHub)' if cluster.is_savvihub_managed else '',
            cluster.kubernetes_master_endpoint or '-',
            cluster.kubernetes_namespace or '-',
            cluster.status.replace('-', ' ').upper(),
        ])

    table = AsciiTable([['NAME', 'K8S MASTER ENDPOINT', 'K8S NAMESPACE', 'STATUS'], *rows])
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)

