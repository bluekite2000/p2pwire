from django.conf import settings

for a in settings.INSTALLED_APPS:
    try:
        __path__.extend(__import__(a + '.templatetags', {}, {}, ['']).__path__)
    except ImportError:
        pass
VERSION = (0, 8, 0, 'alpha', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = "%s %s" % (version, VERSION[3])
            if VERSION[4] != 0:
                version = '%s %s' % (version, VERSION[4])
    return version
