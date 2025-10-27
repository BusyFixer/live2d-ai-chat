import os
import json
import re
import ollama
import pygame
import l2d_sdk
debug = True
def start_l2d():
    """
    启动live2d线程
    launch live2d threading
    """
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        voice = pygame.mixer.Sound(config["voice_path"])
        l2d = l2d_sdk.create_l2d(config["model3.json_path"])
        l2d.start()
        return [voice, l2d]
    except:
        raise
def ask(messages: list, options: dict, model: str, extra : list) -> str:
    """
    一个ollama库的chat调用整合，输出ai的回复。
    a function that asks ollama ai and output its response.
    """
    try:
        if debug: print("asking...")
        voice = extra[0]
        l2d = extra[1]
        # system_prompt = f"{system}\n记忆：\n{memory}"
        response = ollama.chat(
            model=model,
            messages=messages,
            # system=system_prompt,
            # prompt=f"<|im_start|>turns\nLATEST<|im_end|>\n<|im_start|>dev\n{user_input}<|im_end|>\n<|im_start|>tuber\n",
            options=options,
            stream=True,
            format=''
            # think=False,
        )
        print(f"------------------------------------------")
        final_resp = ""
        for resp in response:
            resp = resp['message']['content']
            if final_resp == "":
                if debug: print("Response:")
                voice.set_volume(0.1)
                voice.play(loops=-1)
            final_resp += resp
            """
            此处表情记得改成model3中有的。
            别忘了改提示词。
            """
            pat = re.compile(r'\*(O形嘴|呆脸|害羞|挥手|微笑|害怕|脸红|脸黑)\*')
            match = None
            for match in re.finditer(pat, final_resp):
                pass
            if match:
                l2d.set_exp(match.group().replace("*",""))
            print(resp, end="", flush=True)
        voice.stop()
        # l2d.set_exp("O形嘴.exp3.json")
        # time.sleep(1.5)
        l2d.model.ResetExpression()
        print("")
        print(f"------------------------------------------")
        if debug: print("ask done.")
        return final_resp
    except:
        raise
def create(name: str):
    """
    创建配置文件。
    create cfg file.
    """
    os.makedirs(name, exist_ok=True)
    if not os.path.exists(f"{name}/memory.jsonl"):
        with open(f"{name}/memory.jsonl", "w"): pass
    if not os.path.exists(f"config.json"):
        print("create config.json...")
        with open(f"config.json", "w") as f:
            config = {
                "memory_name": "1.0.0",
                "ask_model": "yi:9b",
                "history_length": 25,
                "system": "Please remind user he/she forget input system prompt.",
                "options" : {
                    "temperature": 0.7,
                    "top_k" : 200,
                    "top_p" : 0.7,
                    "num_predict" : 300,
                    "repeat_penalty" : 1.2,
                    "num_ctx" : 4096,
                },
                "voice_path" : r"./voice/chara.wav",
                "model3.json_path" : r"./2d/CubismNativeSamples-develop/Samples/Resources/阿库露_vts/阿库露_vts.model3.json",
            }
            f.write(json.dumps(config, ensure_ascii=False))
        print("done.")