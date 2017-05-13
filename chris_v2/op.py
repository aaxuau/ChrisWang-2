class Operator(object):

    global wholeHeadings
    wholeHeadings = []

    def _getReadme(self, name,auth=None):
        import requests
        
        get_url = ''.join(["https://api.github.com/repos/",name,"/readme"])

        print("getting the api from here")
        # user_agent = {'User-agent': 'Awesome-Octocat-App'}

        r = requests.get(get_url,auth=('a1699186', '1699186a'))

        # return r
        if "download_url" in r.json():
            url = (r.json()['download_url'])
            r_readme = r = requests.get(url)
            r_readme.text.replace("[","");
            r_readme.text.replace("]","");
            return r_readme.text
        else:
            return None

    def getURLNum(self, text,auth=None):
        import re

        if not text:
            return None

        myfinding = []
        findings = re.findall(r"[^\!]\[[\s\S]*?\]\([\s\S]*?\)",text)
        for finding in findings:

            newfinding = re.findall(r"[a-zA-z]+://[^\s\)]*",finding)
            if len(newfinding)>0:
                myfinding.append(newfinding[0])
        
        return len(myfinding)

    def getURLContents(self, text,auth=None):
        import re

        if not text:
            return None

        myfinding = []
        findings = re.findall(r"[^\!]\[[\s\S]*?\]\([\s\S]*?\)",text)
        for finding in findings:

            newfinding = re.findall(r"[a-zA-z]+://[^\s\)]*",finding)
            if len(newfinding)>0:
                myfinding.append(newfinding[0])
        
        return myfinding

        
    

    def getPic(self, text,auth=None):
        import re

        if not text:
            return None

        #finding = re.findall(r"\!\[[\s\S]*?\]\([\s\S]*?\)",text)
        finding = re.findall(r"png|jpg|PNG|JPG|gif|GIF",text)

        return len(finding)

    def getHeadingNum(self, text,auth=None):
        import re
       
        if not text:
            return None

        finding1 = re.findall(r"[\#]+[\s]+[\s\S]*?\n",text)
        # finding2 = re.findall(r"\n(--*)\n",text)
        
        # return len(finding1)+len(finding2)
        return len(finding1)

    def getHeadingContents(self, text,auth=None):
        global wholeHeadings
        
        import re
        if not text:
            return None
        contents1 = re.findall(r"[\#]+[\s]+[\s\S]*?\n",text)
        # contents2 = re.findall(r"\n(--*)\n",text)

        if len(contents1) == 0:
            return 0
        else:
            for num in range(0,len(contents1)): 
                a = contents1[num].replace("#", "")
                b = a.replace("\n", "")
                c = b.replace("&(.*);", "")
                wholeHeadings.append(c) 

        # if len(contents2) == 0:
        #     return 0
        # else:
        #     for num in range(0,len(contents2)): 
        #         a = contents2[num].replace("#", "")
        #         b = a.replace("\n", "")
        #         c = b.replace("&(.*);", "")
        #         wholeHeadings.append(c) 
            return wholeHeadings

    def getProject(self,auth=None):
        import random
        import requests

        test = set()
        ret = []
        
        id = random.randint(1, 70000000)
        url = ''.join(["https://api.github.com/repositories?since=",str(id)])
        r = requests.get(url,auth=auth)

        result = [r.json()[0]["full_name"].split('/'),r.json()[0]['id']]
        return result

  
       

    def getResult(self, auth=None):
       

        global wholeHeadings
        wholeHeadings = []
        emptyFile = 0;
        ret =[]
        count = 0
        
        while True:
            pro = self.getProject(auth=auth)
            name=pro[0][0]+'/'+pro[0][1]
            text = self._getReadme(name)
            if type(text) is str:
                if text.find("--\n") == -1:
                    if text.find("==\n") == -1:
                        break

        heading = self.getHeadingNum(text,auth=auth)
        if heading == None:
            emptyFile = emptyFile+1
        ret1 = {
                'no':1,
                'id':pro[1],
                'name':name,
                'urlNum': self.getURLNum(text,auth=auth),
                'pic': self.getPic(text,auth=auth),
                'heading':heading,
                'headingContent':self.getHeadingContents(text,auth=auth),
                'urlcontents':self.getURLContents(text,auth=auth),
                'text':text
            }
        ret.append(ret1)


        ret3 = []
        for heading in wholeHeadings:

            myNum = wholeHeadings.count(heading)
            ele = "<td>"+str(heading)+"</td><td>"+str(myNum)+"</td>"

            if ele in ret3:
                continue
            else:
                ret3.append(ele)

        print(emptyFile)
        ret3.append("<td>empty file</td><td>"+str(emptyFile)+"</td>")
        # ret.append(ret3)        


        return ret


   