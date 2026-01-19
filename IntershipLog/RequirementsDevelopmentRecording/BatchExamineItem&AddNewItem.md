# Requirements of 0119

## BatchExamineItem

初来时一头雾水，在这两周的学习中，我发现这个 customer- service 项目没有一个靠谱的技术文档，说的直白点，就是技术文档写的一坨史；所以需要我直接看代码去理解业务逻辑，而且很操蛋的是代码没有注释，只能一点点问 AI；

### Question A: 这个 “RPC” 是什么东西，它怎么路由到业务层的方法上去的？

问题也可以这样表述：前端发过来那个URL，是怎么一步步经过调用，变成后端业务层的逻辑进行执行的？

首先，在 gm.proto 文件里面，通过 rpc PostExamineItem(...) 定义了一个远程过程调用。然后通过 option(google.api.http) 注解，将其绑定到一个 http 路由上面，比如说 Post /gm/v1/item/examine/

然后涉及到一个事：**代码自动生成**，当运行 scripts/gen_proto.sh 脚本时，protoc 会根据 .proto 生成两个**很重要**的 Go 文件：

- pkg/gen/api/gm.pb.go: 这个是定义了 Go 的服务接口(gm_serviceServer), 其中包含了不少方法的签名（比如说 PostExamineItem）

> 这边备注一下，省的后面又忘了：这个 **PostExamineItem** 是用来审批单条邮件 VIP 道具的方法；

- pkg/gen/api/gm_http.pb.go: 这个是**路由**的关键， 这玩意会生成一个 RegisterServiceHttpHandler 函数， 这个函数内部里面实现了一个 HTTP 处理器， 负责解析收到的 HTTP 请求，然后去调用 gm_serviceServer 接口的 PostExamineItem 方法；

### Question B: 这边使用了 gRPC + Gateway 模式，这个 Gateway 是什么东西？

### Question C: gm 是什么东西？是不是一个 package name 下面，只能有一个被定义的 struct example？