# -*- coding: utf-8 -*-
# Özelleştirilmiş Business Hataları için base excepiton classı
class BusinessRuleError(Exception):
    def __init__(self, code: str, message, sub_message: str = None):
        super(BusinessRuleError, self).__init__(message)
        self.code = code or "handler.exception.business_rule_error"
        self.sub_message = sub_message

    @staticmethod
    def get_code(code: str, default: str) -> str:
        if code is None or "":
            return default
        return code


# Forbidden davranışı için Businessdan özelleştimiş exception
class ForbiddenError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.forbidden_handler")
        super(ForbiddenError, self).__init__(code, message, sub_message)


# NotFound davranışı için Businessdan özelleştimiş exception
class NotFoundError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.not_found_error")
        super(NotFoundError, self).__init__(code, message, sub_message)


# 3. parti servis bağlantıları veya davranışları hatası için Businessdan özelleştimiş exception
class ServiceError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.service_error")
        super(ServiceError, self).__init__(code, message, sub_message)


# Şema validasyonu sonucu meydaya gelen hatalar için Validation Exception
class ValidationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.validation_error")
        super(ValidationError, self).__init__(code, message, sub_message)


# Eklenmeye veya güncellenmeye çalışılan veri zaten var ise meydana gelen excepiton türü
class ExistError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.exist_error")
        super(ExistError, self).__init__(code, message, sub_message)


# argüman değeri null geldi ise
class ArgumentNullError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_null_error")
        super(ArgumentNullError, self).__init__(code, message, sub_message)


# argüman gelmedi ise
class ArgumentEmptyError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_empty_error")
        super(ArgumentEmptyError, self).__init__(code, message, sub_message)


# argüman null veya boş geldi ise
class ArgumentNullOrEmptyError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_null_or_empty_error")
        super(ArgumentNullOrEmptyError, self).__init__(code, message, sub_message)


# authentication hatası varsa
class AuthenticationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.authentication_error")
        super(AuthenticationError, self).__init__(code, message, sub_message)


# yetkilendirme hatası varsa
class AuthorizationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.authorization_error")
        super(AuthorizationError, self).__init__(code, message, sub_message)


# sistem kaynaklı hata varsa
class SystemStatusError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.system_status_error")
        super(SystemStatusError, self).__init__(code, message, sub_message)
