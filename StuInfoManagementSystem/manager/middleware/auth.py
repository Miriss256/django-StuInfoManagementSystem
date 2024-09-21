from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect


class AuthMiddleware(MiddlewareMixin):
    """ 检验是否有cookies """
    
    def process_request(self,request):
        if request.path_info in ["/manager/login/","/manager/image/code/"]:
            return
        
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        
        return redirect("/manager/login/")