# my_library
一些常用的辅助代码

## my_thread
这个代码库包含两个类：ThreadWorker 和 ThreadManager。

ThreadWorker 是一个继承自 threading.Thread 的类，它接受一个可调用对象 func 和一个参数列表 args。当线程运行时，它会尝试调用 func 并保存结果。如果在调用过程中抛出异常，它会保存异常信息。

ThreadManager 是一个线程管理器，可以并行、串行或异步地执行任务。它接受一个可调用对象 func，一个可选的池（尚未在代码中使用），以及一个线程数量 thread_num。此类有几个方法：

- get_args(obj): 这是一个抽象方法，需要被子类实现，用来从 obj 中获取参数。
- process_result(obj, result): 这是一个抽象方法，需要被子类实现，用来处理结果。
- handle_error(obj): 这是一个抽象方法，需要被子类实现，用来处理错误。
- start(dictory, start_type='serial'): 这个方法会根据 start_type 的值来选择串行、并行或异步地执行任务。
- start_async(dictory): 这个方法会异步地执行任务。
- run_in_parallel(dictory): 这个方法会并行地执行任务。
- run_in_serial(dictory): 这个方法会串行地执行任务。
- run_in_async(dictory): 这个方法会异步地执行任务。
- get_result_list(): 这个方法返回结果列表。
- get_result_dict(): 这个方法返回结果字典。
