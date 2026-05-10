import logging

from .common import *
from .patcher import KindleHBC

logger = logging.getLogger(__name__)


def patch_registration_detection(khbc: KindleHBC) -> None:
    """
    Patch out the Clould Not Available popup.

    This popup is very common on unregistered devices. Newer devices/firmwares
    require a registration to use, and while jailbreaks allow us to bypass this,
    this popup will always show when navigating to the home page.

    See docs/patch_registration_detection.jpg
    """
    logger.info("Patching registration!")
    khbc.patch_func("checkDeviceRegistration", ALWAYS_UNDEFINED)
    khbc.patch_func("IsDeviceRegistered", ALWAYS_TRUE)
    khbc.patch_func("isDeviceRegistered", ALWAYS_TRUE)


def patch_store_button(khbc: KindleHBC) -> None:
    """
    Patch out the store button.

    See docs/patch_store_button.jpg
    """
    logger.info("Patching store!")
    khbc.patch_func("storeButton", EMPTY_OBJECT)
    khbc.null_string("com.lab126.store")
    khbc.null_string("KPP_STORE")
    khbc.null_string("chrome.topnavbar.button.open_store")
    khbc.null_string("com.lab126.KPPStoreShopping")
    khbc.null_string("cart-filled")
    khbc.patch_func("isStoreLocked", ALWAYS_TRUE)


# def patch_home_to_library(khbc: KindleHBC):
#     logger.info("Removing home tab")
#     fid, _ = khbc.find_func_by_name("navigateToHome")
#     fid2, _ = khbc.find_func_by_name("shouldResetViewState")
#     kpp_home = khbc.find_string("KPP_HOME")
#     kpp_library = khbc.find_string("KPP_LIBRARY")
#     khbc.replace_string_ref_in_func(fid, kpp_home, kpp_library)
#     khbc.replace_string_ref_in_func(fid2, kpp_home, kpp_library)
# CreateClosure       	Reg8:1, Reg8:1, UInt16:15746
# patch = [('CreateClosure', [('Reg8', False, 1, fid)]), ]
# khbc.patch_func("navigateToHome", ALWAYS_UNDEFINED)


def patch_collection_not_synced_popup(khbc: KindleHBC) -> None:
    """
    Patch out the not synced popup when adding sideloaded content to collections.

    When adding sideloaded content to collections, it will show a popup telling
    you that the content is not synced. This patch removes that popup.

    See docs/patch_collection_not_synced_popup.jpg
    """
    logger.info("Patching collection not synced popup!")
    khbc.patch_func("showContentNotSyncedModal$", ALWAYS_UNDEFINED)


def patch_homepage(khbc: KindleHBC) -> None:
    """
    Patch out homepage "Discover Books" carousels.

    Kindles have ads for unrelated Amazon store books that show up in the home
    page. This patch will remove those ad rows.

    NOTE: Might not work or might delete too much in certain devices. Confirmed
    not working on a PW5 with 5.16.2.1.1

    See docs/patch_homepage.jpg
    """
    logger.info("Patching homepage content!")
    khbc.patch_string_regex("Template(\\d*)Card", "Template0Card")
