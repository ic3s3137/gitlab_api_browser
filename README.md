# gitlab_api_browser
在只获得gitlab PRIVATE-TOKEN的情况下，调用gitlab api接口，对gitlab所有项目进行浏览，查看，下载

Usage：python gitlab_api_browser.py  <gitlab_url>  <PRIVATE-TOKEN>
  
Project  >>> help

list 显示项目

list [search] 设置符合条件的项目,条件参数参考gitlab api官方文档

id [project_id] 查看对应id的具体项目文件

dir [dir] 查看目录

cat [filename] 查看文件

dl [path/file] 下载文件/或目录,需完整路径

dlpj [id] 下载对应id的整个项目

n 下一页

l 上一页

p [page_num] 跳转到第几页

limit [per_page] 每页显示的项目条数

quit

Project  >>>
  
   
![image](https://github.com/ic3s3137/gitlab_api_browser/blob/master/1.png)
![image](https://github.com/ic3s3137/gitlab_api_browser/blob/master/2.png)
