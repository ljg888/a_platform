1、前端发送模型路径、测试集路径、项目名过来， /api/submit接口把这些信息存入到postgres的model_testing库的test_configs表中， 数据库连接信息为：ip: 192.168.2.155 port: 20439, user: postgres, password: GX38akOxjGe9cEFT
2、test_configs表交给后端服务来初始化
3、前端增加一个列表， 用来展示存入到model_testing库的每个测试配置， 并给每个测试配置增加一个删除按钮，点击删除时，调用删除接口，并且增加一个“执行”按钮， 调用“执行” run接口
4、后端服务增加一个删除接口，根据id删除model_testing库中的某个测试配置
5、后端服务增加一个执行接口，根据id执行model_testing库中的某个测试配置， 具体的操作我自己来完成就行，




results
    --id
        --


results目录，配置id， 项目名，模型路径， 测试集路径，开始运行时间， 结束运行时间，

@/backend/holly_infer.py 
@/backend/app.py  当调用 run_config 接口时， 异步调用holly_infer.py脚本， 给每个测试配置增加一个运行状态
