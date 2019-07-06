from .models import UserModel


def get_user(request):
    u_id = request.session.get("u_id")
    if u_id:
        u = UserModel.objects.get(id=u_id)
        return {"u": u}
    else:
        return {}



