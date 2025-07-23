from .admins import admins_routers
from .users import users_routers

routers = (*users_routers, *admins_routers)


