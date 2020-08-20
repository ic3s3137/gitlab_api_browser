import sys
import requests
import json
import os
import base64
import chardet
from urllib.parse import quote


get_users_api = "{url}/api/v4/users"
list_projects_api = "{url}/api/v4/projects?simple=true&page={page}&per_page={per_page}&{search}"
list_dirs_api = "{url}/api/v4/projects/{projects_id}/repository/tree?path={path}"
check_file_api = "{url}/api/v4/projects/{projects_id}/repository/blobs/{blob}/raw"
download_file_api = "{url}/api/v4/projects/{projects_id}/repository/files/{path}?ref=master"
save_dir = "download"


def list_project(search=""):
    target = list_projects_api.format(url=url,search=search,page=page,per_page=per_page)   
    rs = requests.get(target,headers=headers)
    Projects = json.loads(rs.text)
    for p in Projects:
        print("id:",p['id'])
        print("desc:",p['description'])
        print("name:",p['name'])
        print("name_with_namespace",p['name_with_namespace'])
        print("path:",p['path'])
        print("created:",p['created_at'])
        print("last_activity:",p['last_activity_at'])
        print("===========================================")

def list_dir(path="",display=True):
    path = path.strip("/")
    if not (path in project_DIR.keys()):
        if path == "*":
            path = ""
        target = list_dirs_api.format(url=url,projects_id=project_ID,path=path)
        rs = requests.get(target,headers=headers)
        Dir = json.loads(rs.text)
        project_DIR[path] = Dir
    else:
        Dir = project_DIR[path]
    if not isinstance(Dir, list):
        print(Dir)
        return True
    if display != True:
        return True
    for d in Dir:
        print("id:",d['id'])
        print("name:",d['name'])
        print("type:",d['type'])
        print("--------------------------------")
    
def check_file(path=""):
    blob = None
    if len(path.split("/")) != 1:
            mdir,mfile = path.rsplit("/",1)
    else:
        mdir = ""
        mfile = path

    if not (mdir in project_DIR.keys()):
        list_dir(path=mdir,display=False)

    for b in project_DIR[mdir]:
        if b['name'] == mfile:
            blob = b['id']
            break
    if blob  == None:
        print("没有该文件")
        return False
    target = check_file_api.format(url=url,projects_id=project_ID,blob=blob)
    rs = requests.get(target,headers=headers)
    print(rs.text)

def download_single_file(path=""):
    path = path.strip("/")
    if os.path.exists(save_dir+"/"+project_ID+"/"+path):
        print(path,"existed!")
        return True
    if len(path.split("/")) != 1:
        mdir,mfile = path.rsplit("/",1)
    else:
        mdir = ""
        mfile = path
    if not os.path.exists(save_dir+"/"+project_ID+"/"+mdir):
            os.makedirs(save_dir+"/"+project_ID+"/"+mdir)
    print("Download",path,"......",end="")
    target = download_file_api.format(url=url,projects_id=project_ID,path=quote(path,'utf-8'))
    rs = requests.get(target,headers=headers)
    downloadfile = json.loads(rs.text)
    content = downloadfile['content']
    content = base64.b64decode(content)
    fp = open(save_dir+"/"+project_ID+"/"+path,"wb+")
    fp.write(content)
    fp.close()
    print("completed")

def download_file(path=""):
    path = path.strip("/")
    if len(path.split("/")) != 1:
        mdir,mfile = path.rsplit("/",1)
    else:
        mdir = ""
        mfile = path
    if not(mdir in project_DIR.keys()):
        list_dir(mdir,display=False)
    for f in project_DIR[mdir]:
        if f['name'] == mfile:
            if f['type'] == 'blob':
                download_single_file(path)
            else:
                list_dir(path,display=False)
                for nf in project_DIR[path]:
                    download_file(path+"/"+nf['name'])
            break



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python gitlat_browser.py <url> <secret>")
        exit(1)

    url = sys.argv[1]
    secret = sys.argv[2]
    Project = ""
    Dir = ""
    Location = ""
    project_ID = ""
    project_DIR = {}
    per_page = '20'
    page = '1'
    search = ""

    headers = {"PRIVATE-TOKEN":secret}
    while True:
        cmd = input("\033[35m"+"Project "+project_ID+" >>> \033[0m").strip().split(" ")
        if cmd[0] == 'quit':
            exit(1)
        elif cmd[0] == 'help':
            print("list")
            print("id [project_id]")
            print("dir [dir]")
            print("cat [filename]")
            print("dl [path/file]")
            print("dlpj [id]")
            print("n")
            print("quit")
            continue
        elif cmd[0] == 'list':
            if len(cmd) == 2:
                search = cmd[1]
                list_project(search)
            else:
                search = ""
                list_project()
        elif cmd[0] == 'id':
            if len(cmd) != 2:
                print("id [project_id]")
                continue
            else:
                if cmd[1] != project_ID:
                    project_DIR = {}
                project_ID = cmd[1]
                list_dir()
        elif cmd[0] == 'dir':
            if len(cmd) != 2:
                print("dir [dir]")
                continue
            else:
                if cmd[1] == '/':
                    list_dir()
                else:
                    list_dir(path=cmd[1])
        elif cmd[0] == 'cat':
            if len(cmd) != 2:
                print("cat [filename]")
                continue
            else:
                check_file(cmd[1])
        elif cmd[0] == 'dl':
            if len(cmd) != 2:
                print("dl [path/file]")
                continue
            else:
                download_file(cmd[1])
        elif cmd[0] == 'dlpj':
            if len(cmd) != 2:
                print("dlpj [id]")
                continue
            else:
                project_ID = cmd[1]
                list_dir(path="*",display=False)
                for f in project_DIR[""]:
                    download_file(f['name'])
        elif cmd[0] == 'n':
            page = str(int(page)+1)
            list_project(search)
        elif cmd[0] == 'l':
            page = str(int(page)-1)
            list_project(search)
        elif cmd[0] == 'p':
            if len(cmd) != 2:
                print("p [page]")
                continue
            else:
                page = cmd[1]
                list_project(search)
        elif cmd[0] == 'limit':
            if len(cmd) != 2:
                print("limit [per_page]")
                continue
            else:
                per_page = cmd[1]
 
