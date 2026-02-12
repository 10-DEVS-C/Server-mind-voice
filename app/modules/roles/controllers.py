from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas import RoleSchema
from .services import RoleService

blp = Blueprint("roles", __name__, description="Operations on roles")

@blp.route("/")
class RoleList(MethodView):
    @blp.response(200, RoleSchema(many=True))
    def get(self):
        """List all roles"""
        return RoleService.get_all()

    @blp.arguments(RoleSchema)
    @blp.response(201, RoleSchema)
    def post(self, new_data):
        """Create a new role"""
        role_id = RoleService.create(new_data)
        return RoleService.get_by_id(role_id)

@blp.route("/<string:role_id>")
class RoleResource(MethodView):
    @blp.response(200, RoleSchema)
    def get(self, role_id):
        """Get role by ID"""
        role = RoleService.get_by_id(role_id)
        if not role:
            abort(404, message="Role not found")
        return role

    @blp.arguments(RoleSchema)
    @blp.response(200, RoleSchema)
    def put(self, update_data, role_id):
        """Update existing role"""
        if not RoleService.update(role_id, update_data):
            abort(404, message="Role not found")
        return RoleService.get_by_id(role_id)

    @blp.response(204)
    def delete(self, role_id):
        """Delete role"""
        if not RoleService.delete(role_id):
            abort(404, message="Role not found")
        return ""
