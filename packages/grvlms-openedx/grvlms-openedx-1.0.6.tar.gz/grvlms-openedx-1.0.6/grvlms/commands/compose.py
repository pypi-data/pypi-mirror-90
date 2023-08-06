import click

from .. import config as grvlms_config
from .. import fmt
from .. import scripts
from .. import utils


class ScriptRunner(scripts.BaseRunner):
    def __init__(self, root, config, docker_compose_func):
        super().__init__(root, config)
        self.docker_compose_func = docker_compose_func

    def exec(self, service, command):
        opts = [] if utils.is_a_tty() else ["-T"]
        self.docker_compose_func(
            self.root, self.config, "exec", *opts, service, "sh", "-e", "-c", command
        )


@click.command(help="Update docker images")
@click.pass_obj
def pullimages(context):
    config = grvlms_config.load(context.root)
    context.docker_compose(context.root, config, "pull")


@click.command(help="Run all or a selection of configured Open edX services")
@click.option("-d", "--detach", is_flag=True, help="Start in daemon mode")
@click.argument("services", metavar="service", nargs=-1)
@click.pass_obj
def start(context, detach, services):
    command = ["up", "--remove-orphans"]
    if detach:
        command.append("-d")

    config = grvlms_config.load(context.root)
    context.docker_compose(context.root, config, *command, *services)


@click.command(help="Stop a running platform")
@click.argument("services", metavar="service", nargs=-1)
@click.pass_obj
def stop(context, services):
    config = grvlms_config.load(context.root)
    context.docker_compose(context.root, config, "rm", "--stop", "--force", *services)


@click.command(
    short_help="Reboot an existing platform",
    help="This is more than just a restart: with reboot, the platform is fully stopped before being restarted again",
)
@click.option("-d", "--detach", is_flag=True, help="Start in daemon mode")
@click.argument("services", metavar="service", nargs=-1)
def reboot(detach, services):
    stop.callback(services)
    start.callback(detach, services)


@click.command(
    short_help="Restart some components from a running platform.",
    help="""Specify 'openedx' to restart the lms, cms and workers, or 'all' to
restart all services. Note that this performs a 'docker-compose restart', so new images
may not be taken into account. It is useful for reloading settings, for instance. To
fully stop the platform, use the 'reboot' command.""",
)
@click.argument("services", metavar="service", nargs=-1)
@click.pass_obj
def restart(context, services):
    config = grvlms_config.load(context.root)
    command = ["restart"]
    if "all" in services:
        pass
    else:
        for service in services:
            if "openedx" == service:
                if config["ACTIVATE_LMS"]:
                    command += ["lms", "lms-worker"]
                if config["ACTIVATE_CMS"]:
                    command += ["cms", "cms-worker"]
            else:
                command.append(service)
    context.docker_compose(context.root, config, *command)


@click.command(
    short_help="Run a command in a new container",
    help="This is a wrapper around `docker-compose run`. Any option or argument passed to this command will be forwarded to docker-compose. Thus, you may use `-v` or `-p` to mount volumes and expose ports.",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("args", nargs=-1, required=True)
@click.pass_obj
def run(context, args):
    config = grvlms_config.load(context.root)
    command = ["run", "--rm"]
    if not utils.is_a_tty():
        command.append("-T")
    context.docker_compose(context.root, config, *command, *args)


@click.command(
    short_help="Run a command in a running container",
    help="This is a wrapper around `docker-compose exec`. Any option or argument passed to this command will be forwarded to docker-compose. Thus, you may use `-e` to manually define environment variables.",
    context_settings={"ignore_unknown_options": True},
    name="exec",
)
@click.argument("args", nargs=-1, required=True)
@click.pass_obj
def execute(context, args):
    config = grvlms_config.load(context.root)
    context.docker_compose(context.root, config, "exec", *args)


@click.command(help="Initialise all applications")
@click.pass_obj
def init(context):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    scripts.initialise(runner)


@click.pass_obj
def initialise_plugin(context, param):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    if param == "init":
        scripts.initialise_plugin(runner, "init")
    else:
        scripts.initialise_plugin(runner, "pre-init")


@click.command(
    short_help="Manually trigger hook (advanced users only)",
    help="""
Manually trigger a hook for a given plugin/service. This is a low-level command
that is convenient when developing new plugins. Ex:

    grvlms local hook mysql hooks mysql init
    grvlms local hook discovery discovery hooks discovery init""",
    name="hook",
)
@click.argument("service")
@click.argument("path", nargs=-1)
@click.pass_obj
def run_hook(context, service, path):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    fmt.echo_info(
        "Running '{}' hook in '{}' container...".format(".".join(path), service)
    )
    runner.run(service, *path)


@click.command(help="View output from containers")
@click.option("-f", "--follow", is_flag=True, help="Follow log output")
@click.option("--tail", type=int, help="Number of lines to show from each container")
@click.argument("service", nargs=-1)
@click.pass_obj
def logs(context, follow, tail, service):
    command = ["logs"]
    if follow:
        command += ["--follow"]
    if tail is not None:
        command += ["--tail", str(tail)]
    command += service
    config = grvlms_config.load(context.root)
    context.docker_compose(context.root, config, *command)


@click.command(help="Create an Open edX user and interactively set their password")
@click.option("--superuser", is_flag=True, help="Make superuser")
@click.option("--staff", is_flag=True, help="Make staff user")
@click.option(
    "-p",
    "--password",
    help="Specify password from the command line. If undefined, you will be prompted to input a password",
)
@click.argument("name")
@click.argument("email")
@click.pass_obj
def createuser(context, superuser, staff, password, name, email):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    runner.check_service_is_activated("lms")
    command = scripts.create_user_command(
        superuser, staff, name, email, password=password
    )
    runner.exec("lms", command)


@click.command(
    help="Set a theme for a given domain name. To reset to the default theme , use 'default' as the theme name."
)
@click.argument("theme_name")
@click.argument("domain_names", metavar="domain_name", nargs=-1)
@click.pass_obj
def settheme(context, theme_name, domain_names):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    for domain_name in domain_names:
        scripts.set_theme(theme_name, domain_name, runner)


@click.command(help="Import the demo course")
@click.pass_obj
def importdemocourse(context):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    fmt.echo_info("Importing demo course")
    scripts.import_demo_course(runner)


@click.command(help="Delete the course")
@click.argument("course_id", metavar="COURSE_ID", required=True)
@click.pass_obj
def deletecourse(context, course_id):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    runner.check_service_is_activated("cms")
    command = scripts.delete_course(course_id)
    runner.exec("cms", command)
    

@click.command(help="List all the courses")
@click.pass_obj
def listcourses(context):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    runner.check_service_is_activated("cms")
    command = scripts.listcourses()
    runner.exec("cms", command)


def add_commands(command_group):
    command_group.add_command(pullimages)
    command_group.add_command(start)
    command_group.add_command(stop)
    command_group.add_command(restart)
    command_group.add_command(reboot)
    command_group.add_command(run)
    command_group.add_command(execute)
    command_group.add_command(init)
    command_group.add_command(logs)
    command_group.add_command(createuser)
    command_group.add_command(importdemocourse)
    command_group.add_command(settheme)
    command_group.add_command(deletecourse)
    command_group.add_command(listcourses)
    # command_group.add_command(run_hook) # Disabled for now
