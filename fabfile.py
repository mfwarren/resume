from fabric.api import *

#Fabric 0.9.0 compatible
# usages: fab prod deploy

REMOTE_HG_PATH = '/home/halotis/bin/hg'

def prod():
    """Set the target to production."""
    env.user = 'halotis'
    env.hosts = ['halotis.webfactional.com']
    env.remote_app_dir = 'webapps/resume'
    env.remote_push_dest = 'ssh://halotis@halotis.webfactional.com/%s' % env.remote_app_dir
    env.tag = 'production'

    
def deploy():
    """Deploy the site.

    This will tag the repository, and push changes to the remote location.
    """
    require('hosts', provided_by=[prod, ])
    require('remote_app_dir', provided_by=[prod, ])
    require('remote_push_dest', provided_by=[prod, ])
    require('tag', provided_by=[prod, ])

    local("hg tag --force %s" % env.tag)
    local("hg push %s --remotecmd %s" % (env.remote_push_dest, REMOTE_HG_PATH))
    run("cd %s; hg update -C %s" % (env.remote_app_dir, env.tag))


