import owncloud
 
oc_config = dict(
    url = "https://dataccess.getui.com",
    username = "admin",
    password = "SiPU9v#PxyU9jrbv"
)

oc = owncloud.Client(oc_config.get('url'))
oc.login(oc_config.get('username'), oc_config.get('password'))
oc.list('')