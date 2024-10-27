from util.model import Model
from util.settings import save_settings, import_settings
from util.generator import Generator
# from util.font2img import font2img, saveImages
from util.img2svg import file_to_svg
from util.interface import Interface
from util.createFolders import createFolders
import os
import logging
import sys

createFolders(False)

def init_loger(name):
    logger = logging.getLogger(name)
    FORMATE = "%(asctime)s - %(name)s: %(funcName)s: %(lineno)d - %(levelname)s - %(message)s"
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMATE))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_log.log"), mode="a")
    fh.setFormatter(logging.Formatter(FORMATE))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.info("Start logging")
    

init_loger("app")
logger = logging.getLogger("app.app")

startupArgs = sys.argv
logger.debug(startupArgs)

settings = import_settings()
logger.info(f"settings: {str(settings)}")


_model = Model(settings=settings)

_generator = Generator()

_interface = Interface(settings=settings)
_interface.createInterface(_model=_model, _generator=_generator, save_settings=save_settings, file_to_svg=file_to_svg)
_interface.demo.launch(share=((settings["IS_SHARE"] or "--share" in startupArgs) and not "--noshare" in startupArgs))
