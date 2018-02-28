# Hello Flask

## 安装

### Python版本

#### 2.x >= 2.6

需要 Python 2.6 或更高的版本

#### 3.x >= 3.3

需要 Python3.3 或更高的版本（本教程使用 Python 3.6.0 版本）

#### 依赖库

Flask 依赖两个外部库：[Werkzeug](http://werkzeug.pocoo.org/) 和 [Jinja2](http://jinja.pocoo.org/2/) 。 Werkzeug 是一个 WSGI（在 Web 应用和多种服务器之间的标准 Python 接口) 工具集。Jinja2 负责渲染模板。

若是Python 3.x 版本，你需要使用最新且最大版本的 itsdangerous 、 Jinja2 和 Werkzeug 。

### pip 安装

首先，强烈建议使用虚拟环境： [virtualenv](https://virtualenv.pypa.io/en/stable/)  或 [pyenv](https://github.com/pyenv/pyenv)  （具体使用这边就不介绍了，请google或百度相关教程）

然后，pip 安装 Flask

```
pip install Flask
```

最后，除Flask外，会安装一些相关的插件，后续章节会介绍，请自行pip安装



## Hello World

### Simple Output

```python
#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

app.run()
```

保存为 xxx.py 文件后，python运行该 xxx.py文件，浏览器访问 <http://127.0.0.1:5000/> ，你会看见 Hello World 

**简析**

1. 从 Flask 库导入了 [`Flask`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask) 类；这个类的实例将会是我们的 WSGI 应用程序
2. `app = Flask(__name__)`；创建一个该类的实例，第一个参数是应用模块或者包的名称。 如果你使用单一的模块（如本例），你应该使用 `__name__`
3. `@app.route('/')` 使用 [`route()`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask.route) 装饰器定义URL路由；你可以试下更改该参数，如 `@app.route('/hello')` ，此时浏览器访问地址就该是  <http://127.0.0.1:5000/hello> 
4. 每个路由装饰器都会包含一个函数（示例中为 `index()` 函数），该函数返回我们想要显示在用户浏览器中的信息。
5. 用 [`run()`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask.run) 函数来让应用运行在本地服务器上




### Advance

上述示例仅返回了字符串 “Hello World！”，返回体为 Content-Type:text/html；但在实际应用中，简单REST服务需要满足以下三点：

- 返回 json 结构的数据
- 动态路由，即给 URL 添加变量部分
- 增删改查的使用，如 PUT、DELETE、POST 和 GET 等

我们下面就来看下如何解决以上三点需求。

#### jsonify

若要返回 json 数据，可使用 Flask 的 jsonify 函数，详见以下示例：

```python
#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})

app.run()
```

运行后，浏览器访问 <http://127.0.0.1:5000/> ，可见返回体为json` {"msg": "Hello World!"}`，响应头变为 `application/json` 



#### 动态路由

要给 URL 添加变量部分，你可以把这些特殊的字段标记为 `<variable_name>` ， 这个部分将会作为命名参数传递到你的函数。此外，规则可以用 `<converter:variable_name>` 指定一个可选的转换器。

```python
#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Flask',
        'description': 'Simple Demo', 
        'done': False
    }
]

@app.route('/<int:task_id>', methods=['GET'])
def index(task_id):         
    return jsonify({'task': tasks[task_id-1]})

if __name__ == '__main__':
    app.run(debug=True)
```

**注意**：以上仅为示例代码，生产代码要做异常返回的处理；`app.run(debug=True)` 表示开启debug模式  

另，转换器有下面几种：

| converter | 描述             |
| --------- | -------------- |
| int       | 接受整数           |
| float     | 同 int ，但是接受浮点数 |
| path      | 和默认的相似，但也接受斜线  |

#### 增删改查

在之前的实例中我们可见 `@app.route('/')` 装饰器定义了URL路由（默认方式为查GET），同样的，其余的各种请求方式也由该装饰器完成。具体使用方式为通过一个叫做 methods 的参数指定，如下分别对应增删改的方式（POST、DELETE、PUT） 进行了路由绑定：

```python
@app.route('/', methods=['POST'])
@app.route('/', methods=['DELETE'])
@app.route('/', methods=['PUT'])
```

有关HTTP方法，如不了解可参考下方，建议学习Flask前就已经熟悉HTTP协议相关内容。

数据库操作超出本章讨论范围，所以这边简单地以内存进行数据存储操作，示例如下：

```python
#!/usr/bin/env python3

from flask import Flask, jsonify, request


app = Flask(__name__)

tasks = ["Hello World"]

@app.route('/task', methods=['GET'])
def getTask():
    return jsonify({'tasks': tasks})

@app.route('/task', methods=['POST'])
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'miss task'})
    tasks.append(request.json['task'])
    return jsonify({'tasks': tasks})

@app.route('/task', methods=['PUT'])
def resetTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'miss task'})
    tasks[:] = []
    tasks.append(request.json['task'])
    return jsonify({'tasks': tasks})

@app.route('/task', methods=['DELETE'])
def deleteTask():
    tasks[:] = []
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
```

以上示例运行后，需要模拟不同请求方式，建议使用Postman等工具。

P.S 有关请求参数：在 Flask 中有一个 request 变量，这是一个请求上下文的变量，里面包含多个属性是可以用来获取请求参数的，例如上例中的`request.json` ，在此仅提下，有关request的更多使用方式请待后续示例。

本节的目标是让大家初步了解Flask是如何对 GET、POST、PUT 等不同的请求方式做处理的。



## 外部可访问的服务器 & 调试模式

最后，简单说下外部访问服务器配置以及调试模式。

如果你禁用了 debug 或信任你所在网络的用户，你可以简单修改调用 [`run()`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask.run) 的方法使你的服务器公开可用，如下:

```
app.run(host='0.0.0.0')
```

这会让操作系统监听所有公网 IP。

有两种途径来启用调试模式。一种是直接在应用对象上设置:

```
app.debug = True
app.run()
```

另一种是作为 run 方法的一个参数传入:

```
app.run(debug=True)
```

两种方法的效果完全相同。

**注意**：尽管交互式调试器在允许 fork 的环境中无法正常使用（也即在生产服务器上正常使用几乎是不可能的），但它依然允许执行任意代码。这使它成为一个巨大的安全隐患，因此它 **绝对不能用于生产环境** 。



## 示例演示

> 个人原因，IDE用VSCode（由于需要写vue，故前后端开发统一用VSCode）；调试用的是Postman
>
> 以下为动图示例，由于是开篇章节，会比较小白些，后续章节将不再演示。



### 01_HelloWorld.py

1.确认环境；2.本地运行；3.测试请求；

![flask_study_01](http://ftopiablog.ufile.ucloud.com.cn/flask_study_01.gif)



### 02_Rest_Jsonify.py

更改返回体为Json格式；

![flask_study_02](http://ftopiablog.ufile.ucloud.com.cn/flask_study_02.gif)



### 03_Rest_Router.py

动态路由的使用；Debug模式下的报错信息显示；

![flask_study_03](http://ftopiablog.ufile.ucloud.com.cn/flask_study_03.gif)



### 04_Rest_Methods.py

多种请求方式的使用；代码运行后测试演示；

![flask_study_04](http://ftopiablog.ufile.ucloud.com.cn/flask_study_04.gif)