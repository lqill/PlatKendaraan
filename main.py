import pygame
import pygame_gui
from component import Plat, Conveyor

from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog


class Pabrik:
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.SIZE = WIDTH, HEIGHT = 800, 600
        pygame.display.set_caption('Plat Kendaraan')
        self.window_surface = pygame.display.set_mode(self.SIZE)
        self.ui_manager = pygame_gui.UIManager(self.SIZE)
        self.background = pygame.Surface(self.SIZE)
        self.background.fill(pygame.Color("#f0f0f0"))

        self.load_button = UIButton(pygame.Rect((20, 20), (100, 50)),
                                    text="PILIH FILE",
                                    manager=self.ui_manager)
        self.file_dialog = None
        self.file_csv = None
        self.list_plat = []
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.belt = Conveyor()
        self.group = pygame.sprite.Group(self.belt)
        # self.plat_baru = Plat()

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(20)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 300, 400),
                                                    self.ui_manager,
                                                    window_title="Pilih list plat kendaraan",
                                                    allow_existing_files_only=True)
                    self.load_button.disable()

                if (event.type == pygame.USEREVENT and
                        event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED):
                    if self.file_csv is not None:
                        pass
                    try:
                        # disini proses csvnyo
                        pass
                    except pygame.error:
                        pass

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                        event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    try:
                        self.file_csv = self.file_dialog.current_file_path.as_posix()
                        if self.file_csv[-3:] == "csv":
                            self.file_dialog = None
                            with open(self.file_csv, 'r') as f:
                                self.list_plat = [
                                    i for i in f.read().split("\n")]
                                pass
                        else:
                            pop_up = pygame_gui.windows.UIMessageWindow(pygame.Rect(
                                200, 300, 200, 300), window_title="Peringatan", html_message="Pilih file dengan format CSV!")
                    except AttributeError:
                        pop_up = pygame_gui.windows.UIMessageWindow(pygame.Rect(
                            200, 300, 200, 300), window_title="Peringatan", html_message="Pilih filenya dahulu!")
                        break

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            # self.window_surface.blit(self.background, self.plat_baru.pos, self.plat_baru.pos)
            # self.plat_baru.move()
            # self.window_surface.blit(self.plat_baru.body, self.plat_baru.pos)
            self.ui_manager.draw_ui(self.window_surface)
            self.group.update()
            self.group.draw(self.window_surface)
            pygame.display.update()


if __name__ == "__main__":
    app = Pabrik()
    app.run()
