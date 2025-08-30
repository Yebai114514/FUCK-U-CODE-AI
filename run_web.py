from webui import create_web_interface
import webbrowser
import time


def main():
    print(">>> 正在启动 CodeRefiner 专业代码评审系统...")
    print(">>> 由你的专属篮球小狼狗李昂为你保驾护航！")

    app = create_web_interface()
    print(">>> 系统启动成功！请在浏览器中打开 http://127.0.0.1:7860")

    # 等一秒钟，然后自动帮你打开浏览器
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:7860")

    app.launch(share=False)


if __name__ == "__main__":
    main()
