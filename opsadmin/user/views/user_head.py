# -*- coding: UTF-8 -*-
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils import timezone
from opsadmin import settings
import os
from PIL import Image
from user.models import user
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import random

class head_pic_set(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('user:login')
    template_name = 'user/user_head.html'

    def get_context_data(self, **kwargs):
        context = super(head_pic_set,self).get_context_data(**kwargs)
        file_dirs = "%s/static/dist/img/local/"%settings.BASE_DIR
        context['head_pic_dict'] = {}
        for root,dirs,files in os.walk(file_dirs):
            context['head_pic_list'] = files

            if len(files) % 4 == 0:
                context['head_pic_page'] = range(1,int(len(files) / 4)+1)
            else:
                context['head_pic_page'] = range(1,int(len(files) / 4 + 2))
        for i in context['head_pic_page']:
            context['head_pic_dict']['%s'%i] = context['head_pic_list'][(i-1)*4:i*4]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user_img_location'] = request.user.get_user_img
        context['random_num'] = random.randint(10,1000)
        return self.render_to_response(context)

def local_head(avatar_file=None,username=None):
    user_pic_path = "%s/static/dist/img/user"%settings.BASE_DIR
    if not os.path.isdir(user_pic_path):
        os.makedirs(user_pic_path)

    pic_name = "%s-temp"%(username)

    with open(os.path.join(user_pic_path,pic_name),'wb') as f:
        for chunk in avatar_file.chunks():
            f.write(chunk)

    return {'pic_file_path':os.path.join(user_pic_path,pic_name),'pic_dir':user_pic_path}

def cut_out_pic(top=None,buttom=None,left=None,right=None,pic_file_path=None,pic_dir=None,username=None):
    im = Image.open(pic_file_path)
    crop_im = im.convert("RGBA").crop((left, top, right, buttom)).resize((64, 64), Image.ANTIALIAS)
    out = Image.new('RGBA', crop_im.size, (255, 255, 255))
    out.paste(crop_im, (0, 0, 64, 64), crop_im)
    out.save("%s/%s.png"%(pic_dir,username))
    user.User.objects.filter(username=username).update(user_img="dist/img/user/%s.png"%username,uer_absolute_img="%s/%s.png"%(pic_dir,username))





@method_decorator(csrf_exempt, name='dispatch')
class head_pic_update(LoginRequiredMixin,View):
    login_url = reverse_lazy('user:login')

    def post(self,request, *args, **kwargs):
        top = int(float(request.POST['avatar_y']))
        buttom = top + int(float(request.POST['avatar_height']))
        left = int(float(request.POST['avatar_x']))
        right = left + int(float(request.POST['avatar_width']))
        if request.FILES.__contains__('avatar_file'):
            if request.user.get_absolute_user_img != '':
                os.remove(request.user.get_absolute_user_img)
            avatar_file = request.FILES['avatar_file']
            pic_dict = local_head(avatar_file=avatar_file, username=request.user)
            cut_out_pic(top=top,buttom=buttom,left=left,right=right,pic_file_path=pic_dict['pic_file_path'],pic_dir=pic_dict['pic_dir'],username=request.user)
            os.remove(pic_dict['pic_file_path'])



        elif request.POST.get('avatar_online') != '':
            online_pic_path = request.POST.get('avatar_online')
            if request.user.get_absolute_user_img != '':
                os.remove(request.user.get_absolute_user_img)
            online_pic_absolute_path = "%s%s"%(settings.BASE_DIR,online_pic_path)
            cut_out_pic(top=top,buttom=buttom,left=left,right=right,pic_file_path=online_pic_absolute_path,pic_dir="%s/static/dist/img/user"%settings.BASE_DIR,username=request.user)
            user.User.objects.filter(username=request.user).update(update_description='用户选用了在线头像图片来修改头像图片'.encode('utf-8'),UpdateTime=timezone.now())
        else:
            return HttpResponse(False)


        return HttpResponse(True)


