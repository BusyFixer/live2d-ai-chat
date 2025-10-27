import traceback
from utils import *
# import threading
def main():
    """
    主线程
    main threading
    """
    try:
        if not os.path.exists("config.json"):
            print("配置文件不存在，请运行 init.py 或手动创建配置文件")
            exit(1)
        with open("config.json", "r", encoding="utf-8") as cfg:
            config = json.load(cfg)
            memory_name = config["memory_name"]
            ask_model = config["ask_model"]
            history_length = config["history_length"]
            system_prompt = config["system"]
            options = config["options"]
        if not os.path.exists(f"{memory_name}/memory.jsonl"):
            print("对话文件不存在，请运行 init.py 或手动创建配置文件")
            exit(1)
        if history_length < 50:
            print(f"warning: history only can saved {history_length} turns !")
        # tts1 = tts_init()
        animation_and_voice = start_l2d()
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
        ]
        with (open(f"{memory_name}/memory.jsonl", "r", encoding="utf-8") as a_r):
            for line in a_r:
                ask_response = json.loads(line.strip())
                # history = f"<|im_start|>turns\n{ask_response["index"]}<|im_end|>\n<|im_start|>dev\n{ask_response["input"]}<|im_end|>\n<|im_start|>tuber\n{ask_response["response"]}<|im_end|>\n"
                if ask_response["role"] == "system":
                    continue
                messages.append(ask_response)
        # if messages[1]["role"] == "system":
        #     messages = messages[1:]
                # {"index":ask_response["index"], "input":ask_response["input"], "response":ask_response["response"]}
                # all_f_history.append(f_history)
                # memory += history
    except Exception:
        traceback.print_exc()
        exit(1)
    while True:
        try:
            # memory = ""
            # all_history, all_f_history = [], []
            user_input = input("->")
            if user_input.startswith("/"):
                match user_input:
                    case "/exit":
                        break
                    case "/?":
                        print(
"""
/exit       --exit the conversation
/?          --print this menu
""")
                        continue
                    case _:
                        print("Unknown command.You can input /? to get help.")
                        continue
            # if not memory:
            #     memory = "暂无"
            # print(f"memory: ...{memory[-70:]}")
            print(f"user_input: {user_input}...")
            print(f"system: {system_prompt}")
            print(f"history_length: {history_length}")
            print(f"options: {options}")
            print("---------------------")
            print(f"messages: {messages}")
            # memory = "暂无"
            messages.append({"role": "user","content": user_input})
            response = ask(
                messages=messages,
                options=options,
                model=ask_model,
                extra=animation_and_voice,
            )
            messages.append({"role": "assistant","content": response})
            # latest_index = all_f_history[-1]["index"]+1 if all_f_history else 1
            # new_f_history = {"index": latest_index, "input": user_input, "response": response}
            # all_f_history.append(new_f_history)
            # if len(all_f_history) > history_length:
            #     all_f_history.pop(0)
            with open(f"{memory_name}/memory.jsonl", "w", encoding="utf-8") as a_w:
                for i in messages:
                    a_w.write(json.dumps(i, ensure_ascii=False) + "\n")
        except Exception:
            traceback.print_exc()
            exit(1)
if __name__ == "__main__":
    main()