from django.views.generic import View
from django.core.cache import cache
from django.shortcuts import render_to_response,HttpResponseRedirect
from opsadmin import settings
import base64
import hashlib
from django.template.context_processors import csrf
from django.shortcuts import reverse
from ..models.user import User
from ..UserMixin import AdminAuthorizedMixin

class AdminAuthorized(AdminAuthorizedMixin,View):

    def get(self,request,name):
        try:
            name = str(base64.b64decode(bytes(name,encoding='utf-8')),encoding='utf-8')
        except:
            return render_to_response('user/deny.html')

        if cache.has_key('%s'%(name)):

            return render_to_response('user/admin_authorized.html',csrf(request))

        return render_to_response('user/deny.html')


    def post(self,request,name):
        data = request.POST
        name = str(base64.b64decode(bytes(name, encoding='utf-8')), encoding='utf-8')
        if data['permit'] == 'yes' and (cache.has_key('%s'%(name)) and dict(cache.get('%s'%(name))).get('random_code') == hashlib.md5(str(data['random_code']).encode('utf-8')).hexdigest()):
            User.objects.filter(username=name).update(admin_active=True)
            cache.set('%s'%(name),dict({'sign':True}),30 * 60)
            return HttpResponseRedirect(reverse('dashboard'))
        elif cache.has_key('%s'%(name)) and dict(cache.get('%s'%(name))).get('random_code') != hashlib.md5(str(data['random_code']).encode('utf-8')).hexdigest():
            data = {}
            data['error'] = '随机验证码出错'
            data.update(csrf(request))
            return render_to_response('user/admin_authorized.html', data)

        elif data['permit'] == 'no' and (cache.has_key('%s'%(name)) and dict(cache.get('%s'%(name))).get('random_code') == hashlib.md5(str(data['random_code']).encode('utf-8')).hexdigest()):
            User.objects.filter(username=name).update(user_role='User')
            cache.set('%s' % (name), dict({'sign': True}), 30 * 60)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render_to_response('user/deny.html')
