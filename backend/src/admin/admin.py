from core.models import User

# # from organisation.models import Organisation, OrganisationUser
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.is_active,
        User.is_verified,
        User.is_deleted,
        User.last_login,
    ]


# # class OrganisationAdmin(ModelView, model=Organisation):
# #     column_list = [
# #         Organisation.id,
# #         Organisation.name,
# #         Organisation.description,
# #         Organisation.creator_id,
# #         Organisation.users,
# #         Organisation.creator,
# #     ]


# class OrganisationUserAdmin(ModelView, model=OrganisationUser):
#     column_list = [
#         OrganisationUser.id,
#         OrganisationUser.email,
#         OrganisationUser.organisation,
#     ]


# # class RoleAdmin(ModelView, model=Role):
# #     column_list = [Role.id, Role.name, Role.description]


# # class PermissionAdmin(ModelView, model=Permission):
# #     column_list = [Permission.id, Permission.name, Permission.description]
