from webui import create_web_interface
import webbrowser
import time


def main():
    print(">>> 正在启动 CodeRefiner 专业代码评审系统...")

    app = create_web_interface()
    print(">>> 系统启动成功！请在浏览器中打开 http://127.0.0.1:7860")

    time.sleep(1)
    webbrowser.open("http://127.0.0.1:7860")

    app.launch(share=False)


if __name__ == "__main__":
    main()

