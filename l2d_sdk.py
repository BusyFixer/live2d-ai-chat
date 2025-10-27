import threading
import time
import live2d.v3 as live2d
import glfw
from OpenGL.GL import *
import win32gui, win32con
live2d.setLogEnable(False)
class create_l2d(threading.Thread):
    """
    创建live2d模型实例。
    create class live2d model
    """
    def __init__(self, path:str):
        super().__init__(daemon=True)
        glfw.init()
        glfw.window_hint(glfw.DECORATED, False)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
        glfw.window_hint(glfw.FLOATING, True)
        self.window = None
        self.path = path
        self.model = None
        self.w, self.h = 1200, 960
        self.dragging = False
        self.drag_x0, self.drag_y0 = 0, 0
        self.win_x0, self.win_y0 = 0, 0
    def run(self):
        def mouse_button_cb(win, button, action, mods):
            if button != glfw.MOUSE_BUTTON_LEFT:
                return
            if action == glfw.PRESS and glfw.get_window_attrib(win, glfw.FOCUSED):
                self.dragging = True
                self.win_x0, self.win_y0 = glfw.get_window_pos(win)
                self.drag_x0, self.drag_y0 = glfw.get_cursor_pos(win)  # 相对窗口
                self.drag_x0 += self.win_x0
                self.drag_y0 += self.win_y0
            else:
                self.dragging = False

        def cursor_pos_cb(win, xpos, ypos):
            if self.dragging:
                dx = xpos + glfw.get_window_pos(win)[0] - self.drag_x0
                dy = ypos + glfw.get_window_pos(win)[1] - self.drag_y0
                glfw.set_window_pos(win,
                                    int(self.win_x0 + (xpos + glfw.get_window_pos(win)[0] - self.drag_x0)),
                                    int(self.win_y0 + (ypos + glfw.get_window_pos(win)[1] - self.drag_y0))
                                    )

        self.window = glfw.create_window(self.w, self.h, "model", None, None)
        # hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not self.window:
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self.window)
        glfw.set_mouse_button_callback(self.window, mouse_button_cb)
        glfw.set_cursor_pos_callback(self.window, cursor_pos_cb)
        glfw.swap_interval(1)
        live2d.init()
        live2d.glInit()
        self.model = live2d.LAppModel()
        self.model.LoadModelJson(self.path)
        # self.model.SetParameterValue('ParamEyeBallX', 0.8)
        glfw.set_window_pos(self.window, 925, 750)
        hwnd = glfw.get_win32_window(self.window)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                               | win32con.WS_EX_LAYERED)
        while not glfw.window_should_close(self.window):
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.model.Update()
            self.model.Draw()
            glfw.swap_buffers(self.window)
            x, y = glfw.get_cursor_pos(self.window)
            mx, my = int(x), int(self.h - y)
            alpha = glReadPixels(mx, my, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)[3]
            if alpha > 0:
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                                       & ~win32con.WS_EX_TRANSPARENT)
            else:
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                                       | win32con.WS_EX_TRANSPARENT)
            glfw.poll_events()
        live2d.dispose()
        glfw.terminate()

    def set_exp(self,emo:str):
        """
        设置live2d当前Expression.
        set current Expression of live2d.
        """
        self.model.SetExpression(emo)
    def set_motion(self,motion:str, no: int = 0, priority: int = 2):
        """
        设置live2d当前Motion.
        set current Motion of live2d.
        """
        self.model.StartMotion(motion, no, priority)
    def reset_exp(self):
        self.model.ResetExpression()

def main():
    """
    live2d测试函数，你可以无视它。
    this function is only used for test live2d. You can ignore this.
    """
    model = create_l2d(r"path_to_model3.json")
    model.start()
    while True:
        time.sleep(3)
        model.set_exp("微笑")
        time.sleep(1)
        model.set_exp("呆脸")
        time.sleep(1)
        # model.model.
        model.model.ResetExpression()
if __name__ == "__main__":
    main()