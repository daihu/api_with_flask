## TODO API

从本章开始，我们将使用 Flask 围绕一个 TODO 应用提供 REST API 进行讲解。

本章介绍了该APP的需求设计以及简单代码实现（为了方便，本章示例仍使用内存存储），相关知识点如下：

- 使用不同请求方式：GET、POST、PUT、DELETE 进行数据增删改查

- `request.json` 表示请求体是json，请求头需加 `Content-Type: application/json`

  有关请求体 request，具体请参考 [官方Flask教程 —— API Request](http://docs.jinkan.org/docs/flask/api.html#id4)

- 返回 json 结构的数据，`jsonify()` 的使用

> 以上很多知识点上一章 Hello Flask 中都有讲解，如仍不理解，请回炉上一章。
>
> 后续将引入数据库存储，但仍会围绕TODO API，其需求及设计基本不变。



### 需求及设计

我们需要编写的 TODO 应用主要功能有：

- 可以查询所有待办事项
- 可以查看指定待办事项的详情
- 可以增加一项待办事项
- 可以删除一项待办事项
- 可以修改一项待办事项，包括待办内容，添加标记
- 完成待办事项后可以标记为完成




优先设计API（API First Design）体现了BDD的思想，为敏捷开发及测试驱动开发提供了先决条件。

所以，我们在写代码之前，先设计API（若只想快速入门Flask，可选择跳过，直接看代码实现）。

> 设计API时，需要考虑数据结构及数据库表的设计，这也是程序员必备的重要技能。
>
> 另外，基本上不同的公司都有其API的标准和规范，本教程示例基本遵循 RESTful 。
>
> 至于如何做？需要经验的积累。可参考 [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html) 。
>
> 本章暂不引入用户的概念，后续会加入。



**GET		/todo/tasks		获取所有待办事项信息**

请求传参：无

返回示例：

```json
{
    "status": 0,
    "tasks": [
        {
            "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
            "done": false,
            "task_id": 1,
            "title": "Buy groceries"
        },
        {
            "description": "Need to find a good Python tutorial on the web",
            "done": false,
            "task_id": 2,
            "title": "Learn Python"
        }
    ]
}
```



**GET		/todo/task/\<int:task_id\>		获取指定待办事项的信息**

请求传参：URL中需带入task_id，必须为int

返回示例：

```json
{
    "status": 0,
    "task": {
        "description": "Need to find a good Python tutorial on the web",
        "done": false,
        "task_id": 2,
        "title": "Learn Python"
    }
}
```

若对应id的task不存在，则返回：

```json
{
    "err": "Not found."
}
```



**POST		/todo/task		增加一项待办事项**

请求传参：

​	Headers		Content-Type: application/json

​	请求体为Json格式，task为必传项，description为选传项

​	示例：

```json
{
	"task": "Study Flask",
	"description": "make a plan"
}
```

返回示例：

```json
{
    "status": 0,
    "task_id": 3
}
```

若传参错误，则返回：

```json
{
    "err": "Request not Json or miss task"
}
```



**DELETE		/todo/task/\<int:task_id\>		删除一项待办事项**

请求传参：URL中需带入task_id，必须为int

返回示例：

```json
{
    "task_id": 3,
    "msg": "Deleted.",
    "status": 0
}
```

若对应id的task不存在，则返回：

```json
{
    "err": "Not found."
}
```



**PUT		/todo/task/\<int:task_id\>		更改一项待办事项**

> 由于标记为完成也可视为更改项的一种方式，故合并在此API中，实际只是传参不同罢了
>
> 另外，done值为布尔，且仅true值时会变更数据（即可更改为完成，但完成后不可更改状态）

​	Headers		Content-Type: application/json

​	请求体为Json格式，示例一为更改task名称或详细描述；实例二为更改task是否已完成

​	示例一：

```json
{
	"task": "Study Flask Further",
	"description": "modify your plan"
}
```

​	示例二：

```json
{
	"done": true
}
```

返回示例：

```json
{
    "status": 0,
    "task": {
        "description": "modify your plan",
        "done": true,
        "task_id": 3,
        "title": "Study Flask Further"
    }
}
```

若对应id的task不存在，则返回：

```json
{
    "err": "Not found."
}
```



### 代码实现

我们用内存存储来进行简单代码编写（实际会用到数据库存储，且代码一般不会这么处理，这里仅做示例）

> 后续章节会引入数据库，并对代码进行改写及分层规范代码结构

以下代码若熟悉Python的应该很好理解，这边将不对代码做多余的解释。Just Code & Try it. 

```python
#!/usr/bin/env python3

from flask import Flask, jsonify, request


app = Flask(__name__)

tasks = [
    {
        'task_id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'task_id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/tasks', methods=['GET'])
def getTasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/task/<int:task_id>', methods=['GET'])
def getTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        return jsonify({'task': task[0]})


@app.route('/todo/task', methods=['POST'])
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'Request not Json or miss task.'})
    else:
        task = {
            # ！实际开发不适用，获取tasks最后一个的task_id+1作为新增task的task_id
            'task_id': tasks[-1]['task_id'] + 1,
            'title': request.json['task'],
            'description': request.json.get('description', ""),
            'done': False
        }
    tasks.append(task)
    return jsonify({'status': 0, 'task_id': task['task_id']})


@app.route('/todo/task/<int:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        tasks.remove(task[0])
        return jsonify({'status': 0, 'task_id': task_id, 'msg': 'Deleted.'})


@app.route('/todo/task/<int:task_id>', methods=['PUT'])
def putTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        if 'task' in request.json:
            task[0]['task'] = request.json['task']
        if 'description' in request.json:
            task[0]['description'] = request.json['description']
        if 'done' in request.json:
            if request.json['done'] == True:
                task[0]['done'] = request.json['done']
        return jsonify({'status': 0, 'task': task[0]})


if __name__ == '__main__':
    app.run(debug=True)

```

