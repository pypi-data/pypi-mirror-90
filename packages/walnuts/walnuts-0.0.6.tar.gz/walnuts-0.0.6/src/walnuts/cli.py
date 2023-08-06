import os
import shutil
import sys

import click
from click import echo, style

from .execute import run_test

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def mkdir_project(project_name):
    if os.path.exists(project_name) and os.path.isdir(project_name):
        echo(style("创建失败, %s已存在" % project_name, fg='red'))
        sys.exit(1)
    try:
        os.mkdir(project_name)
    except OSError as e:
        echo(style("创建 %s 失败, %s" % (project_name, str(e)), fg='red'))
        sys.exit(1)


def get_project_path(project_name):
    return os.path.join(os.getcwd(), project_name)


def generate_project(project_name):
    echo(style('开始创建%s项目' % project_name, fg='red'))
    mkdir_project(project_name)
    project_path = get_project_path(project_name)
    templates_file_list = os.listdir(TEMPLATES_DIR)

    echo(style('开始渲染...', fg='green'))
    for f in templates_file_list:
        try:
            src = os.path.join(TEMPLATES_DIR, f)
            dst = os.path.join(project_path, f)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

            echo(style('生成 %-32s ' % f, fg='green') +
                 style('[√]', fg='blue'))
        except Exception:
            echo(style('生成 %-32s ' % f, fg='red') +
                 style('[×]\n', fg='blue'))
            raise Exception
    echo(style('生成成功,请使用编辑器打开该项目', fg='red'))


def validate_project_name(ctx, argument, value):
    if not value or ' ' in value:
        raise click.BadParameter("项目名称中不能含有空格")
    return value


@click.group()
@click.version_option()
def walnuts_cli():
    """
     walnuts是一个接口测试工具，功能不断完善中
    """


@walnuts_cli.command()
@click.pass_context
@click.option('--project-name', prompt=click.style("请输入项目名称,如order-api-test", fg='green'),
              callback=validate_project_name, help="请输入项目名称,如order-api-test")
def init(ctx, project_name):
    """
    生成接口测试项目

    使用方法:
        $ walnuts init
    """
    generate_project(project_name)


@walnuts_cli.command()
@click.pass_context
def run(ctx):
    """
    运行测试

    使用方法:
        $ walnuts run
    """
    run_test()


if __name__ == '__main__':
    walnuts_cli()
