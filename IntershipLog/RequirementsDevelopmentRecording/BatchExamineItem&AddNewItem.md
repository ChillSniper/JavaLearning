# Requirements of 0119

## BatchExamineItem

初来时一头雾水，在这两周的学习中，我发现这个 customer- service 项目没有一个靠谱的技术文档，说的直白点，就是技术文档写的一坨史；所以需要我直接看代码去理解业务逻辑，而且很操蛋的是代码没有注释，只能一点点问 AI；

### Question A: 这个 “RPC” 是什么东西，它怎么路由到业务层的方法上去的？

问题也可以这样表述：前端发过来那个URL，是怎么一步步经过调用，变成后端业务层的逻辑进行执行的？

首先是**API 定义**，在 gm.proto 文件里面，通过 rpc PostExamineItem(...) 定义了一个远程过程调用。然后通过 option(google.api.http) 注解，将其绑定到一个 http 路由上面，比如说 Post /gm/v1/item/examine/

然后涉及到一个事：**代码自动生成**，当运行 scripts/gen_proto.sh 脚本时，protoc 会根据 .proto 生成两个**很重要**的 Go 文件：

- pkg/gen/api/gm.pb.go: 这个是定义了 Go 的服务接口(gm_serviceServer), 其中包含了不少方法的签名（比如说 PostExamineItem）

> 这边备注一下，省的后面又忘了：这个 **PostExamineItem** 是用来审批单条邮件 VIP 道具的方法；

- pkg/gen/api/gm_http.pb.go: 这个是**路由**的关键， 这玩意会生成一个 RegisterServiceHttpHandler 函数， 这个函数内部里面实现了一个 HTTP 处理器， 负责解析收到的 HTTP 请求，然后去调用 gm_serviceServer 接口的 PostExamineItem 方法；
  
**业务逻辑**（就是那个 service）的实现，是在业务层实现各种各样的接口。比如说，在 item.go 里面，去定义一个 Service 结构体，并且让他实现 gm_serviceServer 接口。也就是说，Service 结构体必须提供一个和接口签名完全一致的 PostExamineItem 方法。

关于**服务注册和启动**， 在项目的启动文件中，就是那个 server.go 里面，会将上面的所有部分组装起来：

- 创建一个 gin 的 HTTP 引擎
- 创建一个 gm 服务的的服务实例（也就是 internal/service/gm/item.go 里面那个 Service）
- 调用自动生成的那个 RegisterGmServiceHandler 函数，去把 gin 引擎和 gm 服务实例传递进去；

上面这堆东西看起来很复杂，再精简一下表述：对于 HTTP 请求到具体的业务逻辑实现函数的完整调用链，当一个请求到达匹配的 URL 时，gin 会把他交给 RegisterGmServiceHandler 生成的处理器，处理器再调用比如说在 item.go 中生成的 PostExamineItem 方法；

### Question B: 这边使用了 gRPC + Gateway 模式，这个 Gateway 是什么东西？

### Question C: gm 是什么东西？是不是一个 package name 下面，只能有一个被定义的 struct example？

### Question D: 为什么代码没有注释？

### Question E: 怎么查看一个页面中的表格查询对应的后端源码？

这个的话，得用开发者工具。需要在点进去那个页面的时候，就按 command+alt+I，然后一般是查看 list 对应的 网络部分信息相关的 **URL**

### Question F: project, err := dao.DefaultProjectDao(c).FindProjectCtx(ctx) 这一行代码里这个 project 是什么东西？

### Question G: 前端页面没有数据，无法进行修改操作，这没数据我怎么查看URL？

即使我可以问AI那个URL在哪，那部分的代码逻辑在项目的什么位置。但是这终究不是长久之计，我需要前端的数据……

### Question H: 那个“配置文件”是前端那边提供的，还是后端项目里哪段代码逻辑生成的？我压根没找到哪个func实现了这个功能……
