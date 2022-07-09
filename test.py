import random

Mails = [
    {
        "mail": "zkzkao@foxmail.com",
        "auth": "ptypudtvvhlecajj",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2683747644@qq.com",
        "auth": "rewhrnednwjjebig",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2326617964@qq.com",
        "auth": "pxljpyegdjkteaja",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2232565130@qq.com",
        "auth": "ctejvcamfkhediid",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "columbusknight@163.com",
        "auth": "IMZSDHKHDACEZDSY",
        'smtp': "smtp.163.com",
        'counts': 0
    },
    {
        "mail": "ColumbusK@163.com",
        "auth": "EJXNFEVIVTGFHEFR",
        'smtp': "smtp.163.com",
        'counts': 0
    },
]


res = random.choice(Mails)
print(res)
res['counts'] += 1
Mails.remove(res)
print(Mails)
