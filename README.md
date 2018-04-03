## API With Flask

### 教程背景

​	记录并整理使用 Flask 作为 *API接口开发* 的学习笔记（不涉及前端，故Flask模板、蓝图等不在学习范围内）

​	教程面向有 Python 基础的初学者，较为初级，讲究循序渐进。

​	所有教程涉及到的代码均开源至本人GitHub：https://github.com/ftopiafee/api_with_flask



### 教程大纲

- Hello Flask
- Flask 实现 TODO API
  - 使用 Flask-MongoEngine 集成数据库 
  - 使用 Flask-Login 完成注册登录
- 规范代码目录结构
- 配置管理优化
- 项目部署



## 前期准备

- Python 编程基础（包含代码编辑器 或 Python IDE 的使用）
- HTTP 基础（包含API测试方式，如curl命令、Postman工具的使用等）
- RESTful API 设计基础
- 数据库的简单使用（本教程使用 MongoDB）



### Python 编程基础

本教程使用 Python 3.6，请查阅官网相关教程：https://docs.python.org/3/

> 另，本人的 Python基础教程相关系列仍在整理中，敬请期待  o(￣▽￣)ｄ



### HTTP 基础

#### HTTP Methods

> 以下引用 Flask 官方文档，仅做初步的简介

HTTP 方法告知服务器，客户端想对请求的页面做些什么。下面的都是非常常见的方法：

- GET

  浏览器告知服务器：只 *获取* 页面上的信息并发给我。这是最常用的方法。

- HEAD

  浏览器告诉服务器：欲获取信息，但是只关心 *消息头* 。应用应像处理 GET 请求一样来处理它，但是不分发实际内容。在 Flask 中你完全无需人工干预，底层的 Werkzeug 库已经替你打点好了。

- POST

  浏览器告诉服务器：想在 URL 上 *发布* 新信息。并且，服务器必须确保 数据已存储且仅存储一次。这是 HTML 表单通常发送数据到服务器的方法。

- PUT

  类似 POST 但是服务器可能触发了存储过程多次，多次覆盖掉旧值。你能会问这有什么用，当然这是有原因的。考虑到传输中连接可能会丢失，在 这种情况下浏览器和服务器之间的系统可能安全地第二次接收请求，而 不破坏其它东西。因为 POST它只触发一次，所以用 POST 是不可能的。

- DELETE

  删除给定位置的信息。

- OPTIONS

  给客户端提供一个敏捷的途径来弄清这个 URL 支持哪些 HTTP 方法。 从 Flask 0.6 开始，实现了自动处理。



### RESTful API 设计基础

每一章教程内会包含相关API设计的内容，若读者认为无用，可掠过直接看代码实现。

虽然本人认为API First的设计思想比只会Coding重要的多。





## 声明

本系列教程均为本人原创，如有转载、商业使用等用途，本人保留一切权利。



### 联系我

如果对提到的知识点有不解或者觉得有误，可根据以下联系方式与我联系。

- 博客：http://ftopia.cn/ 
- 邮箱：ftopia@163.com
- GitHub: https://github.com/ftopiafee/api_with_flask



### 更新记录

#### Version 1.0

- date： 2017-2-28
- desc： 终于2018的3月前完成了第一版 （过年期间带娃嫌隙完成，虽五篇仍实属不易） ；缺失配置管理优化及项目部署；只能期待 V1.1了   (￣▽￣)"  



*参考资料：*

[Flask 官方文档](http://docs.jinkan.org/docs/flask/index.html)

[Designing a RESTful API with Python and Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[The Way to Flask](http://liuliqiang.info/book/)

