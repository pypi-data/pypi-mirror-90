class CertChainResolverException(Exception):
    pass


class ImproperlyFormattedCert(CertChainResolverException):
    pass


class HTTPFailure(CertChainResolverException):
    pass
