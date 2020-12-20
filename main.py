import pygame
import pygame.freetype
import pygame.sprite
import pygame.image
import pygame.font
import pygame.time
import pygame.event
import pygame.display
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog

from component import Plat, Conveyor, Press


from time import process_time as time


class Pabrik:
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.FONT = pygame.freetype.Font("sprites/UniversCondensed.ttf", 65)
        self.SIZE = self.WIDTH, self.HEIGHT = 800, 600
        pygame.display.set_caption('Plat Kendaraan')
        self.window_surface = pygame.display.set_mode(self.SIZE)
        self.ui_manager = pygame_gui.UIManager(self.SIZE)
        self.background = pygame.Surface(self.SIZE)
        self.background.fill(pygame.Color("#f0f0f0"))

        self.load_button = UIButton(pygame.Rect((20, 20), (100, 50)),
                                    text="PILIH FILE",
                                    manager=self.ui_manager)
        self.start_button = UIButton(pygame.Rect((20, 90), (100, 50)),
                                     text="TURN ON",
                                     manager=self.ui_manager)
        self.add_button = UIButton(pygame.Rect((20, 150), (100, 50)),
                                   text="TAMBAH",
                                   manager=self.ui_manager)
        self.add_button.disable()
        self.file_dialog = None
        self.file_csv = None
        self.list_plat = []
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.time = time()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.belt = Conveyor()
        self.press = Press()
        self.group = pygame.sprite.Group(self.belt)
        self.hold = (pygame.image.load("sprites/hold.png"),
                     pygame.image.load("sprites/hold.png").get_rect().move(220, -130))
        self.plats = []
        self.sekali = True
        self.satusatu = True
        self.print = False
        # self.plats.append(Plat(self.belt, "BG 1029 AY", self.FONT))

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(10)/1000.0
            # Otomatis tambah file
            if self.start_button.text == "TURN OFF" and not self.sekali and self.satusatu:
                self.plats.append(
                    Plat(self.belt, self.list_plat.pop(), self.FONT))
                self.satusatu = False

            for plat in self.plats:
                if plat.pos.left == 261 and not self.press.working and self.sekali:
                    self.belt.switch()
                    for plat2 in self.plats:
                        plat2.switch()
                    self.press.switch()
                    self.satusatu = True
                    self.sekali = False
                    break
                elif plat.pos.left == 261 and self.print and self.press.working:
                    plat.setPlat()
                    self.print = False
                    break

            if not self.press.working and not self.sekali:
                self.belt.switch()
                for plat in self.plats:
                    plat.switch()
                self.sekali = True
            # Tombol dan event
            for event in pygame.event.get():

                # QUIT
                if event.type == pygame.QUIT:
                    self.is_running = False

                # Tombol Pilih File
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 300, 400),
                                                    self.ui_manager,
                                                    window_title="Pilih list plat kendaraan",
                                                    allow_existing_files_only=True)
                    self.load_button.disable()

                # Tombol Start
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.start_button):
                    self.belt.switch()
                    for plat in self.plats:
                        plat.switch()
                    if self.start_button.text == "TURN ON":
                        self.start_button.set_text("TURN OFF")
                    else:
                        self.start_button.set_text("TURN ON")

                # Tombol add
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.add_button):
                    self.plats.append(
                        Plat(self.belt, self.list_plat.pop(), self.FONT))
                    pass

                # Event file di pilih
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                        event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.add_button.enable()
                    try:
                        self.file_csv = self.file_dialog.current_file_path.as_posix()
                        if self.file_csv[-3:] == "csv":
                            self.file_dialog = None
                            with open(self.file_csv, 'r') as f:
                                self.list_plat = [
                                    i for i in f.read().split("\n")]
                        else:
                            pop_up = pygame_gui.windows.UIMessageWindow(pygame.Rect(
                                200, 300, 200, 300), manager=self.ui_manager, window_title="Peringatan", html_message="Pilih file dengan format CSV!")
                    except AttributeError:
                        pop_up = pygame_gui.windows.UIMessageWindow(pygame.Rect(
                            200, 300, 200, 300), manager=self.ui_manager, window_title="Peringatan", html_message="Pilih filenya dahulu!")
                        break

                self.ui_manager.process_events(event)

            # Render Window
            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.group.update()
            self.group.draw(self.window_surface)
            for plat in self.plats:
                plat.move()
                self.window_surface.blit(plat.image, plat.pos)
                self.window_surface.blit(plat.teks, plat.pos.move(13, 30))
            self.print = self.press.update()
            self.window_surface.blit(self.press.image, self.press.pos)
            self.window_surface.blit(self.hold[0], self.hold[1])
            self.ui_manager.draw_ui(self.window_surface)
            pygame.display.update()


if __name__ == "__main__":
    app = Pabrik()
    app.run()
