from django.http import HttpResponse
from django.conf import settings
import os,socket
import logging

logger = logging.getLogger(__name__)
accesslogger = logging.getLogger("access")

# Create your views here.
def postfile(request):
 logip(request)
 if request.method == "POST":    # 请求方法为POST时，进行处理
        result = "" 
        if settings.MEDIA_SIZE==None:
            settings.MEDIA_SIZE=getFolderSize(settings.MEDIA_ROOT)
            logger.info("getFolderSize:"+str(settings.MEDIA_SIZE))
        Files =request.FILES.getlist("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not Files:  
            return HttpResponse("no files for upload!")  
        for  File in Files:
            #检查文件是否存在
            if os.path.exists(os.path.join(settings.MEDIA_ROOT,File.name)):
                logger.info(File.name+" "+str(File.size)+" Fail, File exists")
                result =result+File.name+" "+str(File.size)+" Fail, File exists<br>\n"
            else:
                #检查大小超过限制么
                if (File.size+settings.MEDIA_SIZE>settings.MEDIA_LIMIT_SIZE):
                    logger.info(File.name+" "+str(File.size)+" Fail, Total limit exceeded")
                    result = result+File.name+" "+str(File.size)+" Fail, Total limit exceeded<br>\n"
                    continue
                destination = open(os.path.join(settings.MEDIA_ROOT,File.name),'wb+')    # 打开特定的文件进行二进制的写操作  
                for chunk in File.chunks():      # 分块写入文件  
                    destination.write(chunk)  
                destination.close() 
                settings.MEDIA_SIZE+=File.size
                logger.info(File.name+" "+str(File.size)+" Success")
                result =result+File.name+" "+str(File.size)+" Success<br>\n"
        return HttpResponse(result)
 else:
    return HttpResponse("")
 
def upload(request):
 return HttpResponse("""<form enctype="multipart/form-data" action="/postfile/" method="post">  
   <input type="file" multiple="multiple" name="file" /> 
   <input type="submit" value="upload"/>  
</form> """)

def index(request):
  ip=get_host_ip()
  return HttpResponse("welcome! <a href=\"http://"+ip+"\">"+ip+"</a>")
 

def get_host_ip():
    '''获取本机ip'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()

#获取大小
def getFolderSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

#ip记录
def logip(request):
    remote_info = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        remote_info = x_forwarded_for.split(',')[0]
    else:
        remote_info = "n"
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr:
        remote_info += '/' + remote_addr
    accesslogger.info("[%s]" % (remote_info))