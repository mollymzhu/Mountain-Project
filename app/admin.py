from flask import redirect, url_for, g
from flask_admin.contrib.sqla import ModelView

class AdminModelView(ModelView):
    def is_accessible(self):
        """Return True if user is logged in and an administrator
           ****You will probably want to limit access to administrators****
        """
        return g.user is not None and g.user.is_authenticated # and g.user.eid in ('eid123')

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if user doesn't have access"""
        return redirect(url_for('login', next=request.url))
