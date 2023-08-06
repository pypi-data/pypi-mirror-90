#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""

import os
import sys
import json
import string
import random
import shutil
from . import vbuild


def random_id(length=5, isTest=True):
    if isTest:
        return "test"
    return ''.join(random.sample(string.ascii_lowercase, length))


class SimpleHead():
    def __init__(self, title="", icon="", StyleLink=[], ScriptLink=[], loadJs=True):
        self.title = title
        self.icon = icon
        self.StyleLink = StyleLink
        if loadJs:
            self.ScriptLink = ["https://cdn.jsdelivr.net/npm/vue/dist/vue.js",
                               "https://unpkg.com/vue-router/dist/vue-router.js"] + ScriptLink

    def head(self):
        _s = f"""
            <meta charset="UTF-8">
            <title>{self.title if self.title else "Vue"}</title>
            <link rel="icon" href="{self.icon if self.icon else "https://cn.vuejs.org/images/icons/android-icon-144x144.png"}">
        """
        for i in list(self.ScriptLink):
            _s += f"""
                <script type="text/javascript" src="{i}"></script>
                """
        for i in list(self.StyleLink):
            _s += f"""
                <link rel="stylesheet" type="text/css" href="{i}">
                """

        return _s

    def __str__(self):

        return f"""
        </head>
            {self.head()}
        </head>
        """


class SimpleBody():
    def __init__(self, router: list, loadComponents: list, **kwargs):
        """

        :param router:
        :param ChildrenComponentsPath:
        :param kwargs:
        """
        self.router = router
        self.loadComponents = loadComponents

    def body(self):

        _s = str(vbuild.render(*self.loadComponents))
        temp = ""
        for i in self.loadComponents:
            try:
                name = i.split("/")[-1].replace(".vue", "")
            except:
                raise Exception("Please give .vue file")
            temp += f"""
                <{name}></{name}>
                """

        routes = []
        for i in self.router:
            mid = {}
            for k, v in i.items():
                if ".vue" in v:
                    name = v.split("/")[-1].replace(".vue", "")
                    mid[k] = "@@@@@%s@@@@@" % name
                else:
                    mid[k] = v
            routes.append(mid)
        router = json.dumps(routes).replace('"@@@@@', "").replace('@@@@@"', "")
        _id = ''.join(random.sample(string.ascii_lowercase, 5))
        _s += """
        <div id="%s">
            <router-view></router-view>
        </div>
        <script>
        const routes = %s;
        const router = new VueRouter({routes})
        new Vue({el:"#%s",router: router})
        </script>
        """ % (_id, router, _id)
        return _s

    def __str__(self):

        return f"""
        <body>
            {self.body()}
        </body>
        """


class SimpleHTML():
    def __init__(self, staticDir="./", componentsDir="./", htmlDir="./"):
        self.staticDir = staticDir
        self.componentsDir = componentsDir
        self.htmlDir = htmlDir
        self.imgPath = self.dealPath(self.staticDir + "/static/img/")
        self.cssPath = self.dealPath(self.staticDir + "/static/css/")
        self.jsPath = self.dealPath(self.staticDir + "/static/js/")
        self.allcssPath = self.dealPath(self.staticDir + "/all/css/")
        self.alljsPath = self.dealPath(self.staticDir + "/all/js/")
        self.componentsPath = self.dealPath(self.staticDir + "/components/")
        self.htmlPath = self.dealPath(self.htmlDir + "/html/")
        self.indexHtmlPath = "index.html"

    def init_project(self):
        self.__createDir__(self.imgPath)
        self.__createDir__(self.cssPath)
        self.__createDir__(self.jsPath)
        self.__createDir__(self.componentsPath)
        self.__createDir__(self.htmlPath)

    def __createDir__(self, path):
        try:
            os.makedirs(path)
        except:
            pass

    def dealPath(self, path):
        return path.replace("//", "/")

    def vue2html(self, head: SimpleHead, body: SimpleBody):
        _s = f"""
            <!DOCTYPE html>
            <html lang="en" >
            {str(head)}
            {str(body)}
            </html>
        """

        with open(self.dealPath(self.htmlDir + self.indexHtmlPath), "w", encoding="utf8") as f:
            f.write(_s)
        print("成功生成文件 %s" % self.dealPath(self.htmlDir + self.indexHtmlPath))


class HTML(SimpleHTML):
    mainjs = "./main.js"

    def init_project(self):
        self.__createDir__(self.imgPath)
        self.__createDir__(self.cssPath)
        self.__createDir__(self.jsPath)
        self.__createDir__(self.componentsPath)
        self.__createDir__(self.allcssPath)
        self.__createDir__(self.alljsPath)
        self.__check_main__()

    def __check_main__(self):
        if not os.path.exists(self.mainjs):
            with open(self.mainjs, "w", encoding="utf8") as f:
                f.write("""
const routes = [
    // {"path": "/", "component": login},
    
    ];
const router = new VueRouter({
    routes
    });
//router.beforeEach((to, from, next) => {
//      if (to.meta.title) {
//       document.title = to.meta.title;
//      }
//      next();
//     });
new Vue({
    el:"#app",   //不可更改
    router: router,
    });
""")

    def write_script(self, name, content):
        with open(name, "w", encoding="utf8") as f:
            f.write(content)

    def __body__(self, head: SimpleHead, body):
        _s = f"""
<!DOCTYPE html>
<html lang="en" >
{str(head)}
<body>
    <div id="app">
        <router-view></router-view>
    </div>
    {body}

</body>
</html>
                """
        return _s

    def build(self, head: SimpleHead, loadComponents: list, isTest=True):
        shutil.rmtree(self.allcssPath)
        shutil.rmtree(self.alljsPath)
        self.__createDir__(self.allcssPath)
        self.__createDir__(self.alljsPath)
        html = ""
        script = ""
        style = ""
        for i in loadComponents:
            s = vbuild.render(i)
            html += str(s.html + "\n")
            script += str(s.script + "\n")
            style += str(s.style + "\n")
        script_name = self.dealPath(self.jsPath + f"/script-all-{random_id(10, isTest=isTest)}.js").replace("static",
                                                                                                            "all")
        html_name = self.dealPath(self.indexHtmlPath)
        css_name = self.dealPath(self.cssPath + f"/css-all-{random_id(10, isTest=isTest)}.css").replace("static", "all")
        self.write_script(script_name, script)
        self.write_script(css_name, style)
        filenames = os.listdir(self.jsPath)
        body = ""
        for i in filenames:
            name = self.dealPath(self.jsPath + f"/{i}")
            body += f"""<script type="text/javascript" src="{name}"></script>\n"""
        filenames = os.listdir(self.cssPath)
        for i in filenames:
            name = self.dealPath(self.cssPath + f"/{i}")
            body += f"""<link rel="stylesheet" type="text/css" href="{name}">\n"""

        body += f"""<script type="text/javascript" src="{script_name}"></script>\n"""
        body += f"""<link rel="stylesheet" type="text/css" href="{css_name}">\n"""

        body += html
        with open(self.mainjs, "r", encoding="utf8") as f:
            content = f.read()
        body += f"<script>{content}</script>\n"
        self.write_script(html_name, self.__body__(head=head, body=body))
        print("编译成功")
