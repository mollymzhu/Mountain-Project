from app import db
import ldap

class User(db.Model):
    """ User table to keep track of who is allowed
        to see our webpage, how many times they've logged in,
        and when they last logged in
    """
    __bind_key__ = 'local'
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.String(10), unique=True)
    login_ct = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime())

    def __repr__(self):
        return '<User %r>' % (self.eid)

    @classmethod
    def validate_via_ldap(self, eid, pw):
        """ Take an EID and password
            validate via LDAP
            if this is a valid CapOne user, return true
            otherwise (any error) return False
        """

        # fake admin account for testing only
        if eid == 'admin' and pw == 'pw':
            return self(eid)
        try:
            conn = ldap.initialize('ldap://cof.ds.capitalone.com')
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 1)
            conn.protocol_version = ldap.VERSION3
            conn.simple_bind_s('cof\{0}'.format(eid), pw) #pylint: disable=anomalous-backslash-in-string
            return True
        except Exception, e:
            print
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Diamond(db.Model):
    __tablename__ = 'sjf645_diamond'
    __bind_key__ = 'redshift'
    __table_args__ = {'schema': 'ud_interim'}

    id = db.Column(db.Numeric, primary_key=True)
    carat = db.Column(db.Float)
    color = db.Column(db.String(8))
    clarity = db.Column(db.String(8))
    depth = db.Column(db.Float)
    priceperct = db.Column(db.Float)
    totalprice = db.Column(db.Float)
