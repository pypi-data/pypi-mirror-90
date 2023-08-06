import click
import os
import os.path
import sh


HERE = os.path.abspath(os.path.dirname(__file__))


@click.group()
def cli():
    pass


def get_templates():
    dirs = os.scandir(os.path.join(HERE, 'templates'))
    templates = []
    for entry in dirs:
        if entry.is_dir():
            templates.append(entry.name)
    return templates


@cli.command()
@click.option('-t', '--template', default='simple', help='template')
@click.argument('project_name')
def init(template, project_name):
    templates = get_templates()
    if template not in templates:
        click.echo('%s template not found' % template, err=True)
        return
    project_dir = f'./{project_name}'
    sh.mkdir('-p', project_dir)
    sh.cp('-rf', os.path.join(HERE, f'templates/{template}/'), project_dir)
    for f in sh.find(project_dir, '-name', '*.sh'):
        sh.sed('-i', '', '-e', f's/proj/{project_name}/g', f.strip())
    for f in sh.find(project_dir, '-name', '*.yaml'):
        sh.sed('-i', '', '-e', f's/proj/{project_name}/g', f.strip())
    for f in sh.find(project_dir, '-name', 'Dockerfile*'):
        sh.sed('-i', '', '-e', f's/proj/{project_name}/g', f.strip())


@cli.command()
def list():
    templates = get_templates()
    for t in templates:
        print(t)


if __name__ == '__main__':
    cli()
