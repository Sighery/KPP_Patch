import logging

from hbctool import hbc

from .common import *
from .errors import PatchError
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

    NOTE: Likely to work on newer devices and firmwares >= 5.16.3. Try
    `patch_homepage_sf` if this doesn't work.

    See docs/patch_homepage.jpg
    """
    logger.info("Patching homepage content!")
    khbc.patch_string_regex("Template(\\d*)Card", "Template0Card")


def patch_homepage_sf(khbc: KindleHBC) -> None:
    """
    Patch out homepage ad carousels.

    FOR USE IN OLDER FIRMWARES: TRY IF `patch_homepage` FAILS.

    Kindles have ads for unrelated Amazon store books that show up in the home
    page. This patch will remove those ad rows.

    NOTE: Confirmed working on a PW5 with 5.16.2.1.1.

    See docs/patch_homepage_sf.jpg
    """
    logger.info("Patching homepage content for older Soft Float firmwares!")

    base_err = "Failed to apply patch_homepage_sf!"

    # TODO: I want a find function by Levenshtein distance method
    card49_render_strings = ["Template49Card", "Template49Container", "Template49Title"]
    card49_sids: list[int] = []
    card18_render_strings = [
        "Template18Card",
        "Template18Container",
        "Template18Title",
        "Template18Content",
    ]
    card18_sids: list[int] = []

    for string in card49_render_strings:
        sid = khbc.find_string(string)
        if sid == -1:
            raise PatchError(f"{base_err} Couldn't find string {string}!")
        card49_sids.append(sid)

    for string in card18_render_strings:
        sid = khbc.find_string(string)
        if sid == -1:
            raise PatchError(f"{base_err} Couldn't find string {string}!")
        card18_sids.append(sid)

    card49_render_fid: int | None = None
    card18_render_fid: int | None = None

    all_render_functions = khbc.find_all_funcs_by_name(name="render", disasm=True)
    for fid, func in all_render_functions:
        if khbc.are_sids_used_in_func(sids=card49_sids, func=func):
            card49_render_fid = fid
        elif khbc.are_sids_used_in_func(sids=card18_sids, func=func):
            card18_render_fid = fid

    if not card49_render_fid:
        raise PatchError(f"{base_err} Failed to find Card49 render function!")

    if not card18_render_fid:
        raise PatchError(f"{base_err} Failed to find Card18 render function!")

    logger.info(
        "Card49 render fid %d. Card18 render fid: %d",
        card49_render_fid,
        card18_render_fid,
    )

    # Card 49 (Discover Books Shelf) render function
    result = khbc.patch_func_by_id(fid=card49_render_fid, patch=ALWAYS_FALSE)
    if not result:
        raise PatchError(f"{base_err} Patching Card49 render function failed!")

    # Card 18 (Multiple "with/in Prime" shelves) render function
    result = khbc.patch_func_by_id(fid=card18_render_fid, patch=ALWAYS_FALSE)
    if not result:
        raise PatchError(f"{base_err} Patching Card18 render function failed!")

    # "New Releases In Kindle Store" & "Best Sellers included with Prime" shelves
    result = khbc.patch_func("Template5", ALWAYS_FALSE)
    if not result:
        raise PatchError(f"{base_err} Patching Template5 function failed!")

    # "Easily Add Titles To Your Kindle Library" shelf
    result = khbc.patch_func("Template2", ALWAYS_FALSE)
    if not result:
        raise PatchError(f"{base_err} Patching Template2 function failed!")

    # "Try Unlimited Reading & Listening" shelf
    result = khbc.patch_func("Template13", ALWAYS_FALSE)
    if not result:
        raise PatchError(f"{base_err} Patching Template13 function failed!")
