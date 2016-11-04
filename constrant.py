#encoding: utf-8

class Const:
    class ConstError( TypeError ): pass
    class ConstCaseError( ConstError ): pass

    def __setattr__( self, name, value ):
        if name in self.__dict__:
            raise self.ConstError( "can't change const %s" % name )
        if not name.isupper():
            raise self.ConstCaseError( 'const name "%s" is not all uppercase' % name )
        self.__dict__[name] = value

# import sys
# sys.modules[__name__] = Const()

MAIL_WORDS = Const()
MAIL_WORDS.TELEGRAPH_CONTENT_TYPE = 'octet-stream'
MAIL_WORDS.TELEGRAPH_FILENAME = 'telegraph'

